from django.test import TestCase

from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from vuelos.models import Aerolinea, Avion, Pasajero, Vuelo
from vuelos.permisos import ADMINISTRADORES, OPERADORES, crear_grupos


class BaseTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        
        crear_grupos()
        cls.admin = User.objects.create_user('adm', password='x')
        cls.admin.groups.add(Group.objects.get(name=ADMINISTRADORES))
        cls.op1 = User.objects.create_user('op1', password='x')
        cls.op1.groups.add(Group.objects.get(name=OPERADORES))
        cls.op2 = User.objects.create_user('op2', password='x')
        cls.op2.groups.add(Group.objects.get(name=OPERADORES))
        cls.aerolinea = Aerolinea.objects.create(
            nombre='Test Air', codigo='TA', pais='Ecuador')
        cls.avion = Avion.objects.create(
            matricula='HC-TST', modelo='A320', capacidad=2,
            fecha_fabricacion='2020-01-01', aerolinea=cls.aerolinea)
        cls.pasajeros = [Pasajero.objects.create(
            nombre=f'P{i}', apellido='X', documento=f'D{i}',
            fecha_nacimiento='1990-01-01') for i in range(3)]
        salida = timezone.now() + timedelta(days=1)
        cls.vuelo = Vuelo.objects.create(
            codigo='TA1', origen='Quito', destino='Lima',
            fecha_salida=salida, fecha_llegada=salida + timedelta(hours=2),
            precio_base=Decimal('100.00'), avion=cls.avion,
            creado_por=cls.op1)

    def datos_vuelo(self, **extra):
        salida = timezone.localtime() + timedelta(days=2)
        datos = {
            'codigo': 'ta2', 'origen': 'Quito', 'destino': 'Cuenca',
            'avion': self.avion.pk,
            'fecha_salida': salida.strftime('%Y-%m-%dT%H:%M'),
            'fecha_llegada': (salida + timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M'),
            'estado': 'PRO', 'puerta': 'A1', 'precio_base': '50.00',
        }
        datos.update(extra)
        return datos


class AccesoTests(BaseTest):
    def test_anonimo_va_al_login(self):
        r = self.client.get(reverse('vuelo_create'))
        self.assertRedirects(
            r, f"{reverse('login')}?next={reverse('vuelo_create')}")

    def test_id_inexistente_da_404(self):
        self.client.login(username='adm', password='x')
        self.assertEqual(
            self.client.get(reverse('vuelo_detail', args=[9999])).status_code, 404)
        self.assertEqual(
            self.client.get(reverse('vuelo_delete', args=[9999])).status_code, 404)

    def test_logout_solo_por_post(self):
        self.client.login(username='op1', password='x')
        self.assertEqual(self.client.get(reverse('logout')).status_code, 405)
        self.assertEqual(self.client.post(reverse('logout')).status_code, 302)

    def test_registro_crea_usuario_operador(self):
        r = self.client.post(reverse('registro'), {
            'username': 'nuevo', 'email': 'n@x.com',
            'password1': 'ClaveSegura#2026', 'password2': 'ClaveSegura#2026'})
        self.assertRedirects(r, reverse('home'))
        self.assertTrue(User.objects.get(username='nuevo')
                        .groups.filter(name=OPERADORES).exists())


class PermisosTests(BaseTest):
    def test_operador_no_crea_aerolinea(self):
        self.client.login(username='op1', password='x')
        self.assertEqual(
            self.client.get(reverse('aerolinea_create')).status_code, 403)

    def test_operador_ve_listados(self):
        self.client.login(username='op1', password='x')
        for nombre in ('vuelo_list', 'avion_list', 'aerolinea_list',
                       'pasajero_list'):
            self.assertEqual(self.client.get(reverse(nombre)).status_code, 200)

    def test_operador_crea_vuelo_y_queda_como_autor(self):
        self.client.login(username='op2', password='x')
        r = self.client.post(reverse('vuelo_create'), self.datos_vuelo())
        vuelo = Vuelo.objects.get(codigo='TA2')
        self.assertRedirects(r, vuelo.get_absolute_url())
        self.assertEqual(vuelo.creado_por, self.op2)

    def test_propiedad_edicion(self):
        url = reverse('vuelo_update', args=[self.vuelo.pk])
        self.client.login(username='op2', password='x')
        self.assertEqual(self.client.get(url).status_code, 403)  
        self.client.login(username='op1', password='x')
        self.assertEqual(self.client.get(url).status_code, 200)  
        self.client.login(username='adm', password='x')
        self.assertEqual(self.client.get(url).status_code, 200)  

    def test_propiedad_borrado(self):
        url = reverse('vuelo_delete', args=[self.vuelo.pk])
        self.client.login(username='op2', password='x')
        self.assertEqual(self.client.post(url).status_code, 403)
        self.assertTrue(Vuelo.objects.filter(pk=self.vuelo.pk).exists())

    def test_borrado_get_no_elimina(self):
        self.client.login(username='adm', password='x')
        r = self.client.get(reverse('vuelo_delete', args=[self.vuelo.pk]))
        self.assertEqual(r.status_code, 200)
        self.assertTrue(Vuelo.objects.filter(pk=self.vuelo.pk).exists())

    def test_botones_ocultos_al_operador_en_vuelo_ajeno(self):
        self.client.login(username='op2', password='x')
        r = self.client.get(reverse('vuelo_list'))
        self.assertNotContains(r, reverse('vuelo_update', args=[self.vuelo.pk]))


class ReglasNegocioTests(BaseTest):
    def test_detalle_de_vuelo_muestra_avion_y_capacidad(self):
        self.client.login(username='adm', password='x')
        r = self.client.get(reverse('vuelo_detail', args=[self.vuelo.pk]))
        self.assertContains(r, 'HC-TST')
        self.assertContains(r, 'de 2)')

    def test_aerolinea_con_aviones_no_se_borra(self):
        self.client.login(username='adm', password='x')
        r = self.client.post(reverse('aerolinea_delete', args=[self.aerolinea.pk]))
        self.assertEqual(r.status_code, 302)  
        self.assertTrue(Aerolinea.objects.filter(pk=self.aerolinea.pk).exists())

    def test_capacidad_del_avion(self):
        self.client.login(username='adm', password='x')
        r = self.client.post(reverse('vuelo_create'), self.datos_vuelo(
            pasajeros=[p.pk for p in self.pasajeros]))  
        self.assertEqual(r.status_code, 200)
        self.assertFalse(Vuelo.objects.filter(codigo='TA2').exists())

    def test_llegada_posterior_a_salida(self):
        self.client.login(username='adm', password='x')
        datos = self.datos_vuelo()
        datos['fecha_llegada'] = datos['fecha_salida']
        r = self.client.post(reverse('vuelo_create'), datos)
        self.assertEqual(r.status_code, 200)
        self.assertFalse(Vuelo.objects.filter(codigo='TA2').exists())