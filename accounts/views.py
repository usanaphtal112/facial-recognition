from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, DetailView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .forms import CustomUserCreationForm
from .forms import ProfileForm
from .models import CustomUser


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "accounts/signup.html"


class CustomLogoutView(LogoutView):
    next_page = "/"


class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "accounts/profile.html"
    context_object_name = "user"

    def get_object(self):
        return self.request.user


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = ProfileForm
    template_name = "accounts/profile_edit.html"
    success_url = reverse_lazy("profile")

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        try:
            if "profile_image" in self.request.FILES:
                file = self.request.FILES["profile_image"]

                # Save the new profile image to the media directory
                file_path = default_storage.save(
                    f"profile/{file.name}", ContentFile(file.read())
                )
                form.instance.profile_image = file_path

            messages.success(self.request, "Profile updated successfully.")
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)


class CustomPasswordChangeView(PasswordChangeView):
    template_name = "registration/password_change_form.html"
    success_url = reverse_lazy("profile")

    def get_form_class(self):
        return PasswordChangeForm

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))
