from django.shortcuts import render
from django.shortcuts import redirect



def old_to_new_redirect(request):
    return render(request, 'core/index.html')

def index(request):
    return render(request, 'core/index.html')

def posters(request):
    return render(request, 'core/posters.html')

def FAQ(request):
    return render(request, 'core/FAQ.html')

def journals(request):
    return render(request, 'core/journals.html')

def Dashboard(request):
    return render(request, 'core/Dashboard.html')

def Portal(request):
    return render(request, 'core/Portal.html')

def PosterSubmit(request):
    return render(request, 'core/PosterSubmit.html')