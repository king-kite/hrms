from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsHROrMD(BasePermission):
    """
    The request is authenticated as an HR or MD.
    """

    def has_permission(self, request, view):
        valid = False
        try:
            valid = bool(
            request.user.is_anonymous is False and request.user.is_staff and
            request.user.is_authenticated and request.user.is_active and
            (request.user.employee.is_hr or request.user.employee.is_md))
        except:
            pass
        return valid


class IsHROrMDOrAdminUser(BasePermission):
    """
    The request is authenticated as an HR or MD and safe methods for admin users.
    """

    def has_permission(self, request, view):
        valid = False
        try:
            valid = bool(
            request.user.is_anonymous is False and request.user.is_active and (
            request.method in SAFE_METHODS and request.user.is_staff) or
            request.user.is_authenticated and
            (request.user.employee.is_hr or request.user.employee.is_md))
        except:
            pass
        return valid
