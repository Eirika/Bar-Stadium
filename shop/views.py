#-*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

from shop.models import Produit


def home(request):
    text = """
        <h1>Bienvenue sur mon blog !</h1>
        <p>Les crêpes bretonnes ça tue des mouettes en plein vol !</p>
        """
    return HttpResponse(text)


def produits(request):
    produits = Produit.objects.all()
    return render(request, 'index.html', locals())
