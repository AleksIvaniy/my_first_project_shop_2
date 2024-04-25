from rest_framework.serializers import ModelSerializer, StringRelatedField
from .models import *
from django.contrib.auth.models import User

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    category = CategorySerializer()
    # brand = StringRelatedField()
    # color = StringRelatedField()


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