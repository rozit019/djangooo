from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
# posts/urls.py
from django.urls import path, include

# from .views import TaskViewSet

# router = DefaultRouter()
# router.register('tasks', TaskViewSet)



urlpatterns = [
    path('tasks/',views.task_list, name='task_list'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('register/', views.register, name='register'),
    # path('login/', auth_views.LoginView.as_view(template_name='tasks/login.html'), name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('tasks/add/', views.add_task, name='add_task'),
    path('tasks/delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('chatbot/api/', views.chatbot_api, name='chatbot_api'),
    path('profile/', views.profile_view, name='profile'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), name='password_change_done'),
    path('tasks/complete/<int:task_id>/', views.mark_task_completed, name='mark_task_completed'),
    path('tasks/toggle/', views.toggle_task_completion, name='toggle_task'),
    

]