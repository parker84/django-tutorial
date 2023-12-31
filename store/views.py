from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
# from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly

from store.filters import ProductFilter
from store.pagination import DefaultPageNumberPagination
from store.permissions import FullDjangoModelPermissions, IsAdminOrReadOnly, ViewCustomerHistoryPermissions

from .models import Cart, CartItem, Collection, Customer, OrderItem, Product, Review

from.serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer, CustomerSerializer, ProductSerializer, CollectionSerializer, ReviewSerializer, UpdateCartItemSerializer
from django.db.models.aggregates import Count
from rest_framework import status

# Create your views here.

class ProductViewSet(ModelViewSet): # other options: ReadOnlyModelViewSet
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['collection_id', 'unit_price']
    filterset_class = ProductFilter
    # pagination_class = PageNumberPagination
    pagination_class = DefaultPageNumberPagination
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']
    permission_classes = [IsAdminOrReadOnly]
    
    # def get_queryset(self):
    #     queryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         return queryset.filter(collection_id=collection_id)
    #     else:
    #         return queryset

    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response(
                {'error': 'Product cannot be deleted because its associated with orderitem'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            ) # see more status codes here: https://www.webfx.com/web-development/glossary/http-status-codes/
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        count_products=Count('products')
    )
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        product_count = Product.objects.filter(collection_id=kwargs['pk']).count()
        if product_count > 0:
            return Response(
                {'error': f'Collection cannot be deleted because its associated with {product_count} products'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            ) # see more status codes here: https://www.webfx.com/web-development/glossary/http-status-codes/
        return super().destroy(request, *args, **kwargs)
    

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_serializer_context(self): # in the view set we have access to the url => access to the product_id
        return {'product_id': self.kwargs['product_pk']} # then we can use the context object to pass this to the serializer
        # self.kwargs contains our url parameters
    
    def get_queryset(self):
        return Review.objects.filter(
            product_id=self.kwargs['product_pk']
        )

# class CartViewSet(ModelViewSet): # don't want this because we don't want all carts to be exposed to an endpoint
class CartViewSet(
    CreateModelMixin,
    RetrieveModelMixin, 
    DestroyModelMixin, 
    GenericViewSet
): # don't want this because we don't want all carts to be exposed to an endpoint
    serializer_class = CartSerializer
    queryset = Cart.objects.prefetch_related('items__product').all() # prefetch

class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        if self.request.method == 'PATCH': # no put requests bc we only want to update a single property
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_queryset(self):
        queryset = CartItem.objects.filter(
            cart_id=self.kwargs['carts_pk']
        ).select_related('product').all()
        return queryset
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['carts_pk']} # then we can use the context object to pass this to the serializer


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]
    # permission_classes = [DjangoModelPermissions]
    # permission_classes = [FullDjangoModelPermissions]
    # permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]
    #     else:
    #         return [IsAuthenticated()]

    @action(detail=True, methods=['GET'], permission_classes=[ViewCustomerHistoryPermissions]) # detail=True => available on the detail endpoint
    def history(self, request, pk):
        return Response({'message': f'history for customer {pk}'})

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated]) # detail=False => available on the list endpoint
    def me(self, request): # defining a customer action
        customer, created = Customer.objects.get_or_create(user_id=request.user.id) # create the customer if a customer with this user_id does not exist yet 
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)