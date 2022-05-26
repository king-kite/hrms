# Generated by Django 4.0.3 on 2022-05-23 20:26

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    replaces = [('employees', '0001_initial'), ('employees', '0002_auto_20220202_2233'), ('employees', '0003_auto_20220203_1257'), ('employees', '0004_auto_20220203_2001'), ('employees', '0005_auto_20220208_1535'), ('employees', '0006_auto_20220208_1735'), ('employees', '0007_auto_20220208_2019'), ('employees', '0008_auto_20220210_1543'), ('employees', '0009_leave_status'), ('employees', '0010_auto_20220215_2112'), ('employees', '0011_auto_20220216_1509'), ('employees', '0012_auto_20220216_1510'), ('employees', '0013_auto_20220217_1054'), ('employees', '0014_leave_created_by'), ('employees', '0015_job'), ('employees', '0016_employee_job'), ('employees', '0017_auto_20220304_1017'), ('employees', '0018_alter_department_id_alter_employee_id_and_more'), ('employees', '0019_remove_leave_created_by_remove_leave_employee_and_more'), ('employees', '0020_alter_department_hod'), ('employees', '0021_alter_department_hod'), ('employees', '0022_remove_employee_is_hod_remove_employee_is_supervisor'), ('employees', '0023_alter_employee_date_employed'), ('employees', '0024_remove_employee_status'), ('employees', '0025_company_client'), ('employees', '0026_rename_user_client_contact_and_more'), ('employees', '0027_alter_client_company_delete_company'), ('employees', '0028_alter_client_contact'), ('employees', '0029_holiday'), ('employees', '0030_rename_title_holiday_name'), ('employees', '0031_alter_holiday_unique_together'), ('employees', '0032_attendance'), ('employees', '0033_alter_attendance_employee')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(choices=[('A', 'Administration'), ('L', 'Labour'), ('M', 'Marketing')], max_length=2)),
                ('status', models.CharField(choices=[('A', 'Active'), ('OL', 'On Leave')], default='A', max_length=2)),
                ('date_employed', models.DateField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('supervisor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='employees.employee')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('hod', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='head_of_department', to='employees.employee')),
            ],
        ),
        migrations.AlterField(
            model_name='employee',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='employees.department'),
        ),
        migrations.AddField(
            model_name='employee',
            name='date_updated',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='employee',
            name='is_hr',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='employee',
            name='is_md',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='employee',
            name='date_employed',
            field=models.DateField(default=datetime.datetime(2022, 2, 16, 14, 9, 7, 251019, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='employee',
            name='date_employed',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='employee',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employee', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='employee',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AddField(
            model_name='employee',
            name='job',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='jobs.job'),
        ),
        migrations.AlterField(
            model_name='department',
            name='hod',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='head_of_department', to='employees.employee', unique=True),
        ),
        migrations.AlterField(
            model_name='department',
            name='hod',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='head_of_department', to='employees.employee'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='date_employed',
            field=models.DateField(auto_now=True),
        ),
        migrations.RemoveField(
            model_name='employee',
            name='status',
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='client', to=settings.AUTH_USER_MODEL)),
                ('company', models.CharField(max_length=255)),
                ('position', models.CharField(default=1, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateField()),
            ],
            options={
                'unique_together': {('name', 'date')},
            },
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('punch_in', models.TimeField()),
                ('punch_out', models.TimeField(blank=True, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance', to='employees.employee')),
            ],
            options={
                'unique_together': {('employee', 'date')},
            },
        ),
    ]