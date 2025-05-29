from django.urls import path
from . import views

app_name = 'trabajos'

urlpatterns = [
   
    path('', views.index_trabajo, name='index_trabajo'),
    path('crear_trabajo/', views.crear_trabajo, name='crear_trabajo'),
    path('registro_individual/', views.registro_individual, name='registro_individual'),
    path('registro_empresa/', views.registro_empresa, name='registro_empresa'),
    path('all_trabajos', views.all_trabajos,name='all_trabajos')
]
    
    
    