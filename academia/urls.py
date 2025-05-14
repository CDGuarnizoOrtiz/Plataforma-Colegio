from django.contrib import admin
from django.urls import path
from plataforma import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name = 'dashboard'),
    path('create/', views.create_estudiante, name = 'create'),
    path('aggnota/', views.agregar_nota, name = 'aggnota'),
    path('notas/', views.vernotas, name = 'notas'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    
    
]
