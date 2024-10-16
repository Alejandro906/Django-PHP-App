from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('form/', views.first_form, name = 'form'),
    path('login-register/', views.login_register, name = 'login-register'),
    path('get_houses/', views.get_houses, name = 'get_houses'),
    path('', views.home, name = 'home')
]


urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)