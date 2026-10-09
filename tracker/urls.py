from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('accounts/register/', views.register, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', views.logout_user, name='logout'),
    path('', views.home, name='home'),
    path('workouts/start/', views.start_workout, name='start_workout'),
    path('workouts/current/', views.workout_page, name='workout'),
    path('workouts/<int:pk>/timer/', views.timer_action, name='timer_action'),
    path('workouts/<int:pk>/', views.workout_detail, name='workout_detail'),
    path('workouts/<int:pk>/delete/', views.delete_workout, name='delete_workout'),
    path('exercises/', views.exercises, name='exercises'),
    path('exercises/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('history/', views.history, name='history'),
    path('analytics/', views.analytics, name='analytics'),
    path('settings/', views.settings_page, name='settings'),
]
