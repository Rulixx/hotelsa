# Generated by Django 5.2 on 2025-04-29 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0002_booking_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomtype',
            name='quantity',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='Количество таких номеров'),
        ),
    ]
