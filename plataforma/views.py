from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import EstudianteForm, NotaForm,BuscarEstudianteForm, NotaeditForm,RegistroCompletoForm
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
@login_required
def base(request):
    return render(request, 'base_est.html')
@login_required
def base2(request):
    return render(request, 'base_teacher.html')

@login_required
def perfil_student(request):
    estudiante = get_object_or_404(Estudiante, user = request.user)
    notas = Nota.objects.filter(estudiante=estudiante)
    return render(request, 'perfil_student.html', {
        'estudiante': estudiante,
        'notas': notas
    })



def signup(request):
    if request.method == 'POST':
        form = RegistroCompletoForm(request.POST, request.FILES)  
        if form.is_valid():
            # Crear usuario
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            # Crear perfil
            Profile.objects.create(
                user=user,
                role=form.cleaned_data['role']
            )
            # Crear estudiante (solo si el rol es estudiante)
            if form.cleaned_data['role'] == 'student':
                Estudiante.objects.create(
                    user=user,
                    nombre=form.cleaned_data['nombre'],
                    apellido=form.cleaned_data['apellido'],
                    email=form.cleaned_data['email'],
                    foto=form.cleaned_data.get('foto')  
                )
            login(request, user)
            messages.success(request, "Usuario registrado correctamente.")
            return redirect('signin')
        else:
            messages.error(request, "Error en el formulario.")
    else:
        form = RegistroCompletoForm()

    return render(request, 'registro_completo.html', {'form': form})





def create_estudiante(request):
    if request.method == 'GET':
        return render(request, 'crearestudiantes.html', {
            'form': EstudianteForm,
        })
    else:
        try:
            form = EstudianteForm(request.POST)
            new_student = form.save(commit=False)
            new_student.user = request.user  
            new_student.save()
            return redirect('create')
        except ValueError:
            return render(request, 'crearestudiantes.html', {
                'form': EstudianteForm,
                'error': 'Por favor proporciona datos válidos.'
            })


@login_required

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
def lista_estudiantes(request):
    estudiantes = Estudiante.objects.all().order_by('nombre','apellido')
    return render(request, 'listaestudiantes.html', {'estudiantes': estudiantes})




@login_required

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
            try:
                role = user.profile.role
            except Profile.DoesNotExist:
                return redirect('signin')
            if role == 'teacher':
                return redirect('base_teacher')
            if role == 'student':
                return redirect('base')
            else:
                return render(request,'signin')

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
