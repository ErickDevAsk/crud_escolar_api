# Generated by Django 5.0.2 on 2025-03-17 03:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crud_escolar_api', '0003_alumnos_maestros'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='maestros',
            name='edad',
        ),
    ]
