from django import forms
from .models import Estudiante, Nota
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile 


class EstudianteForm(forms.ModelForm):
    class Meta: 
        model = Estudiante
        fields = ['nombre','apellido', 'email']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'write a title'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'write a description'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'write a email'}),
        }
        
class NotaForm(forms.ModelForm):
    class Meta: 
        model = Nota
        fields = ['estudiante', 'materia', 'calificacion']
        widgets = {
            'estudiante': forms.Select(attrs={'class': 'form-control'}),
            'materia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe la materia'}),
            'calificacion': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Escribe la calificación'}),
        }

class NotaeditForm(forms.ModelForm):
    class Meta: 
        model = Nota
        fields = ['materia', 'calificacion'] 
        widgets = {
            'materia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe la materia'}),
            'calificacion': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Escribe la calificación'}),
        }

        
class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('admin','Administrador'),
        ('student','Estudiante'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, label='Rol')
    
    class Meta:
        model = User
        fields = ['username','password1', 'password2', 'role']

    def save(self, commit=True):
        user = super().save(commit)  # Guarda el usuario
        role = self.cleaned_data['role']  # Obtiene el rol seleccionado en el formulario
        Profile.objects.create(user=user, role=role)  # Crea el perfil vinculado
        return user 
        
class BuscarEstudianteForm(forms.Form):
    nombre = forms.CharField(label="buscar estudiante", max_length=100, required= False)