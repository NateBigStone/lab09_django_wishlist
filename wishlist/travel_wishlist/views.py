from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


@login_required()
def place_list(r):
    if r.method == 'POST':
        form = NewPlaceForm(r.POST)
        place = form.save(commit=False)
        place.user = r.user
        if form.is_valid():
            place.save()
            return redirect('place_list')

    places = Place.objects.filter(user=r.user).filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()
    return render(r, 'travel_wishlist/wishlist.html', {'places': places, 'new_place_form': new_place_form})


@login_required()
def places_visited(r):
    visited = Place.objects.filter(visited=True)
    return render(r, 'travel_wishlist/visited.html', {'visited': visited})


@login_required()
def place_was_visited(r, place_pk):
    if r.method == 'POST':
        place = get_object_or_404(Place, pk=place_pk)
        if place.user == r.user:
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden()
    return redirect('place_list')


@login_required()
def about(r):
    author = 'Nate'
    about = 'A website to create a list of places to visit'
    return render(r, 'travel_wishlist/about.html', {'author': author, 'about': about})


@login_required()
def place_details(r, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    return render(r, 'travel_wishlist/place_detail.html', {'place': place})


@login_required()
def delete_place(r, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == r.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden()


