from django.urls import path
# from rest_framework.routers import SimpleRouter
from rest_framework.routers import DefaultRouter
from . import views
from django.urls.conf import include
from pprint import pprint
# map urls to view functions

# router = SimpleRouter()
router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)
pprint(router.urls)
urlpatterns = router.urls

# urlpatterns = [
#     path('', include(router.urls))
# ]

# URL configuration
# urlpatterns = [
    # path(route='products/', view=views.ProductList.as_view()), # always end routes with a /
    # # path(route='products/<int:id>/', view=views.ProductDetail.as_view()),
    # path(route='products/<int:pk>/', view=views.ProductDetail.as_view()),
    # # path(route='collections/<int:id>/', view=views.collection_detail, name='collection-detail')
    # path(route='collections/', view=views.CollectionList.as_view()), # always end routes with a /
    # # path(route='collections/<int:id>/', view=views.collection_detail, name='collection-detail')
    # path(route='collections/<int:pk>/', view=views.CollectionDetail.as_view(), name='collection-detail')
# ]