# hotels/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError # Импорт правильный
from django.utils.translation import gettext_lazy as _ # <--- Импорт
from .models import Hotel, RoomType, Amenity, Booking, Review # Hotel уже импортирован
from django.db.models import Q, Min
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .utils import check_room_type_availability
from .forms import BookingForm, ReviewForm, SignUpForm # Импортируем SignUpForm
import datetime

def home_page(request):
    """Отображает главную страницу."""
    # Получаем несколько случайных рекомендуемых отелей (как было)
    featured_hotels = Hotel.objects.order_by('?')[:3]
    # Получаем отели, помеченные как специальное предложение
    special_offer_hotels = Hotel.objects.filter(is_special_offer=True).order_by('?')[:4] # Показываем до 4 акционных отелей

    context = {
        'featured_hotels': featured_hotels,
        'special_offer_hotels': special_offer_hotels, # <-- Передаем акционные отели
    }
    return render(request, 'hotels/index.html', context)

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home_page')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Импортируйте login из django.contrib.auth
            messages.success(request, _('Регистрация прошла успешно! Добро пожаловать!')) # Перевод
            return redirect('home_page')
        else:
            messages.error(request, _('Пожалуйста, исправьте ошибки в форме регистрации.')) # Перевод
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def hotel_list(request):
    hotels_list = Hotel.objects.all().prefetch_related('amenities', 'room_types') # Оптимизация запросов
    query_params = request.GET.copy() # Для сохранения параметров в пагинации и фильтрах

    hotel_name = request.GET.get('hotel_name')
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    selected_stars = request.GET.getlist('stars')
    selected_amenities = request.GET.getlist('amenities') # Ожидаем ID

    check_in_str = request.GET.get('checkin')
    check_out_str = request.GET.get('checkout')
    guests_count_str = request.GET.get('guests', '1')

    # Фильтрация по названию
    if hotel_name:
        hotels_list = hotels_list.filter(name__icontains=hotel_name)

    # Фильтрация по звездам
    if selected_stars:
        valid_stars = [int(s) for s in selected_stars if s.isdigit() and 1 <= int(s) <= 5]
        if valid_stars:
            hotels_list = hotels_list.filter(rating__in=valid_stars)

    # Фильтрация по удобствам (требует наличия ВСЕХ выбранных)
    if selected_amenities:
        valid_amenities = [int(a) for a in selected_amenities if a.isdigit()]
        if valid_amenities:
            for amenity_id in valid_amenities:
                hotels_list = hotels_list.filter(amenities__id=amenity_id)
            # distinct() может понадобиться, если фильтрация по amenities дублирует отели
            hotels_list = hotels_list.distinct()


    # Аннотируем минимальную цену (лучше делать после фильтрации по удобствам)
    hotels_list = hotels_list.annotate(min_price=Min('room_types__base_price'))

    # Фильтрация по цене
    if price_min and price_min.isdigit():
        hotels_list = hotels_list.filter(min_price__gte=int(price_min))
    if price_max and price_max.isdigit():
        # Убедимся, что фильтруем отели, у которых цена ВООБЩЕ есть
        hotels_list = hotels_list.filter(min_price__isnull=False, min_price__lte=int(price_max))


    # Фильтрация по доступности на даты
    available_hotels_pks = []
    apply_date_filter = False
    check_in_date, check_out_date, guests_needed = None, None, 1
    if check_in_str and check_out_str:
        try:
            check_in_date = datetime.datetime.strptime(check_in_str, '%Y-%m-%d').date()
            check_out_date = datetime.datetime.strptime(check_out_str, '%Y-%m-%d').date()
            guests_needed = int(guests_count_str) if guests_count_str.isdigit() else 1

            if check_in_date >= check_out_date or check_in_date < datetime.date.today():
                # Сообщение об ошибке лучше выводить через messages, если это результат поиска
                # messages.error(request, _("Некорректные даты поиска."))
                pass # Пока просто не фильтруем по датам
            else:
                apply_date_filter = True

        except (ValueError, TypeError):
             # messages.error(request, _("Некорректный формат дат или количества гостей."))
             pass # Не фильтруем по датам при ошибке

    if apply_date_filter:
        pks_to_check = list(hotels_list.values_list('pk', flat=True))
        # Получаем все нужные типы номеров одним запросом
        relevant_room_types = RoomType.objects.filter(
            hotel_id__in=pks_to_check,
            capacity__gte=guests_needed
        ).select_related('hotel')

        # Словарь для хранения доступности отелей
        hotel_availability = {pk: False for pk in pks_to_check}

        for room_type in relevant_room_types:
            if hotel_availability[room_type.hotel_id]: # Если для этого отеля уже нашли номер, пропускаем
                continue
            if check_room_type_availability(room_type, check_in_date, check_out_date):
                hotel_availability[room_type.hotel_id] = True

        # Собираем PK отелей, где есть доступные номера
        available_hotels_pks = [pk for pk, available in hotel_availability.items() if available]
        hotels_list = hotels_list.filter(pk__in=available_hotels_pks)


    # Пагинация
    paginator = Paginator(hotels_list.order_by('name'), 10) # 10 отелей на страницу
    page_number = request.GET.get('page')
    try:
        hotels_page = paginator.page(page_number)
    except PageNotAnInteger:
        hotels_page = paginator.page(1)
    except EmptyPage:
        hotels_page = paginator.page(paginator.num_pages)

    # Удаляем 'page' из параметров для ссылок пагинации
    if 'page' in query_params:
        del query_params['page']

    context = {
        'hotels_page': hotels_page,
        'all_amenities': Amenity.objects.all(),
        'query_params': query_params.urlencode(), # Параметры для пагинации и сохранения фильтров
        # Передаем выбранные значения обратно в шаблон для отображения в фильтрах
        'checkin_date_str': check_in_str,
        'checkout_date_str': check_out_str,
        'guests_count_str': guests_count_str,
        'selected_stars': selected_stars, # Список строк
        'selected_amenities': [int(a) for a in selected_amenities if a.isdigit()], # Список int
        'price_min': price_min,
        'price_max': price_max,
        'hotel_name': hotel_name,
    }
    return render(request, 'hotels/search_results.html', context)

def hotel_detail(request, pk):
    hotel = get_object_or_404(Hotel, pk=pk)
    room_types = hotel.room_types.order_by('base_price') # Или .all()
    reviews = hotel.reviews.order_by('-created_at')

    review_form = None
    can_add_review = False
    if request.user.is_authenticated:
        if not Review.objects.filter(hotel=hotel, author=request.user).exists():
            # Проверка, бронировал ли пользователь этот отель (упрощенная)
            # В идеале нужно проверять статус = 'completed'
            if Booking.objects.filter(guest=request.user, room_type__hotel=hotel, status='completed').exists():
                 can_add_review = True
                 review_form = ReviewForm()
            # else: # Можно добавить сообщение, что отзыв можно оставить только после проживания
            #     pass

    context = {
        'hotel': hotel,
        'room_types': room_types, # <-- Убедитесь, что эта строка есть
        'reviews': reviews,
        'review_form': review_form,
        'can_add_review': can_add_review,
    }
    return render(request, 'hotels/hotel_detail.html', context)

@login_required
def create_booking(request, room_type_id):
    room_type = get_object_or_404(RoomType, pk=room_type_id)
    hotel = room_type.hotel

    initial_data = {
        'check_in_date': request.GET.get('checkin'),
        'check_out_date': request.GET.get('checkout'),
        'guests_count': request.GET.get('guests', 1)
    }

    if request.method == 'POST':
        form = BookingForm(request.POST, room_type=room_type)
        if form.is_valid():
            try:
                booking = form.save(commit=False)
                booking.room_type = room_type
                booking.guest = request.user
                booking.status = 'pending' # Или 'confirmed', если оплата не требуется
                # Еще раз проверяем доступность перед сохранением (на всякий случай)
                if not check_room_type_availability(room_type, booking.check_in_date, booking.check_out_date):
                     raise ValidationError(
                         _("К сожалению, номер стал недоступен, пока вы заполняли форму."), code='unavailable'
                     )
                booking.save() # Вызовет clean и save модели
                messages.success(request, _("Ваше бронирование номера '%(room)s' в отеле '%(hotel)s' успешно создано! Ожидайте подтверждения.") % {'room': room_type.name, 'hotel': hotel.name}) # Перевод
                return redirect('account_bookings')
            except ValidationError as e:
                # Добавляем ошибки валидации (из clean формы или модели) в сообщения
                error_messages = e.messages if hasattr(e, 'messages') else [str(e)]
                for msg in error_messages:
                     messages.error(request, msg) # Ошибки уже должны быть переведены в формах/моделях
        else:
            messages.error(request, _("Пожалуйста, исправьте ошибки в форме.")) # Перевод
    else:
        form = BookingForm(initial=initial_data, room_type=room_type)

    context = {
        'form': form,
        'room_type': room_type,
        'hotel': hotel,
    }
    return render(request, 'hotels/create_booking.html', context)

@login_required
def add_review(request, hotel_id):
    hotel = get_object_or_404(Hotel, pk=hotel_id)
    # Проверяем, можно ли вообще оставить отзыв (бронировал и жил)
    can_review = Booking.objects.filter(guest=request.user, room_type__hotel=hotel, status='completed').exists()

    if not can_review:
         messages.error(request, _("Вы можете оставить отзыв только для отелей, в которых проживали.")) # Перевод
         return redirect('hotel_detail', pk=hotel_id)

    # Проверяем, не оставлял ли уже отзыв
    if Review.objects.filter(hotel=hotel, author=request.user).exists():
        messages.error(request, _("Вы уже оставляли отзыв для этого отеля.")) # Перевод
        return redirect('hotel_detail', pk=hotel_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.hotel = hotel
            review.author = request.user
            review.is_verified = True # Считаем верифицированным, т.к. проверили бронь
            review.save()
            messages.success(request, _("Спасибо за ваш отзыв!")) # Перевод
            return redirect('hotel_detail', pk=hotel_id)
        else:
            messages.error(request, _("Пожалуйста, исправьте ошибки в форме отзыва.")) # Перевод
            # Если форма невалидна, покажем страницу отеля снова, но с ошибками формы
            # Нужно передать невалидную форму обратно в контекст hotel_detail
            # Это усложнит hotel_detail view, пока оставим редирект
            return redirect('hotel_detail', pk=hotel_id)
    else:
        # GET запрос на этот URL нелогичен
        return redirect('hotel_detail', pk=hotel_id)


@login_required
def account_profile(request):
    user = request.user
    context = {'user': user}
    return render(request, 'accounts/profile.html', context)

@login_required
def account_bookings(request):
    user_bookings = Booking.objects.filter(guest=request.user).select_related('room_type__hotel').order_by('-check_in_date')
    context = {'bookings': user_bookings}
    return render(request, 'accounts/bookings.html', context)

# Импортируем login из django.contrib.auth для signup_view
from django.contrib.auth import login