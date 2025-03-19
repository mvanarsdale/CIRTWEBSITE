from django.shortcuts import render


def index(request):
    return render(request, 'core/index.html')

def posters(request):
    return render(request, 'core/posters.html')
