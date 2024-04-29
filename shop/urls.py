
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('products_set', ProductViewSet)
router.register('carts', CartViewSet)

product_router = routers.NestedSimpleRouter(router, 'products_set', lookup='product')
product_router.register('ratings', RatingViewSet, basename='rating')
#products/1/ratings

urlpatterns = [
    path('profile', ProfileApiView.as_view(), name='profile_url'),
    path('auth/', include('rest_framework.urls')),
    path('user_registr', ProfileApiRegistrationView.as_view(), name='user_registr_url'),
    path("", include(product_router.urls))
]

urlpatterns += router.urls
