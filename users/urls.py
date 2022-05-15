from django.urls import path
from .views import CreateUserView, relatorios

urlpatterns = [
    path('registration', CreateUserView.as_view(), name='cadastro_usuario'),
    path('relatorios/', relatorios, name='relatorios'),
    path('relatorios/start=<str:start>/stop=<str:stop>', relatorios, name='relatorios-filtrados')
]
