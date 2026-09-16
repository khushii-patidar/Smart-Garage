from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['service_type', 'booking_date', 'problem_description']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
            'problem_description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Gaadi me kya theek karwana hai?'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input'})
