# Generated by Django 4.0.4 on 2022-04-28 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Никнэйм')),
                ('game', models.CharField(choices=[('CS:Go', 'CS:Go'), ('Dota 2', 'Dota 2'), ('World of warcraft', 'World of warcraft'), ('Mortal combat', 'Mortal combat'), ('God of war', 'God of war'), ('GTA V', 'GTA V'), ('FIFA', 'FIFA'), ('NHL', 'NHL')], max_length=30, verbose_name='Основная игра')),
                ('description', models.TextField(blank=True, verbose_name='О себе')),
                ('search', models.BooleanField(default=True, verbose_name='Статус для поиска')),
                ('chat_id', models.IntegerField(verbose_name='ID чата')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
    ]
