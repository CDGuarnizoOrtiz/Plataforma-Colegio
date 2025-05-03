from django import forms
from .models import estudiante, nota

class estudianteform(forms.ModelForm):
    class Meta: 
        model = estudiante
        fields = ['nombre','apellido', 'email']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'write a title'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'write a description'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'write a email'}),
        }
        
class notaform(forms.ModelForm):
    class Meta: 
        model = nota
        fields = ['estudiante', 'materia', 'calificacion']
        widgets = {
            'estudiante': forms.Select(attrs={'class': 'form-control'}),
            'materia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe la materia'}),
            'calificacion': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Escribe la calificación'}),
        }