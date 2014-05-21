#-*- coding: utf-8 -*-

from django.shortcuts import render

from shop.models import Produit, Boisson, Glace


def home(request):
    return render(request, 'index2.html')


def produits(request):
    produits = Produit.objects.all()
    return render(request, 'boutique.html', locals())


def boissons(request):
    produits = Boisson.objects.all()
    return render(request, 'boutique.html', locals())


def glaces(request):
    produits = Glace.objects.all()
    return render(request, 'boutique.html', locals())
