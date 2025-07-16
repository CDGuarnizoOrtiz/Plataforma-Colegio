from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Estudiante, Nota, Profile


class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['nombre', 'apellido', 'email']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
        }


class NotaForm(forms.ModelForm):
    class Meta: 
        model = Nota
        fields = ['estudiante', 'materia', 'calificacion']
        widgets = {
            'estudiante': forms.Select(attrs={'class': 'form-control'}),
            'materia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Materia'}),
            'calificacion': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Calificación'}),
        }


class NotaeditForm(forms.ModelForm):
    class Meta: 
        model = Nota
        fields = ['materia', 'calificacion'] 
        widgets = {
            'materia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Materia'}),
            'calificacion': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Calificación'}),
        }


class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('teacher', 'Docente'),
        ('student', 'Estudiante'),
    )

    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        label='Rol',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nombre de usuario'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Contraseña'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirmar contraseña'
        })

    def save(self, commit=True):
        user = super().save(commit)
        role = self.cleaned_data['role']
        Profile.objects.create(user=user, role=role)
        return user


class BuscarEstudianteForm(forms.Form):
    nombre = forms.CharField(
        label="Buscar estudiante",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese nombre del estudiante'
        })
    )
