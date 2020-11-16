import requests
from .models import CatFact
from django.http import HttpResponse


def get_cat_fact(r):
    resp = requests.get('https://catfact.ninja/fact').json()
    fact = resp['fact']
    CatFact(fact=fact).save()
    return HttpResponse('ok')
