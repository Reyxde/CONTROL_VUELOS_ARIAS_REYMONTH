from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from vuelos.forms import VueloForm
from vuelos.models import Vuelo


def vuelo_list(request):
    q = request.GET.get('q', '').strip()
    estado = request.GET.get('estado', '').strip()
    vuelos = Vuelo.objects.select_related(
        'aeronave', 'aeronave__aerolinea', 'creado_por')
    if q:
        vuelos = vuelos.filter(
            Q(codigo__icontains=q) | Q(origen__icontains=q)
            | Q(destino__icontains=q))
    if estado:
        vuelos = vuelos.filter(estado=estado)
    vuelos = list(vuelos)
    for vuelo in vuelos:  # la plantilla usa esta marca para mostrar botones
        vuelo.modificable = puede_modificar_vuelo(request.user, vuelo)
    return render(request, 'vuelos/vuelos/vuelo_list.html', {
        'vuelos': vuelos, 'q': q, 'estado': estado,
        'estados': Vuelo.Estado.choices,
    })



def vuelo_detail(request, pk):
    vuelo = get_object_or_404(
        Vuelo.objects.select_related('aeronave__aerolinea', 'creado_por'),
        pk=pk)
    return render(request, 'vuelos/vuelos/vuelo_detail.html', {
        'vuelo': vuelo,
        'modificable': puede_modificar_vuelo(request.user, vuelo),
    })



def vuelo_create(request):
    if request.method == 'POST':
        form = VueloForm(request.POST)
        if form.is_valid():
            vuelo = form.save(commit=False)
            vuelo.creado_por = request.user
            vuelo.save()
            form.save_m2m()
            messages.success(request, 'Vuelo creado exitosamente.')
            return redirect(vuelo)
    else:
        form = VueloForm()
    return render(request, 'vuelos/vuelos/formulario.html', {'form': form})



def vuelo_update(request, pk):
    vuelo = get_object_or_404(Vuelo, pk=pk)
    if not puede_modificar_vuelo(request.user, vuelo):
        raise PermissionDenied('Solo puede editar los vuelos que usted creó.')
    if request.method == 'POST':
        form = VueloForm(request.POST, instance=vuelo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vuelo actualizado exitosamente.')
            return redirect(vuelo)
    else:
        form = VueloForm(instance=vuelo)
    return render(request, 'vuelos/vuelos/formulario.html',
                  {'form': form, 'vuelo': vuelo})



def vuelo_delete(request, pk):
    vuelo = get_object_or_404(Vuelo, pk=pk)
    if not puede_modificar_vuelo(request.user, vuelo):
        raise PermissionDenied('Solo puede eliminar los vuelos que usted creó.')
    if request.method == 'POST':
        try:
            vuelo.delete()
        except ProtectedError:
            messages.error(request, 'No se puede eliminar este vuelo.')
            return redirect(vuelo)
        messages.success(request, 'Vuelo eliminado exitosamente.')
        return redirect('vuelo_list')
    return render(request, 'vuelos/vuelos/confirm_delete.html',
                  {'vuelo': vuelo})
