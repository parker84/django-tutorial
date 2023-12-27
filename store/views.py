from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Product, Collection
from.serializers import ProductSerializer, CollectionSerializer
from rest_framework import status
from django.db.models.aggregates import Count

# Create your views here.

# class ProductList(APIView):

    # def get(self, request):
    #     queryset = Product.objects.select_related('collection').all()
    #     serializer = ProductSerializer(queryset, many=True, context={'request':request})
    #     return Response(serializer.data)
    
    # def post(self, request):
    #     serializer = ProductSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(status=status.HTTP_201_CREATED)

class ProductList(ListCreateAPIView):

    # because we didn't have any extra logic in those functions
    # we can just define these directly:
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer

    # def get_queryset(self):
    #     return Product.objects.select_related('collection').all()
    
    # def get_serializer_class(self):
    #     return ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}

# class ProductDetail(APIView):
class ProductDetail(RetrieveUpdateDestroyAPIView):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = 'id' # can do this if we don't want to use pk default

    # def get(self, request, id):
    #     product = get_object_or_404(Product, pk=id)
    #     serializer = ProductSerializer(product) # convert to dict
    #     return Response(serializer.data) # json rendering will be handled under the hood
    
    # def post(self, request, id):
    #     product = get_object_or_404(Product, pk=id)
    #     serializer = ProductSerializer(data=request.data, instance=product)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0:
            return Response(
                {'error': 'Product cannot be deleted because its associated with orderitem'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            ) # see more status codes here: https://www.webfx.com/web-development/glossary/http-status-codes/
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CollectionDetail(RetrieveUpdateDestroyAPIView):

    queryset = Collection.objects.annotate(
        count_products=Count('products')
    )
    serializer_class = CollectionSerializer

    def delete(self, request, pk):
        collection = get_object_or_404(
            Collection.objects.annotate(
                count_products=Count('products')
            ), pk=pk
        )
        if collection.products.count() > 0:
            return Response(
                {'error': f'Collection cannot be deleted because its associated with {collection.products.count()} products'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            ) # see more status codes here: https://www.webfx.com/web-development/glossary/http-status-codes/
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(
        count_products=Count('products')
    ).all()
    serializer_class = CollectionSerializer

    def get_serializer_context(self):
        return {'request': self.request}