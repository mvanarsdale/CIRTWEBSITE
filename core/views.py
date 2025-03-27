from django.shortcuts import redirect, render
from django.urls import reverse


from django.contrib.auth import authenticate, login
from django.http import JsonResponse

from django.contrib.auth.models import User
from django.contrib import messages

from core.models import CustomUser






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


# code from ChatGPT
def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        # Check if username or email already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken!')
            return redirect('signup')
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email is already in use!')
            return redirect('signup')
        
        CustomUser.objects.create_user(username=username, password=password, email=email, first_name=name, role=role)        
        # Save role if using a Profile model
        #Profile.objects.create(user=user, role=role)
        
        #messages.success(request, 'Account created successfully!')
        return redirect(ajax_login(request))
    
    return render(request, 'components/signup_popup.html')
        

# move to users later 
# Code from ChatGPT
def ajax_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        # check for user in database
        if user is not None:
            login(request, user)
            return JsonResponse({
                'success': True,
                # to change the login button when signed in
                'username': user.username,
                # Redirect to the Dashboard URL
                'redirect_url': reverse('Dashboard')  
            })
        else:
            # user doesn't exist or a typo happened 
            return JsonResponse({
                'success': False,
                'error_message': 'Invalid credentials'
            })
