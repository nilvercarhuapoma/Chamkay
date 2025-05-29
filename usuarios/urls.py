from django.urls import path
from . import views


app_name = 'usuarios'
urlpatterns = [
    
  path('login/', views.login, name='login'),
  path('register/', views.register, name='register'),
  

  path('ubicacion/', views.register_two, name='register_two'),  # Paso 2


]

