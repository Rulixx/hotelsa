# hotels/models.py
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _ 


from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit

class Amenity(models.Model):
    """Модель удобства (Спа, Бассейн, Wi-Fi и т.д.)"""
    name = models.CharField(max_length=100, unique=True, verbose_name=_("Название удобства"))
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name=_("Класс иконки (например, 'fa fa-wifi')"))

    class Meta:
        verbose_name = _("Удобство")
        verbose_name_plural = _("Удобства")
        ordering = ['name']

    def __str__(self):
        
        return self.name

class Hotel(models.Model):
    """Модель отеля"""
    name = models.CharField(max_length=200, verbose_name=_("Название отеля"))
    address = models.CharField(max_length=255, verbose_name=_("Адрес"))
    description = models.TextField(verbose_name=_("Описание"))
    rating = models.PositiveSmallIntegerField(
        choices=[(i, _(f"{i} звезд(ы)")) for i in range(1, 6)], #
        verbose_name=_("Рейтинг (звезды)")
    )
    amenities = models.ManyToManyField(Amenity, blank=True, verbose_name=_("Удобства"))

    main_image = models.ImageField(
        upload_to='hotel_images/',
        verbose_name=_("Главное изображение (оригинал)")
    )

    
    latitude = models.DecimalField(
        max_digits=10,  
        decimal_places=7,
        null=True,       
        blank=True,      
        verbose_name=_("Широта")
    )
    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7,
        null=True,
        blank=True,
        verbose_name=_("Долгота")
    )
    #

    
    is_special_offer = models.BooleanField(
        default=False,
        verbose_name=_("Специальное предложение?"),
        help_text=_("Отметьте, если для этого отеля есть действующая акция")
    )
    special_offer_description = models.CharField(
        max_length=255, 
        blank=True,     
        null=True,
        verbose_name=_("Описание спецпредложения"),
        help_text=_("Например: '-15% на выходные', 'Завтрак в подарок'")
    )
    

    image_card = ImageSpecField(
        source='main_image', processors=[ResizeToFill(300, 220)], format='JPEG', options={'quality': 80}
    )
    image_large = ImageSpecField(
        source='main_image', processors=[ResizeToFit(1200, 600, upscale=False)], format='JPEG', options={'quality': 85}
    )
    image_thumbnail = ImageSpecField(
        source='main_image', processors=[ResizeToFill(100, 80)], format='JPEG', options={'quality': 70}
    )

    class Meta:
        verbose_name = _("Отель")
        verbose_name_plural = _("Отели")
        ordering = ['name']

    def __str__(self):
        
        return self.name

    def get_absolute_url(self):
        return reverse('hotel_detail', kwargs={'pk': self.pk})


class RoomType(models.Model):
    """Модель типа номера (Стандарт, Люкс и т.д.)"""
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='room_types', verbose_name=_("Отель"))
    name = models.CharField(max_length=100, verbose_name=_("Название типа номера"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Описание номера"))
    base_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Базовая цена за ночь (KGS)"))
    capacity = models.PositiveSmallIntegerField(default=2, verbose_name=_("Вместимость (чел.)"))
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name=_("Количество таких номеров"))

    class Meta:
        verbose_name = _("Тип номера")
        verbose_name_plural = _("Типы номеров")
        ordering = ['hotel', 'base_price']

    def __str__(self):
        return f"{self.hotel.name} - {self.name}"

class Booking(models.Model):
    """Модель бронирования"""
    STATUS_CHOICES = (
        ('pending', _('Ожидание')),
        ('confirmed', _('Подтверждено')),
        ('cancelled', _('Отменено')),
        ('completed', _('Завершено')),
    )

    room_type = models.ForeignKey(RoomType, on_delete=models.PROTECT, related_name='bookings', verbose_name=_("Тип номера"))
    guest = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings', verbose_name=_("Гость"))
    check_in_date = models.DateField(verbose_name=_("Дата заезда"))
    check_out_date = models.DateField(verbose_name=_("Дата выезда"))
    guests_count = models.PositiveSmallIntegerField(default=1, verbose_name=_("Количество гостей"))
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name=_("Статус"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Дата обновления"))
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name=_("Общая стоимость"))

    class Meta:
        verbose_name = _("Бронирование")
        verbose_name_plural = _("Бронирования")
        ordering = ['-check_in_date', '-created_at']

    def clean(self):
        """Добавляем валидацию дат и вместимости"""
        if self.check_in_date and self.check_out_date and self.check_in_date >= self.check_out_date:
            raise ValidationError(_("Дата выезда должна быть позже даты заезда."))
        if self.guests_count <= 0:
            raise ValidationError(_("Количество гостей должно быть больше нуля."))

    def calculate_nights(self):
        if self.check_in_date and self.check_out_date:
            delta = self.check_out_date - self.check_in_date
            return delta.days
        return 0

    def calculate_total_price(self):
        nights = self.calculate_nights()
        if nights > 0 and self.room_type:
            return nights * self.room_type.base_price
        return 0

    def save(self, *args, **kwargs):
        self.total_price = self.calculate_total_price()
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return _("Бронь %(room_type)s для %(guest)s (%(check_in)s - %(check_out)s)") % {
            'room_type': self.room_type,
            'guest': self.guest.username,
            'check_in': self.check_in_date,
            'check_out': self.check_out_date
        }

class Review(models.Model):
    """Модель отзыва"""
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)] 

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reviews', verbose_name=_("Отель"))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews', verbose_name=_("Автор"))
    text = models.TextField(verbose_name=_("Текст отзыва"))
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, verbose_name=_("Оценка"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    is_verified = models.BooleanField(default=False, verbose_name=_("Верифицирован"))

    class Meta:
        verbose_name = _("Отзыв")
        verbose_name_plural = _("Отзывы")
        ordering = ['-created_at']
        unique_together = ('hotel', 'author')

    def __str__(self):
        return _("Отзыв от %(author)s на %(hotel)s (%(rating)s*)") % {
            'author': self.author.username,
            'hotel': self.hotel.name,
            'rating': self.rating
        }