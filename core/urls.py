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
    path('contact/', views.contact, name='contact'),
    # for user portal view 
    path('Portal/', views.Portal, name='Portal'),
    # for poster submit view 
    path('PosterSubmit/', views.PosterSubmit, name='PosterSubmit'),
    # for log in view 
    path('ajax_login/', views.ajax_login, name='ajax_login'), 
    # url for signup view 
    #path('signup/', views.signup, name='signup'),
    # url to check if someone is logged in
    path('check_login_status/', views.check_login_status, name='check_login_status'), 
    path('logout/', views.logout_view, name='logout'), 
    path('ajax_signup/', views.ajax_signup, name='ajax_signup'), 
    # for user portal view 
    path('Portal/', views.Portal, name='Portal'),
    # for editor portal view 
    path('editPort/', views.editPort, name='editPort'),
    # for reviewer portal view 
    path('reviewPort/', views.reviewPort, name='reviewPort'),
    # for author portal view 
    path('authPort/', views.authPort, name='authPort'), 
     # for poster submit view 
    path('posterSub/', views.posterSub, name='posterSub'),
    # for journal submit view 
    path('journalSub/', views.journalSub, name='journalSub'),
    # for poster submit view 
    path('subComp/', views.subComp, name='subComp'),
    # for journal process submit view 
    path('JournalProc/', views.JournalProc, name='JournalProc'),
    
    

]


     
    
