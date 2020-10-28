from django.shortcuts import render
from .models import Place


def place_list(r):
    places = Place.objects.all()
    return render(r, 'travel_wishlist/wishlist.html', {'places': places})
