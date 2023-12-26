from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F, Func, Value, ExpressionWrapper, DecimalField
from django.db.models.functions import Concat
from django.db import transaction, connection
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.db.models.aggregates import Count, Sum, Min, Max, Avg
from store.models import Product, OrderItem, Order, Customer, Collection
from tags.models import TaggedItem

# Create your views here.
# request handlers

# def calculate():
#     x = 1
#     y = 2
#     return x

# def say_hello(request):
#     # next: need to map this view to a url
#     # return HttpResponse('Hello World')
#     x = calculate()
#     return render(request, 'hello.html', {'name': 'Brydon'}) # now returning html content
    
def say_hello1(request):
    # Product.objects. every model in django has a manager object
    query_set = Product.objects.all() # returns all the objects in the database
    # for product in query_set: # can also chain queries together on the query_set:
    for product in query_set.filter().filter().order_by(): 
        print(product)
    return render(request, 'hello.html', {'name': 'Brydon'}) # now returning html content


def say_hello(request):
    # try: 
    #     product = Product.objects.get(pk=0) # will throw an exception if we can't find this object
    # except ObjectDoesNotExist as err:
    #     print(err)
    product_exists = Product.objects.filter(pk=1).exists()
    if product_exists:
        query_set = Product.objects.filter(pk=1)
        product = query_set[0]
    return render(request, 'hello.html', {'name': 'Brydon'}) # now returning html content

def say_hello3(request):
    # see more here: https://docs.djangoproject.com/en/5.0/ref/models/querysets/
    #----------------filtering
    queryset = Product.objects.filter(unit_price__gte=20) # name of our keyword defines the filter
    queryset = Product.objects.filter(unit_price__range=(20, 30))
    queryset = Product.objects.filter(title__icontains='coffee') # icontains => not case senstivie
    queryset = Product.objects.filter(description__isnull=False)
    # and operator
    queryset = Product.objects.filter(inventory__lt=10, unit_price__lt=10) # double filters
    queryset = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=10) # same as above
    # or operator
    queryset = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=10))
    # not + and operator
    queryset = Product.objects.filter(Q(inventory__lt=10) & ~Q(unit_price__lt=10))
    # inventory = unit_price
    queryset = Product.objects.filter(inventory=F('unit_price'))
    #------------------sorting data
    # '-' -> desc order
    queryset = Product.objects.filter(inventory__lt=10, unit_price__lt=10).order_by('unit_price', '-title').reverse()
    queryset = Product.objects.filter(inventory__lt=10).earliest('title')
    queryset = Product.objects.filter(inventory__lt=10).latest('unit_price')
    #------------------limiting results
    queryset = Product.objects.filter(unit_price__lt=10).order_by('-unit_price')
    queryset = queryset[5:10]
    #-----------------selecting fields
    queryset = Product.objects.values('id', 'title', 'collection__title') # collection => we'll bring an inner join in
    # ^ returns dict not product instance
    # values_list => return list instead of dict
    #-----------------exercise
    # products with orders, sorted by title
    # queryset = Product.objects.filter(order_item_id__isnull=False).order_by('title')
    queryset = OrderItem.objects.filter(quantity__gt=0).values(
        'product_id',
        'product__title',
        'product__unit_price',
        'product__inventory'
    ).distinct().order_by('product__title')
    # an alternative way to do this - filter products that are in a list
    queryset = Product.objects.filter(
        id__in=OrderItem.objects.filter(quantity__gt=0).values('product_id').distinct()
    ).order_by('title').values('title')
    #-------------------deferring fields
    queryset = Product.objects.only('id', 'title') # only => returns a product instance, where values returns a dict
    # be careful with only though -> because it can generate a ton of queries if you reference an attribute not included in the only
    queryset = Product.objects.only('id', 'title', 'unit_price') # this is better if we need to use unit_price
    queryset = Product.objects.defer('description') # this will defer the description field to later
    #------------------pre-loading related objects
    queryset = Product.objects.select_related('collection').all() # join with the collection table
    # for many to many (ex: promotions) -> use prefetch_related
    queryset = Product.objects.prefetch_related(
        'promotions'
    ).select_related('collection').all()
    # return render(request, 'hello.html', {'name': 'Brydon', 'products': list(queryset)}) # now returning html content
    #-------exercize
    # last 5 order with their customer and items (incl product)
    queryset = (
        Order.objects.order_by('-placed_at')[:5]
        .select_related('customer')
        # .prefetch_related('orderitem') # incorrect
        # .prefetch_related('orderitem_set')
        .prefetch_related('orderitem_set__product')
    )
    result = Product.objects.aggregate(Count('id'), min_price=Min('unit_price')) # count total number of products, because every product has an id
    # return render(request, 'hello.html', {'name': 'Brydon', 'result': result, 'orders': list(queryset)}) # now returning html content
    #-------------------annotate
    # add additional attributes to objects when querying them
    queryset = Customer.objects.annotate(is_new=Value(True), new_id=F('id')+1).values()
    # return render(request, 'hello.html', {'name': 'Brydon', 'customers': list(queryset)}) # now returning html content
    #------------------calling database functions
    # see more here: https://docs.djangoproject.com/en/5.0/ref/models/database-functions/
    queryset = Customer.objects.annotate(
        # full_name=Func(F('first_name'), Value(' '), F('last_name'), function='CONCAT') # need to wrap in F/V
        full_name=Concat('first_name', Value(' '), 'last_name') # notice we don't need to wrap in F now, but still need Vs
    ).values()
    #-----------------grouping data
    queryset = Customer.objects.annotate(
        # order_count=Count('order_set') # this does not work
        order_count=Count('order') # this is how we count orders
    ).values()
    # #------------working w expression wrappers
    queryset = Product.objects.annotate(
        # discounted_price=F('unit_price') * 0.8 # doesn't work, mixing types
        discounted_price=ExpressionWrapper(F('unit_price') * 0.8, DecimalField())
        # use decimal instead of float for currency bc float has rounding issues
    ).values()
    # return render(request, 'hello.html', {'name': 'Brydon', 'customers': list(queryset)}) # now returning html content
    #--------------querying generic relationships
    content_type = ContentType.objects.get_for_model(Product) # content type id for the product model
    queryset = TaggedItem.objects.select_related('tag').filter(
        content_type=content_type,
        object_id=1
    )
    # return render(request, 'hello.html', {'name': 'Brydon', 'tags': list(queryset)})
    #------------custom managers
    queryset = TaggedItem.objects.get_tags_for(Product, 1)
    # return render(request, 'hello.html', {'name': 'Brydon', 'tags': list(queryset)})
    #-----------understanding queryset cache
    # reading from disk is always slower than reading from memory
    queryset = Product.objects.all()
    result = list(queryset) # => go to the db and execute (expensive)
    # expensive bc it's reading from disk and running computations
    # ^ but this will also store it in cache
    result = list(queryset) # so when it's run again it will read from the querset cache which is stored in memory instead
    result = queryset[0] # same here - read from the querset cache
    # Note: this caching will only happen bc we first evaluated the entire queryset
    # but if we first did querset[0] and then list(queryset) it would make 2 queries
    #-----------creating objects
    # how to insert a record into the database
    collection = Collection() # you could pass the values in keywords, but - no auto complete or refactor renaming
    collection.title = 'Video Games'
    collection.featured_product = Product(pk=1) # product needs to already exist
    # collection.featured_product.id = 1 # same result as above
    collection.save()
    # or:
    # collection.objects.create(title='Video Games', feature_product_id=1)
    # but again ^ keywords arguments won't get auto-completed and refactor / rename doesn't change these
    #-----------update object
    collection = Collection(pk=11) # you could pass the values in keywords, but - no auto complete or refactor renaming
    collection.title = 'Games'
    collection.featured_product = Product(pk=1) # product needs to already exist
    collection.save()
    # update without changing title
    collection = Collection.objects.get(pk=11) # if you don't use objects.get - it will set text defaults to ''
    collection.featured_product = Product(pk=2) 
    collection.save()
    #---------deleting objects
    collection = Collection(pk=11)
    collection.delete()
    # deleting multiple objects
    collection = Collection(pk=12)
    collection.save()
    collection = Collection(pk=13)
    collection.save()
    Collection.objects.filter(pk__gt=11).delete()
    #---------transactions
    # making changes to our database in an atomic way => all changes should be saved together or if one change fails => they should all fail
    # common example: saving an order with it's items
    with transaction.atomic():
        order = Order() # always need to create the parent record first, before the child records
        order.customer_id = 1
        order.save()

        item = OrderItem()
        item.order = order
        item.product_id = 1
        item.quantity = 1
        item.unit_price = 10
        item.save()
        # but what would happen if we get an error when creating the order itmes?
        # => we'd have an order without any items (which we don't want)
        # so we need to make a transaction
        # which we've done at the top with the with, another example on an entire function is below
    #----------executing raw sql queries
    queryset = Product.objects.raw('SELECT id, title FROM store_product') # only required for complex queries
    # accessing the db directly, if we have queries that don't map to our model objects
    with connection.cursor() as cursor:
        cursor.execute('select * from store_product')
        cursor.callproc('get_customers', [1,2,'a']) # better than having sql sitting right in your python code
    return render(request, 'hello.html', {'name': 'Brydon', 'result': list(queryset)})

@transaction.atomic # ensures the entire function is atomic
def say_hello_atomic(request):
    # because of the decorator on the top => this function becomes an atomic transaction
    # => 
    #---------transactions
    # making changes to our database in an atomic way => all changes should be saved together or if one change fails => they should all fail
    # common example: saving an order with it's items
    order = Order() # always need to create the parent record first, before the child records
    order.customer_id = 1
    order.save()
 
    item = OrderItem()
    item.order = order
    item.product_id = 1
    item.quantity = 1
    item.unit_price = 10
    item.save()
    return render(request, 'hello.html', {'name': 'Brydon'})