from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import StudentGroup


CustomUser = get_user_model()


class CustomUsersInLine(admin.TabularInline):
    model = CustomUser
    extra = 0
    fields = ['index_number', 'last_name', 'first_name', 'email',]


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'first_name', 'last_name', ]


class StudentGroupAdmin(admin.ModelAdmin):
    inlines = [
        CustomUsersInLine,
    ]
    list_display = ('name',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(StudentGroup, StudentGroupAdmin)
