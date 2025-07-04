from django.shortcuts import render

def home(request):
    return render(request, 'memory_game/home.html')
