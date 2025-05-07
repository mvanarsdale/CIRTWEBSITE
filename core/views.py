from django.shortcuts import redirect, render
from django.urls import reverse


from django.contrib.auth import authenticate, login
from django.http import JsonResponse

# for messages with log in success / failure
from django.contrib import messages

from core.models import CustomUser
<<<<<<< Updated upstream
=======
from core.models import PDFStorage, PDFComment
from core.models import Paper
from core.models import Poster
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
>>>>>>> Stashed changes

# an attempt to fix my redirect problem 
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
<<<<<<< Updated upstream
    return render(request, 'core/Dashboard.html')

def Portal(request):
    return render(request, 'core/Portal.html')

def PosterSubmit(request):
    return render(request, 'core/PosterSubmit.html')
=======
    return render(request, 'core/Dashboard.html', {'user': request.user})
        
# portals 
# editor portal
def editPort(request):
    new_papers = Paper.objects.filter(status='submitted')
    in_progress_papers = Paper.objects.filter(status='editor_reached')
    reviewers = CustomUser.objects.filter(role='Reviewer')

    return render(request, 'core/editPort.html', {
        'new_papers': new_papers,
        'in_progress_papers': in_progress_papers,
        'reviewers': reviewers,
    })

# reviewer portal
def reviewPort(request):
    return render(request, 'core/reviewPort.html')

# author portal
@login_required
def authPort(request):
    user_posters = Poster.objects.filter(author=request.user)
    return render(request, 'core/authPort.html', {'posters': user_posters})

# admin portal
def adminPort(request):
    return render(request, 'core/adminPort.html')

#################################################
>>>>>>> Stashed changes


# code from ChatGPT
def signup(request):
    if request.method == 'POST':
<<<<<<< Updated upstream
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
=======
        poster_file = request.FILES.get('PDF_file')
        description = request.POST.get('description')
        comments = request.POST.get('comments')

        if poster_file:
            # 1️⃣ Save the PDF to pdf_storage
            pdf_instance = PDFStorage.objects.create(file=poster_file)

            # 2️⃣ Save the description/comments to pdf_comments (linked to the PDF)
            PDFComment.objects.create(
                pdf=pdf_instance,
                description=description,
                comments=comments
            )

            return redirect('subComp')  # ✅ Redirect to success page

        else:
            # 🚨 Handle error: no file uploaded
            return render(request, 'core/Journal_Process.html', {
                'error': 'No file uploaded. Please try again.',
                'paper': paper  # ✅ Pass paper here too even if error
            })

    # ✅ For GET requests, render the form and pass 'paper'
    return render(request, 'core/Journal_Process.html', {'paper': paper})

def assign_reviewer(request, journal_id):
    if request.method == 'POST' and request.user.role == 'Editor':
        reviewer_id = request.POST.get('reviewer_id')
        comment = request.POST.get('comment')

        journal = get_object_or_404(JournalSubmission, id=journal_id)
        reviewer = get_object_or_404(get_user_model(), id=reviewer_id, role='Reviewer')

        journal.assigned_reviewer = reviewer
        journal.status = 'editor_reached'
        journal.save()

        return redirect('editPort')
    
def mark_editor_reached(request, paper_id):
    return HttpResponse(f"Editor reached for paper {paper_id}")

def subComp(request):
    return render(request, 'core/subComp.html')

def logout_view(request):
    logout(request)
    return redirect('home')
>>>>>>> Stashed changes

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
<<<<<<< Updated upstream
=======

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

        user = User.objects.create_user(username=username, password=password, email=email, role=role)
        user.first_name = name
        user.save()

        login(request, user)

        return JsonResponse({'success': True, 'username': user.username})
    
    return JsonResponse({'success': False, 'error_message': 'Invalid request'})

"""Uploading PDF views""" 
def upload_poster(request):
    if request.method == 'POST':
        # title of poster
        title = request.POST.get('title')
        
        # pdf for poster
        pdf = request.FILES.get('pdf')
        
        # getting the authors specfic username - help from ChatGPT
        user = request.user
        
        # date poster as submitted
        submitted_date = request.POST.get('submitted_date')

        # create and save poster
        poster = Poster.objects.create(title=title, author=user, submitted_date=submitted_date, pdf=pdf)
        poster.save()
    

        return redirect('subComp')  
    else:
        return render(request, 'core/subComp.html')
    

# view for journal submit
def upload_journal(request):
    if request.method == 'POST':
        # title for journal 
        title = request.POST.get('title')
        
        # pdf for journal
        pdf = request.FILES.get('pdf')
        
        # getting the authors specfic username - help from ChatGPT
        user = request.user
        
        # date poster as submitted
        submitted_date = request.POST.get('submitted_date')

        # create and save journal 
        journal = Paper.objects.create(
            title=title,
            author=user,
            submitted_date=submitted_date,
            pdf=pdf,
            status='submitted',
        )
        # save journal 
        journal.save()
        
    
        # redirect to journal process page
        return redirect('JournalProc') 
    else:
        return render(request, 'core/JournalProc.html')

# view to save poster form ChatGPT
def serve_poster_pdf(request, poster_id):
    try:
        poster = Poster.objects.get(id=poster_id)
        return FileResponse(poster.pdf.open('rb'), content_type='application/pdf')
    except Poster.DoesNotExist:
        raise Http404("Poster not found")
>>>>>>> Stashed changes
