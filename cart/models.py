from django.db import models
from store.models import Product

# Cart model 
class Cart(models.Model):
	cart_id = models.CharField(max_length=250, blank=True)
	date_added = models.DateField(auto_now_add=True)

	# meta class 
	class Meta:
		db_table = 'Cart'
		ordering = ['date_added']

	def __str__(self):
		return self.cart_id

# Cart item model
class CartItem(models.Model):
	# cart item has two foreign keys, product and cart
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
	quantity = models.IntegerField()
	active = models.BooleanField(default=True)

	# meta class
	class Meta:
		db_table = 'CartItem'

	def sub_total(self):
		return self.product.price * self.quantity

	def __str__(self):
		return self.product