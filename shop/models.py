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


class LigneCom(models.Model):
    quantite = models.IntegerField(default=1)
    produit = models.ForeignKey(Produit)
    commande = models.ForeignKey(Commande)

    #Overriding
    def save(self, *args, **kwargs):
        commandeExistante = Commande.objects.exclude(servie=True).exclude(validee=True).filter(**kwargs).first()
        if not commandeExistante:
            commande = Commande(**kwargs)
            commande.save()
            self.commande = commande
        else:
            self.commande = commandeExistante
            self.commande.date = timezone.now()
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
