from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)

products_router = routers.NestedDefaultRouter(
    router, 
    'products', 
    lookup='product',
)
products_router.register(
    prefix='reviews',
    viewset=views.ReviewViewSet,
    basename='product-reviews'
)

urlpatterns = router.urls + products_router.urls