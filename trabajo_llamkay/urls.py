from django.urls import path
from . import views

app_name = 'trabajo_llamkay'

urlpatterns = [
    path('', views.index, name='index'),
   path('nosotros/', views.nosotros, name='nosotros'),
  path('medios/', views.medios, name='medios'),
  path('contactanos/', views.contactanos, name='contactanos'),
]
