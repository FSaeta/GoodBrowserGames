from django.urls import path
from .views import index, avaliacoes, marcar_como_util

urlpatterns = [
    path('', index, name='index'),
    path('avaliacoes', avaliacoes, name='avaliacoes'),
    path('marcar_como_util/<int:av_id>', marcar_como_util, name='marcar_como_util')
]
