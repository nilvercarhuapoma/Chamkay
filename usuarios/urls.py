from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('ubicacion/', views.register_two, name='register_two'),
    path('ajax/cargar-provincias/', views.cargar_provincias, name='ajax_cargar_provincias'),
    path('ajax/cargar-distritos/', views.cargar_distritos, name='ajax_cargar_distritos'),
    path('habilidades/', views.register_three, name='register_three')
]
