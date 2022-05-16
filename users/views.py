from django.shortcuts import render, redirect
from django.db.models import Count, Avg

import datetime
import pytz

from django.views.generic.edit import CreateView

from .models import User
from games.models import BrowserGame, Categoria

from .forms import UserCreateForm

class CreateUserView(CreateView):
    
    model = User
    form_class = UserCreateForm

    template_name = 'registration/user_registration.html'
    success_url = '/auth/login'

class LinhaRelatorio:
    def __init__(self, pos, nome, valor):
        self.pos = pos
        self.nome = nome
        self.valor = valor

class Relatorio:
    def __init__(self, start=0, stop=0, class_obj=BrowserGame, top=5):
        self.start = datetime.datetime(start.year, start.month, start.day, tzinfo=pytz.UTC) if start else start
        self.stop = datetime.datetime(stop.year, stop.month, stop.day, tzinfo=pytz.UTC) if stop else stop
        self.class_obj = class_obj
        self.top = top
        self.objects = self.compute_objects()
        self.objs_len = len(self.objects)
        self.nome = 'Games Com Mais Avaliações'
    
    def get_objects_vals(self, objects):
        values = [x for x in objects.order_by('-av_count')[:self.top].values('av_count', 'nome')]
        [values[x].update({'pos': x+1}) for x in range(len(values))]
        return values

    def compute_objects(self):
        objs_grouped = self.class_obj.objects.annotate(av_count=Count('avaliacao__id'))

        objs_grouped = self.filter_date_objs(objs_grouped)
        values = self.get_objects_vals(objs_grouped)

        values = [LinhaRelatorio(v['pos'], v['nome'], v['av_count']) for v in values]
        values = self.ajustar_linhas(values)

        return values

    def filter_date_objs(self, objs):
        if self.start:
            objs = objs.filter(avaliacao__create_date__gte=self.start)
        if self.stop:
            objs = objs.filter(avaliacao__create_date__lte=self.stop)
        return objs
    
    def ajustar_linhas(self, values):
        while len(values) < 5:
            values.append(LinhaRelatorio('---', '-----', '---'))
        return values
    
    def value_label(self):
        return 'Qtd. Avaliações'
    
    def object_label(self):
        return 'Browser Game'

class RelatorioCategorias(Relatorio):
    def __init__(self, start=0, stop=0, class_obj=Categoria, top=3):
        super().__init__(start, stop, class_obj, top)
        self.nome = 'Categorias Mais Avaliadas'

    def compute_objects(self):
        objs_grouped = self.class_obj.objects.annotate(
            av_count=Count('browsergame__avaliacao__id')
        )
        if self.start:
            objs_grouped = objs_grouped.filter(browsergame__avaliacao__create_date__gte=self.start)
        if self.stop:
            objs_grouped = objs_grouped.filter(browsergame__avaliacao__create_date__lte=self.stop)

        values = self.get_objects_vals(objs_grouped)
        values = [LinhaRelatorio(v['pos'], v['nome'], v['av_count']) for v in values]
        values = self.ajustar_linhas(values)

        return values

    def object_label(self):
        return 'Categoria'

class RelatorioUsers(Relatorio):
    def __init__(self, start=0, stop=0, class_obj=User, top=5):
        super().__init__(start, stop, class_obj, top)
        self.nome = 'Usuários que mais Avaliaram'

    def compute_objects(self):
        objs_grouped = self.class_obj.objects.annotate(
            av_count=Count('avaliacao__id')
        )
        objs_grouped = self.filter_date_objs(objs_grouped)

        values = [x for x in objs_grouped.order_by('-av_count')[:self.top].values('av_count', 'username')]
        [values[x].update({'pos': x+1, 'nome': values[x]['username']}) for x in range(len(values))]

        values = [LinhaRelatorio(v['pos'], v['nome'], v['av_count']) for v in values]
        values = self.ajustar_linhas(values)

        return values

    def object_label(self):
        return 'Usuário'

class RelatorioMediaGames(Relatorio):
    def __init__(self, start=0, stop=0, class_obj=BrowserGame, top=5):
        super().__init__(start, stop, class_obj, top)
        self.nome = 'Games com Maiores Médias'

    def compute_objects(self):
        objs_grouped = self.class_obj.objects.annotate(
            av_media=Avg('avaliacao__rating'), 
            av_count=Count('avaliacao__id')
        ).filter(av_count__gte=4)

        objs_grouped = self.filter_date_objs(objs_grouped)

        values = [x for x in objs_grouped.order_by('-av_media')[:self.top].values('av_media', 'av_count', 'nome')]
        [values[x].update({'pos': x+1}) for x in range(len(values))]

        values = [LinhaRelatorio(v['pos'], v['nome'], v['av_media']) for v in values]
        values = self.ajustar_linhas(values)

        return values

    def value_label(self):
        return 'Nota Média'


def criar_relatorios(start=0, stop=0):
    dict_relatorios = {
        'games_mais_avaliados': Relatorio(start, stop),
        'usuarios_mais_avaliaram': RelatorioUsers(start, stop, User),
        'categorias_mais_avaliadas': RelatorioCategorias(start, stop, Categoria, 3),
        'games_maior_media': RelatorioMediaGames(start, stop)
    }
    return dict_relatorios


def relatorios(request, start=0, stop=0):
    user = request.user

    str_stop, str_start = '', ''

    if request.method == 'POST':
        if 'refresh-period' in request.POST:
            str_start = request.POST.get('start', 0)
            str_stop = request.POST.get('stop', 0)

            return redirect(f'/user/relatorios/start={str_start or "0"}/stop={str_stop or "0"}')

    if start and start != '0':
        str_start = start
        start = datetime.datetime.strptime(start, '%Y-%m-%d')
    elif start == '0':
        start = 0

    if stop and stop != '0':
        str_stop = stop
        stop = datetime.datetime.strptime(stop, '%Y-%m-%d')
    elif stop == '0':
        stop = 0

    context = {
        'user': user,
        'relatorios': criar_relatorios(start, stop),
        'start': str_start,
        'stop': str_stop,
        'range1_5': range(0, 5)
    }
    return render(request, 'relatorios.html', context)