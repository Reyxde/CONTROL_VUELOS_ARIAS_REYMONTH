from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from vuelos.forms import RegistroForm
from vuelos.forms import RegistroForm
from vuelos.permisos import OPERADORES


def registro_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            grupo, _ = Group.objects.get_or_create(name=OPERADORES)
            user.groups.add(grupo)
            login(request, user)
            messages.success(request, 'Cuenta creada. ¡Bienvenido!')
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = RegistroForm()
    return render(request, 'vuelos/autenticacion/registro.html',
                  {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    siguiente = request.POST.get('next') or request.GET.get('next', '')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            if siguiente and url_has_allowed_host_and_scheme(
                    siguiente, allowed_hosts={request.get_host()},
                    require_https=request.is_secure()):
                return redirect(siguiente)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = AuthenticationForm(request)
    return render(request, 'vuelos/autenticacion/login.html',
                  {'form': form, 'next': siguiente})


@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, 'Sesión cerrada correctamente.')
    return redirect(settings.LOGOUT_REDIRECT_URL)
