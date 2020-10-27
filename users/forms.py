from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    email = forms.CharField(max_length=75, required=True)

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )

    def clean(self):
        cleaned_data = super(CustomUserCreationForm, self).clean()

        email_field = cleaned_data.get('email')

        if email_field is not None:
            if get_user_model().objects.filter(email=email_field).first():
                self.add_error(None, ValidationError('this email already exist'))


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'index_number',
            'student_group',
            'sub_group',
        )


class UserProfileStudentChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            'index_number',
            'student_group',
            'sub_group',
        )


class CustomUserChangeEmailForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = (
            'email',
        )

    def clean(self):
        cleaned_data = super(CustomUserChangeEmailForm, self).clean()

        email_field = cleaned_data.get('email')

        if email_field is not None:
            if get_user_model().objects.filter(email=email_field).first():
                self.add_error(None, ValidationError('this email already exist'))
