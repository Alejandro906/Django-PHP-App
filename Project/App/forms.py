from django import forms
from .models import User, Casa, Casa_images



class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Correo'}))
    password = forms.CharField(widget = forms.PasswordInput(attrs={'placeholder':'Contraseña'}))

class CasaForm(forms.ModelForm):
    class Meta:
        model = Casa
        fields = '__all__' 
        exclude = ['longitud', 'latitud']

class CasaImageForm(forms.ModelForm):
    class Meta:
        model = Casa_images
        fields = ['image']
