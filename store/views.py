from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import OrderItem, Product, Collection
from rest_framework.viewsets import ModelViewSet
from.serializers import ProductSerializer, CollectionSerializer
from rest_framework import status
from django.db.models.aggregates import Count

# Create your views here.

class ProductViewSet(ModelViewSet): # other options: ReadOnlyModelViewSet
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
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