from django.db import models
from django.contrib.auth.models import AbstractUser
import geocoder

# Create your models here.

class User(AbstractUser):

    email = models.EmailField(unique=True, max_length=200)
    username = models.CharField(unique=False, max_length=200, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Casa(models.Model):
    title = models.CharField(max_length = 200)
    description = models.TextField()
    rating = models.FloatField()
    country = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    address = models.CharField(max_length=300)
    longitud = models.FloatField(null=True, blank=True)
    latitud = models.FloatField(null=True, blank=True)
    rooms = models.IntegerField()
    bathrooms = models.IntegerField()
    kitchen = models.BooleanField(default=False)
    AC = models.BooleanField(default=False)
    wifi = models.BooleanField(default=False)
    date_uploaded = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    recommended = models.BooleanField(default=False, null=True, blank=True)
    square_meter = models.IntegerField(null=True, blank=True)
    parking = models.BooleanField(default=False)
    TV = models.BooleanField(default=False)
    tub = models.BooleanField(default=False)

    def __str__(self):
        return f"casa en {self.country} con direccion {self.address}"

    def save(self, *args, **kwargs):
        try:
            token = 'pk.eyJ1Ijoiam9yZ2UyMiIsImEiOiJjbTIyY2s1MncwNXZ6MmlzZTRyZ3BocjFmIn0.JC_oYwALzZQ7pIsgDdJ0Hw'
            g = geocoder.mapbox(self.address, key=token)
            
            if g and g.latlng:
                self.latitud = g.latlng[0]
                self.longitud = g.latlng[1]
            else:
                # If geocoding fails, keep the existing coordinates or set to None
                if not self.latitud or not self.longitud:
                    self.latitud = None
                    self.longitud = None
        except Exception as e:
            # Log the error if you have logging configured
            print(f"Geocoding error: {str(e)}")
            # Keep existing coordinates or set to None
            if not self.latitud or not self.longitud:
                self.latitud = None
                self.longitud = None
        
        return super(Casa, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-id']
    

class Casa_images(models.Model):
    casa = models.ForeignKey(Casa, related_name='casa_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='casa_images/', null=True, blank=True)
    
    def __str__(self):
        return f"foto de {self.casa}"
