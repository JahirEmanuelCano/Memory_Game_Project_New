from django.contrib import admin
from .models import Card, GameSession, Stats

admin.site.register(Card)
admin.site.register(GameSession)
admin.site.register(Stats)