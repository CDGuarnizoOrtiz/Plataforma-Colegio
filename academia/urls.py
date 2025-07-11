from django.contrib import admin
from django.urls import path,include
from plataforma import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = 'dashboard'),
    path('index/', views.index, name = 'dashboard'),
    path('buscar/', views.vista_estudiantes, name = 'buscar'),
    path('create/', views.create_estudiante, name = 'create'),
    path('aggnota/', views.agregar_nota, name = 'aggnota'),
    path('notas/', views.vernotas, name = 'notas'),
    path('lista_estudiantes/', views.lista_estudiantes, name = 'lista_estudiantes'),
    path('base_est/', views.base, name = 'base'),
    path('base_teacher/', views.base2, name = 'base_teacher'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('perfil_student/', views.perfil_student, name='perfil_student'),
    path('nota_edit/<int:nota_id>/', views.nota_edit, name='nota_edit'),
    path('tasks/<int:nota_id>/delete', views.delete_note, name='delete_note'),
    path('accounts/',include('django.contrib.auth.urls')),
    
    
]
