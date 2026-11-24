from django.urls import path

from vuelos.views import (
    avion_list, avion_detail, avion_create, avion_update, avion_delete)

urlpatterns = [
    path('aviones/', avion_list, name='avion_list'),
    path('aviones/nuevo/', avion_create, name='avion_create'),
    path('aviones/<int:pk>/', avion_detail, name='avion_detail'),
    path('aviones/<int:pk>/editar/', avion_update, name='avion_update'),
    path('aviones/<int:pk>/eliminar/', avion_delete, name='avion_delete'),
]
