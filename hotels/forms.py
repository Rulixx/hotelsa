# hotels/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone 
from django.utils.translation import gettext_lazy as _ 
from .models import Booking, Review

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        required=True,
        help_text=_('Обязательно. Укажите действующий email.'),
        label=_('Email')
        )
    first_name = forms.CharField(max_length=150, required=False, label=_("Имя")) # Увеличил max_length до стандартного
    last_name = forms.CharField(max_length=150, required=False, label=_("Фамилия"))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
       

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in_date', 'check_out_date', 'guests_count']
        widgets = {
            'check_in_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'guests_count': forms.NumberInput(attrs={'min': 1, 'class': 'form-control'}),
        }
       
        labels = {
             'check_in_date': _('Дата заезда'),
             'check_out_date': _('Дата выезда'),
             'guests_count': _('Количество гостей'),
         }

    def __init__(self, *args, **kwargs):
        self.room_type = kwargs.pop('room_type', None)
        super().__init__(*args, **kwargs)
        if self.room_type:
            self.fields['guests_count'].widget.attrs['max'] = self.room_type.capacity
            self.fields['guests_count'].max_value = self.room_type.capacity
            self.fields['guests_count'].help_text = _("Максимум: %(capacity)s") % {'capacity': self.room_type.capacity}

    def clean_check_in_date(self):
        """Валидация даты заезда"""
        check_in = self.cleaned_data.get('check_in_date')
        if check_in and check_in < timezone.now().date():
             raise forms.ValidationError(_("Дата заезда не может быть в прошлом."))
        return check_in

    def clean_check_out_date(self):
         """Валидация даты выезда (должна быть после заезда)"""
         check_in = self.cleaned_data.get('check_in_date')
         check_out = self.cleaned_data.get('check_out_date')
         if check_in and check_out and check_out <= check_in:
             raise forms.ValidationError(_("Дата выезда должна быть позже даты заезда."))
         return check_out

    def clean_guests_count(self):
        """Валидация количества гостей"""
        guests = self.cleaned_data.get('guests_count')
        if self.room_type and guests > self.room_type.capacity:
             raise forms.ValidationError(
                 _(f"Количество гостей превышает вместимость номера ({self.room_type.capacity}).")
             )
        return guests


    def clean(self):
        """Общая валидация формы, проверка доступности"""
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in_date')
        check_out = cleaned_data.get('check_out_date')

        
        if check_in and check_out and self.room_type:
            from .utils import check_room_type_availability 
            if not check_room_type_availability(self.room_type, check_in, check_out):

                 raise forms.ValidationError(
                     _("К сожалению, этот тип номера недоступен на выбранные даты."),
                     code='unavailable' 
                     )

        return cleaned_data

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }
        
        labels = {
             'rating': _('Ваша оценка'),
             'text': _('Текст отзыва'),
         }