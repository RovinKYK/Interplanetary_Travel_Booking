# Generated by Django 4.2.4 on 2023-08-20 15:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_remove_flightschedule_flight_photo_link'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='departure_date',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='destination_planet_id',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='is_completed',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='payment_id',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='spaceship_id',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='starting_planet_id',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='total_price',
        ),
    ]
