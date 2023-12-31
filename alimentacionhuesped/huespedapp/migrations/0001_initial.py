# Generated by Django 4.2.4 on 2023-08-16 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PersonaSeleccionada',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('habitacion', models.CharField(max_length=10)),
                ('cedula', models.CharField(max_length=20)),
                ('nombre', models.CharField(max_length=100)),
                ('alimentacion', models.CharField(max_length=100)),
                ('nom_plan', models.CharField(max_length=100)),
                ('fecha_actual', models.DateField()),
            ],
            options={
                'verbose_name_plural': 'Personas Seleccionadas',
            },
        ),
    ]
