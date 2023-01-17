from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
# Para controlar excepciones de una manera más especifica
from django.db import IntegrityError
from .forms import TaskForm  # Importar formulario
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import  login_required #Para proteger las rutas y solo se puedan acceder a ellas logeandose
# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            "form": UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                # Para guardar cookie con sesión del usuario
                login(request, user)
                return redirect("tasks")
            except IntegrityError:
                return render(request, 'signup.html', {
                    "form": UserCreationForm,
                    "error": "Username already exists"
                })
        else:
            return render(request, 'signup.html', {
                "form": UserCreationForm,
                "error": "Password do not match"
            })


@login_required
def tasks(request):  # Obtener la lista de tareas
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True) # Solo muestra los no completados
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def tasks_terminated(request):
     tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
     return render(request, 'tasks_terminated.html', {'tasks': tasks})

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_Task.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                "form": TaskForm,
                "error": "Please provide valida data"
            })

@login_required
def task_detail(request, task_id):
    if request.method == "GET":
        # Task.objects.get(pk=task_id)
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        # Cargar información en formulario para ser editada
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            # Solo trae las tareas del usuario 'Parametro user'
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': "Error updating task"})

@login_required
def task_complete(request, task_id):  # Dar como completa una tarea
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def task_delete(request, task_id):
     if request.method == 'POST':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        task.delete()
        return redirect('tasks')

@login_required
def signout(request):  # Para cerrar sesión de usuario
    logout(request)
    return redirect('home')


def signin(request):  # Para el login
    if request.method == "GET":
        return render(request, "signin.html", {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, "signin.html", {
                'error': "Username or password is incorrect",
                'form': AuthenticationForm
            })
        else:
            login(request, user)
            return redirect('tasks')
