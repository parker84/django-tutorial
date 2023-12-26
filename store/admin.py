from django.contrib import admin, messages
from .models import Collection, Product, Customer, Order, OrderItem
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from django.db.models.query import QuerySet

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low')
        ]
    
    def queryset(self, request, queryset:QuerySet):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)

# see more here: https://docs.djangoproject.com/en/5.0/ref/contrib/admin/#modeladmin-objects
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ['title']
    }
    autocomplete_fields = ['collection'] # useful if you have too many fields to use a dropdown effectively
    # but we need to add 
    # fields = ['title', 'slug'] # fields for creating a new product
    # exclude = ['promotions'] # exclude fields for adding  new product
    # readonly_fields = ['title']
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title', 'collection']
    list_editable = ['unit_price'] # => you can edit the price of the product in the admin
    list_per_page = 25
    ordering = ['inventory']
    list_select_related = ['collection'] # pre-load so we don't need run a new query for every new record
    list_filter = ['collection', 'last_update', InventoryFilter]
    search_fields = ['title__istartswith']

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'Okay'
    
    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated',
            messages.ERROR
        )

# Register your models here.
# admin.site.register(Collection)
# admin.site.register(Product, ProductAdmin) # use this if you don't have the decorator on the top
# admin.site.register(Product) # don't need this with the decorator on the class

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    # list_display = ['first_name', 'last_name', 'email', 'membership', 'order_set']
    # list_display = ['first_name', 'last_name', 'email', 'membership', 'orders_count']
    list_display = ['first_name', 'last_name', 'email', 'membership', 'orders_count', 'orders']
    list_editable = ['membership', 'email']
    list_per_page = 10
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

    @admin.display(ordering='orders_count')
    def orders(self, customer):
        output_str = ''
        for order in customer.order_set.order_by('id'):
            output_str += str(order.id) + ','
            # url = (
            #     reverse('admin:store_order_changelist')
            #     + '?'
            #     + urlencode({
            #         'order__id': str(order.id)
            #     })
            # )
            # html = format_html('<a href="{}">{}</a>', url, order.id)
            # output_str += ', ' + html
        return output_str
    
    @admin.display(ordering='orders_count')
    def orders_count(self, customer):
        return customer.orders_count
    
    def get_queryset(self, request): 
        # overriding the current method and adding the products_count
        return (
            super().get_queryset(request)
            .prefetch_related('order_set')
            .annotate(
                orders_count=Count('order')
            )
        )


class OrderItemInline(admin.TabularInline): # alternatively you could use admin.StackedInline
    # this also inherits from admin.ModelAdmin
    autocomplete_fields = ['product']
    model = OrderItem
    extra = 0 # no extra rows
    min_num = 1 # always need at least 1 item
    max_num = 10 # can't have more than 

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'payment_status', 'customer']
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    # want to see how many products are in each collection
    list_display = ['title', 'products_count']
    search_fields = ['title'] # this is necessary if you want to use auto complete in the productadmin for collections

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        # return format_html('<a href="http://google.com">{}</a>', collection.products_count)
        url = (
            reverse('admin:store_product_changelist') 
            + '?'
            + urlencode({
                'collection__id': str(collection.id)
            })
        )
        return format_html('<a href="{}">{}</a>', url, collection.products_count)
    
    def get_queryset(self, request): 
        # overriding the current method and adding the products_count
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )