from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserForm, CasaForm, CasaImageForm
from .models import Casa, Casa_images
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Count
import time
import random

# Create your views here.

def home(request):
     return render(request, 'home.html', {})

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


from django.core.paginator import Paginator
import random
import time

def get_houses(request):
    times = [0.1, 0.5, 1.5, 2.0, 0.2]
    time_to_load = random.choice(times)
    time.sleep(time_to_load)

    city = request.GET.get('city')
    print(city)
    if city:
        casas = Casa.objects.filter(city__icontains = city)
    else:
        casas = Casa.objects.all()
        
    paginator = Paginator(casas, 4)
    page = request.GET.get('page')
    page_objs = paginator.get_page(page)

    return render(request, 'partials/casas.html', {'casas': page_objs, 'city': city})


def login_form(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email = email, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Bievenido {user}")
            return redirect('form')
        else:
            messages.error(request, 'Correo o contraseña incorecto')
            return redirect('home')

def get_house(request, id):
    casa = Casa.objects.get(id = id)
    return render(request, 'vivienda.html', {'casa':casa})
def main_map(request):
    token = 'pk.eyJ1Ijoiam9yZ2UyMiIsImEiOiJjbTIyY2s1MncwNXZ6MmlzZTRyZ3BocjFmIn0.JC_oYwALzZQ7pIsgDdJ0Hw'
    return render(request, 'partials/main-map.html', {'token':token})

def search_filter(request):
    search_value = request.GET.get('search')
    filter_values = Casa.objects.filter(city__icontains=search_value)
    unique_results = {casa.city: casa for casa in filter_values}.values()
    return render(request, 'partials/search.html', {'results': unique_results})

def clear_filter(request):
    return render(request, 'partials/clear-filter.html', {})

def dashboard(request):
    city_data = Casa.objects.values('city').annotate(total=Count('city')).order_by('city')
    total_casas = len(Casa.objects.all())
    casa_mas_viviendas = Casa.objects.filter()
    
    # Extract the labels (city names) and data (counts)
    labels = [entry['city'] for entry in city_data]
    data = [entry['total'] for entry in city_data]
    
    return render(request, 'dashboard.html', {
        'labels': labels,
        'data': data,
        'total': total_casas
    })


    

        

