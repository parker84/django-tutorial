from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('carts', views.CartViewSet, basename='carts')
router.register('collections', views.CollectionViewSet)
router.register('customers', views.CustomerViewSet)

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

carts_router = routers.NestedDefaultRouter(
    router,
    'carts',
    lookup='carts'
)
carts_router.register(
    prefix='items',
    viewset=views.CartItemViewSet,
    basename='cart-items'
)

urlpatterns = router.urls + products_router.urls + carts_router.urls