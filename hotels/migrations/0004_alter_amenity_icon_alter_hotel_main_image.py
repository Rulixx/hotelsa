# Generated by Django 5.2 on 2025-04-29 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0003_roomtype_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amenity',
            name='icon',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name="Класс иконки (например, 'fa fa-wifi')"),
        ),
        migrations.AlterField(
            model_name='hotel',
            name='main_image',
            field=models.ImageField(upload_to='hotel_images/', verbose_name='Главное изображение (оригинал)'),
        ),
    ]
