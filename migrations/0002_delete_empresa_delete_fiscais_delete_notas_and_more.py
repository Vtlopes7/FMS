# Generated by Django 5.1.1 on 2024-10-01 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FMS', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Empresa',
        ),
        migrations.DeleteModel(
            name='Fiscais',
        ),
        migrations.DeleteModel(
            name='Notas',
        ),
        migrations.DeleteModel(
            name='Processo',
        ),
        migrations.AddField(
            model_name='unidade',
            name='CEP',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='unidade',
            name='bairro',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='unidade',
            name='codigo',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='unidade',
            name='endereço',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AddField(
            model_name='unidade',
            name='nome_unidade',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
