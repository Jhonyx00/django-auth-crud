from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

# proteger rutas
from django.contrib.auth.decorators import login_required

from django.utils import timezone

from .forms import TaskForm
from .models import Task

from django.db import IntegrityError

# Create your views here.
# RUTAS DESDE LA URL DEL NAVEGADOR


def home(request):
    title = 'Hello world'
    return render(request, 'home.html')


def singup(request):
    if request.method == 'GET':
        print('enviando formulario')
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        # si las contraseñas coinciden
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                # siempre usar el return
                return redirect('tasks')

            except IntegrityError:
                return render(request, 'signup.html', {
                    # estos dos son los que se muestran en la plantilla html, "form" y "error"
                    'form': UserCreationForm,
                    'error': 'Username already exists'
                })
        else:
            return render(request, 'signup.html', {
                'form': UserCreationForm,
                'error': 'Password do not match'
            })


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            "form": AuthenticationForm
        })
    # POST
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                "form": AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)  # guardar sesion del usuario
            return redirect('tasks')


@login_required
def signout(request):
    logout(request)
    return redirect('home')


@login_required
def tasks(request):
    # el filter se usar para consultar en la base de datos a partir de los parametros de la funcion
    # user=request.user significa que va a buscar el usuario que esta logeado y no entre todos
    # datecompleted__isnull = True significa que mostrara todas las tareas que no esten completadas
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks})


@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            # GENERAL: se reciben los datos del front end (request.POST) y se los pasamos a la clase TaskForm y el va a generar por mi un formulario
            # SE OBTIENE EL FORMULARIO
            form = TaskForm(request.POST)
            # almacenar solo los datos
            # antes de renderizar ocupamos pasarle el usuario
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Please provide valid data'
            })


@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        # obtenemos la tarea que le pertenezca al usuario logueado
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        # aqui se le indica que se llena el formulario con los datos de la misma tarea
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            # buscar las tareas que le pertenezcan al usuario logeado 'user = request.user'
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html',
                          {'task': task,
                           'form': form,
                           'error': 'Error updating task'})


@login_required
def complete_task(request, task_id):
    # en que modelo se busca, en este caso en la tabla Task
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        # se realizan operaciones en la base de datos
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')


@login_required
def delete_task(request, task_id):
    # en que modelo se busca, en este caso en la tabla Task
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')


@login_required
def tasks_completed(request):
    # LO MISMO QUE TASKS PERO CON OTRO FILTRO
    tasks = Task.objects.filter(
        user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {'tasks': tasks})
