#-*- coding: utf-8 -*-

from django.shortcuts import render
from shop.models import Produit, Boisson, Glace, Commande, LigneCom
from django.contrib.auth import authenticate, login
from shop.forms import ConnexionForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import datetime
from django.core.exceptions import ObjectDoesNotExist


def home(request):
    return render(request, 'index2.html')


@login_required
def produits(request):
    produits = Produit.objects.all()
    updatePanier(request)

    try:
        if request.user.loge:
            commandeExistante = Commande.objects.exclude(validee=True).exclude(servie=True).filter(loge=request.user.loge).first()
    except ObjectDoesNotExist:
        pass

    return render(request, 'boutique.html', locals())


@login_required
def boissons(request):
    produits = Boisson.objects.all()
    updatePanier(request)

    try:
        if request.user.loge:
            commandeExistante = Commande.objects.exclude(validee=True).exclude(servie=True).filter(loge=request.user.loge).first()
    except ObjectDoesNotExist:
        pass

    return render(request, 'boutique.html', locals())


@login_required
def glaces(request):
    produits = Glace.objects.all()
    updatePanier(request)

    try:
        if request.user.loge:
            commandeExistante = Commande.objects.exclude(validee=True).exclude(servie=True).filter(loge=request.user.loge).first()
    except ObjectDoesNotExist:
        pass

    return render(request, 'boutique.html', locals())


@login_required
def gestionService(request):
    if request.method == "POST" and request.POST.get('commandeServie'):
        idCommande = int(request.POST.get('commandeServie'))
        laCommande = Commande.objects.get(pk=idCommande)
        laCommande.servie = True
        laCommande.save()

    commandes = Commande.objects.exclude(servie=True)

    commandeNonValidee = commandes.exclude(validee=True)
    for commandeExistante in commandeNonValidee:
        if commandeExistante.date + datetime.timedelta(minutes=20) < timezone.now():
            commandeExistante.delete()

    return render(request, 'serveur.html', locals())


def updatePanier(request):
    if request.method == "POST":
        if request.POST.get('addPanier'):
            idProduit = int(request.POST.get('leProduit', False))
            quantite = int(request.POST.get('quantite', 1))

            produit_existant = False
            commandeExistante = Commande.objects.exclude(validee=True).exclude(servie=True).filter(loge=request.user.loge).first()
            if commandeExistante:
                for ligneCom in commandeExistante.lignecom_set.all():
                    if ligneCom.produit.pk == idProduit:
                        ligneCom.quantite += quantite
                        ligneCom.save(loge=request.user.loge)
                        produit_existant = True
            if not produit_existant:
                ligneCom = LigneCom(produit=Produit.objects.get(pk=idProduit), quantite=quantite)
                ligneCom.save(loge=request.user.loge)
        else:
            if request.POST.get('validerCommande'):
                commandeExistante = Commande.objects.exclude(validee=True).exclude(servie=True).filter(loge=request.user.loge).first()
                commandeExistante.validee = True
                commandeExistante.save()


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
