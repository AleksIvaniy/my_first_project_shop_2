
from rest_framework.routers import DefaultRouter
# router = DefaultRouter()
# router.register('products', views.ProductViewSet)
#
# urlpatterns = router.urls

from django.urls import path, include
from .views import *

router = DefaultRouter()
router.register('products_set', ProductViewSet)

urlpatterns = [
    # path('products', ProductApiView.as_view(), name='api_product_url'),
    # path('product_detail/<int:pk>', ProductDetailApiView.as_view(), name='api_product_detail_url'),
    path('profile', ProfileApiView.as_view(), name='profile_url'),
    path('auth/', include('rest_framework.urls')),
    path('user_registr', ProfileApiRegistrationView.as_view(), name='user_registr_url')
    # path('login', AuthApiView.as_view(), name='login_url'),
    #path('products_set', ProductViewSet.as_view)
]

urlpatterns += router.urls
