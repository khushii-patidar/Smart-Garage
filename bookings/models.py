from django.db import models
from django.conf import settings
from customers.models import Vehicle

class Booking(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending (Wait)'),
        ('Repairing', 'Repairing (Kaam Chalu)'),
        ('Ready', 'Ready (Le Jao)'),
        ('Delivered', 'Delivered (Done)'),
    )

    SERVICE_CHOICES = (
        ('General', 'General Service / Oil Change'),
        ('Wash', 'Car Wash & Cleaning'),
        ('AC', 'AC Repair & Gas'),
        ('Denting', 'Denting & Painting'),
        ('Custom', 'Other / Custom Issue'),
    )

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='bookings')
    
    service_type = models.CharField(max_length=20, choices=SERVICE_CHOICES, default='General')
    problem_description = models.TextField(blank=True, help_text="Kya problem aa rahi hai?")
    booking_date = models.DateField(help_text="Kis din service ke liye aana hai?")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    final_bill = models.PositiveIntegerField(blank=True, null=True, help_text="Final amount to pay")
    
    # Feedback & Rating
    rating = models.IntegerField(null=True, blank=True, help_text="Rating out of 5")
    feedback = models.TextField(blank=True, null=True, help_text="Customer Review")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.vehicle.registration_number} - {self.service_type} ({self.status})"
