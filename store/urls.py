from rest_framework.routers import DefaultRouter
from . import views
# map urls to view functions

router = DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collections', views.CollectionViewSet)
urlpatterns = router.urls