from django import forms
from .models import User, Casa, Casa_images

class UserForm(forms.ModelForm):

    password = forms.CharField(widget = forms.PasswordInput(attrs={'placeholder': 'contraseña'}))
    password_2 = forms.CharField(widget = forms.PasswordInput(attrs={'placeholder': 'confirma contraseña'}))


    class Meta:
        model = User
        fields = ['email']
    
    def clean_password_2(self):
        pass1 = self.cleaned_data.get('password')
        pass2 = self.cleaned_data.get('password 2')

        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError('La contraseña no coincidiron')
        
        return pass2
    
    def save(self):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['pass2'])
        user.save()

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
