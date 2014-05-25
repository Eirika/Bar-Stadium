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
    return render(request, 'index.html')


@login_required  # Signifie qu'un utilisateur doit être authentifié et connecté pour acceder à cette vue
def produits(request):
    #On récupère tous nos produit et la commande en cours s'il y en une
    produits = Produit.objects.all()
    commandeExistante = updatePanier(request)
    #on spécifie à notre template que nous affichons toute la boutique
    location = "boutique"

    return render(request, 'boutique.html', locals())


@login_required
def boissons(request):
    #On récupère les boissons et la commande en cours s'il y en une
    produits = Boisson.objects.all()
    commandeExistante = updatePanier(request)
    #on spécifie à notre template que nous affichons seulement les boissons
    location = "boissons"

    return render(request, 'boutique.html', locals())


@login_required
def glaces(request):
    #On récupère les glaces et la commande en cours s'il y en une
    produits = Glace.objects.all()
    commandeExistante = updatePanier(request)
    #on spécifie à notre template que nous affichons seulement les glaces
    location = "glaces"

    return render(request, 'boutique.html', locals())


@login_required
def gestionService(request):
    if request.method == "POST" and request.POST.get('laCommande'):  # si on a envoyé un formulaire et que l'id de la commande est bien présente
        idCommande = int(request.POST.get('laCommande'))  # on récupère cet id
        laCommande = Commande.objects.get(pk=idCommande)    # On récupère la commande associé
        laCommande.servie = True                            # on indique quelle est servie
        laCommande.save()                                   # on met à jour la base de donnée

    commandes = Commande.objects.exclude(servie=True)       # on rafraichie notre liste de commande sans celle déjà servie

    #on vérifie ici les commandes non validé et les détruisons si aucun article n'a été ajouté depuis plus de 20 minutes
    commandeNonValidee = commandes.exclude(validee=True)
    for commandeExistante in commandeNonValidee:
        if commandeExistante.date + datetime.timedelta(minutes=20) < timezone.now():
            commandeExistante.delete()

    return render(request, 'serveur.html', locals())


def updatePanier(request):
    #On récupère la commande existante associé a la loge connecté,
    # par mesure de sécurité, on n'execute pas de requete en base de donnée si l'utilisateur connecté n'a pas de loge associé
    try:
        if request.user.loge:
            commandeExistante = Commande.objects.exclude(validee=True).exclude(servie=True).filter(loge=request.user.loge).first()
    except ObjectDoesNotExist:
        pass

    if request.method == "POST":
        if request.POST.get('addPanier'):  # Si la soumission de formulaire est un ajout au panier
            idProduit = int(request.POST.get('leProduit', False))  # on récupère le produit concerné
            quantite = int(request.POST.get('quantite', 1))         # ainsi que la quantité

            produit_existant = False
            commandeExistante = Commande.objects.exclude(validee=True).exclude(servie=True).filter(loge=request.user.loge).first()
            # si il existe une commande pour cette loge, on verifie que le produit ajouté n'est pas déjà présent dans la commande
            # si tel est le cas, on se contente de mettre a jour la quantité
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
            # si le formulaire est une validation, on valide la commande existante et la sauvegarde
            if request.POST.get('validerCommande'):
                commandeExistante = Commande.objects.exclude(validee=True).exclude(servie=True).filter(loge=request.user.loge).first()
                commandeExistante.validee = True
                commandeExistante.save()

    return commandeExistante


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
                return render(request, 'index.html', locals())
            else:  # sinon une erreur sera affichée
                error = True
    else:
        form = ConnexionForm()
    return render(request, 'connexion.html', locals())


def deconnexion(request):
    logout(request)
    return render(request, 'index.html')
