# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Count


class Ingredient(models.Model):
    libelle = models.CharField(max_length=50)

    def __unicode__(self):
        return self.libelle


class Produit(models.Model):
    nom = models.CharField(max_length=50)
    description = models.TextField()
    prix = models.DecimalField(max_digits=6, decimal_places=2)
    urlImg = models.TextField(null=True, blank=True)
    ingredients = models.ManyToManyField(Ingredient)

    def __unicode__(self):
        return self.nom


class Boisson(Produit):
    degre = models.IntegerField()
    alcool = models.BooleanField(default=False)


class Glace(Produit):
    parfum = models.CharField(max_length=50)


class Commande(models.Model):
    prixTTC = models.DecimalField(default=0, max_digits=6, decimal_places=2, null=True, blank=True)
    prixHT = models.DecimalField(default=0, max_digits=6, decimal_places=2, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    serveur = models.ForeignKey('Serveur', null=True, blank=True)
    loge = models.ForeignKey('Loge')
    produit = models.ManyToManyField(Produit, through='LigneCom')
    finie = models.BooleanField(default=False)

        #Overriding
    def save(self, *args, **kwargs):
        if not self.serveur:
            self.serveur = Serveur.objects.exclude(commande__finie=True).annotate(num=Count('commande')).order_by("num").first()
        super(Commande, self).save(*args, **kwargs)


class LigneCom(models.Model):
    quantite = models.IntegerField(default=1)
    produit = models.ForeignKey(Produit)
    commande = models.ForeignKey(Commande)

    #Overriding
    def save(self, *args, **kwargs):
        self.commande.prixTTC += self.quantite * self.produit.prix
        self.commande.save()

        super(LigneCom, self).save(*args, **kwargs)


class Serveur(models.Model):
    class Meta:
        unique_together = (("nom", "prenom", "dateNaissance"),)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    dateNaissance = models.DateField()
    adresse = models.CharField(max_length=200)
    ville = models.CharField(max_length=200)
    codePostal = models.CharField(max_length=5)
    tauxCommission = models.DecimalField(max_digits=5, decimal_places=2)


class Loge(models.Model):
    libelle = models.CharField(max_length=50)
