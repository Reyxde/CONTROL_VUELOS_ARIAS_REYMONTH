from django.urls import path
from vuelos.views import home_view

urlpatterns = [
    path('', home_view, name='home'),
]
