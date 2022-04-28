from django.db import models


GAMES = (
    ('CS:Go', 'CS:Go'),
    ('Dota 2', 'Dota 2'),
    ('World of warcraft', 'World of warcraft'),
    ('Mortal combat', 'Mortal combat'),
    ('God of war', 'God of war'),
    ('GTA V', 'GTA V'),
    ('FIFA', 'FIFA'),
    ('NHL', 'NHL')
)


class Profile(models.Model):
    name = models.CharField(max_length=50, verbose_name='Никнэйм')
    game = models.CharField(max_length=30, choices=GAMES, verbose_name='Основная игра')
    description = models.TextField(blank=True, verbose_name='О себе')
    search = models.BooleanField(default=True, verbose_name='Статус для поиска')
    chat_id = models.IntegerField(verbose_name='ID чата')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
