from django.urls import path

from vuelos.views.vuelo_views import (
    vuelo_list, vuelo_detail, vuelo_create, vuelo_update, vuelo_delete)

urlpatterns = [
    path('vuelos/', vuelo_list, name='vuelo_list'),
    path('vuelos/nuevo/', vuelo_create, name='vuelo_create'),
    path('vuelos/<int:pk>/', vuelo_detail, name='vuelo_detail'),
    path('vuelos/<int:pk>/editar/', vuelo_update, name='vuelo_update'),
    path('vuelos/<int:pk>/eliminar/', vuelo_delete, name='vuelo_delete'),
]
