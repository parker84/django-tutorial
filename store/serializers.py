from rest_framework import serializers
from decimal import Decimal
from store.models import Cart, CartItem, Product, Collection, Review
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
    
class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']
    
    def create(self, validated_data):
        product_id = self.context['product_id'] # context allows us to provide additional data to a serializer
        return Review.objects.create(
            product_id=product_id,
            **validated_data
        )

class SimpleProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']

class CartItemSerializer(serializers.ModelSerializer):

    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    class Meta:
        model = CartItem
        # fields = ['id', 'product_id', 'quantity', 'cart_id'] # incorrect
        fields = ['id', 'product', 'quantity', 'total_price']
    
    def get_total_price(self, cartitem: CartItem):
        return cartitem.quantity * cartitem.product.unit_price
    
    def create(self, validated_data):
        cart_id = self.context['cart_id'] # context allows us to provide additional data to a serializer
        return CartItem.objects.create(
            cart_id=cart_id,
            **validated_data
        )

class CartSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']
    
    def get_total_price(self, cart: Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

    
class AddCartItemSerializer(serializers.ModelSerializer):

    product_id = serializers.IntegerField()
    
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                'No product with given ID was found'
            )
        return value

    def save(self, **kwargs):
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        cart_id = self.context['cart_id']
        try:
            cartitem = CartItem.objects.get(
                cart_id = cart_id,
                product_id = product_id
            )
            cartitem.quantity += quantity
            cartitem.save()
            self.instance = cartitem
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id,
                **self.validated_data
            )
        self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']

class UpdateCartItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ['quantity']
