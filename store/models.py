from django.db import models

# Create your models here.

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.DecimalField
    # product_set -> this will be automatically created, showing all the products that this promotion is applied to

class Collection(models.Model):
    # product = models.ForeignKey(to=Product, on_delete=models.SET_NULL) # this is wrong, because each row is a collection and so we need this on
    # the product class so we can assign each product to a collection 
    title = models.CharField(max_length=255)
    # In a one-to-many relationship in a relational database, the "one" side is typically referred to as the "parent" and the "many" side as the "child."
    featured_product = models.ForeignKey(
        to='Product', 
        on_delete=models.SET_NULL, # if the product gets deleted then this featured_product column will be set to null
        null=True, # notice we need to set null=True when setting on_delete=models.SET_NULL
        related_name='+' # => no reverse relationship created, without this we get an issue because the collections name is already used on the product model
    ) 

class Product(models.Model): # Tip: F2 -> rename everywhere -> but notice if you do this the 'Product' above won't get renamed
    # Django automatically creates an ID field that is a primary key
    # sku = models.CharField(max_length=255, primary_key=True) # this would stop Django from making a primary key and use this instead
    title = models.CharField(max_length=255)
    # slug = models.SlugField() # note: you can't add a non-nullable slug field without a default
    slug = models.SlugField()
    # slug = models.SlugField(null=True)
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2) # always use for monetary values (bc floats have rounding issues)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(to='Collection', on_delete=models.PROTECT) # you can pass to='string' if the parent class is below the child class
    # PROTECT => if you delete a collection - you don't delete all the products in that collection
    # collection = models.ForeignKey(to=Collection, on_delete=models.SET_NULL)
    promotions = models.ManyToManyField(
        to=Promotion, 
        # related_name='products' # this will change the related name on product to product_set
    ) # plural because there can be multiple promotions applied to a product

class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold')
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    # address = ... # Django automatically handled this in the Address class
    birth_date = models.DateField(null=True)

    class Meta:
        # where we define the models metadata
        # options: https://docs.djangoproject.com/en/5.0/ref/models/options/
        # db_table = 'store_customers' # but not recommended to customize tablenames though - just use django defaults
        indexes = [ # used to speed up queries
            models.Index(fields=['last_name', 'first_name'])
        ]
        # note: best not to mix migrations bc the names get shitty


class Order(models.Model):
    PENDING_STATUS = 'P'
    COMPLETE_STATUS = 'C'
    FAILED_STATUS = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PENDING_STATUS, 'Pending'),
        (COMPLETE_STATUS, 'Complete'),
        (FAILED_STATUS, 'Failed')
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PENDING_STATUS)
    customer = models.ForeignKey(to=Customer, on_delete=models.PROTECT) # protect => if the customer is deleted the orders are not

class OrderItem(models.Model):
    order = models.ForeignKey(to=Order, on_delete=models.PROTECT) # now we can have multiple items in an order
    product = models.ForeignKey(to=Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2) # store this because the price of products can change over time

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.CharField(max_length=255, null=True)
    #-------one to one
    # customer = models.OneToOneField(to=Customer, on_delete=models.CASCADE, primary_key=True) # primary key => can only have one address per customer
    # customer = models.OneToOneField(to=Customer, on_delete=models.SET_NULL)
    # customer = models.OneToOneField(to=Customer, on_delete=models.SET_DEFAULT)
    # customer = models.OneToOneField(to=Customer, on_delete=models.PROTECT)
    #-------one to many
    customer = models.ForeignKey(to=Customer, on_delete=models.CASCADE)

class Cart(models.Model):
    # customer = models.ForeignKey(to=Customer, on_delete=models.SET_NULL) # he didn't include this
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CartItem(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE) # delete product => removed from all shopping carts
    quantity = models.PositiveSmallIntegerField()
    cart = models.ForeignKey(to=Cart, on_delete=models.CASCADE) # enabling multiple items in a cart