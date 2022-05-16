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

class SearchFiltersOption:
    def __init__(self, opt, string):
        self.option = opt
        self.str = string

def get_search_options(kind):
    """<option value="-create_date" selected>Mais Recentes</option>
       <option value="create_date">Mais Antigos</option>
       <option value="nome">Ordem Alfabética</option>
       <option value="recomendados">Recomendados</option>
    """
    if kind == 'order':
        options = [
            ('-create_date', 'Mais Recentes'),
            ('create_date', 'Mais Antigos'),
            ('nome', 'Ordem Alfabética'),
            ('recomendados', 'Recomendados')
        ]
    else:
        options = [
            ('nome', 'Nome'),
            ('categoria', 'Categoria')
        ]
    return [SearchFiltersOption(option[0], option[1]) for option in options]

def games(request, page=1, orderby='-create_date', filter='nome', search=False):
    user = request.user

    if request.method == 'POST':
        if 'search_submit' in request.POST:
            order_by = request.POST.get('orderby', orderby)
            filter_by = request.POST.get('filter', filter)
            search_by = request.POST.get('search', '').strip()

            redirect_page = f'/games-1/orderby={order_by}/filter={filter_by}'
            if search_by:
                redirect_page += f'/search={search_by}'

            return redirect(redirect_page)

    if orderby == 'recomendados':
        games_to_show = user.get_games_recomendados(30, False)
    else:
        games_to_show = BrowserGame.objects.order_by(orderby)

    if filter and search:
        if filter == 'nome':
            games_to_show = games_to_show.filter(nome__icontains=search)
        else:
            games_to_show = games_to_show.filter(categoria__nome__icontains=search)

    games_to_show = games_to_show[30*(page-1):30*page]

    context = {
        'user': user,
        'games': games_to_show,
        'order_options': get_search_options('order'),
        'filter_options': get_search_options('filter'),
        'search_by': search,
        'filter_by': filter,
        'order_by': orderby
    }
    return render(request, 'games.html', context)

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
