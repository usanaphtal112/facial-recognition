from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import CustomUser


class AdminRoleTestPassMixin(UserPassesTestMixin):
    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.role == CustomUser.Role.ADMIN
        )

    def handle_no_permission(self):
        raise PermissionDenied


class UserRoleTestPassMixin(UserPassesTestMixin):
    def test_func(self):
        return (
            self.request.user.is_authenticated
            and self.request.user.role == CustomUser.Role.USER
        )

    def handle_no_permission(self):
        raise PermissionDenied
