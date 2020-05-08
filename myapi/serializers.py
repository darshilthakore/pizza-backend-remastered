from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Item, Cart, Topping, Order, CartItem
from rest_framework.authtoken.models import Token

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class ToppingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topping
        fields = ['id', 'name', 'rate']

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'category', 'price_small', 'price_large']


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'name', 'baseprice', 'topping', 'extraprice', 'quantity', 'total']

class CartSerializer(serializers.ModelSerializer):
    cartitems = CartItemSerializer(many=True)
    
    class Meta:
        model = Cart
        fields = ['id', 'user', 'cartitems', 'grand_total']


    def create(self, validated_data):
        cartitems_data = validated_data.pop('cartitems')
        cart = Cart.objects.create(**validated_data)
        for cartitem_data in cartitems_data:
            CartItem.objects.create(cart=cart, **cartitem_data)
        return cart


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['customer', 'item', 'topping', 'base_price', 'grand_total', 'status']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        Cart.objects.create(user=user.username)
        return user