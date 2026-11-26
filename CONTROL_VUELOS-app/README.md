# CONTROL_VUELOS — Control de vuelos de un aeropuerto

Aplicación web hecha con Django (vistas de función) para gestionar aerolíneas,
aviones, pasajeros y vuelos de un aeropuerto, con registro e inicio de sesión
de usuarios, grupos y permisos.

- **Autor:** Reymonth Arias
- **Tema asignado:** Control de vuelos de un aeropuerto
- **Tecnologías:** Python 3, Django 6.1.3, SQLite

## Modelo de datos (4 tablas)

```
Aerolinea 1 ──< Avion 1 ──< Vuelo >──< Pasajero
                              │
                              └── creado_por ──> User
```

| Modelo | Campos principales | Relaciones |
|---|---|---|
| **Aerolinea** | nombre, codigo (único), pais | 1 → N Avion (`aviones`) |
| **Avion** | matricula (única), modelo, capacidad, fecha_fabricacion, estado (`TextChoices`) | FK `aerolinea` → Aerolinea (`PROTECT`, `related_name='aviones'`) |
| **Pasajero** | nombre, apellido, documento (único), nacionalidad, fecha_nacimiento | N ↔ N Vuelo (`vuelos`) |
| **Vuelo** | codigo (único), origen, destino, fecha_salida, fecha_llegada, estado (`TextChoices`), puerta, precio_base (`DecimalField`) | FK `avion` → Avion (`PROTECT`, `related_name='vuelos'`); M2M `pasajeros` → Pasajero; FK `creado_por` → User (`SET_NULL`, `related_name='vuelos_creados'`) |

Decisiones de modelado:

- `PROTECT` en `Aerolinea → Avion` y en `Avion → Vuelo`: no se puede borrar una
  aerolínea con aviones ni un avión con vuelos.
- `SET_NULL` en `creado_por`: si se elimina un usuario, sus vuelos se conservan.

## Estructura del proyecto

```
CONTROL_VUELOS-app/
  config/                  settings.py, urls.py, wsgi.py, asgi.py
  vuelos/
    models/                un archivo por modelo + __init__.py 
    forms/                 un ModelForm por entidad + registro_form.py
    views/                 un archivo de vistas por entidad + auth_views.py
    urls/                  un archivo de urls por entidad
    templates/vuelos/      plantillas 
    static/vuelos/css/     estilos.css 
    management/commands/   crear_grupos.py, cargar_datos.py
    permisos.py            grupos, permisos y regla de propiedad
    admin.py  apps.py  tests.py  migrations/
  manage.py
  requirements.txt
```

## Cómo levantar el proyecto desde cero

Requisito: Python 3. No hace falta instalar ni configurar ninguna base de datos:
la aplicación usa SQLite y el archivo `db.sqlite3` se crea solo con `migrate`
(no se sube al repositorio).

**1. Clonar el repositorio y entrar a la carpeta del proyecto**

```bash
git clone https://github.com/Reyxde/CONTROL_VUELOS_ARIAS_REYMONTH.git
cd CONTROL_VUELOS_ARIAS_REYMONTH/CONTROL_VUELOS-app
```

**2. Crear y activar el entorno virtual**

```bash
python3 -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux / macOS
```

**3. Instalar las dependencias**

```bash
pip install -r requirements.txt
```

**4. Aplicar las migraciones**

```bash
python manage.py migrate
```

Este comando también crea automáticamente los grupos `administradores` y
`operadores` con sus permisos (señal `post_migrate` en `apps.py`).

**5. Cargar los datos de prueba**

```bash
python manage.py cargar_datos
```

**6. Iniciar el servidor**

```bash
python manage.py runserver
```

## Datos de prueba

`python manage.py cargar_datos` crea:

| Tabla | Registros |
|---|---|
| Aerolínea | 5 |
| Avión | 6 |
| Pasajero | 7 |
| Vuelo | 6 |

## Usuarios de prueba

| Usuario | Contraseña | Rol |
|---|---|---|
| `admin` | `Admin2026!` | Superusuario (también entra a `/admin/`) |
| `jefe_vuelos` | `Jefe2026!` | Grupo **administradores** |
| `operador1` | `Operador2026!` | Grupo **operadores** |
| `operador2` | `Operador2026!` | Grupo **operadores** |

## Grupos y permisos

Los grupos se crean al ejecutar `migrate`
y también con `python manage.py crear_grupos`.

| Grupo | Puede | No puede |
|---|---|---|
| **administradores** | Ver, crear, editar y eliminar las 4 entidades | — |
| **operadores** | Ver las 4 entidades; crear vuelos; editar y eliminar solo los vuelos que ellos crearon | Crear, editar o eliminar aerolíneas, aviones y pasajeros; modificar vuelos de otros usuarios |

