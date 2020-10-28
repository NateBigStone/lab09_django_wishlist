from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm


def place_list(r):
    if r.method == 'POST':
        form = NewPlaceForm(r.POST)
        place = form.save()
        if form.is_valid():
            place.save()
            return redirect('place_list')

    places = Place.objects.filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()
    return render(r, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})


def places_visited(r):
    visited = Place.objects.filter(visited=True)
    return render(r, 'travel_wishlist/visited.html', {'visited': visited})


def place_was_visited(r, place_pk):
    if r.method == 'POST':
        place = get_object_or_404(Place, pk=place_pk)
        place.visited = True
        place.save()
    return redirect('place_list')


def about(r):
    author = 'Nate'
    about = 'A website to create a list of places to visit'
    return render(r, 'travel_wishlist/about.html', {'author': author, 'about': about})
