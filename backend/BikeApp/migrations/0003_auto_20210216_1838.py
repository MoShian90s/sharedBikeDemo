# Generated by Django 3.1.5 on 2021-02-16 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BikeApp', '0002_auto_20210212_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderhistory',
            name='End_date',
            field=models.DateField(max_length=100),
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='End_time',
            field=models.TimeField(max_length=100),
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='Start_date',
            field=models.DateField(max_length=100),
        ),
        migrations.AlterField(
            model_name='orderhistory',
            name='Start_time',
            field=models.TimeField(max_length=100),
        ),
    ]