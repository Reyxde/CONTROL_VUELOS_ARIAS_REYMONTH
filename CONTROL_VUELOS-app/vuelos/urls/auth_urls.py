from django.urls import path

from vuelos.views.auth_views import login_view, logout_view, registro_view

urlpatterns = [
    path('cuentas/login/', login_view, name='login'),
    path('cuentas/logout/', logout_view, name='logout'),
    path('cuentas/registro/', registro_view, name='registro'),
]
