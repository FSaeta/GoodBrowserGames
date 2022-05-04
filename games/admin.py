from django.contrib import admin

from .models import BrowserGame, Categoria, Avaliacao


@admin.register(BrowserGame)
class SerieAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'game_url', 'video_url', 'descricao', 'imagem')


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('game', 'rating', 'user', 'comentario')
