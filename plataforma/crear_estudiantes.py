from django.contrib.auth.models import User
from plataforma.models import Profile, Estudiante

perfiles_estudiantes = Profile.objects.filter(role='student')

for perfil in perfiles_estudiantes:
    user = perfil.user

    # Validar que el usuario tiene email
    if not user.email:
        print(f"⛔ Usuario {user.username} no tiene email. Saltando...")
        continue

    # Evitar duplicados por email
    if Estudiante.objects.filter(email=user.email).exists():
        print(f"⚠️ Ya existe un estudiante con el email: {user.email}")
        continue

    estudiante, creado = Estudiante.objects.get_or_create(
        user=user,
        defaults={
            'nombre': user.first_name or 'Nombre',
            'apellido': user.last_name or 'Apellido',
            'email': user.email,
        }
    )

    if creado:
        print(f"✅ Estudiante creado para: {user.username}")
    else:
        print(f"⚠️ Ya existía estudiante para: {user.username}")
