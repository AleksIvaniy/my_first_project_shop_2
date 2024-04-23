from rest_framework.serializers import ModelSerializer
from .models import *
from django.contrib.auth.models import User

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

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