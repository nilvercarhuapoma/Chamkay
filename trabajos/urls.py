from django.urls import path
from . import views
from usuarios.decoradores import rol_requerido

app_name = 'trabajos'

urlpatterns = [
    path('all-trabajos/', views.all_trabajos, name='all_trabajos'),
    path('', views.index_trabajo, name='index_trabajo'),

    # Para usuarios que ofrecen trabajo o ambos
    
    path('registro-individual/', rol_requerido('ofrecer-trabajo', 'ambos')(views.registro_individual), name='registro_individual'),

    # Para empresas exclusivamente
    path('registro-empresa/', rol_requerido('empresa')(views.registro_empresa), name='registro_empresa'),
]
