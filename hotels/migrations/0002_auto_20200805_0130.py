# Generated by Django 3.0.7 on 2020-08-05 01:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='facility',
            table='facilities',
        ),
        migrations.AlterModelTable(
            name='hotel_facility',
            table='hotels_facilities',
        ),
    ]