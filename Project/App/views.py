from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserForm, CasaForm
from .models import Casa
from django.core.paginator import Paginator
from django.contrib import messages
import time

# Create your views here.

def home(request):
     form = LoginForm()
     return render(request, 'home.html', {'form' : form})

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
    time.sleep(2)
    casas = Casa.objects.all()
    paginator = Paginator(casas, 4)
    page = request.GET.get('page')
    page_objs = paginator.get_page(page)

    return render(request, 'partials/casas.html', {'casas': page_objs})

def login_form(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        email = form.data['email']
        password = form.data['password']
        user = authenticate(email = email, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Bievenido {user}")
            return redirect('home')
        else:
            messages.error(request, 'Correo o contraseña incorecto')
            return render(request, 'home.html', {'form':form})

def get_house(request, id):
    casa = Casa.objects.get(id = id)
    return render(request, 'vivienda.html', {'casa':casa})
        

