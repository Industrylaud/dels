from .forms import CustomUserChangeEmailForm
from .models import CustomUser
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from allauth.account.views import PasswordChangeView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin


class CustomPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('home')


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'user_profile.html'
    queryset = CustomUser.objects.all()
    fields = (
            'index_number',
            'student_group',
            'sub_group',
        )

    def get_object(self):
        return self.request.user


class CustomUserChangeEmailView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'email_change.html'
    form_class = CustomUserChangeEmailForm

    def get_object(self):
        return self.request.user
