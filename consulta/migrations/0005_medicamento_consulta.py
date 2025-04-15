# Generated by Django 5.1.1 on 2025-04-09 01:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consulta', '0004_remove_avaliacao_consulta_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicamento',
            name='consulta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='consulta.consulta'),
        ),
    ]
