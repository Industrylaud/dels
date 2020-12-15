from django import forms

from subjects.models import Task, Resource


class CustomDateTimeInput(forms.DateTimeInput):
    input_type = 'date'


class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'body',
            'deadline',
            'file',
        ]
        widgets = {
            'deadline': CustomDateTimeInput(),
            'body': forms.Textarea()
        }


class ResourceCreationForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = [
            'body',
            'file',
        ]
        widgets = {
            'body': forms.Textarea()
        }
