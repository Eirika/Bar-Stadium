#-*- coding: utf-8 -*-

from django.shortcuts import render
from shop.models import Produit, Boisson, Glace, Commande, LigneCom
from django.contrib.auth import authenticate, login
from shop.forms import ConnexionForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'index2.html')


@login_required
def produits(request):
    produits = Produit.objects.all()
    return render(request, 'boutique.html', locals())


@login_required
def boissons(request):
    produits = Boisson.objects.all()
    if request.method == "POST":
            idBoisson = request.POST.get("theId", False)
            commande = Commande(request.user.loge.pk)
            commande.save()

            ligneCom = LigneCom(commande=commande, produit=Produit.objects.get(pk=idBoisson))
            ligneCom.save()

            return render(request, "boutique.html", locals())
    return render(request, 'boutique.html', locals())


@login_required
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
                return render(request, 'index2.html', locals())
            else:  # sinon une erreur sera affichée
                error = True
    else:
        form = ConnexionForm()
    return render(request, 'connexion.html', locals())

                                                                                            
def deconnexion(request):
    logout(request)
    return render(request, 'index2.html')
