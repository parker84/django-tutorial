from django.urls import path
from . import views
# map urls to view functions

# URL configuration
urlpatterns = [
    path(route='products/', view=views.ProductList.as_view()), # always end routes with a /
    path(route='products/<int:id>/', view=views.ProductDetail.as_view()),
    # path(route='collections/<int:id>/', view=views.collection_detail, name='collection-detail')
    path(route='collections/', view=views.collection_list), # always end routes with a /
    path(route='collections/<int:id>/', view=views.collection_detail, name='collection-detail')
]