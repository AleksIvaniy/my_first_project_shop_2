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
from drf_yasg.utils import swagger_auto_schema


from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse



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

class MyJsonResponse(JsonResponse):
    def __init__(self, data, encoder=DjangoJSONEncoder, safe=True, **kwargs):
        json_dumps_params = dict(ensure_ascii=False)
        super().__init__(data, encoder, safe, json_dumps_params, **kwargs)

def WeatherApiView(request, city):
    import requests
    api_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=48ab3092d8fce2319f231ab8b9717278&units=metric'
    response = requests.get(api_url)
    data = response.json()

    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    d = {}
    weather_descript = data['weather'][0]['main']
    if weather_descript in code_to_smile:
        wd = code_to_smile[weather_descript]
    else:
        wd = 'Посмотри сам в окно, я не знаю что там происходит'
    # pprint(data)
    d['descr'] = wd
    city = data['name']
    d['city'] = city
    cur_weather = str(data['main']['temp']) + "°C"
    d['cur_weather'] = cur_weather
    humidity = str(data['main']['humidity']) + '%'
    d['humidity'] = humidity
    pressure = str(data['main']['pressure']) + 'мм.рт.ст'
    d['pressure'] = pressure
    wind = str(data['wind']['speed']) + 'м/с'
    d['wind'] =  wind
    return MyJsonResponse(d)


class ProductViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = Product.objects.all()
    # serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'brand__name'] # brand
    ordering_fields = ['price']
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PATCH':
            return ProductPostSerializer
        return ProductSerializer

    # @swagger_auto_schema(operation_summary="Post product", request_body=ProductSerializer)
    # def post(self, request, *args, **kwargs):
    #     return super().post(request, *args, **kwargs)


    # def patch(self, request, pk):
    #     product = get_object_or_404(Product, id=pk)
    #     serializer = ProductSerializer(product, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(data=serializer.data, status=status.HTTP_200_OK)

    # def post(self, request):
    #     serializer = ProductSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(data=serializer.data, status=status.HTTP_201_CREATED)

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
    permission_classes = [IsOwnerOrAdmin]

    def get_serializer_context(self):
        user_id = self.request.user.id
        return {'user_id': user_id}

class CartItemViewSet(ModelViewSet):
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
        user_id = self.request.user.id
        product_id = self.kwargs['product__pk']
        return {'user_id': user_id, 'product_id': product_id}


class OrderViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        return OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(owner=user)
    def get_serializer_context(self):
        return {'user_id': self.request.user.id}

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

from ipware import get_client_ip
import urllib, json

def get_user_ip(request):
    client_ip, is_routable = get_client_ip(request)
    if client_ip is None:
        client_ip="0.0.0.0"
    else:
        if is_routable:
            ip_type="Public"
        else:
            ip_type="Private"
    ip_address = '106.220.90.88'
    try:
        url = 'https://api.ipfind.com/?ip=' + client_ip
        response = urllib.request.urlopen(url)
        data1 = json.loads(response.read())
        longitude=data1["longitude"]
        latitude=data1["latitude"]
    except:
        url = 'https://api.ipfind.com/?ip=' + ip_address
        response = urllib.request.urlopen(url)
        data1 = json.loads(response.read())
        longitude=data1["longitude"]
        latitude=data1["latitude"]

    return JsonResponse({'longitude': longitude, 'latitude': latitude})
