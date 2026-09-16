from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from customers.models import Vehicle
from .models import Booking
from .forms import BookingForm

@login_required
def create_booking(request, vehicle_id):
    # Ensure the vehicle belongs to the current user
    vehicle = get_object_or_404(Vehicle, id=vehicle_id, owner=request.user)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.vehicle = vehicle
            booking.save()
            messages.success(request, 'Service successfully booked! Hum aapka wait karenge.')
            return redirect('core:customer_dashboard')
    else:
        form = BookingForm()
    
    return render(request, 'bookings/create_booking.html', {'form': form, 'vehicle': vehicle})

from django.core.mail import send_mail
from django.conf import settings

def update_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        bill = request.POST.get('final_bill')
        
        if new_status:
            booking.status = new_status
        if bill:
            booking.final_bill = bill
            
        booking.save()
        messages.success(request, f'Booking for {booking.vehicle.registration_number} updated!')
        
    next_url = request.META.get('HTTP_REFERER')
    if next_url:
        return redirect(next_url)
    return redirect('core:home')

@login_required
def rate_service(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        feedback = request.POST.get('feedback')
        if rating:
            booking.rating = int(rating)
            booking.feedback = feedback
            booking.save()
            messages.success(request, 'Thank you for your feedback!')
        return redirect('core:customer_dashboard')
    
    return render(request, 'bookings/rate_service.html', {'booking': booking})

@login_required
def delete_booking(request, booking_id):
    if request.user.role != 'OWNER' and not request.user.is_superuser:
        messages.error(request, 'You do not have permission.')
        return redirect('core:dashboard_redirect')

    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, 'Booking history deleted successfully!')
    return redirect('core:owner_dashboard')


@login_required
def view_invoice(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    # Ensure only the owner or the customer of the car can view it
    if request.user.role != 'OWNER' and not request.user.is_superuser and booking.customer != request.user:
        messages.error(request, 'You do not have permission to view this invoice.')
        return redirect('core:dashboard_redirect')
    return render(request, 'bookings/invoice.html', {'booking': booking})

