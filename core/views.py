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
from django.db.models import Q


#to be sure that login is required for the dashboard 
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
    query = request.GET.get('filter_term')
    filter_by = request.GET.get('filter_by')
    sort_by = request.GET.get('sort_by')

    posters = Poster.objects.all()

    # First, apply filtering
    if query and filter_by:
        if filter_by == 'author':
            posters = posters.filter(author__username__icontains=query)
        elif filter_by == 'title':
            posters = posters.filter(title__icontains=query)
        elif filter_by == 'submitted_date':
            posters = posters.filter(submitted_date__icontains=query)

    # Now apply sorting
    if sort_by:
        if sort_by == 'author_asc':
            posters = posters.order_by('author__username')  # A → Z
        elif sort_by == 'author_desc':
            posters = posters.order_by('-author__username')  # Z → A
        elif sort_by == 'newest':
            posters = posters.order_by('-submitted_date')  # Newest first
        elif sort_by == 'oldest':
            posters = posters.order_by('submitted_date')  # Oldest first

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

def adminPort(request):
    return render(request, 'core/adminPort.html')

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

def logout_view(request):
    logout(request)
    return redirect('home')

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

def check_login_status(request):
    if request.user.is_authenticated:
        return JsonResponse({
            'is_logged_in': True,
            'username': request.user.username
        })
    else:
        return JsonResponse({
            'is_logged_in': False
        })
    
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

# view for poster submit form
def upload_poster(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        #author = request.POST.get('author')
        pdf = request.FILES.get('pdf')
        
        # getting the authors specfic username - help from ChatGPT
        user = request.user
        
        # date poster as submitted
        submitted_date = request.POST.get('submitted_date')

        # create and save poster
        poster = Poster.objects.create(title=title, author=user, submitted_date=submitted_date, pdf=pdf)
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