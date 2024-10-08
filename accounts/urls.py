from django.urls import path
from .views import (
    CustomLoginView,
    SignUpView,
    CustomLogoutView,
    ProfileEditView,
    ProfileView,
    PasswordChangeView,
)

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile/edit/", ProfileEditView.as_view(), name="profile_edit"),
    path("password_change/", PasswordChangeView.as_view(), name="password_change"),
]
