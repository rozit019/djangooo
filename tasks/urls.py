from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('tasks/',views.task_list, name='task_list'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='tasks/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='tasks/logout.html'), name='logout'),

]