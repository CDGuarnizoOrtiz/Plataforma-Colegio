from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import EstudianteForm, NotaForm,BuscarEstudianteForm, NotaeditForm
from .models import Estudiante,Nota
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .decorators import solo_admin


# Create your views here.
@login_required
def index(request):
    return render(request, 'dashboard.html')

def base(request):
    return render(request, 'base_est.html')

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




@login_required
@solo_admin
def create_estudiante(request):
    if request.method == 'GET':
        return render(request, 'crearestudiantes.html',{
            'form': EstudianteForm,
            #'form': notaform,  
        })
    else:
        try:
            form = EstudianteForm(request.POST)
            #form2 = notaform(request.POST)
            new_student = form.save(commit=False)
            new_student.save()
            return redirect('create')
        except ValueError:
            return render(request, 'crearestudiantes.html', {
                'form': EstudianteForm,
                'error': 'please provide valide data'
        })

@login_required
@solo_admin
def agregar_nota(request):
    if request.method == 'GET':
        return render(request, 'agregarestudiante.html',{
            'form': NotaForm,
            #'form': notaform,  
        })
    else:
        try:
            form = NotaForm(request.POST)
            #form2 = notaform(request.POST)
            new_nota = form.save(commit=False)
            new_nota.save()
            return redirect('aggnota')
        except ValueError:
            return render(request, 'agregarestudiante.html', {
                'form': NotaForm,
                'error': 'please provide valide data'
        })    

@login_required
def vernotas(request):
    notas = Nota.objects.select_related('estudiante').all()
    return render(request, 'notas.html', {'notas': notas})

@login_required
@solo_admin
def nota_edit(request, nota_id):
    newnota = get_object_or_404(Nota, pk=nota_id)

    if request.method == 'GET':
        form = NotaeditForm(instance=newnota)
        return render(request, 'nota_edit.html', {
            'newnota': newnota,
            'form': form,
        })
    else:
        form = NotaeditForm(request.POST, instance=newnota)
        if form.is_valid():
            form.save()
            return redirect('notas')
        else:
            return render(request, 'nota_edit.html', {
                'newnota': newnota,
                'form': form,
                'error': "Error updating nota"
            })
 
@login_required    
@solo_admin       
def delete_note(request, nota_id):
    delete = get_object_or_404(Nota, pk=nota_id)
    if request.method == 'POST':
        print('Eliminando nota:', delete.id)  # debug
        delete.delete()
        return redirect('notas')
    else:
        print('Método no permitido:', request.method)


def signin(request):
    if request.method == 'GET':
        return render(request, 'registration/login.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'registration/login.html', {
                'form': AuthenticationForm,
                'error': 'username o password is incorrect'
            })
        else:
            login(request, user)
            return redirect('dashboard')

@login_required
def vista_estudiantes(request):
    form = BuscarEstudianteForm(request.GET or None)
    estudiantes = Estudiante.objects.all()  

    if form.is_valid():
        nombre = form.cleaned_data.get('nombre')
        if nombre:
            estudiantes = estudiantes.filter(nombre__icontains=nombre)

    estudiantes_data = []
    for est in estudiantes:
        notas = Nota.objects.filter(estudiante=est)
        estudiantes_data.append({
            'estudiante': est,
            'notas': notas
        })

    return render(request, 'buscarestudiante.html', {
        'form': form,
        'estudiantes_data': estudiantes_data
    })
