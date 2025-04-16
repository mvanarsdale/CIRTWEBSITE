from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from django.contrib.auth import get_user_model
#from . import models

from django.contrib.auth import authenticate, login
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required

# for messages with log in success / failure
#from django.contrib import messages


from core.models import Editor, Reviewer, Author #CustomUser

# for poster upload


from django.http import FileResponse, Http404
from .models import Poster



# page views
def old_to_new_redirect(request):
    return render(request, 'core/index.html')

# for the homepage
def index(request):
    return render(request, 'core/index.html')

# for the posters page
def posters(request):
    posters = Poster.objects.all()
    return render(request, 'core/posters.html', {'posters': posters})

# for the homepage
def contact(request):
    return render(request, 'core/contact.html')

# for the FAQ page
def FAQ(request):
    return render(request, 'core/FAQ.html')

# for the publications page
def journals(request):
    return render(request, 'core/journals.html')

# for the dashboard page
#@login_required
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
@login_required
def authPort(request):
    user_posters = Poster.objects.filter(author=request.user)
    return render(request, 'core/authPort.html', {'posters': user_posters})

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
        
        if role:
            user.role = role  # ←💥 ADD THIS LINE to set the role!
        user.save()


        if role == 'Author':
            Author.objects.create(user=user)
        elif role == 'Editor':
            Editor.objects.create(user=user)
        elif role == 'Reviewer':
            Reviewer.objects.create(user=user)

        login(request, user)

        return JsonResponse({'success': True, 'username': user.username})
    
    return JsonResponse({'success': False, 'error_message': 'Invalid request'})

# view for poster submit form
def upload_poster(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        #author = request.POST.get('author')
        pdf = request.FILES.get('pdf')
        
        # getting the authors specfic username - help from ChatGPT
        user = request.user
        #usern = CustomUser.objects.get(user=user)
        #username = user.username
        #author = CustomUser.objects.get(author=author)
        date = request.submitted_date
        
    
        poster = Poster.objects.create(title=title, author=user, date=date, pdf=pdf)
        poster.save()
        
    
        return redirect('subComp')  # or wherever you want to go after upload (づ￣ ³￣)づ
    else:
        return render(request, 'core/subComp.html')
    
# view to save poster form ChatGPT
def serve_poster_pdf(request, poster_id):
    try:
        poster = Poster.objects.get(id=poster_id)
        return FileResponse(poster.pdf.open('rb'), content_type='application/pdf')
    except Poster.DoesNotExist:
        raise Http404("Poster not found")