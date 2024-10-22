from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserForm, CasaForm
from .models import Casa
from django.core.paginator import Paginator
from django.contrib import messages
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
            casa_obj = Casa.objects.get(id = casa.id)
            print(casa_obj)
            return redirect('login-register')
        else:
            return render(request, 'form.html', {'form':form})
    return render(request, 'form.html', {'form':form})

def second_form(request):
    pass


def get_houses(request):
    times = [0.1, 0.5, 1.5, 2.0, 0.2]
    time_to_load = random.choice(times)
    time.sleep(time_to_load)
    casas = Casa.objects.all()
    paginator = Paginator(casas, 4)
    page = request.GET.get('page')
    page_objs = paginator.get_page(page)

    return render(request, 'partials/casas.html', {'casas': page_objs})

def login_form(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email = email, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Bievenido {user}")
            return redirect('home')
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
    unique_results = {casa.city: casa for casa in filter_values}.values()  # Use a dictionary to ensure unique cities
    return render(request, 'partials/search.html', {'results': unique_results})

from django.core.paginator import Paginator

def search_input_filter(request, city):
    times = [0.1, 0.5, 1.5, 2.0, 0.2]
    time_to_load = random.choice(times)
    time.sleep(time_to_load)
    filter_houses = Casa.objects.filter(city=city)
    paginator = Paginator(filter_houses, 4)
    page = request.GET.get('page')
    page_objs = paginator.get_page(page)
    return render(request, 'partials/casas.html', {'casas': page_objs})

    

        

