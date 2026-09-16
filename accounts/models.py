from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model for Smart Garage.
    Every person who logs in (owner, advisor, mechanic, customer) is a User.
    The `role` field decides which dashboard they see and what they can do.
    """

    class Role(models.TextChoices):
        OWNER = 'OWNER', 'Owner / Admin'
        ADVISOR = 'ADVISOR', 'Service Advisor'
        MECHANIC = 'MECHANIC', 'Mechanic'
        CUSTOMER = 'CUSTOMER', 'Customer'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)
    phone = models.CharField(max_length=15, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"

    @property
    def is_owner(self):
        return self.role == self.Role.OWNER

    @property
    def is_advisor(self):
        return self.role == self.Role.ADVISOR

    @property
    def is_mechanic(self):
        return self.role == self.Role.MECHANIC

    @property
    def is_customer_role(self):
        return self.role == self.Role.CUSTOMER


class MechanicProfile(models.Model):
    """Extra details for users with role=MECHANIC."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mechanic_profile')
    specialization = models.CharField(
        max_length=100, blank=True,
        help_text="e.g. Engine, Electrical, AC, Bodywork"
    )
    experience_years = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    jobs_completed = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Mechanic: {self.user.get_full_name() or self.user.username}"


class AdvisorProfile(models.Model):
    """Extra details for users with role=ADVISOR."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='advisor_profile')
    branch = models.CharField(max_length=100, default='Main Branch')
    employee_id = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Advisor: {self.user.get_full_name() or self.user.username}"
