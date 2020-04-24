from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Item, Cart, Topping, Order

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class ToppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topping
        fields = ['name', 'rate']

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['name', 'category', 'price_small', 'price_large']

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['user', 'item', 'topping', 'base_price', 'grand_total']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['customer', 'item', 'topping', 'base_price', 'grand_total', 'status']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
