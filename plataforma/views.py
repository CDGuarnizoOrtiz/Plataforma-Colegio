from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import estudianteform, notaform,BuscarEstudianteForm
from .models import estudiante,nota
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile

# Create your views here.
def index(request):
    return render(request, 'index.html')


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  
            login(request, user)
            messages.success(request, "Usuario registrado correctamente.")
            return redirect('signin')
        else:
            messages.error(request, "Hubo un error al crear la cuenta.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})



def signin(request):
    return render(request,'signin.html')


def create_estudiante(request):
    if request.method == 'GET':
        return render(request, 'crearestudiantes.html',{
            'form': estudianteform,
            #'form': notaform,  
        })
    else:
        try:
            form = estudianteform(request.POST)
            #form2 = notaform(request.POST)
            new_student = form.save(commit=False)
            new_student.save()
            return redirect('create')
        except ValueError:
            return render(request, 'crearestudiantes.html', {
                'form': estudianteform,
                'error': 'please provide valide data'
        })

def agregar_nota(request):
    if request.method == 'GET':
        return render(request, 'agregarestudiante.html',{
            'form': notaform,
            #'form': notaform,  
        })
    else:
        try:
            form = notaform(request.POST)
            #form2 = notaform(request.POST)
            new_nota = form.save(commit=False)
            new_nota.save()
            return redirect('aggnota')
        except ValueError:
            return render(request, 'agregarestudiante.html', {
                'form': notaform,
                'error': 'please provide valide data'
        })    

def vernotas(request):
    notas = nota.objects.select_related('estudiante').all()
    return render(request, 'notas.html', {'notas': notas})

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'username o password is incorrect'
            })
        else:
            login(request, user)
            return redirect('notas')

def vista_estudiantes(request):
    form = BuscarEstudianteForm(request.GET or None)
    estudiantes = estudiante.objects.all()  

    if form.is_valid():
        nombre = form.cleaned_data.get('nombre')
        if nombre:
            estudiantes = estudiantes.filter(nombre__icontains=nombre)

    estudiantes_data = []
    for est in estudiantes:
        notas = nota.objects.filter(estudiante=est)
        estudiantes_data.append({
            'estudiante': est,
            'notas': notas
        })

    return render(request, 'buscarestudiante.html', {
        'form': form,
        'estudiantes_data': estudiantes_data
    })