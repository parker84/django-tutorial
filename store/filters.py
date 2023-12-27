from django_filters.rest_framework import FilterSet
from .models import Product

class ProductFilter(FilterSet):
    # see more here: https://django-filter.readthedocs.io/en/stable/guide/usage.html

    class Meta:
        model = Product
        fields = {
            'collection_id': ['exact'],
            'unit_price': ['lt', 'gt']
        }