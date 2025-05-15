# hotels/urls.py (создать этот файл)
from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home_page, name='home_page'), 
    path('hotels/', views.hotel_list, name='hotel_list'), 
    path('hotel/<int:pk>/', views.hotel_detail, name='hotel_detail'), 
    path('booking/create/<int:room_type_id>/', views.create_booking, name='create_booking'), 
    path('hotel/<int:hotel_id>/review/add/', views.add_review, name='add_review'), 
    # TODO: 
]