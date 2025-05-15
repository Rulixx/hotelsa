# hotels/utils.py
from django.db.models import Q, Count
from .models import Booking
import datetime

def check_room_type_availability(room_type, check_in_date, check_out_date):
    """
    Проверяет, доступен ли ДАННЫЙ ТИП номера на указанные даты.
    Сравнивает количество номеров этого типа с количеством пересекающихся подтвержденных броней.
    """
    if not isinstance(check_in_date, datetime.date):
        check_in_date = datetime.datetime.strptime(check_in_date, '%Y-%m-%d').date()
    if not isinstance(check_out_date, datetime.date):
        check_out_date = datetime.datetime.strptime(check_out_date, '%Y-%m-%d').date()

    
    overlapping_bookings = Booking.objects.filter(
        room_type=room_type,
        status='confirmed', 
        check_in_date__lt=check_out_date, 
        check_out_date__gt=check_in_date 
    ).count() 

   
    available_rooms = room_type.quantity - overlapping_bookings

    return available_rooms > 0