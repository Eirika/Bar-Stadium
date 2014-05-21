#-*- coding: utf-8 -*-

from django.shortcuts import render

from shop.models import Produit


def home(request):
    return render(request, 'index2.html')


def produits(request):
    produits = Produit.objects.all()
    return render(request, 'boutique.html', locals())
