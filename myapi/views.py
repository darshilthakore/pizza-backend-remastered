from django.shortcuts import render
from django.views.generic import TemplateView

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from django.contrib.auth.models import User
import stripe
stripe.api_key = "sk_test_BxiB7UMirS3oOu638rkFU01z00flaseLYK"

from .serializers import CategorySerializer, ToppingSerializer, ItemSerializer, CartSerializer, OrderSerializer, UserSerializer, CartItemSerializer
from .models import Category, Item, Cart, Topping, Order, CartItem
# Create your views here.



class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'index.html', context=None)

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
        cartitem.save()
        cart.grand_total = 0
        for item in cart.cartitems.all():
            cart.grand_total += item.total

        # cart.grand_total += (cartitem.baseprice + cartitem.extraprice)
        cart.save()
        
        

        return Response(None) 
    
    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        print(f"reques data is {request.data}")
        cart = Cart.objects.get(id=pk)
        items = cart.cartitems.all()
        
        line_items = []
        for item in items:
            line_items.append({
                'name': item.name,
                'quantity': item.quantity,
                'currency': 'inr',
                'amount': int(item.total * 100),
            })


        print("inside checkout req")
        
        chk_ses = stripe.checkout.Session.create(
            success_url = 'http://localhost:4200/checkout?session_id={CHECKOUT_SESSION_ID}',
            cancel_url = 'http://localhost:4200/checkout',
            payment_method_types = ['card'],
            line_items = line_items,
            
            # shipping_address_collection = request.data['address']
            # line_items = [
            #     {
            #         'name': 'test',
            #         'quantity': 1,
            #         'currency': 'inr',
            #         'amount': 120,
            #     },
            #     {
            #         'name': 'test 2',
            #         'quantity': 3,
            #         'currency': 'inr',
            #         'amount': 120,
            #     }
            # ],
            mode = 'payment',
            shipping_address_collection = None,
        )

        print(f"chk ses is : {chk_ses}")
        return Response(chk_ses)


        
          

    

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

# class CartSerializer(viewsets.ModelViewSet):
#     queryset = Cart.objects.filter(user = request.user)
#     serializer_class = CartSerializer

# class CheckOutViewSet(viewsets.ViewSet):

#     @action(detail=True, methods=['post'])
#     def checkout(self, request):

#         print("inside checkout req")
#         print(f"address is {request.data['address']}")
#         chk_ses = stripe.checkout.Session.create(
#             success_url = 'http://localhost:4200/success?session_id={CHECKOUT_SESSION_ID}',
#             cancel_url = 'http://localhost:4200/checkout',
#             payment_method_types = ['card'],

#             # shipping_address_collection = request.data['address']
#             line_items = [
#                 {
#                     'name': 'test',
#                     'quantity': 1,
#                     'currency': 'usd',
#                     'amount': 120,
#                 },
#                 {
#                     'name': 'test 2',
#                     'quantity': 3,
#                     'currency': 'usd',
#                     'amount': 120,
#                 }
#             ],
#             mode = 'payment',
#         )

#         print(f"chk ses is : {chk_ses}")
#         return Response(chk_ses)



# To do
# class OrderViewSet


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (AllowAny, )

    