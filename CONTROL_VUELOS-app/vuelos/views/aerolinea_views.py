from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from vuelos.forms import AerolineaForm
from vuelos.models import Aerolinea


def home(request):
    return render(request, 'vuelos/home.html')


def aerolinea_list(request):
    aerolineas = Aerolinea.objects.all()
    return render(
        request,
        'vuelos/aerolinea/aerolinea_list.html',
        {'aerolineas': aerolineas},
    )


def aerolinea_detail(request, pk):
    aerolinea = get_object_or_404(Aerolinea, pk=pk)
    return render(
        request,
        'vuelos/aerolinea/aerolinea_detail.html',
        {'aerolinea': aerolinea},
    )


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


def aerolinea_delete(request, pk):
    aerolinea = get_object_or_404(Aerolinea, pk=pk)
    if request.method == 'POST':
        aerolinea.delete()
        messages.success(request, 'Aerolínea eliminada correctamente.')
        return redirect('aerolinea_list')
    return render(
        request,
        'vuelos/aerolinea/confirm_delete.html',
        {'aerolinea': aerolinea},
    )
