from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('ubicacion/', views.register_two, name='register_two'),
    path('dashboard/', views.dashboard, name='dashboard'),  
    path('register/', views.register, name='register'),
    path('perfil/', views.perfil, name='perfil'),
    path('actualizar_perfil/', views.actualizar_perfil, name='actualizar_perfil'),
    path('configuracion/', views.configuracion, name='configuracion'),
    path('ayuda/', views.ayuda, name='ayuda'),
    path('accesibilidad/', views.accesibilidad, name='accesibilidad'),
    path('comentarios/', views.comentarios, name='comentarios'),
    path('cargar_provincias/', views.cargar_provincias, name='cargar_provincias'),
    path('cargar_distritos/', views.cargar_distritos, name='cargar_distritos'),
    path('validar_correo/', views.validar_correo, name='validar_correo'),
    path('habilidades/', views.register_three, name='register_three')
    
]