from django.db import models

# Create your models here.
class Topping(models.Model):
	name = models.CharField(max_length=64)
	rate = models.FloatField()

	def __str__(self):
		return f"{self.name}"

class Category(models.Model):
	name = models.CharField(max_length=64, primary_key=True)

	def __str__(self):
		return f"{self.name}"

class Item(models.Model):
	name = models.CharField(max_length=64)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="itemname")
	price_small = models.FloatField(default=0)
	price_large = models.FloatField(default=0)

	def __str__(self):
		return f"{self.category} - {self.name} | Small : ${self.price_small} | Large : ${self.price_large}"


class Cart(models.Model):
	user = models.CharField(max_length=64)
	item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="cartitem")
	topping = models.ManyToManyField(Topping, blank=True, related_name="carttopping")
	base_price = models.FloatField(default=0)
	grand_total = models.FloatField(default=0)

	def __str__(self):
		return f"Cart | {self.user} | {self.item.name}"


class Order(models.Model):
	customer = models.CharField(max_length=64)
	item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="orderitem")
	topping = models.ManyToManyField(Topping, blank=True, related_name="ordertopping")
	base_price = models.FloatField(default=0)
	grand_total = models.FloatField(default=0)
	status = models.CharField(max_length=64, default="Waiting for Confirmation")

	def __str__(self):
		return f"Order | {self.customer} | {self.item.name}"