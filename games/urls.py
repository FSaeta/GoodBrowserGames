from django.urls import path
from .views import index, games, avaliacoes, marcar_como_util

urlpatterns = [
    path('', index, name='index'),
    path('games-<int:page>', games, name='games'),
    path('games-<int:page>/orderby=<str:orderby>/filter=<str:filter>', games, name='game_search'),
    path('games-<int:page>/orderby=<str:orderby>/filter=<str:filter>/search=<str:search>', games, name='game_search'),
    path('avaliacoes', avaliacoes, name='avaliacoes'),
    path('marcar_como_util/<int:av_id>', marcar_como_util, name='marcar_como_util')
]
