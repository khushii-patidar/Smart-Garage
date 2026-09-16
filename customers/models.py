from django.db import models
from django.conf import settings

class Vehicle(models.Model):
    FUEL_CHOICES = (
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
        ('CNG', 'CNG'),
        ('EV', 'Electric (EV)'),
    )

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vehicles')
    registration_number = models.CharField(max_length=20, unique=True, help_text="e.g. MH 04 AB 1234")
    brand = models.CharField(max_length=50, help_text="e.g. Honda, Tata, Hyundai")
    car_model = models.CharField(max_length=50, help_text="e.g. City, Nexon, i20")
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES, default='Petrol')
    manufacturing_year = models.PositiveIntegerField()
    mileage = models.PositiveIntegerField(help_text="Current KMs driven", default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.registration_number} - {self.brand} {self.car_model}"
