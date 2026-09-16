from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Vehicle
from .forms import VehicleForm

@login_required
def add_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.owner = request.user
            vehicle.save()
            messages.success(request, 'Vehicle added successfully! Now book your service.')
            # Seedha booking page par bhejo naye vehicle ke liye
            return redirect('bookings:create_booking', vehicle_id=vehicle.id)
    else:
        form = VehicleForm()
    
    return render(request, 'customers/add_vehicle.html', {'form': form})
