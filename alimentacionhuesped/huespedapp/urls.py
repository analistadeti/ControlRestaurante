from django.urls import path
from . import views

urlpatterns = [
    path('', views.mostrar_personas, name='mostrar_personas'),
    path('guardar_persona_seleccionada/', views.guardar_persona_seleccionada, name='guardar_persona_seleccionada'),
    path('mostrar_personas_seleccionadas/', views.mostrar_personas_seleccionadas, name='mostrar_personas_seleccionadas')


    # Otras URLS de tu aplicación si las tienes...
]