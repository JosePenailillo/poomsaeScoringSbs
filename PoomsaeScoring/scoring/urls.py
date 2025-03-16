from django.urls import path, include
from .views import evaluar_view, evaluar, enviar_notas, obtener_notas, ver_notas, custom_logout, ver_notas3_1, ver_notas3_2, ver_notas5_2, ver_notas7_2

urlpatterns = [
    path("evaluar/", evaluar_view, name="evaluar_view"),  # Muestra el formulario HTML
    path("evaluar/enviar/", evaluar, name="evaluar"),  # API para guardar evaluación
    path("ver-notas/", ver_notas, name="ver_notas"),  # Muestra la página HTML para ver notas
    path("ver-notas3-1/", ver_notas3_1, name="ver_notas_3_1"),  # Muestra la página HTML para ver notas
    path("ver-notas3-2/", ver_notas3_2, name="ver_notas_3_2"),  # Muestra la página HTML para ver notas
    path("ver-notas5-2/", ver_notas5_2, name="ver_notas_5_2"),  # Muestra la página HTML para ver notas
    path("ver-notas7-2/", ver_notas7_2, name="ver_notas_7_2"),  # Muestra la página HTML para ver notas
    path("enviar_notas/", enviar_notas, name="enviar_notas"),  # API para enviar notas
    path("obtener_notas/", obtener_notas, name="obtener_notas"),  # API para obtener notas
    path('logout/', custom_logout, name='logout'),

]