from django.shortcuts import render

from django.views.generic.edit import CreateView

from .models import User
from .forms import UserCreateForm

class CreateUserView(CreateView):
    
    model = User
    form_class = UserCreateForm

    template_name = 'registration/user_registration.html'
    success_url = '/auth/login'

