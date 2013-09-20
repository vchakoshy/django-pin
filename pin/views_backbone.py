
from django.shortcuts import render


def home(request):
    return render(request, 'pin/backbone-home.html')


def notif(request):
    return render(request, 'pin/backbone-notif.html')
