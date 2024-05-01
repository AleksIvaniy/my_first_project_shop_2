
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import *
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('products_set', ProductViewSet)
router.register('carts', CartViewSet)

product_router = routers.NestedSimpleRouter(router, 'products_set', lookup='product')
product_router.register('ratings', RatingViewSet, basename='rating')
#product_router.register('reviews', ReviewViewSet, basename='review')
#products_set/4/ratings/1

cart_router = routers.NestedSimpleRouter(router, 'carts', lookup='cart')
cart_router.register('items', CartItemViewSet, basename='cart-items')

urlpatterns = [
    path('profile', ProfileApiView.as_view(), name='profile_url'),
    path('auth/', include('rest_framework.urls')),
    path('user_registr', ProfileApiRegistrationView.as_view(), name='user_registr_url'),
    path("", include(product_router.urls)),
    path("", include(cart_router.urls)),
]

urlpatterns += router.urls
