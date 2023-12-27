from rest_framework import serializers
from decimal import Decimal
from store.models import Product, Collection
from django.db.models.aggregates import Count


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'count_products']
    
    count_products = serializers.IntegerField(read_only=True)

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price', 'collection', 'price_with_tax', 'slug', 'inventory', 'description']
    
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
    