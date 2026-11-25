from django.db import migrations


def renombrar_columna(apps, schema_editor):
    tabla = 'vuelos_vuelo'
    with schema_editor.connection.cursor() as cursor:
        columnas = {
            columna.name
            for columna in schema_editor.connection.introspection.get_table_description(
                cursor, tabla)
        }

    if 'aeronave_id' in columnas and 'avion_id' not in columnas:
        qn = schema_editor.quote_name
        schema_editor.execute(
            f'ALTER TABLE {qn(tabla)} '
            f'RENAME COLUMN {qn("aeronave_id")} TO {qn("avion_id")}'
        )


def revertir_renombre(apps, schema_editor):
    tabla = 'vuelos_vuelo'
    with schema_editor.connection.cursor() as cursor:
        columnas = {
            columna.name
            for columna in schema_editor.connection.introspection.get_table_description(
                cursor, tabla)
        }

    if 'avion_id' in columnas and 'aeronave_id' not in columnas:
        qn = schema_editor.quote_name
        schema_editor.execute(
            f'ALTER TABLE {qn(tabla)} '
            f'RENAME COLUMN {qn("avion_id")} TO {qn("aeronave_id")}'
        )


class Migration(migrations.Migration):
    dependencies = [
        ('vuelos', '0004_vuelo'),
    ]

    operations = [
        migrations.RunPython(renombrar_columna, revertir_renombre),
    ]
