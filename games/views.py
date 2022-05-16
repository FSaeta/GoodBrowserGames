from django.shortcuts import render, redirect

from django.db.models import Count
from .models import *
from users.models import Pais

def index(request):
    user = request.user

    if not Categoria.objects.exclude(nome='TESTE'):
        Categoria.carregar_categorias_padrao()
    if not Pais.objects.all():
        Pais.add_paises()

    if user.is_authenticated:
        games_to_show = user.get_games_to_show(main_page=True)
    else:
        games_to_show = BrowserGame.objects.order_by('-create_date')[:16]
    
    context = {
        'user': user,
        'games_sections': games_to_show
    }
    return render(request, 'index.html', context)


def avaliacoes(request):
    user = request.user

    avaliacoes = Avaliacao.objects.annotate(
        likes_count=Count('users_liked'),
    ).order_by('-likes_count', '-rating')

    likes_dict = {av.id: user in av.users_liked.all() for av in avaliacoes}

    context = {
        'user': user,
        'avaliacoes': avaliacoes,
        'range1_5': [x for x in range(1, 6)],
        'likes_dict': likes_dict
    }
    return render(request, 'avaliacoes.html', context)

def marcar_como_util(request, av_id):
    user = request.user
    if not user.is_authenticated:
        return redirect('/')

    av = Avaliacao.objects.get(id=av_id)
    if not user in av.users_liked.all():
        av.users_liked.add(user)
    return redirect(f'/avaliacoes#av_{av_id}')
