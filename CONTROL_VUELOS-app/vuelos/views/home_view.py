from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from vuelos.models import Vuelo


@login_required
def home_view(request):
    proximos = []
    if request.user.has_perm('vuelos.view_vuelo'):
        proximos = Vuelo.objects.select_related('avion').exclude(
            estado__in=[Vuelo.Estado.ATERRIZADO, Vuelo.Estado.CANCELADO]
        )[:5]
    return render(request, 'vuelos/home.html', {'proximos': proximos})
