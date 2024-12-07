import django_filters
from django import forms
from .models import Casa
from django.db.models import Q

class CasaFilter(django_filters.FilterSet):
    ROOMS_CHOICES = [
        (1, '1 Habitación'),
        (2, '2 Habitaciones'),
        (3, '3 Habitaciones'),
        (4, '4 Habitaciones')
    ]

    RATING_CHOICES = [
        (3, '3+ Estrellas'),
        (4, '4+ Estrellas'),
        (5, '5 Estrellas')
    ]

    city = django_filters.CharFilter(
        field_name='city',
        lookup_expr='icontains',
        label='Ciudad'
    )

    rooms = django_filters.ChoiceFilter(
        choices=ROOMS_CHOICES,
        field_name='rooms',
        lookup_expr='exact',
        empty_label='Habitaciones',
        label='Habitaciones'
    )

    rating = django_filters.ChoiceFilter(
        choices=RATING_CHOICES,
        field_name='rating',
        lookup_expr='gte',
        empty_label='Calificación',
        label='Calificación'
    )

    # Custom method filters for boolean fields
    kitchen = django_filters.BooleanFilter(
        field_name='kitchen',
        label='Cocina',
        method='filter_kitchen',
        widget=forms.CheckboxInput()
    )

    AC = django_filters.BooleanFilter(
        field_name='AC',
        label='Aire Acondicionado',
        method='filter_ac',
        widget=forms.CheckboxInput()
    )

    wifi = django_filters.BooleanFilter(
        field_name='wifi',
        label='WiFi',
        method='filter_wifi',
        widget=forms.CheckboxInput()
    )

    recommended = django_filters.BooleanFilter(
        field_name='recommended',
        label='Recomendado',
        method='filter_recommended',
        widget=forms.CheckboxInput()
    )

    parking = django_filters.BooleanFilter(
        field_name='parking',
        label='Estacionamiento',
        method='filter_parking',
        widget=forms.CheckboxInput()
    )

    TV = django_filters.BooleanFilter(
        field_name='TV',
        label='Televisión',
        method='filter_tv',
        widget=forms.CheckboxInput()
    )

    tub = django_filters.BooleanFilter(
        field_name='tub',
        label='Bañera',
        method='filter_tub',
        widget=forms.CheckboxInput()
    )

    # Custom filtering methods
    def filter_kitchen(self, queryset, name, value):
        return queryset.filter(kitchen=value) if value else queryset

    def filter_ac(self, queryset, name, value):
        return queryset.filter(AC=value) if value else queryset

    def filter_wifi(self, queryset, name, value):
        return queryset.filter(wifi=value) if value else queryset

    def filter_recommended(self, queryset, name, value):
        return queryset.filter(recommended=value) if value else queryset

    def filter_parking(self, queryset, name, value):
        return queryset.filter(parking=value) if value else queryset

    def filter_tv(self, queryset, name, value):
        return queryset.filter(TV=value) if value else queryset

    def filter_tub(self, queryset, name, value):
        return queryset.filter(tub=value) if value else queryset

    class Meta:
        model = Casa
        fields = [
            'rooms', 'rating', 'bathrooms', 'kitchen', 
            'AC', 'wifi', 'recommended', 'square_meter', 
            'parking', 'TV', 'tub'
        ]