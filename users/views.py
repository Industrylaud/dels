from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from allauth.account.views import PasswordChangeView


# class SignupPageView(generic.CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'signup.html'


class CustomPasswordChangeView(PasswordChangeView):
    success_url = reverse_lazy('home')
