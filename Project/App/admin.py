from django.contrib import admin
from .models import User, Casa, Casa_images

# Register your models here.

admin.site.register(User)
admin.site.register(Casa)
admin.site.register(Casa_images)
