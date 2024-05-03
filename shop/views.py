from django.shortcuts import render
from .serializers import *
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from . filters import ProductFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from . permissions import *
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'brand__name'] # brand
    ordering_fields = ['price']
    permission_classes = [IsAdminOrReadOnly]

    def patch(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

# class AuthApiView(APIView):
#     permission_classes = []
#     def post(self, request):
#         from django.contrib.auth import authenticate, login
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return Response(data={'msg': 'logined successfully'}, status=status.HTTP_200_OK)
#         return Response(status=status.HTTP_401_UNAUTHORIZED)

class ProfileApiView(APIView):
    permission_classes = []

    #from rest_framework.decorators import api_view, permission_classes

    def get(self, request):
        if request.user.is_authenticated:
            data = UserSerializer(request.user, many=False).data
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response(data={'msg': 'You must login!'}, status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request):
        if request.user.is_authenticated:
            serializer = UserUpdateSerializer(request.user, partial=True, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'msg': 'You must login'}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request):
        if request.user.is_authenticated:
            request.user.is_active = False
            request.user.save()
            return Response(data={'msg': 'Your account successfully deactivated!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'msg': 'You must login!'}, status=status.HTTP_401_UNAUTHORIZED)

class ProfileApiRegistrationView(APIView):
    permission_classes = []
    def post(self, request):
        from django.db.utils import IntegrityError
        username = request.data.get('username')
        fn = request.data.get('first_name')
        last_name = request.data.get('last_name')
        password = request.data.get('password')
        email = request.data.get('email')
        try:
            user = User.objects.create_user(username=username, first_name=fn, last_name=last_name, password=password,
                                            email=email)
            data = UserSerializer(user, many=False).data
            return Response(data=data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(data={'msg': 'This username is already taken'}, status=status.HTTP_400_BAD_REQUEST)


class CartViewSet(ListModelMixin, CreateModelMixin, GenericViewSet, RetrieveModelMixin, DestroyModelMixin):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartItemViewSet(ModelViewSet):
    #serializer_class = CartItemSerializer

    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return CartItems.objects.filter(cart_id=self.kwargs['cart__pk'])
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart__pk']}

class RatingViewSet(ModelViewSet):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, OwnerOrReadOnly]

    def get_queryset(self):
        return Rating.objects.filter(product_id=self.kwargs['product__pk'])

    def get_serializer_context(self):
        #a = self.request
        list_rating = [i.rating for i in  Rating.objects.filter(product_id=self.kwargs['product__pk'])]
        #common_rating = sum(list_rating)/ len(list_rating)
        user_id = self.request.user.id
        product_id = self.kwargs['product__pk']
        return {'user_id': user_id, 'product_id': product_id}


class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(owner=user)

# class ProductApiView(APIView):
#     permission_classes = []
#
#     def get(self, request):
#         products = Product.objects.all()
#         data = {
#             'products': ProductSerializer(products, many=True).data
#         }
#         return Response(data=data, status=status.HTTP_200_OK)
#
#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(data=serializer.data, status=status.HTTP_201_CREATED)
#
# class ProductDetailApiView(APIView):
#     permission_classes = []
#     def get(self, request, pk):
#         product = get_object_or_404(Product, id=pk)
#         data = {
#             'product': ProductSerializer(product, many=False).data
#         }
#         return Response(data=data, status=status.HTTP_200_OK)
#
#     def patch(self, request, pk):
#         product = get_object_or_404(Product, id=pk)
#         serializer = ProductSerializer(product, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(data=serializer.data, status=status.HTTP_200_OK)
#
#     def delete(self, request, pk):
#         product = get_object_or_404(Product, id=pk)
#         product.delete()
#         return Response(data={"msg": "Product deleted!"}, status=status.HTTP_204_NO_CONTENT)
