from django.urls import path
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenRefreshView

from commerce.views import *

router = routers.SimpleRouter()
router.register('health', HealthViewSet, 'health')
router.register('constants', ConstantsViewSet, basename='constants')

router.register('companies', customers.CompanyViewSet, 'companies')
router.register('products', customers.ProductViewSet, 'products')
router.register('categories', customers.CategoryViewSet, 'categories')
router.register('orders', customers.OrderViewSet, 'orders')

urlpatterns = [
    path('login/', auth.MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    *router.urls,
]
