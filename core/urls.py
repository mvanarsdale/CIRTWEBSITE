"""Imports"""
from django.urls import path
from . import views


urlpatterns = [
    ### URL for main siz pages ###
    # for default / homepage (index) view
    path('', views.index, name='index'),
    # for poster view
    path('posters/', views.posters, name='posters'),
    # for faq view
    path('FAQ/', views.FAQ, name='FAQ'),
    # for journal view
    path('journals/', views.journals, name='journals'),
    # for poster view
    path('posters/', views.posters, name='posters'),
    # for user portal view 
    path('contact/', views.contact, name='contact'),
    # for dashboard view 
    path('Dashboard/', views.Dashboard, name='Dashboard'),
    # for faq view
    path('FAQ/', views.FAQ, name='FAQ'),
    



    ### URLS for user authentication ###
    # for log in view 
    path('ajax_login/', views.ajax_login, name='ajax_login'), 
    # url for signup view 
    #path('signup/', views.signup, name='signup'),
    # url to check if someone is logged in
    path('check_login_status/', views.check_login_status, name='check_login_status'), 
    # url to log out
    path('logout/', views.logout_view, name='logout'), 
    # url for user sign up 
    path('ajax_signup/', views.ajax_signup, name='ajax_signup'), 
    


    ### URLS for user portals ###
    # for editor portal view 
    path('editPort/', views.editPort, name='editPort'),
    # Route to allow editors to mark a journal as 'editor_reached' (updates Paper status)
    #path('mark_editor_reached/<int:paper_id>/', views.mark_editor_reached, name='mark_editor_reached'),
    # for reviewer portal view 
    path('reviewPort/', views.reviewPort, name='reviewPort'),
    # for author portal view 
    path('authPort/', views.authPort, name='authPort'), 
    # admin portal 
    path('adminPort/', views.adminPort, name='adminPort'),
    


    ### URLS for PDF submissions ###
    # url for view of page user uses to submit a poster
    path('posterSub/', views.posterSub, name='posterSub'),
    # for poster submit view which shows once user submits a poster
    path('subComp/', views.subComp, name='subComp'),
    
    # for journal submit view 
    path('journalSub/', views.journalSub, name='journalSub'),
    # for poster submit view 
    path('subComp/', views.subComp, name='subComp'),
    # for journal process submit view 
    path('JournalProc/', views.JournalProc, name='JournalProc'),
    
    # for uploading posters
    path('upload_poster/', views.upload_poster, name='upload_poster'),
    # for uploading journals
    path('upload_journal/', views.upload_journal, name='upload_journal'),
    
    # generating pdf for posters
    path('poster/pdf/<int:poster_id>/', views.serve_poster_pdf, name='serve_poster_pdf'),
    
    


]


     
    
