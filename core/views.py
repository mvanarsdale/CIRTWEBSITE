from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse




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

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.shortcuts import redirect

# move to users later
def ajax_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({
                'success': True,
                # to change the login button when signed in
                'username': user.username,
                'redirect_url': reverse('Dashboard')  # Redirect to the Dashboard URL
            })
        else:
            return JsonResponse({
                'success': False,
                'error_message': 'Invalid credentials'
            })
