# hotels/translation.py
from modeltranslation.translator import register, TranslationOptions
from .models import Hotel, RoomType, Amenity 

@register(Hotel)
class HotelTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'address') 

@register(RoomType)
class RoomTypeTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

@register(Amenity)
class AmenityTranslationOptions(TranslationOptions):
    fields = ('name',) 