# Generated by Django 5.2 on 2025-04-29 05:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in_date', models.DateField(verbose_name='Дата заезда')),
                ('check_out_date', models.DateField(verbose_name='Дата выезда')),
                ('guests_count', models.PositiveSmallIntegerField(default=1, verbose_name='Количество гостей')),
                ('status', models.CharField(choices=[('pending', 'Ожидание'), ('confirmed', 'Подтверждено'), ('cancelled', 'Отменено'), ('completed', 'Завершено')], default='pending', max_length=10, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('total_price', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True, verbose_name='Общая стоимость')),
                ('guest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL, verbose_name='Гость')),
                ('room_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bookings', to='hotels.roomtype', verbose_name='Тип номера')),
            ],
            options={
                'verbose_name': 'Бронирование',
                'verbose_name_plural': 'Бронирования',
                'ordering': ['-check_in_date', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Текст отзыва')),
                ('rating', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], verbose_name='Оценка')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('is_verified', models.BooleanField(default=False, verbose_name='Верифицирован')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='hotels.hotel', verbose_name='Отель')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'ordering': ['-created_at'],
                'unique_together': {('hotel', 'author')},
            },
        ),
    ]
