from django.urls import path
from . import views
from .views import music_categories_view,signup_user,profile_view
from .views import admin_redirect

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', profile_view, name='profile'),
    path('profile/', views.user_profile, name='user_profile'),
    path('login/', views.login_user, name='login'),
    path('signup/', views.signup_user, name='signup'),
    path('logout/', views.logout_user, name='logout'),
    path('music_categories/',views.music_categories_view, name='music_categories'),
    path('study_tracker/', views.study_tracker, name='study_tracker'),
    path('admin-panel/', admin_redirect, name='admin-panel'),
    path('about/', views.about, name='about'),
    path("chatbot-response/", views.chatbot_response, name="chatbot_response")
]
