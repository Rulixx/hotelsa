# hotels/account_urls.py (новый файл)
from django.urls import path
from . import views # Импортируем основные views

urlpatterns = [
    path('profile/', views.account_profile, name='account_profile'),
    path('bookings/', views.account_bookings, name='account_bookings'),
    # TODO: Добавить другие разделы ЛК (лояльность, настройки)
]