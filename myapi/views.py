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
        cart.save()

        topping_serialized = ToppingSerializer(cartitem.topping)

        serializer = CartItemSerializer(cartitem)
        # cartitem = CartItem.objects.create(name=request.data['name'],baseprice=request.data["baseprice"])
        # serial = CartItemSerializer(cartitem)
        return Response(serializer.data)

    @action(detail=True, methods=['put'])
    def deletequantity(self, request, pk=None):
        print(request.data)
        cart = Cart.objects.get(id=pk)
        cartitem = CartItem.objects.get(id=request.data)
        if (cartitem.quantity <= 1):
            cartitem.delete()
            cart.grand_total = 0
            for item in cart.cartitems.all():
                cart.grand_total += item.total

            cart.save()

            return Response(None)
        cartitem.quantity -= 1
        cartitem.total = (cartitem.baseprice + cartitem.extraprice)*cartitem.quantity
        cartitem.save()
        print(cartitem.quantity)
        cart.grand_total = 0
        for item in cart.cartitems.all():
            cart.grand_total += item.total

        
        cart.save()
        return Response(None)

    @action(detail=True, methods=['put'])
    def addquantity(self, request, pk=None):
        print(request.data)
        cart = Cart.objects.get(id=pk)
        cartitem = CartItem.objects.get(id=request.data)
        cartitem.quantity += 1

        cartitem.total = (cartitem.baseprice + cartitem.extraprice)*(cartitem.quantity)
        print(cartitem.quantity) 

        cart.grand_total = 0
        for item in cart.cartitems.all():
            cart.grand_total += item.total

        # cart.grand_total += (cartitem.baseprice + cartitem.extraprice)
        cart.save()
        
        cartitem.save()

        return Response(None)   

    

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