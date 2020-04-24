from django.contrib import admin

# Register your models here.
from .models import Category, Item, Cart, Topping, Order


def order_confirmation(modeladmin, request, queryset):
	queryset.update(status="Order Confirmed")

order_confirmation.short_description = "Confirm the selected orders"

class OrderAdmin(admin.ModelAdmin):
	list_display = ['customer', 'item', 'grand_total', 'status']
	actions = [order_confirmation]

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Cart)
admin.site.register(Topping)
admin.site.register(Order, OrderAdmin)