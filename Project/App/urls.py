from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('form/', views.first_form, name = 'form'),
    path('login_form/', views.login_form, name = 'login_form'),
    path('get_houses/', views.get_houses, name = 'get_houses'),
    path('', views.home, name = 'home'),
    path('get_house/<int:id>', views.get_house, name = 'get_house')
]


urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)