from django.db import models


class Produit(models.Model):
    nom = models.CharField(max_length=50)
    description = models.TextField()
    prix = models.IntegerField()
    urlImg = models.TextField()


class Boisson(Produit):
    degre = models.IntegerField()
    alcool = models.BooleanField(default=False)


class Glace(Produit):
    parfum = models.CharField(max_length=50)


class Commande(models.Model):
    prixTTC = models.DecimalField(max_digits=6, decimal_places=2)
    prixHT = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    serveur = models.ForeignKey('Serveur')
    loge = models.ForeignKey('Loge')
    produit = models.ManyToManyField(Produit, through='LigneCom')


class LigneCom(models.Model):
    quantite = models.IntegerField()
    produit = models.ForeignKey(Produit)
    commande = models.ForeignKey(Commande)


class Serveur(models.Model):
    class Meta:
        unique_together = (("nom", "prenom"),)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)


class Loge(models.Model):
    libelle = models.CharField(max_length=50)
