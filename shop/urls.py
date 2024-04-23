
from rest_framework.routers import DefaultRouter
# router = DefaultRouter()
# router.register('products', views.ProductViewSet)
#
# urlpatterns = router.urls

from django.urls import path
from .views import *

urlpatterns = [
    path('products', ProductApiView.as_view(), name='api_product_url'),
    path('product_detail/<int:pk>', ProductDetailApiView.as_view(), name='api_product_detail_url'),
    path('profile', ProfileApiView.as_view(), name='profile_url'),
    path('login', AuthApiView.as_view(), name='login_url'),
]