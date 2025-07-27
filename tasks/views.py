from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Task
from .forms import TaskForm,RegisterForm
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')  # replace with your home view name
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
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'tasks/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

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
