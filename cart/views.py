from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product
from .models import Cart, CartItem
from django.conf import settings
import stripe
from order.models import Order, OrderItem

# generate a shopping cart id
def _cart_id(request):
    # request the current seesion key
    cart = request.session.session_key
    # if there is none
    if not cart:
        # create a new session
        cart = request.session.create()
    # return cart id
    return cart

# add item to cart and create the shopping cart
def add_cart(request, product_id):
    # query the product object by id
    product = Product.objects.get(id=product_id)
    try:
        # query the cart object by cart id 
        cart = Cart.objects.get(cart_id=_cart_id(request))
    # if cart doesn't exist    
    except Cart.DoesNotExist:
        # create a new cart and save cart
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
        cart.save()
    try:
        # query to get the item in the cart
        cart_item = CartItem.objects.get(product=product, cart=cart)
        # add item to cart if the quantity in cart is less than the stock quantity
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
        # save created cart item to cart
        cart_item.save()
    # if the cartitem doesn't exists then create a new one
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
        # save the created cart item
        cart_item.save()
    # redirect to the cart detail url path
    return redirect('cart:cart_detail')

# the cart detail handles the requests and functions of the cart
def cart_detail(request, total=0, counter=0, cart_items=None):
    try:
        # query by cart by cart id
        cart = Cart.objects.get(cart_id=_cart_id(request))
        # query the cart items in cart
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        # loop through all the cart_items list and calculate the total and quantity
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass
    # https://stripe.com/docs/api/
    # get the sripe API secret key from the settings file
    stripe.api_key = settings.STRIPE_SECRET_KEY
    # initilize the stripe_total since the smallest unit is a cent
    stripe_total = int(total * 100)
    description = 'Finer Things - New Order'
    # the data key will be the stripe's publishable key from the settings file
    data_key = settings.STRIPE_PUBLISHABLE_KEY
    if request.method == 'POST':
        try:
            # the post request is used to create the customer token and a new charge
            token = request.POST['stripeToken']
            email = request.POST['stripeEmail']
            billing_name = request.POST['stripeBillingName']
            billing_address1 = request.POST['stripeBillingAddressLine1']
            billing_city = request.POST['stripeBillingAddressCity']
            billing_postcode = request.POST['stripeBillingAddressZip']
            billing_country = request.POST['stripeBillingAddressCountryCode']
            shipping_name = request.POST['stripeShippingName']
            shipping_address1 = request.POST['stripeShippingAddressLine1']
            shipping_city = request.POST['stripeShippingAddressCity']
            shipping_postcode = request.POST['stripeShippingAddressZip']
            shipping_country = request.POST['stripeShippingAddressCountryCode']
            # create a new customer
            customer = stripe.Customer.create(
                email=email,
                source=token
                )
            # create a new charge
            charge = stripe.Charge.create(
                amount=stripe_total,
                currency="usd",
                description=description,
                customer=customer.id)
            # create the new order
            try:
                order_details = Order.objects.create(
                        token = token,
                        total = total,
                        email_address = email,
                        billing_name = billing_name,
                        billing_address1 = billing_address1,
                        billing_city = billing_city,
                        billing_postcode = billing_postcode,
                        billing_country = billing_country,
                        shipping_name = shipping_name,
                        shipping_address1 = shipping_address1,
                        shipping_city = shipping_city,
                        shipping_postcode = shipping_postcode,
                        shipping_country = shipping_country
                    )
                order_details.save()
                # create the order items for every item currently in the cart
                for order_item in cart_items:
                    oi = OrderItem.objects.create(
                            product = order_item.product.name,
                            quantity = order_item.quantity,
                            price = order_item.product.price,
                            order = order_details
                        )
                    oi.save()
                    # reduce stock when order is placed or saved
                    products = Product.objects.get(id=order_item.product.id)
                    products.stock = int(order_item.product.stock - order_item.quantity)
                    products.save()
                    order_item.delete()
                    # the terminal will print this message when the order is saved
                    print('The order has been created')
                return redirect('store:allProdCat')
            except ObjectDoesNotExist:
                pass
        # catches any card errors, invalid cc number, expiration date, etc
        except stripe.error.CardError as e:
            return False, e
    # renders the template using the request and a dictionary as context
    return render(request, 'cart.html', dict(cart_items=cart_items, total=total, counter=counter, data_key=data_key,
                                             stripe_total=stripe_total, description=description))

# this function handles the removing of items from cart one item at a time
def cart_remove(request, product_id):
    # get the cart, product, and cart item
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    # if cart item is still greater than 1 then continue to remove on at a time
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        # save the status of the current item
        cart_item.save()
    # if less than one, then delete the item from cart
    else:
        cart_item.delete()
    # redirect to the cart detail url path
    return redirect('cart:cart_detail')

# this function handle the complete removal of an item in the cart
def full_remove(request, product_id):
    # get the cart, product, and cart item
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    # delete the cart_item completely
    cart_item.delete()
    # redirect to the cart detail url path
    return redirect('cart:cart_detail')
