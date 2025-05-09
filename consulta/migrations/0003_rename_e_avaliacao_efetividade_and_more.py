# Generated by Django 5.1.1 on 2025-04-08 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consulta', '0002_rename_alcançado_planoatuacao_alcancado_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='avaliacao',
            old_name='e',
            new_name='efetividade',
        ),
        migrations.RenameField(
            model_name='avaliacao',
            old_name='n',
            new_name='necessidade',
        ),
        migrations.RenameField(
            model_name='avaliacao',
            old_name='s',
            new_name='seguranca',
        ),
        migrations.AlterField(
            model_name='avaliacao',
            name='classificacao_rnm_1',
            field=models.CharField(choices=[('PSNT', 'Problema de saúde não tratado'), ('EMD', 'Efeito de medicamento desnecessário'), ('INQ', 'Inefetividade não quantitativa'), ('IQ', 'Inefetividade quantitativa'), ('ISQ', 'Insegurança quantitativa')], max_length=50),
        ),
        migrations.AlterField(
            model_name='avaliacao',
            name='classificacao_rnm_2',
            field=models.CharField(choices=[('PSNT', 'Problema de saúde não tratado'), ('EMD', 'Efeito de medicamento desnecessário'), ('INQ', 'Inefetividade não quantitativa'), ('IQ', 'Inefetividade quantitativa'), ('ISQ', 'Insegurança quantitativa'), ('NC', 'Não consta')], max_length=50),
        ),
        migrations.AlterField(
            model_name='planoatuacao',
            name='descricao_planejamento',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='planoatuacao',
            name='o_que_aconteceu',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='planoatuacao',
            name='resultado',
            field=models.TextField(blank=True),
        ),
    ]
