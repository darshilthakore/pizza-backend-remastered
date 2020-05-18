from django.urls import path
from rest_framework import routers
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import include

from . import views

router = routers.DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'items', views.ItemViewSet)
router.register(r'toppings', views.ToppingViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'carts', views.CartViewSet)
# router.register(r'cartitems', views.CartItemViewSet)

urlpatterns = [
    # path('checkout/', csrf_exempt(views.checkout), name='checkout'),
    path('', include(router.urls)),
]

