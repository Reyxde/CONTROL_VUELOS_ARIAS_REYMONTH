from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from vuelos.forms import AerolineaForm
from vuelos.models import Aerolinea


def home(request):
    return render(request, 'vuelos/home.html')

@login_required
@permission_required('vuelos.view_aerolinea', raise_exception=True)
def aerolinea_list(request):
    aerolineas = Aerolinea.objects.all()
    return render(
        request,
        'vuelos/aerolinea/aerolinea_list.html',
        {'aerolineas': aerolineas},
    )

@login_required
@permission_required('vuelos.view_aerolinea', raise_exception=True)
def aerolinea_detail(request, pk):
    aerolinea = get_object_or_404(Aerolinea, pk=pk)
    return render(
        request,
        'vuelos/aerolinea/aerolinea_detail.html',
        {'aerolinea': aerolinea},
    )

@login_required
@permission_required('vuelos.add_aerolinea', raise_exception=True)
def aerolinea_create(request):
    if request.method == 'POST':
        form = AerolineaForm(request.POST)
        if form.is_valid():
            aerolinea = form.save()
            messages.success(request, 'Aerolínea creada correctamente.')
            return redirect(aerolinea)
    else:
        form = AerolineaForm()
    return render(request, 'vuelos/aerolinea/formulario.html', {'form': form})

@login_required
@permission_required('vuelos.change_aerolinea', raise_exception=True)
def aerolinea_update(request, pk):
    aerolinea = get_object_or_404(Aerolinea, pk=pk)
    if request.method == 'POST':
        form = AerolineaForm(request.POST, instance=aerolinea)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aerolínea actualizada correctamente.')
            return redirect(aerolinea)
    else:
        form = AerolineaForm(instance=aerolinea)
    return render(
        request,
        'vuelos/aerolinea/formulario.html',
        {'form': form, 'aerolinea': aerolinea},
    )

@login_required
@permission_required('vuelos.delete_aerolinea', raise_exception=True)
def aerolinea_delete(request, pk):
    aerolinea = get_object_or_404(Aerolinea, pk=pk)
    if request.method == 'POST':
        try:
            aerolinea.delete()
        except ProtectedError:
            messages.error(request, 'No se puede eliminar: tiene aviones asociados.')
            return redirect(aerolinea)
        messages.success(request, 'Aerolínea eliminada correctamente.')
        return redirect('aerolinea_list')
    return render(
        request,
        'vuelos/aerolinea/confirm_delete.html',
        {'aerolinea': aerolinea},
    )
