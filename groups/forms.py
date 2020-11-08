from django import forms


class PostCreationForm(forms.Form):
    body = forms.CharField(strip=False, max_length=1000)