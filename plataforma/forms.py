from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Estudiante, Nota, Profile
from django.core.exceptions import ValidationError

# ✅ Declaramos esto como constante global, así lo puedes usar en cualquier form sin errores
ROLE_CHOICES = (
    ('teacher', 'Docente'),
    ('student', 'Estudiante'),
)



class RegistroCompletoForm(forms.Form):
    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'})
    )
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'})
    )
    role = forms.ChoiceField(
        choices=(('teacher', 'Docente'), ('student', 'Estudiante')),
        label='Rol',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    nombre = forms.CharField(
        label='Nombre',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'})
    )
    apellido = forms.CharField(
        label='Apellido',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'})
    )
    email = forms.EmailField(
        label='Correo',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'})
    )
    foto = forms.ImageField(
        label='Foto',
        required=False
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Este nombre de usuario ya está en uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Este correo ya está registrado.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Las contraseñas no coinciden.")

        return cleaned_data


class CustomUserCreationForm(UserCreationForm):
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
