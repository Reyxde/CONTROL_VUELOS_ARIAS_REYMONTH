from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from vuelos.forms import PasajeroForm
from vuelos.models import Pasajero


def pasajero_list(request):
    pasajeros = Pasajero.objects.all()
    return render(request, 'vuelos/pasajeros/pasajero_list.html',
                  {'pasajeros': pasajeros})


def pasajero_detail(request, pk):
    pasajero = get_object_or_404(Pasajero, pk=pk)
    return render(request, 'vuelos/pasajeros/pasajero_detail.html',
                  {'pasajero': pasajero})


def pasajero_create(request):
    if request.method == 'POST':
        form = PasajeroForm(request.POST)
        if form.is_valid():
            pasajero = form.save()
            messages.success(request, 'Pasajero creado exitosamente.')
            return redirect(pasajero)
    else:
        form = PasajeroForm()
    return render(request, 'vuelos/pasajeros/formulario.html',
                  {'form': form})


def pasajero_update(request, pk):
    pasajero = get_object_or_404(Pasajero, pk=pk)
    if request.method == 'POST':
        form = PasajeroForm(request.POST, instance=pasajero)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pasajero actualizado exitosamente.')
            return redirect(pasajero)
    else:
        form = PasajeroForm(instance=pasajero)
    return render(request, 'vuelos/pasajeros/formulario.html',
                  {'form': form, 'pasajero': pasajero})

def pasajero_delete(request, pk):
    pasajero = get_object_or_404(Pasajero, pk=pk)
    if request.method == 'POST':
        try:
            pasajero.delete()
        except ProtectedError:
            messages.error(
                request,
                'No se puede eliminar: tiene registros relacionados.')
            return redirect(pasajero)
        messages.success(request, 'Pasajero eliminado exitosamente.')
        return redirect('pasajero_list')
    return render(request, 'vuelos/pasajeros/confirm_delete.html',
                  {'pasajero': pasajero})
