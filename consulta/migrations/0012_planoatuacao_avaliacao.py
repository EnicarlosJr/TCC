# Generated by Django 5.1.1 on 2025-05-07 20:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consulta', '0011_alter_consulta_exames_arquivo'),
    ]

    operations = [
        migrations.AddField(
            model_name='planoatuacao',
            name='avaliacao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='planos_atuacao', to='consulta.avaliacao'),
        ),
    ]
