from django.urls import path
from . import views


app_name = 'Login'

urlpatterns = [

    path('signup/', views.sign_up, name='signup'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('profile/', views.profile, name='profile'),

    # path('change-profile/', views.user_change, name='user_change'),
    # path('update_password/', views.update_password, name='update_password'), 
    path('add_propic/', views.add_propic, name='add_propic'),  
    path('change_propic/', views.change_propic, name='change_propic'),     


]

