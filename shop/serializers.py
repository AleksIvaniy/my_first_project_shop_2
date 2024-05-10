from rest_framework.serializers import ModelSerializer, StringRelatedField
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django.db import transaction

class BrandSerializer(ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ColorSerializer(ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'

class RatingSimpleSerializer(ModelSerializer):
    class Meta:
        model = Rating
        fields = ['rating']

class ProductPostSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['VIN', 'name', 'description', 'price', 'category', 'brand', 'color']

class ProductSerializer(ModelSerializer):
    rating = RatingSimpleSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'VIN', 'name', 'description', 'price', 'category', 'brand', 'color', 'rating']

    category = CategorySerializer()
    brand = BrandSerializer()
    color = ColorSerializer()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['rating'] = []
        for elem in instance.rating.all():
            representation['rating'].append(elem.rating)
        if not sum(representation['rating']):
            representation['rating'] = 0
        else:
            representation['rating'] = sum(representation['rating'])/len(representation['rating'])
        return representation


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
    product = SimpleProductSerializer(many=False)
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
    class Meta:
        model = Rating
        fields = ['id', 'rating', 'description', 'user']

    def create(self, validated_data):
        product_id = self.context['product_id']
        user_id = self.context['user_id']
        rating = Rating.objects.create(product_id=product_id, user_id=user_id, **self.validated_data)
        return rating

    # def common_rating(self, validated_data):
    #     return self.context['common_rating']

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('There is no product associated with the given ID')
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data.get('product_id')
        quantity = self.validated_data['quantity']

        try:
            cartitem = CartItems.objects.get(product_id=product_id, cart_id=cart_id)
            cartitem.quantity += quantity
            cartitem.save()

            self.instance = cartitem

        except:
            self.instance = CartItems.objects.create(product_id=product_id, cart_id=cart_id, quantity=quantity)
        return self.instance

    class Meta:
        model = CartItems
        fields = ['id', 'product_id', 'quantity']

class UpdateCartItemSerializer(ModelSerializer):
    #id = serializers.IntegerField(read_only=True)
    class Meta:
        model = CartItems
        fields = ['quantity']


class OrderItemSerializer(ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']

class OrderSerializer(ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'placed_at', 'pending_status', 'owner', 'items']

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            user_id = self.context['user_id']
            order = Order.objects.create(owner_id=user_id)
            cartitems = CartItems.objects.filter(cart_id=cart_id)
            orderitems = [OrderItem(order=order, product=item.product, quantity=item.quantity)for item in cartitems]
            OrderItem.objects.bulk_create(orderitems)
            Cart.objects.filter(id=cart_id).delete()

