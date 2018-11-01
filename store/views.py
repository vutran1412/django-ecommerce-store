from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Category, Product
from django.core.paginator import Paginator, EmptyPage, InvalidPage


def index(request):
	text_var = 'This is my first django web page.'
	return HttpResponse(text_var)

# Category view
def allProdCat(request, c_slug=None):
	c_page = None
	products_list = None
	# if the category slug is not none
	if c_slug is not None:
		# get the category page or return 404
		c_page = get_object_or_404(Category, slug=c_slug)
		# query the product list by category
		products_list = Product.objects.filter(category=c_page, available=True)
	else:
		# query all the available products
		products_list = Product.objects.all().filter(available=True)
	# paginate to only include 3 products per page
	paginator = Paginator(products_list, 3)
	try:
		page = int(request.GET.get('page', '1'))
	except:
		page = 1
	try:
		products = paginator.page(page)
	except (EmptyPage, InvalidPage):
		products = paginator.page(paginator.num_pages)
	# render the request, the template, and the paginated products context
	return render(request, 'store/category.html', {'category': c_page, 'products': products})

# product detail view
def ProdCatDetail(request, c_slug, product_slug):
	try:
		product = Product.objects.get(category__slug=c_slug, slug=product_slug)
	except Exception as e:
		raise e
	return render(request, 'store/product.html', {'product': product,})