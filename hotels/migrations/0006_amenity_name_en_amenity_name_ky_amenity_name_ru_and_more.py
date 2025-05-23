# Generated by Django 5.2 on 2025-05-08 04:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0005_hotel_latitude_hotel_longitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='amenity',
            name='name_en',
            field=models.CharField(max_length=100, null=True, unique=True, verbose_name='Название удобства'),
        ),
        migrations.AddField(
            model_name='amenity',
            name='name_ky',
            field=models.CharField(max_length=100, null=True, unique=True, verbose_name='Название удобства'),
        ),
        migrations.AddField(
            model_name='amenity',
            name='name_ru',
            field=models.CharField(max_length=100, null=True, unique=True, verbose_name='Название удобства'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='address_en',
            field=models.CharField(max_length=255, null=True, verbose_name='Адрес'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='address_ky',
            field=models.CharField(max_length=255, null=True, verbose_name='Адрес'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='address_ru',
            field=models.CharField(max_length=255, null=True, verbose_name='Адрес'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='description_en',
            field=models.TextField(null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='description_ky',
            field=models.TextField(null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='description_ru',
            field=models.TextField(null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='name_en',
            field=models.CharField(max_length=200, null=True, verbose_name='Название отеля'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='name_ky',
            field=models.CharField(max_length=200, null=True, verbose_name='Название отеля'),
        ),
        migrations.AddField(
            model_name='hotel',
            name='name_ru',
            field=models.CharField(max_length=200, null=True, verbose_name='Название отеля'),
        ),
        migrations.AddField(
            model_name='roomtype',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Описание номера'),
        ),
        migrations.AddField(
            model_name='roomtype',
            name='description_ky',
            field=models.TextField(blank=True, null=True, verbose_name='Описание номера'),
        ),
        migrations.AddField(
            model_name='roomtype',
            name='description_ru',
            field=models.TextField(blank=True, null=True, verbose_name='Описание номера'),
        ),
        migrations.AddField(
            model_name='roomtype',
            name='name_en',
            field=models.CharField(max_length=100, null=True, verbose_name='Название типа номера'),
        ),
        migrations.AddField(
            model_name='roomtype',
            name='name_ky',
            field=models.CharField(max_length=100, null=True, verbose_name='Название типа номера'),
        ),
        migrations.AddField(
            model_name='roomtype',
            name='name_ru',
            field=models.CharField(max_length=100, null=True, verbose_name='Название типа номера'),
        ),
    ]
