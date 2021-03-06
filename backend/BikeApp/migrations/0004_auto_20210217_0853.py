# Generated by Django 3.1.5 on 2021-02-17 08:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('BikeApp', '0003_auto_20210216_1838'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderhistory',
            name='End_date',
        ),
        migrations.RemoveField(
            model_name='orderhistory',
            name='Start_date',
        ),
        migrations.AlterField(
            model_name='customerinfo',
            name='Customer_wallet',
            field=models.FloatField(default=20.0),
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='End_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='Ride_Bill',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='Start_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
