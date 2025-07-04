from django.db import models
from django.contrib.auth.models import User

class Card(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='cards/')  # Opcional, si usas imágenes

    def __str__(self):
        return self.name

class GameSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=10)
    time_taken = models.IntegerField()  # tiempo en segundos
    won = models.BooleanField()
    date_played = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.difficulty} - {"Ganó" if self.won else "Perdió"}'

class Stats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    total_games = models.IntegerField(default=0)
    average_time = models.FloatField(default=0.0)
    favorite_difficulty = models.CharField(max_length=10, default="básico")
