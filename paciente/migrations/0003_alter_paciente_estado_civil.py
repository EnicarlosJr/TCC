# Generated by Django 5.1.1 on 2025-04-29 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paciente', '0002_remove_paciente_numero_formulario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='estado_civil',
            field=models.CharField(choices=[('Casado(a)', 'Casado(a)'), ('Solteiro(a)', 'Solteiro(a)'), ('Separado(a)', 'Separado(a)'), ('Amigado(a)', 'Amigado(a)'), ('Viuvo(a)', 'Viúvo(a)'), ('Nao consta', 'Não consta'), ('Outro', 'Outro')], max_length=20),
        ),
    ]
