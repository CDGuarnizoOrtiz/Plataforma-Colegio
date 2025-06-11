from django.contrib import admin
from django.urls import path
from plataforma import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = 'index'),
    path('index/', views.index, name = 'index'),
    path('buscar/', views.vista_estudiantes, name = 'buscar'),
    path('create/', views.create_estudiante, name = 'create'),
    path('aggnota/', views.agregar_nota, name = 'aggnota'),
    path('notas/', views.vernotas, name = 'notas'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('nota_edit/<int:nota_id>/', views.nota_edit, name='nota_edit'),
    path('tasks/<int:nota_id>/delete', views.delete_note, name='delete_note')
    
    
]
