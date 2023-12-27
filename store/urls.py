from django.urls import path
from . import views
# map urls to view functions

# URL configuration
urlpatterns = [
    path(route='products/', view=views.product_list), # always end routes with a /
    path(route='products/<int:id>/', view=views.product_detail),
    # path(route='collections/<int:id>/', view=views.collection_detail, name='collection-detail')
    path(route='collections/', view=views.collection_list), # always end routes with a /
    path(route='collections/<int:id>/', view=views.collection_detail, name='collection-detail')
]