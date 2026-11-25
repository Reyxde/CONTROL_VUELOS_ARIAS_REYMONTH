from django.urls import include, path

urlpatterns = [
    path('', include('vuelos.urls.aerolinea_urls')),
    path('', include('vuelos.urls.avion_urls')),
    path('', include('vuelos.urls.pasajero_urls')),
    path('', include('vuelos.urls.vuelo_urls')),
    path('', include('vuelos.urls.auth_urls')),

]
