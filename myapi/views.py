from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth.models import User

from .serializers import CategorySerializer, ToppingSerializer, ItemSerializer, CartSerializer, OrderSerializer, UserSerializer
from .models import Category, Item, Cart, Topping, Order
# Create your views here.


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer