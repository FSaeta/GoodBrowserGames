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

    games_viewed = models.ManyToManyField(
        'games.BrowserGame',
        verbose_name='Games Visualizados')


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

    def get_categorias_melhores_avaliadas(self):
        """ - Utiliza dicionário para somar a nota e quantidade total de avaliações realizadas
            agrupando pelas categorias. 
            - O id de todas as categorias foram setados como as chaves do dicionário, e valores 
            zerados para cada categoria foram adicionados como o valor.
        """
        # Obtendo referência aos objetos do BrowserGame e Categoria
        Game = apps.get_model('games', 'BrowserGame')
        Categoria = apps.get_model('games', 'Categoria')

        default_values = {'nota': 0, 'qtd': 0, 'media': 0}
        # Cria dicionário agrupado pelos ids das categorias que possuem jogos cadastrados 
        categ_dict = {categ.id: {**default_values} for categ in Categoria.objects.exclude(browsergame=None)}

        avaliacoes = self.avaliacao_set.order_by('-create_date')[:100]
        avaliacoes_values = avaliacoes.values('game', 'rating')

        # Analisa cada avaliação das 100 ultimas feitas pelo usuário
        for avaliacao in avaliacoes_values:
            # Obtém o jogo e a categoria correspondente à avaliação
            game_obj = Game.objects.get(pk=avaliacao['game'])
            categ_id = game_obj.categoria.id

            # Obtém nota, quantidade de avaliações feitas ref a categoria e 
            # media da nota total / qtd avaliacões  da categoria
            categ_values = categ_dict.get(categ_id, default_values).copy()

            # Atualiza valores acumulados referente a categoria
            categ_values['nota'] += avaliacao['rating']
            categ_values['qtd'] += 1
            categ_values['media'] = categ_values['nota']/categ_values['qtd']
            categ_dict[categ_id] = categ_values

        # Transforma dicionário das categorias em uma lista para poder ordená-la pelas
        # categorias que tiveram as maiores médias
        categ_list = [{'categ_id': categ_id,
                       'qtd_games': Game.objects.filter(categoria=categ_id).count(), 
                       **categ_data} for categ_id, categ_data in categ_dict.items()]

        categ_list = sorted(categ_list,
                            key=lambda item: item['media'],
                            reverse=True)

        return categ_list

    def get_games_recomendados(self, limit, not_seen_only=True):
        # Obtendo objetos dos games
        Game = apps.get_model('games', 'BrowserGame')

        # Obtém uma lista ordenada pelas categorias de jogos melhores avaliadas pelo usuário 
        categs_preferidas = self.get_categorias_melhores_avaliadas()
        # Obtém as top3 categorias preferidas pelo usuário
        top3_preferidas = [categs_preferidas.pop(0) for i in range(3 if 3 < len(categs_preferidas) else len(categs_preferidas))]

        # Lista utilizada para mostrar quais games serão mostrados como recomendados
        games_to_show = []
        # Adicionamos games na lista enquanto a lista for menor que o limite, ou houverem games
        # a serem mostrados
        categ_index = 0
        while len(games_to_show) != limit and (categs_preferidas or top3_preferidas):
            # o peso determina quantos games serão selecionados da categoria
            peso = 4 - categ_index if top3_preferidas else 3
            
            # Caso ainda existam categorias no top3, será utilizada uma de lá, se ja tiverem
            # acabado os games das top3 será recomendado games de outras categorias.
            categs = top3_preferidas or categs_preferidas
            categ = categs.pop(categ_index)

            games_ids = [game.id for game in games_to_show]
            # Se devemos buscar apenas por novos jogos, como ocorre na pág principal
            if not_seen_only and (categs or categs_preferidas):
                games_ignored = Game.objects.filter(avaliacao__user__id=self.id, categoria=categ['categ_id'])
                games_ids.extend((x[0] for x in games_ignored.values_list('id')))
            else:
                games_ignored = []

            # Jogos selecionados para a primeira categoria
            games_filtered = Game.objects.filter(categoria=categ['categ_id']) \
                                         .exclude(id__in=games_ids)           \
                                         .order_by('-create_date')[:peso]

            games_to_show.extend(games_filtered)
            categ['qtd_games'] -= len(games_filtered)

            # Atualiza o índice da categoria sendo avaliada para alterar o peso e 
            # mesclar com games de outras categorias
            if categ['qtd_games'] - len(games_ignored) > 0 and len(categs) > 0:
                categs.insert(categ_index, categ)
                categ_index += 1
            elif categ['qtd_games'] - len(games_ignored) > 0:
                categs.insert(categ_index, categ)
            else:
                categ_index = 0
            if categ_index >= len(categs):
                categ_index = 0

        return games_to_show


    def get_games_to_show(self, main_page=True):
        limit = 8 if main_page else 30
        Games = apps.get_model('games', 'BrowserGame')
        all_games = Games.objects.all()
        games_dict = {
            'recomendado': self.get_games_recomendados(limit, not_seen_only=main_page)[:limit],
            'recente': all_games.order_by('-create_date')[:limit],
            'most_rated': sorted(all_games, key=lambda game: game.avaliacao_set.count())[:limit]
        }

        return games_dict

