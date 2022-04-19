from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

from django.apps import apps

import datetime
import pycountry


class Pais(models.Model):

    sigla = models.CharField(verbose_name='Sigla', max_length=3)
    nome = models.CharField(verbose_name='Nome', max_length=255)

    def __str__(self):
        return f'{self.nome} ({self.sigla})'

    def add_paises():
        for country in pycountry.countries:
            new_country = Pais(sigla=country.alpha_3, nome=country.name)
            new_country.save()
            print(f"País '{country.name}' foi carregado.")
        print("Todos os Países foram carregados !")


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, first_name, last_name, password=None, **extra_fields):
        if not email:
            raise ValueError('O campo email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, username, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, first_name, last_name, password, **extra_fields)


    def create_superuser(self, username, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('data_nascimento', datetime.date.today())
        return self._create_user(username, email, first_name, last_name, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(
        'E-mail', unique=True)

    estado = models.CharField(
        'Estado', max_length=255, default="São Paulo", blank=False)

    pais = models.ForeignKey(
        Pais, verbose_name='Pais', on_delete=models.RESTRICT, blank=False, null=True)

    data_nascimento = models.DateField(
        "Data de Nascimento")

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'password']

    objects = UserManager()


    def get_fields_kwargs(self):
        return {
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'estado': self.estado,
            'cidade': self.cidade,
            'data_nascimento': self.data_nascimento
        }

    def get_games_to_show(self):
        import pdb; pdb.set_trace()
        Games = apps.get_model('games', 'BrowserGame')

