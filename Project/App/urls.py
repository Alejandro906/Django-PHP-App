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
    path('search_values/', views.search_filter, name = 'search_filter'),
    path('image-form/<int:casa_id>', views.second_form, name = 'image-form'),
    path('clear-filter/', views.clear_filter, name = 'clear_filter'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('edit_house/<int:casa_id>', views.edit_casa_data, name = 'edit_house'),
    path('edit_house_images/<int:casa_id>', views.edit_casa_images, name = 'edit_house_images'),
    path('send_email/', views.send_email, name = 'send_email'),
    path('logout_page/', views.logout_session, name = 'logout')
]


urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)