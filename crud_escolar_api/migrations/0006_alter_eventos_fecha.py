# Generated by Django 5.0.2 on 2025-05-21 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud_escolar_api', '0005_eventos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventos',
            name='fecha',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
