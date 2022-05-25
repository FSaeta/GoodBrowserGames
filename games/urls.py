from django.urls import path
from .views import index, games, avaliacoes, marcar_como_util, game_page, fazer_avaliacao

urlpatterns = [
    path('', index, name='index'),
    path('games/game_id=<int:pk>', game_page, name='game_page'),
    path('games/game_id=<int:pk>/edit=<int:edit>', game_page, name='game_page_edit'),
    path('avaliar/game=<int:game_id>', fazer_avaliacao, name='fazer_avaliacao'),
    path('games-<int:page>', games, name='games'),
    path('games-<int:page>/orderby=<str:orderby>/filter=<str:filter>', games, name='game_search'),
    path('games-<int:page>/orderby=<str:orderby>/filter=<str:filter>/search=<str:search>', games, name='game_search'),
    path('avaliacoes', avaliacoes, name='avaliacoes'),
    path('marcar_como_util/<int:av_id>', marcar_como_util, name='marcar_como_util')
]
