from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def home(request):
    """Public marketing landing page."""
    return render(request, 'core/landing.html')


@login_required
def dashboard_redirect(request):
    """After login, send each role to its own dashboard."""
    # Superusers (created via terminal) should ALWAYS go to Admin Dashboard
    if request.user.is_superuser:
        return redirect('core:owner_dashboard')
        
    role = request.user.role
    mapping = {
        'OWNER': 'core:owner_dashboard',
        'ADVISOR': 'core:advisor_dashboard',
        'MECHANIC': 'core:mechanic_dashboard',
        'CUSTOMER': 'core:customer_dashboard',
    }
    return redirect(mapping.get(role, 'core:home'))


@login_required
def owner_dashboard(request):
    from bookings.models import Booking
    from django.db.models import Sum
    
    bookings = Booking.objects.all().order_by('-created_at')
    
    # Analytics
    total_revenue = bookings.aggregate(total=Sum('final_bill'))['total'] or 0
    repaired_count = Booking.objects.filter(status='Delivered').count()
    pending_count = Booking.objects.filter(status='Pending').count()
    repairing_count = Booking.objects.filter(status='Repairing').count()
    ready_count = Booking.objects.filter(status='Ready').count()

    context = {
        'bookings': bookings,
        'total_revenue': total_revenue,
        'repaired_count': repaired_count,
        'pending_count': pending_count,
        'repairing_count': repairing_count,
        'ready_count': ready_count,
    }
    return render(request, 'dashboard/owner_dashboard.html', context)


@login_required
def advisor_dashboard(request):
    return render(request, 'dashboard/advisor_dashboard.html')


def mechanic_dashboard(request):
    from bookings.models import Booking
    # Mechanic sees all cars that need fixing or are currently being fixed
    pending_cars = Booking.objects.filter(status='Pending').order_by('booking_date')
    repairing_cars = Booking.objects.filter(status='Repairing').order_by('booking_date')
    return render(request, 'dashboard/mechanic_dashboard.html', {
        'pending_cars': pending_cars,
        'repairing_cars': repairing_cars
    })


@login_required
def ai_mechanic_page(request):
    """Renders the AI Mechanic chat interface."""
    return render(request, 'core/ai_mechanic.html')


import json
import os
import urllib.request
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@login_required
@csrf_exempt
def ai_mechanic_chat(request):
    """Handles the chat request, calls OpenRouter API securely from backend."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            history = data.get('history', [])
            
            api_key = os.environ.get('OPENROUTER_API_KEY')
            if not api_key or api_key == 'yahan_openrouter_ki_api_key_paste_karein':
                return JsonResponse({'error': 'Please add your OPENROUTER_API_KEY in the .env file.'}, status=400)
            
            # Using Llama 3.1 8B Free via OpenRouter
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:8000",
                "X-Title": "SmartGarage"
            }
            # Fallback list of free models on OpenRouter
            models_to_try = [
                "meta-llama/llama-3.1-8b-instruct:free",
                "google/gemma-2-9b-it:free",
                "google/gemma-4-31b-it:free",
                "huggingfaceh4/zephyr-7b-beta:free",
                "microsoft/phi-3-mini-128k-instruct:free",
                "openrouter/free"
            ]
            
            system_msg = {
                "role": "system",
                "content": "You are a highly experienced and friendly Indian Car Mechanic AI. "
                           "Answer car repair questions simply and clearly. "
                           "If the user asks in Hindi or Hinglish, reply in the same natural Hinglish/Hindi tone. "
                           "Keep your answers helpful, practical, and short (3-4 sentences max)."
            }
            
            messages_payload = [system_msg] + history
            
            last_error = ""
            for model_id in models_to_try:
                payload = {
                    "model": model_id,
                    "messages": messages_payload
                }
                
                req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers)
                try:
                    with urllib.request.urlopen(req, timeout=30) as response:
                        response_data = json.loads(response.read().decode())
                        ai_reply = response_data['choices'][0]['message']['content']
                        
                        # Some OpenRouter models glitch and just return "User Safety: safe"
                        if "User Safety: safe" in ai_reply:
                            continue
                            
                        return JsonResponse({'reply': ai_reply})
                except Exception as e:
                    if hasattr(e, 'read'):
                        last_error = e.read().decode()
                    else:
                        last_error = str(e)
                    continue # Try next model if ANY error happens (timeout, dropped connection, 429)
            
            # If we reach here, all models failed
            return JsonResponse({'error': f"API Error: Sabhi free models down hain. Last error: {last_error}"}, status=503)
                
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required
def customer_dashboard(request):
    # Pass vehicles and bookings to dashboard
    vehicles = request.user.vehicles.all()
    bookings = request.user.bookings.all().order_by('-created_at')
        
    return render(request, 'dashboard/customer_dashboard.html', {'vehicles': vehicles, 'bookings': bookings})

@login_required
def emergency_sos(request):
    from django.conf import settings
    # Pass the API key to the template
    api_key = getattr(settings, 'GOOGLE_MAPS_API_KEY', '')
    return render(request, 'core/sos.html', {'google_maps_api_key': api_key})
