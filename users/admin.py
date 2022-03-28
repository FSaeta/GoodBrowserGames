from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

# from .forms import UsuarioCreateForm, AlteracaoCadastro


@admin.register(User)
class UsuarioAdmin(admin.ModelAdmin):
    # add_form = UsuarioCreateForm
    # form = AlteracaoCadastro
    model = User

    list_display = (
        'username', 'email', 
        'password', 'first_name', 'last_name',
        'data_nascimento')

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'data_nascimento')}),
        ('Segurança', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas', {'fields': ('last_login', 'date_joined')}),
    )

"""@admin.register(Cidade)
class CidadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'estado')

@admin.register(Estado)
class EstadoAdmin(admin.ModelAdmin):
    list_display = ('sigla',)"""