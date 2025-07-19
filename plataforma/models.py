from django.db import models
from django.contrib.auth.models import User


class Estudiante(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField()
    foto = models.ImageField(upload_to='fotos_estudiantes/', default='fotos_estudiantes/default.jpg')

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
 
class Nota(models.Model):
    estudiante= models.ForeignKey(Estudiante, on_delete=models.CASCADE, related_name="notas")
    materia = models.CharField(max_length=100)
    calificacion = models.FloatField()
    
    def __str__(self):
     return f"{self.materia} {self.calificacion}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=[('teacher', 'Docente'), ('student', 'Estudiante')])

    def __str__(self):
        return f"{self.user.username} - {self.role}"