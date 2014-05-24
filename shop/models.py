# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Ingredient(models.Model):
    libelle = models.CharField(max_length=50)

    def __unicode__(self):
        return self.libelle


class Produit(models.Model):
    nom = models.CharField(max_length=50)
    description = models.TextField()
    prix = models.FloatField()
    urlImg = models.TextField(null=True, blank=True)
    ingredients = models.ManyToManyField(Ingredient)

    def __unicode__(self):
        return self.nom


class Boisson(Produit):
    degre = models.IntegerField(default=0)
    alcool = models.BooleanField(default=False, editable=False)

    #Overriding
    def save(self, *args, **kwargs):
        if self.degre > 0:
            self.alcool = True
        super(Boisson, self).save(*args, **kwargs)

    def __unicode__(self):
            return self.nom


class Glace(Produit):
    pass


class Commande(models.Model):
    prixTTC = models.FloatField(default=0, null=True, blank=True)
    prixHT = models.FloatField(default=0, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    serveur = models.ForeignKey('Serveur', null=True, blank=True)
    loge = models.ForeignKey('Loge')
    produit = models.ManyToManyField(Produit, through='LigneCom')
    validee = models.BooleanField(default=False)
    servie = models.BooleanField(default=False)

# on est d'accord qu'il nous faut une vue pour les serveurs. Sur laquelle ils verront les commandes qu'ils doivent faire.
# je propose un truc :
# Sur cette vue, en auto refresh toutes les x secondes, on voit en rouge les commandes non servies et non validées (permet de suivre en temps réel les commandes)
# En vert les commandes non servies et validées
# a coté des commandes en vert s'affiche un bouton "Servie"
# dès qu'on clique dessus, commande.servie=true
# ca, c'est juste pour le swag.

# --option 2 : tu restes en mode "finie", et le serveur se fait niquer le temps de préparation/service
# option 3: pareil que la 1, mais tu oublies l'histoire d'afficher en temps réel les commandes en train d'être commandées

# dernière étape: tu t'entraineras à présenter le projet, tu implémentes vraiment beaucoup de petits détails qui tuent et filent des points :D

# fais moi penser à te presenter le fichier settings.py. Tu y as pas touché et s'il modifie un truc ici tu seras dans le caca si tu sais pas de quoi il parle :p

#bisous #coeur #hashtag


class LigneCom(models.Model):
    quantite = models.IntegerField(default=1)
    produit = models.ForeignKey(Produit)
    commande = models.ForeignKey(Commande)

# Il faut tester ca maintenant ! :p Enfin un vrai test :) (voir même faire plusieurs test pour tester cette grosse fonction)
    #Overriding
    def save(self, *args, **kwargs):
        commandeExistante = Commande.objects.exclude(servie=True).exclude(validee=True).filter(**kwargs).first()
        if not commandeExistante:
            commande = Commande(**kwargs)
            self.commande = commande
            self.commande.save()
            print "NEW COMMANDE"
            # self.commande est forcément null à la création d'une nouvelle LigneCom. Il faut regarder s'il y a une commande active dans cette loge
            # Un kwarg est déjà un couple clé=valeur. **kwargs une sorte de liste de kwarg. kwarg veut probablement dire key with argument
        else:
            if self.commande != commandeExistante:
                self.commande = commandeExistante
                self.commande.date = timezone.now()
                print "OLD COMMANDE"
        self.commande.prixTTC += self.quantite * self.produit.prix
        self.commande.prixHT = round(self.commande.prixTTC * 0.90, 2)
        self.commande.save()

        super(LigneCom, self).save()


class Serveur(models.Model):
    class Meta:
        unique_together = (("nom", "prenom", "dateNaissance"),)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    dateNaissance = models.DateField()
    adresse = models.CharField(max_length=200)
    ville = models.CharField(max_length=200)
    codePostal = models.CharField(max_length=5)
    tauxCommission = models.FloatField()

    def get_commissions(self):
        commissions = 0
        commandes = self.commande_set.filter(validee=True, servie=True)
        for commande in commandes:
            commissions += commande.prixTTC * self.tauxCommission / 100
        return commissions

    def __unicode__(self):
        return "%s - %s" % (self.nom, self.prenom)


class Loge(models.Model):
    user = models.OneToOneField(User)
    libelle = models.CharField(max_length=50)

    def __unicode__(self):
        return self.libelle


from shop.signals import *
