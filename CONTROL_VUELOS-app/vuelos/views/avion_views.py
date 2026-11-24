from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from vuelos.forms import AvionForm
from vuelos.models import Avion


def avion_list(request):
    aviones = Avion.objects.select_related('aerolinea').all()
    return render(request, 'vuelos/avion/avion_list.html',
                  {'aviones': aviones})


def avion_detail(request, pk):
    avion = get_object_or_404(Avion, pk=pk)
    return render(request, 'vuelos/avion/avion_detail.html',
                  {'avion': avion})



def avion_create(request):
    if request.method == 'POST':
        form = AvionForm(request.POST)
        if form.is_valid():
            avion = form.save()
            messages.success(request, 'Avión creado correctamente.')
            return redirect(avion)
    else:
        form = AvionForm()
    return render(request, 'vuelos/avion/formulario.html',
                  {'form': form})


def avion_update(request, pk):
    avion = get_object_or_404(Avion, pk=pk)
    if request.method == 'POST':
        form = AvionForm(request.POST, instance=avion)
        if form.is_valid():
            avion = form.save()
            messages.success(request, 'Avión actualizado correctamente.')
            return redirect(avion)
    else:
        form = AvionForm(instance=avion)
    return render(request, 'vuelos/avion/formulario.html',
                  {'form': form, 'avion': avion})



def avion_delete(request, pk):
    avion = get_object_or_404(Avion, pk=pk)
    if request.method == 'POST':
        try:
            avion.delete()
        except ProtectedError:
            messages.error(
                request,
                'No se puede eliminar: tiene registros relacionados.')
            return redirect(avion)
        messages.success(request, 'Avión eliminado correctamente.')
        return redirect('avion_list')
    return render(request, 'vuelos/avion/confirm_delete.html',
                  {'avion': avion})
