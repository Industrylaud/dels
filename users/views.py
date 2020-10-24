from .models import CustomUser
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from allauth.account.views import PasswordChangeView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


# class SignupPageView(generic.CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'signup.html'


class CustomPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('home')


class UserProfileView(UpdateView):
    model = get_user_model()
    template_name = 'user_profile.html'
    queryset = CustomUser.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("username")
        user = get_object_or_404(CustomUser, username=id_)
        return user

    fields = [
        'index_number',
        'student_group',
        'sub_group',
        'email',
    ]
