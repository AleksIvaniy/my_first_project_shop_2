from rest_framework.serializers import ModelSerializer, StringRelatedField
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    category = CategorySerializer()
    brand = BrandSerializer()
    color = StringRelatedField()


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'date_joined']


class UserUpdateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email'
        ]


class SimpleProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']


class CartItemSerializer(ModelSerializer):
    product = SimpleProductSerializer()
    sub_total = serializers.SerializerMethodField(method_name='total')

    class Meta:
        model = CartItems
        fields = ['id', 'cart', 'product', 'quantity', 'sub_total']

    def total(self, cartitem: CartItems):
        return cartitem.quantity * cartitem.product.price


class CartSerializer(ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    grand_total = serializers.SerializerMethodField(method_name='main_total')

    class Meta:
        model = Cart
        fields = ['id', 'items', 'grand_total']

    def main_total(self, cart: Cart):
        items = cart.items.all()
        total = sum(item.quantity * item.product.price for item in items)
        return total


class RatingSerializer(ModelSerializer):
    user =  UserUpdateSerializer(read_only=True)
    cr = serializers.SerializerMethodField(method_name='common_rating')
    class Meta:
        model = Rating
        fields = ['id', 'rating', 'description', 'user', 'cr']

    def create(self, validated_data):
        product_id = self.context['product_id']
        user_id = self.context['user_id']
        rating = Rating.objects.create(product_id=product_id, user_id=user_id, **self.validated_data)
        return rating

    def common_rating(self, validated_data):
        return self.context['common_rating']

