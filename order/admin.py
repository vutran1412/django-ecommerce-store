from django.contrib import admin
from .models import Order, OrderItem

# configure the order admin and and field sets
class OrderItemAdmin(admin.TabularInline):
	model = OrderItem
	fieldsets = [
	('Product',{'fields':['product'],}),
	('Quantity',{'fields':['quantity'],}),
	('Price',{'fields':['price'],}),
	]
	# read only fields
	readonly_fields = ['product','quantity','price']
	can_delete= False
	max_num = 0
	template = 'admin/order/tabular.html'

# register the admin
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

	list_display = ['id','billing_name','email_address','created']
	list_display_links = ('id','billing_name')
	# searchable
	search_fields = ['id','billing_name','email_address']
	readonly_fields = ['id','token','total','email_address','created','billing_name','billing_address1','billing_city',
					'billing_postcode','billing_country','shipping_name','shipping_address1','shipping_city','shipping_postcode','shipping_country']
	fieldsets = [
	('ORDER INFORMATION',{'fields': ['id','token','total','created']}),
	('BILLING INFORMATION', {'fields': ['billing_name','billing_address1','billing_city','billing_postcode','billing_country','email_address']}),
	('SHIPPING INFORMATION', {'fields': ['shipping_name','shipping_address1','shipping_city','shipping_postcode','shipping_country']}),
	]
	
	inlines = [
		OrderItemAdmin,
	]

	def has_delete_permission(self, request, obj=None):
		return False

	def has_add_permission(self, request):
		return False