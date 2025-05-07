from django.urls import path
from . import views

urlpatterns = [
    # for default / homepage (index) view
    path('', views.index, name='index'),
    # for poster view
    path('posters/', views.posters, name='posters'),
    # for faq view
    path('FAQ/', views.FAQ, name='FAQ'),
    # for journal view
    path('journals/', views.journals, name='journals'),
    # for dashboard view 
    path('Dashboard/', views.Dashboard, name='Dashboard'),
    # for user portal view 
    path('Portal/', views.Portal, name='Portal'),
    # for poster submit view 
<<<<<<< Updated upstream
    path('PosterSubmit/', views.PosterSubmit, name='PosterSubmit'),
    # for log in view 
    path('ajax-login/', views.ajax_login, name='ajax_login'),
    # url for signup view 
    path('signup/', views.signup, name='signup'),    
=======
    path('subComp/', views.subComp, name='subComp'),
    # for journal process submit view 
    path('JournalProc/', views.JournalProc, name='JournalProc'),
    
    # for uploading posters
    path('upload_poster/', views.upload_poster, name='upload_poster'),
    # for uploading journals
    path('upload_journal/', views.upload_journal, name='upload_journal'),
    
    # generating pdf for posters
    path('poster/pdf/<int:poster_id>/', views.serve_poster_pdf, name='serve_poster_pdf'),

    path('assign_reviewer/<int:journal_id>/', views.assign_reviewer, name='assign_reviewer'),

    
    


>>>>>>> Stashed changes
]


     
    
