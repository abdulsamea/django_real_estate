from django.shortcuts import get_object_or_404, render
from .models import Listing
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import bedroom_choices, price_choices, state_choices


# Create your views here.
def index(request):
   listings = Listing.objects.order_by('-list_date').filter(is_published = True)

   paginator = Paginator(listings, 2)
   page = request.GET.get('page')
   paged_listings = paginator.get_page(page)


   context = {
      'listings' : paged_listings
   }

   return render(request, 'listings/listings.html', context)

def listing(request, listing_id):
   listing = get_object_or_404(Listing, pk=listing_id)

   context = {
      'listing' : listing
   }

   return render(request, 'listings/listing.html', context)

def search(request):

   search_listings = Listing.objects.order_by('-list_date').filter(is_published = True)

   # match keywords
   if 'keywords' in request.GET:
      keywords  = request.GET['keywords']
      if 'keywords' and len(keywords) > 0 :
         search_listings = search_listings.filter(description__icontains = keywords)


   # city
   if 'city' in request.GET:
      city  = request.GET['city']
      if 'city' and len(city) > 0 :
         search_listings = search_listings.filter(city__iexact = city)
   

   #state
   if 'state' in request.GET:
      state  = request.GET['state']
      if 'state' and len(state) > 0 :
         search_listings = search_listings.filter(state__iexact = state)
   
   #bedrooms
   if 'bedrooms' in request.GET:
      bedrooms  = request.GET['bedrooms']
      if 'bedrooms' and len(bedrooms) > 0 :
         search_listings = search_listings.filter(bedrooms__lte = bedrooms)
   
   
   #price
   if 'price' in request.GET:
      price  = request.GET['price']
      if 'price' and len(price) > 0 :
         search_listings = search_listings.filter(price__lte = price)
   

   paginator = Paginator(search_listings, 6)
   page = request.GET.get('page')
   search_listings = paginator.get_page(page)
   
   context = {
        'listings' : search_listings,
        'bedroom_choices' : bedroom_choices,
        'state_choices' : state_choices,
        'price_choices' : price_choices,
        'values' : request.GET
   }
   return render(request, 'listings/search.html', context)