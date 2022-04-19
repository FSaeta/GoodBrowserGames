# Generated by Django 4.0.3 on 2022-04-09 03:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sigla', models.CharField(max_length=3, verbose_name='Sigla')),
                ('nome', models.CharField(max_length=255, verbose_name='Nome')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='estado',
            field=models.CharField(default='São Paulo', max_length=255, verbose_name='Estado'),
        ),
        migrations.AddField(
            model_name='user',
            name='pais',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='users.pais', verbose_name='Pais'),
        ),
    ]