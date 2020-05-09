from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from django.contrib.auth.models import User


from .serializers import CategorySerializer, ToppingSerializer, ItemSerializer, CartSerializer, OrderSerializer, UserSerializer, CartItemSerializer
from .models import Category, Item, Cart, Topping, Order, CartItem
# Create your views here.


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

class ToppingViewSet(viewsets.ModelViewSet):
    queryset = Topping.objects.all()
    serializer_class = ToppingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def update(self, request, pk=None):
        cart = Cart.objects.get(id=pk)
        # serializer = CartSerializer(cart)
        toppings = request.data['toppings']
        # topping_serialized = ToppingSerializer(toppings, many=True)
        cartitem = CartItem.objects.create(cart=cart)
        cartitem.name = request.data['name']
        cartitem.baseprice = request.data['baseprice']
        # cartitem.topping.add(topping_serialized.data)
        cartitem.extraprice = request.data['extraprice']
        cartitem.quantity = request.data['quantity']
        cartitem.total = request.data['total']
        cartitem.save()

        for t in toppings:
            topping = Topping.objects.get(pk=t['id'])
            print(f"topping {topping}")
            cartitem.topping.add(topping)

        cart.grand_total += cartitem.total

        topping_serialized = ToppingSerializer(cartitem.topping)

        serializer = CartItemSerializer(cartitem)
        # cartitem = CartItem.objects.create(name=request.data['name'],baseprice=request.data["baseprice"])
        # serial = CartItemSerializer(cartitem)
        return Response(serializer.data)

    

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

# class CartSerializer(viewsets.ModelViewSet):
#     queryset = Cart.objects.filter(user = request.user)
#     serializer_class = CartSerializer



# To do
# class OrderViewSet


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )