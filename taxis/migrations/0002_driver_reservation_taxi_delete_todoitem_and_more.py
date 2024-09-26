# Generated by Django 5.0.6 on 2024-06-24 14:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('license_number', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passenger_name', models.CharField(max_length=100)),
                ('pickup_location', models.CharField(max_length=200)),
                ('dropoff_location', models.CharField(max_length=200)),
                ('pickup_time', models.DateTimeField()),
                ('dropoff_time', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Taxi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_number', models.CharField(max_length=50)),
                ('brand', models.CharField(max_length=50)),
                ('model', models.CharField(max_length=50)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taxis.driver')),
            ],
        ),
        migrations.DeleteModel(
            name='TodoItem',
        ),
        migrations.AddField(
            model_name='reservation',
            name='taxi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taxis.taxi'),
        ),
    ]
