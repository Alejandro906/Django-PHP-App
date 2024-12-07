from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, CasaForm, CasaImageForm
from .models import Casa, Casa_images
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Count
from .filters import *
from django.contrib.auth.decorators import login_required
import time
import random

# Create your views here.

def home(request):
    # Create filter with all GET parameters
    casa_filters = CasaFilter(request.GET, queryset=Casa.objects.all())
    return render(request, 'home.html', {'filter': casa_filters})

def login_register(request):
    return render(request, 'login_register.html', {})


def first_form(request):    
    form = CasaForm()
    if request.method == 'POST':
        form = CasaForm(request.POST)
        if form.is_valid():
            casa = form.save()
            return redirect('image-form', casa_id=casa.id)
        else:
            return render(request, 'form.html', {'form': form})
    return render(request, 'form.html', {'form': form})

def second_form(request, casa_id):
    casa = Casa.objects.get(id=casa_id)
    if request.method == 'POST':
        image_form = CasaImageForm(request.POST, request.FILES)
        images = request.FILES.getlist('image')
        if image_form.is_valid():
            for image in images:
                Casa_images.objects.create(casa=casa, image=image)
                messages.success(request, f"Casa en {casa.country}, {casa.city} se añadio con exsito")
            return redirect('home')
    else:
        image_form = CasaImageForm()
    return render(request, 'image_form.html', {'form': image_form, 'casa': casa})

def edit_casa_data(request, casa_id):
    casa = Casa.objects.get(id = casa_id)
    if request.method == 'POST':
        form = CasaForm(request.POST, instance=casa)
        if form.is_valid():
            form.save()
            messages.success(request, f"Detalles de la casa en {casa.country}, {casa.city} actualizados con éxito.")
            return redirect('edit_house_images', casa_id=casa.id)
        else:
            return render(request, 'edit_from.html', {'form': form, 'casa': casa})
    else:
        form = CasaForm(instance=casa)
    
    return render(request, 'edit_form.html', {'form': form, 'casa': casa})

def edit_casa_images(request, casa_id):
    casa = Casa.objects.get(id=casa_id)
    existing_images = Casa_images.objects.filter(casa=casa)
    
    # Calculate remaining slots (6 total slots - number of existing images)
    total_slots = 6
    existing_count = existing_images.count()
    # Generate a range for remaining slots, starting after existing images
    remaining_slots = range(existing_count + 1, total_slots + 1)
    
    if request.method == 'POST':
        image_form = CasaImageForm(request.POST, request.FILES)
        new_images = request.FILES.getlist('image')
        
        if image_form.is_valid():
            if new_images:
                for image in new_images:
                    if image:  # Only create if an image was actually uploaded
                        Casa_images.objects.create(casa=casa, image=image)
                messages.success(request, f"Imágenes de la casa en {casa.country}, {casa.city} actualizadas con éxito.")
            else:
                return redirect('home')
        else:
            return render(request, 'image_form.html', {
                'form': image_form,
                'casa': casa,
                'existing_images': existing_images,
                'remaining_slots': remaining_slots
            })
    else:
        image_form = CasaImageForm()
    
    return render(request, 'image_form.html', {
        'form': image_form,
        'casa': casa,
        'existing_images': existing_images,
        'remaining_slots': remaining_slots
    })


def get_houses(request):
    # Simulating variable load time
    times = [0.1, 0.5, 1.5, 2.0, 0.2]
    time_to_load = random.choice(times)
    time.sleep(time_to_load)

    # Apply filtering
    filterset = CasaFilter(request.GET, queryset=Casa.objects.all())
    
    # Paginate the filtered results
    paginator = Paginator(filterset.qs, 4)
    page = request.GET.get('page', 1)
    page_objs = paginator.get_page(page)

    # Additional context for potential city-based filtering
    city = request.GET.get('city', '')

    return render(request, 'partials/casas.html', {
        'casas': page_objs, 
        'city': city,
        'filter': filterset  # Pass the filter to the template if needed
    })


def login_form(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email = email, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Bievenido {user}")
            return redirect('dashboard')
        else:
            messages.error(request, 'Correo o contraseña incorecto')
            return redirect('home')

def get_house(request, id):
    casa = Casa.objects.get(id = id)
    return render(request, 'vivienda.html', {'casa':casa})

def search_filter(request):
    search_value = request.GET.get('city')
    filter_values = Casa.objects.filter(city__icontains=search_value)
    unique_results = {casa.city: casa for casa in filter_values}.values()
    return render(request, 'partials/search.html', {'results': unique_results})

def clear_filter(request):
    return render(request, 'partials/clear-filter.html', {})

@login_required(login_url='home')
def dashboard(request):
    city_data = Casa.objects.values('city').annotate(total=Count('city')).order_by('city')
    total_casas = len(Casa.objects.all())
    ciudad_con_mas_casas = (
        Casa.objects
        .values('city')
        .annotate(num_casas=Count('id'))
        .order_by('-num_casas')
        .first()
    )
    # Access the city name
    nombre_ciudad = ciudad_con_mas_casas['city']

    numero_casas = ciudad_con_mas_casas['num_casas']
    
    # Extract the labels (city names) and data (counts)
    labels = [entry['city'] for entry in city_data]
    data = [entry['total'] for entry in city_data]
    
    return render(request, 'dashboard.html', {
        'labels': labels,
        'data': data,
        'total': total_casas,
        'ciudad_con_mas': nombre_ciudad,
        'num_casa_con_mas': numero_casas
    })

from django.http import HttpResponse
from django.core.mail import EmailMessage

def send_email(request):
    if request.method == 'POST':
        email_message = request.POST.get('email-msg', '')
        print(f"Email message: {email_message}")
        
        email = EmailMessage(
            "BnbHousing Request",  # Subject
            email_message,  # Body
            "desarolloservidor1@gmail.com",  # From
            ["desarolloservidor1@gmail.com"],  # To
        )
        email.send()
        messages.success(request, 'Correo enviado con exito')
        return redirect('home')
    else:
        return HttpResponse("Only POST method allowed.", status=405)

def logout_session(request):
    logout(request)
    messages.success(request, 'Session Se Cerro Con exito')
    return redirect('home')


