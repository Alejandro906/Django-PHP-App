from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('form/', views.first_form, name = 'form'),
    path('login_form/', views.login_form, name = 'login_form'),
    path('get_houses/', views.get_houses, name = 'get_houses'),
    path('', views.home, name = 'home'),
    path('get_house/<int:id>', views.get_house, name = 'get_house'),
    path('main-map/', views.main_map, name = 'main-map'),
    path('search_values/', views.search_filter, name = 'search_filter'),
    path('image-form/<int:casa_id>', views.second_form, name = 'image-form'),
    path('clear-filter/', views.clear_filter, name = 'clear_filter')
]


urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)