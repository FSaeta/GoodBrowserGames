from django.db import models
from users.models import User

from stdimage.models import StdImageField


class Categoria(models.Model):
    nome = models.CharField("Nome", max_length=255)

    def __str__(self):
        return self.nome

    def carregar_categorias_padrao():
        categorias = ['Strategy', 'Shooter', 'Puzzle', 'Arcade', 'RPG', 'Sports', 'Action', 'Adventure']
        for name in categorias: 
            categoria = Categoria(nome=name)
            categoria.save()
            print(f"Categoria '{name}' foi carregada.")
        print("Todas as Categorias foram carregadas !")


class BrowserGame(models.Model):
    nome = models.CharField("Nome", max_length=255, unique=True)

    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.RESTRICT,
        verbose_name='Categoria')

    game_url = models.URLField(verbose_name='Url do Jogo')

    video_url = models.URLField(
        verbose_name='Url do Vídeo', null=True, blank=True)

    descricao = models.TextField(max_length=255)

    imagem = StdImageField(
        "Imagem", null=True, blank=True, 
        upload_to='games/uploads/imgs',
        variations={'thumbnail': (200, 200, True), 'large': (500, 500)})


class Avaliacao(models.Model):
    VALORES = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))

    game = models.ForeignKey(
        BrowserGame, on_delete=models.CASCADE, verbose_name='Jogo')

    rating = models.IntegerField(
        'Avaliação', choices=VALORES)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Usuário")

    comentario = models.TextField(
        "Comentário", max_length=255, null=True, blank=True)

    create_date = models.DateTimeField(
        "Data de Criação", auto_now=True, blank=True)

    users_liked = models.ManyToManyField(
        User, 
        verbose_name="Users Liked",
        related_name="liked_avaliacoes")

    class Meta:
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"


