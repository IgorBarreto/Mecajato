# Generated by Django 4.1.3 on 2022-11-02 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("clientes", "0002_carro_ano_alter_carro_placa"),
    ]

    operations = [
        migrations.AlterField(
            model_name="carro",
            name="ano",
            field=models.IntegerField(),
        ),
    ]
