from django import forms
from .models import estudiante,nota

class estudianteform(forms.ModelForm):
    class meta: 
        model = estudiante
        fields = ['nombre','apellido', 'email']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'write a title'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'write a description'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'write a email'}),
        }
        
class notaform(forms.ModelForm):
    class meta: 
        model = nota
        fields = ['nombre','apellido', 'email']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'write a title'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'write a description'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'write a email'}),
        }