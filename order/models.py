from django.db import models

# the order db model, with all of the customer information
class Order(models.Model):
	token = models.CharField(max_length=250, blank=True)
	total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='USD Order Total')
	email_address = models.EmailField(max_length=250, blank=True, verbose_name='Email Address')
	created = models.DateTimeField(auto_now_add=True)
	billing_name = models.CharField(max_length=250, blank=True)
	billing_address1 = models.CharField(max_length=250, blank=True)
	billing_city = models.CharField(max_length=250, blank=True)
	billing_postcode = models.CharField(max_length=10, blank=True)
	billing_country = models.CharField(max_length=200, blank=True)
	shipping_name = models.CharField(max_length=250, blank=True)
	shipping_address1 = models.CharField(max_length=250, blank=True)
	shipping_city = models.CharField(max_length=250, blank=True)
	shipping_postcode = models.CharField(max_length=10, blank=True)
	shipping_country = models.CharField(max_length=200, blank=True)

	class Meta:
		db_table = 'Order'

	def __str__(self):
		return str(self.id)

# the order item db model containing all of the order item information
class OrderItem(models.Model):
	product = models.CharField(max_length=250)
	quantity = models.IntegerField()
	price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='USD Price')
	order = models.ForeignKey(Order, on_delete=models.CASCADE)

	class Meta:
		db_table = 'OrderItem'

	def sub_total(self):
		return self.quantity * self.price

	def __str__(self):
		return self.product
