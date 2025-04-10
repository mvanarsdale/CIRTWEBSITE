from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.contrib.auth import get_user_model



from django.contrib.auth import authenticate, login
from django.http import JsonResponse

# for messages with log in success / failure
from django.contrib import messages

from core.models import CustomUser

# page views
def old_to_new_redirect(request):
    return render(request, 'core/index.html')

# for the homepage
def index(request):
    return render(request, 'core/index.html')

# for the posters page
def posters(request):
    return render(request, 'core/posters.html')

# for the FAQ page
def FAQ(request):
    return render(request, 'core/FAQ.html')

# for the publications page
def journals(request):
    return render(request, 'core/journals.html')

# for the dashboard page
def Dashboard(request):
    return render(request, 'core/Dashboard.html')

# portals 
# editor portal
def editPort(request):
    return render(request, 'core/editPort.html')

# reviewer portal
def reviewPort(request):
    return render(request, 'core/reviewPort.html')

# author portal
def authPort(request):
    return render(request, 'core/authPort.html')

# poster submit view 
def PosterSubmit(request):
    return render(request, 'core/PosterSubmit.html')

# 
def posterSub(request):
    return render(request, 'core/posterSub.html')

def Portal(request):
    return render(request, 'core/Portal.html')

def journalSub(request):
    return render(request, 'core/journalSub.html')

def JournalProc(request):
    return render(request, 'core/Journal_Process.html')

def subComp(request):
    return render(request, 'core/subComp.html')


# code pulled from ChatGPT
def signup(request):
    # defines new user variables
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
        
        # create a user object
        CustomUser.objects.create_user(username=username, password=password, email=email, first_name=name, role=role)        
        
        #messages.success(request, 'Account created successfully!')
        return redirect(ajax_login(request))
    
    return render(request, 'components/signup_popup.html')

# Code generated from ChatGPT
def ajax_login(request):
    # checks for user in database
    if request.method == 'POST':
        # variables for username and password
        username = request.POST.get('username')
        password = request.POST.get('password')

        # defines user username and password to be checked
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

# Jamie's code
def check_login_status(request):
    if request.user.is_authenticated:
        return JsonResponse({
            'is_logged_in': True,
            'username': request.user.username
        })
    else:
        return JsonResponse({'is_logged_in': False})
  
# Jamie's code  
@csrf_exempt  # Only use this if you aren't passing CSRF token properly
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Only POST allowed'}, status=405)
#added from chatgpt
@csrf_exempt
def ajax_signup(request):
    User = get_user_model()
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'error_message': 'Username already taken'})

        user = User.objects.create_user(username=username, password=password, email=email)
        user.first_name = name
        user.save()

        login(request, user)

        return JsonResponse({'success': True, 'username': user.username})
    
    return JsonResponse({'success': False, 'error_message': 'Invalid request'})