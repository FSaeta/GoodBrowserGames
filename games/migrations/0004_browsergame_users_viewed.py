# Generated by Django 4.0.3 on 2022-04-28 14:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('games', '0003_alter_browsergame_options_avaliacao_create_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='browsergame',
            name='users_viewed',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Users Viewed'),
        ),
    ]