# Generated by Django 5.1.1 on 2025-04-22 18:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consulta', '0007_alter_problemasaude_consulta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problemasaude',
            name='consulta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='problemas_saude', to='consulta.consulta'),
        ),
    ]
