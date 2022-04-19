from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms

from .models import User

from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

class UserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'data_nascimento', 'pais', 'estado']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
            'password': forms.PasswordInput
        }
        labels = {
            'username': 'Username',
        }
    
    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].required = True
            if field in ('username','email', 'password1','password2'):
                self.fields[field].help_text = ''
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user