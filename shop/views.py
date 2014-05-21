#-*- coding: utf-8 -*-

from django.shortcuts import render
from shop.models import Produit, Boisson, Glace
from django.contrib.auth import authenticate, login
from shop.forms import ConnexionForm
from django.contrib.auth import logout


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


def connexion(request):
    error = False

    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]  # Nous récupérons le nom d'utilisateur
            password = form.cleaned_data["password"]  # … et le mot de passe
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
            else:  # sinon une erreur sera affichée
                error = True
    else:
        form = ConnexionForm()
    return render(request, 'connexion.html', locals())

                                                                                            
def deconnexion(request):
    logout(request)
    return render(request, 'index2.html')
