from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .models import Task
from .forms import LoginForm, RegisterForm, TaskForm


# Create your views here.

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('secret')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def main_page(request):
    return render(request, "main_page.html")


def info(request):
    return render(request, "info.html")


@login_required
def secret_view(request):
    return render(request, "secret.html")


@login_required()
def task_list(request):
    filter_status = request.GET.get('status', 'all')
    if filter_status == 'completed':
        tasks = Task.objects.filter(completed=True)
    elif filter_status == 'incomplete':
        tasks = Task.objects.filter(completed=False)
    else:
        tasks = Task.objects.all()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task_list.html', {'tasks': tasks, 'form': form})


def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_edit.html', {'form': form, 'task': task})


def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('task_list')


def task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = True
    task.save()
    return redirect('task_list')


def task_incomplete(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = False
    task.save()
    return redirect('task_list')

