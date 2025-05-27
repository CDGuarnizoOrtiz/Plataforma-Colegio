from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    
    def __str__(self):
     return f"{self.nombre} {self.apellido}"
 
class nota(models.Model):
    estudiante= models.ForeignKey(estudiante, on_delete=models.CASCADE, related_name="notas")
    materia = models.CharField(max_length=100)
    calificacion = models.FloatField()
    
    def __str__(self):
     return f"{self.materia} {self.calificacions}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=[('admin', 'Administrador'), ('student', 'Estudiante')])

    def __str__(self):
        return f"{self.user.username} - {self.role}"