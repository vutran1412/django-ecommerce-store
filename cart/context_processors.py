from .models import Cart, CartItem
from .views import _cart_id

# function to count all the items in the shopping cart
def counter(request):
	item_count = 0
	# return an empty dict if admin is the request path
	if 'admin' in request.path:
		return {}
	else:
		try:
			# get the cart and and cart item object
			cart = Cart.objects.filter(cart_id=_cart_id(request))
			cart_items = CartItem.objects.all().filter(cart=cart[:1])
			# loop over the cart items and count the number of items in the cart
			for cart_item in cart_items:
				item_count += cart_item.quantity
		except Cart.DoesNotExist:
			item_count = 0
	return dict(item_count = item_count)