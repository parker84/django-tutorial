from rest_framework import serializers
from decimal import Decimal
from store.models import Product, Collection
from django.db.models.aggregates import Count


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'count_products']
    
    count_products = serializers.IntegerField(read_only=True)

    # count_products = serializers.SerializerMethodField(method_name='count_products')
    
    # def count_products(self, collection: Collection):
    #     import ipdb; ipdb.set_trace()
    #     count_products = collection.objects.aggregate(Count('product'))
    #     return count_products

# class CollectionSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField()

class ProductSerializer(serializers.ModelSerializer):
    # by using the ModelSerializer we can reduce the amount of code vs below
    # by leaning on the model definitions 
    class Meta:
        model = Product
        # fields = '__all__' # bad practice: if add a new field it would automatically get exposed to the outside world
        fields = ['id', 'title', 'unit_price', 'collection', 'price_with_tax', 'slug', 'inventory', 'description']
    
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # can still overide like below if we want:
    # collection = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),
    #     view_name='collection-detail'
    # )
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
    
    # note: these 2 below are not needed at the moment, but can be useful
    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.other = 1
    #     product.save()
    #     return product
    
    # def update(self, instance, validated_data):
    #     instance.unit_price = validated_data.get('unit_price')
    #     instance.save()
    #     return instance
    

    # def validate(self, data):
    #     if data['passsword'] != data['confirmed_password']:
    #         return serializers.ValidationError('Passwords do not match')
    #     return data

class ProductSerializerOG(serializers.Serializer):
    # need to build an external representation of a product
    # see more here: https://www.django-rest-framework.org/api-guide/serializers/
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255) # setting max_length now bc we'll use this for accepting data as well
    # price = serializers.DecimalField(max_digits=6, decimal_places=2) # could set a different name if we wanted to
    # unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset=Collection.objects.all()
    # )
    # collection = serializers.StringRelatedField()
    # collection = CollectionSerializer()
    collection = serializers.HyperlinkedRelatedField(
        queryset=Collection.objects.all(),
        view_name='collection-detail'
    )

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)