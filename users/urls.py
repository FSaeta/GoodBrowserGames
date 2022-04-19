from django.urls import path
from .views import CreateUserView

urlpatterns = [
    path('registration', CreateUserView.as_view(), name='cadastro_usuario')
]
