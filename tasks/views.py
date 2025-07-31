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

@login_required
def task_list(request):
    tasks=Task.objects.filter(user=request.user)
    return render(request,'tasks/tasklist.html',{'tasks':tasks}) 

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
        # form = UserCreationForm()
        form = RegisterForm()
    return render(request, 'tasks/register.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        messages.success(request, "You have been logged out successfully.")
    logout(request)
    return redirect('tasks/login.html')

@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    return redirect('task_list')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('task_list')

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, "Task deleted successfully!")
        return redirect('task_list')
    return render(request, 'tasks/delete_task.html', {'task': task})

def chatbot(request):
    return render(request, 'tasks/chatbot.html')

@login_required
def profile_view(request):
    # Get or create Profile for logged-in user
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,  # to handle uploaded files (profile pic)
            instance=profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("profile")
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, "tasks/profile.html", context)

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