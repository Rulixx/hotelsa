# hotels/admin.py
from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin 
from django.utils.translation import gettext_lazy as _
from .models import Hotel, Amenity, RoomType, Booking, Review


@admin.register(Amenity)
class AmenityAdmin(TabbedTranslationAdmin): 
    list_display = ('name', 'icon')
    search_fields = ('name',) 

class RoomTypeInline(admin.TabularInline):
    model = RoomType
    extra = 1
    # TODO: 

@admin.register(Hotel)
class HotelAdmin(TabbedTranslationAdmin): 
    

    list_display = ('name', 'address', 'rating', 'is_special_offer') 
    list_filter = ('rating', 'amenities', 'is_special_offer') 
    search_fields = ('name', 'address', 'description', 'special_offer_description') 
    filter_horizontal = ('amenities',)
    
    
    fieldsets = (
        (_('Основная информация'), {
            'fields': ('name', 'address', 'description', 'rating', 'main_image')
        }),
        (_('Удобства и Расположение'), {
            'fields': ('amenities', 'latitude', 'longitude')
        }),
        (_('Специальное Предложение'), { 
            'fields': ('is_special_offer', 'special_offer_description'),
            'classes': ('collapse',), 
        }),
    )

@admin.register(RoomType)
class RoomTypeAdmin(TabbedTranslationAdmin): 
    list_display = ('name', 'hotel', 'base_price', 'capacity')
    list_filter = ('hotel', 'capacity')
    search_fields = ('name', 'hotel__name')
    list_editable = ('base_price', 'capacity')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('room_type', 'guest', 'check_in_date', 'check_out_date', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'check_in_date', 'room_type__hotel') 
    search_fields = ('guest__username', 'guest__email', 'room_type__name', 'room_type__hotel__name')
    list_editable = ('status',) 
    readonly_fields = ('created_at', 'updated_at', 'total_price') 
    autocomplete_fields = ['guest', 'room_type']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'author', 'rating', 'created_at', 'is_verified')
    list_filter = ('rating', 'created_at', 'is_verified', 'hotel')
    search_fields = ('author__username', 'hotel__name', 'text')
    list_editable = ('is_verified',)
    readonly_fields = ('created_at',)
    autocomplete_fields = ['hotel', 'author'] 