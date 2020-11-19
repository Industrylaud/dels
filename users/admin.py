from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from groups.models import Post
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import StudentGroup


CustomUser = get_user_model()


class PostInLine(admin.TabularInline):
    model = Post
    extra = 0


class CustomUsersInLine(admin.TabularInline):
    model = CustomUser
    extra = 0
    fields = ['index_number', 'last_name', 'first_name', 'email', 'sub_group', ]
    readonly_fields = ['index_number', 'last_name', 'first_name', 'email', 'sub_group', ]


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'first_name', 'last_name', ]
    fieldsets = UserAdmin.fieldsets + (
            (('Student'), {'fields': ('index_number', 'student_group', 'sub_group')}),
    )
    list_filter = ['student_group', 'sub_group']


@admin.register(StudentGroup)
class StudentGroupAdmin(admin.ModelAdmin):
    inlines = [
        CustomUsersInLine,
        PostInLine,
    ]
    list_display = ('name',)


# admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(StudentGroup, StudentGroupAdmin)
