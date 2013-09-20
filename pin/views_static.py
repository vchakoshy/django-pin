from django.shortcuts import render


def android(request):
    return render(request, 'pin/android.html')
