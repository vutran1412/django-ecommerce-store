from django.shortcuts import render
from store.models import Product
from django.db.models import Q

# search product function
def searchResult(request):
	products = None
	query = None
	# if product contains the marker
	if 'q' in request.GET:
		# query using the marker
		query = request.GET.get('q')
		# return all the product containing the query by name and description
		products = Product.objects.all().filter(Q(name__contains=query) | Q(description__contains=query))
	return render(request, 'search.html', {'query': query, 'products': products})


