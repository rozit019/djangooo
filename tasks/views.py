from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Task
from .forms import TaskForm,RegisterForm
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import openai
from .forms import ProfileUpdateForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileUpdateForm, UserUpdateForm
from .forms import TaskForm
from .models import Task
from django.utils.timezone import now
from django.db.models import Q
from datetime import timedelta
from datetime import timedelta
from django.utils import timezone
from django.views.decorators.http import require_POST


# class TaskViewSet(viewsets.ModelViewSet):
#     serializer_class = TaskSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return Task.objects.filter(user=self.request.user)

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

@login_required
def get_due_soon_count(request):
    today = timezone.localdate()
    soon_threshold = today + timedelta(days=3)
    due_soon_count = Task.objects.filter(
        user=request.user,
        completed=False,
        due_date__gte=today,
        due_date__lte=soon_threshold
    ).count()
    return JsonResponse({'count': due_soon_count})

def edit_task(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_detail', task_id=task.pk)
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/edit_task.html', {'form': form, 'task': task})

def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_detail', task_id=task.id)
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/task_detail.html', {'task': task, 'form': form})



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('task_list')  # replace with your home view name
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'tasks/login.html')

# @login_required
# def task_list(request):
#     tasks=Task.objects.filter(user=request.user).order_by('completed', '-due_date')
#     return render(request,'tasks/tasklist.html',{'tasks':tasks}) 
@login_required
def task_list(request):
    # Existing code for getting tasks
    today = timezone.localdate()
    soon_threshold = today + timedelta(days=3)

    tasks = Task.objects.filter(user=request.user).order_by('due_date')



    due_soon_tasks = tasks.filter(
        completed=False,
        due_date__gte=today,
        due_date__lte= soon_threshold
    )
    due_soon_count = due_soon_tasks.count()

    context = {
        'tasks': tasks,

        'due_soon_tasks': due_soon_tasks,
    'due_soon_count': due_soon_tasks.count(),
        # optionally pass due_soon_tasks for detailed list
    }
    return render(request, 'tasks/tasklist.html', context)
# @login_required
# def task_list(request):
#     # Get all tasks
#     tasks = Task.objects.all().order_by('due_date')

#     # Filter by status
#     pending_tasks = tasks.filter(completed=False)
#     completed_tasks = tasks.filter(completed=True)

#     # Tasks due within the next 3 days (including today)
#     today = timezone.now().date()
#     upcoming = today + timedelta(days=3)
#     due_soon_tasks = tasks.filter(completed=False, due_date__lte=upcoming, due_date__gte=today)

#     # Count for badge
#     due_soon_count = due_soon_tasks.count()

#     context = {
#         'tasks': tasks,
#         'pending_tasks': pending_tasks,
#         'completed_tasks': completed_tasks,
#         'due_soon_tasks': due_soon_tasks,
#         'due_soon_count': due_soon_count,
#     }

#     return render(request, 'tasks/tasklist.html',{'tasks':tasks})


@login_required
def task_create(request):
    if request.method=='POST':
        form=TaskForm(request.POST)
        if form.is_valid():
            task=form.save()
            task.user=request.user
            task.save()
            return redirect('task-list')
        else:
            form=TaskForm()
            return render(request,'tasks/taskform.html',{'form':form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')  # Redirect to task list or login page
    else:
        form = UserCreationForm()
        return render(request, 'tasks/register.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        messages.success(request, "You have been logged out successfully.")
    logout(request)
    return redirect('login')

# @login_required
# def add_task(request):
#     if request.method == 'POST':
#         form = TaskForm(request.POST)
#         if form.is_valid():
#             task = form.save(commit=False)
#             task.user = request.user
#             task.save()
#             return redirect('task_list')
#     return redirect('task_list')

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'success'
                #                      ,  "task": {
                #     "id": task.id,
                #     "title": task.title,
                #     "description": task.description,
                #     "priority": task.priority,
                #     "due_date": task.due_date.strftime("%Y-%m-%d"),
                # }
                })
            else:
                return redirect('task_list')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'errors': form.errors})
    return redirect('task_list')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('task_list')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
        else:
            messages.success(request, "Task deleted successfully!")
            return redirect('task_list')
    return render(request, 'tasks/delete_task.html', {'task': task})

def chatbot(request):
    return render(request, 'tasks/chatbot.html')

# @login_required
# def profile_view(request):
#     # Get or create Profile for logged-in user
#     profile, created = Profile.objects.get_or_create(user=request.user)

#     if request.method == "POST":
#         user_form = UserUpdateForm(request.POST, instance=request.user)
#         profile_form = ProfileUpdateForm(
#             request.POST,
#             request.FILES,  # to handle uploaded files (profile pic)
#             instance=profile
#         )

#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             messages.success(request, "Your profile has been updated!")
#             return redirect("profile")
#     else:
#         user_form = UserUpdateForm(instance=request.user)
#         profile_form = ProfileUpdateForm(instance=profile)

#     context = {
#         "user_form": user_form,
#         "profile_form": profile_form,
#     }
#     return render(request, "tasks/profile.html", context)

@login_required
def profile_view(request):
    # Show profile page (read only)
    return render(request, 'tasks/profile.html')

def home(request):
    return render(request, 'core/home.html')



@login_required
def edit_profile_view(request):
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,  # to handle uploaded files (profile pic)
            instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'tasks/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

@login_required
def mark_task_completed(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id, user=request.user)
        data = json.loads(request.body)
        task.completed = data.get('completed', False)
        task.save()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def toggle_task_completion(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        completed = request.POST.get('completed') == 'true'
        try:
            task = Task.objects.get(pk=task_id)
            task.completed = completed
            task.save()
            return JsonResponse({'status': 'success'})
        except Task.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Task not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

@csrf_exempt
def chatbot_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get('message', '').lower()

        # Simple keyword matching example
        if 'hello' in user_message or 'hi' in user_message:
            bot_reply = "Hello! How can I assist you today?"
        elif 'task' in user_message:
            bot_reply = "You can add, view, or delete tasks in your task manager."
        elif 'bye' in user_message or 'exit' in user_message:
            bot_reply = "Goodbye! Have a great day!"
        elif 'tralalero' in user_message:
            bot_reply =  "tralala"  
        elif 'rosha' in user_message  in user_message:
            bot_reply = "my sister is rosha"
        elif 'biraj' in user_message:
            bot_reply =  "maka"
        else:
            bot_reply = "Sorry, I didn't understand that. Could you rephrase?"


        return JsonResponse({'reply': bot_reply})
    return JsonResponse({'error': 'POST request required.'}, status=400)