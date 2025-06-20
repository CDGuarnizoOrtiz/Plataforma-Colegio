from django.shortcuts import redirect
from django.http import HttpResponseForbidden

def solo_admin(view_func):
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, 'profile') and request.user.profile.role == 'admin':
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Acceso restringido: Solo administradores.")
    return wrapper

def solo_estudiante(view_func):
    def wrapper(request, *args, **kwargs):
        if hasattr(request.user, 'profile') and request.user.profile.role == 'student':
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("Acceso restringido: Solo estudiantes.")
    return wrapper