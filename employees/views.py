import csv
import datetime
import xlwt
from allauth.account.adapter import get_adapter
from collections import OrderedDict
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpResponse
from rest_framework import permissions, status
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError, server_error
from rest_framework.response import Response
from rest_framework.views import APIView

from common.utils import get_instance
from core.views import (
	ListView,
	ListCreateRetrieveDestroyView,
	ListCreateRetrieveUpdateView,
	ListCreateRetrieveUpdateDestroyView
)
from .filters import ClientFilter
from .models import (
	Attendance, 
	Client, 
	Department, 
	Employee, Holiday, 
	Project, 
	ProjectFile, 
	Task
)
from .pagination import (
	ClientPagination,
	EmployeePagination,
	ProjectPagination,
	TaskPagination
)
from .permissions import (
	IsEmployee,
	IsHROrMD,
	IsHROrMDOrAdminUser,
	IsHROrMDOrReadOnly,
	IsHROrMDOrLeaderOrReadOnlyEmployee,
	IsHROrMDOrLeaderOrReadOnlyEmployeeAndClient
)
from .serializers import (
	AttendanceSerializer,
	ClientSerializer,
	DepartmentSerializer,
	EmployeeSerializer,
	HolidaySerializer,
	ProjectSerializer,
	UserEmployeeSerializer,
	ProjectFileSerializer,
	TaskSerializer
)


User = get_user_model()


class AttendanceInfoView(APIView):
	def get(self, request, *args, **kwargs):
		return Response(OrderedDict([
				('hours_spent_today', Attendance.objects.get_hours(
					self.request.user.employee.has_attendance())),
				('week_hours', Attendance.objects.get_week_hours(
					employee=self.request.user.employee)),
				('overtime_hours', self.get_overtime_hours()),
				('statistics', self.get_statistics()),
			]))

	def get_overtime_hours(self):
		overtime = self.request.user.employee.has_overtime()
		return overtime.hours if overtime else None

	def get_statistics(self):
		today_total_expected_hours = self.request.user.employee.total_hours_for_the_day()
		today_total_hours_spent = self.request.user.employee.total_hours_spent_for_the_day()

		week_total_expected_hours = self.request.user.employee.total_hours_for_the_week()
		week_total_hours_spent = self.request.user.employee.total_hours_spent_for_the_week()

		month_total_expected_hours = self.request.user.employee.total_hours_for_the_month()
		month_total_hours_spent = self.request.user.employee.total_hours_spent_for_the_month()

		statistics = OrderedDict({})
		statistics["today"] = today_total_hours_spent / today_total_expected_hours
		statistics["week"] = week_total_hours_spent / week_total_expected_hours
		statistics["month"] = month_total_hours_spent / month_total_expected_hours
		statistics["overtime"] = self.get_overtime_statistics()
		return statistics

	def get_overtime_statistics(self):
		overtime = self.request.user.employee.has_overtime()
		attendance = self.request.user.employee.has_attendance()
		if not overtime or not attendance or not attendance.punch_in:
			return 0
		hours_spent = self.request.user.employee.total_hours_spent_for_the_day()
		hours_without_overtime = self.request.user.employee.total_hours_for_the_day(wo=True)
		if hours_spent > hours_without_overtime:
			return (hours_spent - hours_without_overtime) / overtime.hours
		return 0


class AttendanceListView(ListView):
	serializer_class = AttendanceSerializer
	permission_classes = (IsEmployee, )

	def post(self, request, *args, **kwargs):
		action = request.data.pop("action", None)

		context = self.get_serializer_context()
		context.update({"action": action})

		serializer = AttendanceSerializer(data=request.data, context=context)
		serializer.is_valid(raise_exception=True)
		if serializer.errors:
			return Response(serializer.errors)
		serializer.save()

		message = "Punched In" if action == "in" else "Punched Out"
		return Response({"detail": message}, status=status.HTTP_200_OK)

	def get_queryset(self):
		return Attendance.objects.filter(employee__user=self.request.user).order_by('-date')

	def get_serializer_context(self):
		return {
			'request': self.request,
			'format': self.format_kwarg,
			'view': self,
		}


class ClientView(ListCreateRetrieveUpdateDestroyView):
	queryset = Client.objects.all().order_by('-id')
	pagination_class = ClientPagination
	permission_classes = (IsHROrMD, )
	serializer_class = ClientSerializer
	ordering_fields = ('contact__first_name', 'contact__last_name', 'company', 'contact__is_active')
	search_fields = ('contact__first_name', 'contact__last_name', 'company', 'contact__is_active')
	lookup_field = 'id'
	filterset_class = ClientFilter


class DepartmentView(ListCreateRetrieveUpdateDestroyView):
	permission_classes = (IsHROrMDOrAdminUser, )
	queryset = Department.objects.all().order_by('-id')
	serializer_class = DepartmentSerializer
	ordering_fields = ('name', 'hod__user__first_name', 'hod__user__last_name', 'hod__user__email')
	search_fields = ('name', 'hod__user__first_name', 'hod__user__last_name', 'hod__user__email')
	lookup_field = 'id'

	def put(self, request, *args, **kwargs):
		if request.user.employee.is_hr or request.user.employee.is_md:
			return self.custom_update(request, *args, **kwargs)
		return Response({"detail": "You are not authorized to make this request"},
			status=status.HTTP_403_FORBIDDEN)


class EmployeeView(ListCreateRetrieveUpdateDestroyView):
	serializer_class = EmployeeSerializer
	pagination_class = EmployeePagination
	permission_classes = (IsHROrMDOrAdminUser, IsEmployee)
	ordering_fields = ('user__first_name', 'user__last_name', 'user__email')
	search_fields = ('user__first_name', 'user__last_name', 'user__email')
	lookup_field = 'id'

	def delete(self, request, *args, **kwargs):
		if not request.user.employee.is_md and not request.user.employe.is_hr:
			raise PermissionDenied({"detail": "You are not authorized to make this request!"})
		return self.destroy(request, *args, **kwargs)

	def get_queryset(self):
		try:
			queryset = Employee.objects.employees(
				self.request.user.employee).order_by('user__first_name', 'user__last_name', 'id')
			return queryset
		except:
			pass
		return Employee.objects.none()


class EmployeeExportDataView(APIView):
	permission_classes = (permissions.IsAdminUser, )

	def get(self, request, *args, **kwargs):
		file_type = kwargs["file_type"]
		if file_type == "csv":
			response = self.export_csv_data()
			return response
		elif file_type == "excel":
			response = self.export_excel_data()
			return response
		return Response(
			{"error": "invalid content type. can only export csv and excel file format."},
			status=status.HTTP_400_BAD_REQUEST)

	def export_csv_data(self):
		response = HttpResponse(content_type='text/csv',
			headers={'Content-Disposition': 'attachment; filename="employees.csv"'})
		writer = csv.writer(response)
		writer.writerow(self.get_emp_headers())

		employees = self.get_queryset()
		for emp in employees:
			writer.writerow(self.get_emp_data(emp))
		return response

	def export_excel_data(self):
		response = HttpResponse(content_type='application/ms-excel',
			headers={'Content-Disposition': 'attachment; filename="employees.xls"'})
		wb = xlwt.Workbook(encoding='utf-8')
		ws = wb.add_sheet('Employees')
		row_num = 0
		font_style = xlwt.XFStyle()
		font_style.font.bold = True

		columns = self.get_emp_headers()
		for col_num in range(len(columns)):
			ws.write(row_num, col_num, columns[col_num], font_style)
		font_style = xlwt.XFStyle()

		emps = self.get_queryset()
		for emp in emps:
			row_num += 1
			data = self.get_emp_data(emp)

			for col_num in range(len(data)):
				ws.write(row_num, col_num, str(data[col_num]), font_style)
		wb.save(response)
		return response

	def get_emp_headers(self):
		return ['First Name', 'Last Name', 'E-mail', 'Department', 'Job', 'Status',
			'Supervisor Name', 'Supervisor E-mail', 'Date Employed']

	def get_emp_data(self, emp):
		try:
			return [
				emp.user.first_name, emp.user.last_name, emp.user.email, emp.department_name,
				emp.job_name, emp.status, emp.get_supervisor("name"),
				emp.get_supervisor("email"), str(emp.date_employed)
			]
		except:
			pass
		return []

	def get_queryset(self):
		try:
			name = self.request.query_params.get('name', None)
			queryset = Employee.objects.employees(
				self.request.user.employee).order_by('-date_updated')
			if name:
				queryset = queryset.filter(
					Q(user__first_name__icontains=name.lower()) |
					Q(user__last_name__icontains=name.lower()) |
					Q(user__email__icontains=name.lower()))
			status = self.request.query_params.get('status', None)
			if status:
				queryset = [x for x in queryset if x.status.lower() == status.lower()]
			return queryset
		except:
			pass
		return Employee.objects.none()


# Use Allauth Get adapter validate password to do this
class EmployeePasswordChangeView(APIView):
	permission_classes = (IsHROrMD, )

	def post(self, request, *args, **kwargs):
		email = self._validate_email(request.data.get("email"))
		password = self._validate_passwords(
			request.data.get("new_password1"),
			request.data.get("new_password2"))

		user = get_instance(User, { "email": email })
		user.set_password(password)
		user.save()
		return Response({"detail": "Password Changed Successfully"})

	def _validate_email(self, value):
		email = value.strip().lower()
		request_user = self.request.user
		user = get_instance(User, { "email": email })

		form_type = self.request.data.get("type")
		if form_type and form_type == "client":
			if user is None or user.client is None:
				raise ValidationError("client does not exist")
		else:
			if user is None or user.employee is None:
				raise ValidationError("employee does not exist")

		if request_user.employee.is_hr and user.employee.is_md:
			raise PermissionDenied("You are forbidden from making this request")

		return email

	def _validate_passwords(self, password1, password2):
		if password1 is None or password1 == "":
			raise ValidationError({"new_password1": "This field is required"})
		if password2 is None or password2 == "":
			raise ValidationError({"new_password2": "This field is required"})
		if password1 != password2:
			raise ValidationError({
				"new_password1": "passwords do not match",
				"new_password2": "passwords do not match",
			})
		try:
			password = get_adapter().clean_password(password1)
			return password
		except Exception as e:
			raise ValidationError({"new_password1": e})


class EmployeeDeactivateView(APIView):
	permission_classes = (IsHROrMD, )

	def post(self, request, *args, **kwargs):
		admin = self._validate_user()
		user = self._validate_email(request.data.get("email", None))
		action = self._validate_action(request.data.get("action", None))
		_type = self.request.data.get("type", None)
		if action == "deactivate":
			user.is_active = False
			if _type is None or _type != "client":
				user.employee.relinquish_status()
		elif action == "activate":
			user.is_active = True
		user.save()
		res_status = status.HTTP_200_OK
		if _type == "client":
			user_type_id = user.client.id
			user_type = "client"
		else:
			user_type_id = user.employee.id
			user_type = "employee"
		if action == "activate":
			message = {
				"detail": f"{user_type.capitalize()} Activated Successfully", 
				"type": user_type, "id": user_type_id}
		elif action == "deactivate":
			message = {
				"detail": f"{user_type.capitalize()} De-activated Successfully", 
				"type": user_type, "id": user_type_id}
		else:
			message = {"detail", "A server error occurred! Please try again later."}
			res_status = status.HTTP_400_BAD_REQUEST
		return Response(message, status=res_status)

	def _validate_email(self, email):
		if email is None:
			raise ValidationError({"detail": "e-mail is required" })
		_type = self.request.data.get("type", None)
		if _type == "client":
			client = get_instance(Client, { "contact__email": email })
			if client is None:
				raise ValidationError({"detail": "client does not exist" })
			return client.contact
		employee = get_instance(Employee, { "user__email": email })
		if employee is None:
			raise ValidationError({"detail": "employee does not exist" })
		return employee.user

	def _validate_action(self, action):
		if action is None:
			raise ValidationError({"detail": "action is required" })
		if action != "activate" and action != "deactivate":
			raise ValidationError({"detail": "action is invalid. use activate or deactivate"})

		user = self._validate_email(self.request.data.get("email", None))
		_type = self.request.data.get("type", None)

		if action == "deactivate" and user.is_active is False:
			if _type == "client":
				raise ValidationError({"detail": "client is already inactive"})
			raise ValidationError({"detail": "employee is already inactive"})
		if action == "activate" and user.is_active is True:
			if _type == "client":
				raise ValidationError({"detail": "client is already active"})
			raise ValidationError({"detail": "employee is already active"})
		return action

	def _validate_user(self):
		request_user = self.request.user
		user = self._validate_email(self.request.data.get("email", None))

		if (
			request_user.employee.is_hr is False and request_user.employee.is_md is False
		) or (
			request_user.employee.is_hr is True and user.employee.is_md is True
		):
			raise PermissionDenied({"detail": "you are forbidden from making this request"})

		if request_user == user:
			raise ValidationError({"detail": "you cannot deactivate yourself"})

		return request_user


class HolidayView(ListCreateRetrieveUpdateDestroyView):
	queryset = Holiday.objects.all().order_by('-date')
	permission_classes = (IsHROrMDOrReadOnly, )
	serializer_class = HolidaySerializer
	ordering_fields = ('-date', 'name')
	search_fields = ('name', )
	lookup_field = 'id'


class ProjectView(ListCreateRetrieveUpdateDestroyView):
	pagination_class = ProjectPagination
	permission_classes = (IsHROrMDOrLeaderOrReadOnlyEmployeeAndClient, )
	serializer_class = ProjectSerializer
	search_fields = ('name', 'client__company')
	ordering_fields = ('name', 'client__company')
	lookup_field = 'id'

	def get_queryset(self):
		user = self.request.user
		if not user.is_client and not user.is_employee:
			return Project.objects.none()
		if user.is_client:
			queryset = Project.objects.filter(client__contact=user).distinct()
		if user.is_employee and (user.employee.is_hr or user.employee.is_md):
			queryset = Project.objects.all().distinct()
		else:
			queryset = Project.objects.filter(Q(created_by__user=user) | Q(team=user.employee)).distinct()
		return queryset


class ProjectCompletedView(APIView):
	permission_classes = (IsHROrMD, )

	def post(self, request, *args, **kwargs):
		project_id = kwargs.get("id", None)
		if not project_id:
			raise ValidationError({"detail": "Project 'id' is required"})
		project = get_instance(Project, {"id": project_id})
		if project is None:
			raise NotFound({"detail": "Project was not Found"})
		action = request.data.get("action", None)
		if action is None:
			raise ValidationError({"detail": "Action is required"})
		if action is not True and action is not False:
			raise ValidationError({"detail": "Action is either true or false"})

		if (action is True and project.completed is True) or (action is False and
			project.completed is False):
			pass
		else:
			project.completed = action if action is True or action is False else False
			project.save()

		message = "completed" if action is True else "ongoing"

		return Response({ "detail": f"Project is marked {message}"
			}, status=status.HTTP_200_OK)


class ProjectEmployeesView(ListView):
	serializer_class = UserEmployeeSerializer
	permission_classes = (IsHROrMDOrLeaderOrReadOnlyEmployeeAndClient, )

	def get_queryset(self):
		project_id = self.kwargs.get("id", None)
		if not project_id:
			raise ValidationError({"detail": "Project ID is required"})
		project = get_instance(Project, {"id": project_id})
		if not project:
			raise NotFound({"detail": f"Project with ID {project_id} was not found"})
		return project.team.all()


class ProjectFileView(ListCreateRetrieveDestroyView):
	permission_classes = (IsHROrMDOrLeaderOrReadOnlyEmployeeAndClient, )
	serializer_class = ProjectFileSerializer
	lookup_field = 'id'

	def get_queryset(self):
		project_id = self.kwargs.get('project_id', None)
		if not project_id:
			raise ValidationError({"detail": "Project ID is required"})
		project = get_instance(Project, {"id": project_id})
		if not project:
			raise ValidationError({"detail": f"Project with ID {project_id} was not found!"})
		queryset = ProjectFile.objects.filter(project=project)
		return queryset
		

class TaskView(ListCreateRetrieveUpdateDestroyView):
	pagination_class = TaskPagination
	permission_classes = (IsHROrMDOrLeaderOrReadOnlyEmployee, )
	serializer_class = TaskSerializer
	search_fields = ('name', )
	ordering_fields = ('name', )
	lookup_field = 'id'

	def get(self, request, *args, **kwargs):
		project_id = self.kwargs.get("project_id", None)
		id = self.kwargs.get("id", None)

		if project_id and id:
			self.get_project(project_id)
			self.get_task()
			return self.retrieve(request, *args, **kwargs)

		if project_id and not id:
			return self.list(request, *args, **kwargs)

		if not project_id and not id:
			raise ValidationError({"detail": "Invalid route params"})

	def delete(self, request, *args, **kwargs):
		task = self.get_task()
		emp = request.user.employee
		if task is not None and (
			task.created_by.user == request.user or emp.is_hr is True or emp.is_md is True
			):
			return self.destroy(request, *args, **kwargs)
		raise PermissionDenied({"detail": "You do not have permission to make this request!"})

	def get_queryset(self):
		project_id = self.kwargs.get("project_id", None)

		if not project_id:
			raise ValidationError({"detail": "Project ID is required!"})
		project = self.get_project(project_id)

		try:
			employee = self.request.user.employee
			if employee.is_hr or employee.is_md:
				queryset = project.task.all()
			else:
				queryset = project.task.filter(followers=employee)
		except:
			queryset = project.task.none()
		return queryset

	def get_project(self, id):
		try:
			project = Project.objects.get(id=id)
			return project
		except:
			raise NotFound({"detail": f"Project was id {id} was not found"})

	def get_task(self):
		id = self.kwargs.get("id", None)
		try:
			task = Task.objects.get(id=id)
			return task
		except:
			raise NotFound({"detail": f"Task was id {id} was not found"})
		return None
