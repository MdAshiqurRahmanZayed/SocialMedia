from django.urls import path
from .views import *

urlpatterns = [
     path('signup/',sign_up,name="sign_up"),
     path('login/',login_page,name="login_page"),
     path('logout/',logout_user, name='logout'),
     path('edit/',edit_profile, name='edit'),
     path('logout/',logout_user, name='logout'),
     path('profile/',profile, name='profile'),
    path('user/<username>/', user, name='user'),
    path('follow/<username>', follow, name='follow'),
    path('unfollow/<username>', unfollow, name='unfollow'),
]
