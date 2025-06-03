from django.urls import path
from . import views
from usuarios.decoradores import rol_requerido

app_name = 'usuarios'

urlpatterns = [
    # Rutas públicas - acceso libre
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),  
    path('register/', views.register, name='register'),
    path('seleccionar_registro/', views.seleccionar_registro, name='seleccionar_registro'),

    # Rutas con restricción por rol
    path('perfil/', rol_requerido('buscar-trabajo', 'ofrecer-trabajo', 'ambos', 'empresa')(views.profile_view), name='perfil'),

    path('actualizar-foto/', rol_requerido('buscar-trabajo', 'ofrecer-trabajo', 'ambos')(views.actualizar_foto), name='actualizar_foto'),
    
    path('actualizar-foto-empresa/', rol_requerido('empresa')(views.actualizar_foto_empresa), name='actualizar_foto_empresa'),

    #path('registro-individual/', rol_requerido('buscar-trabajo', 'ofrecer-trabajo', 'ambos')(views.registro_individual), name='registro_individual'),
    path('registro-empleador/', views.registro_empleador, name='registro_empleador'),

    path('empresa/perfil/', rol_requerido('empresa')(views.perfil_empresa), name='perfil_empresa'),

    path('registro_two/',views.register_two, name='register_two'),
]
