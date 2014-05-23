# -*- coding: utf-8 -*-
from django.test import TestCase
from shop.models import Produit, Serveur, Loge, Commande, LigneCom, Ingredient, Boisson
from django.contrib.auth.models import User, Group


class CommandeTestCase(TestCase):

    def setUp(self):
        self.p = Produit(nom="pomme", description="Belle pomme rouge", prix=2, urlImg="http://google_une_pomme_pour_moi.com")
        self.p.save()

        self.s = Serveur(nom='Ornottoobi', prenom="Toobi", dateNaissance="1992-08-26", adresse="700 Rue neuve", ville="Saint paul", codePostal="26750", tauxCommission=12.12)
        self.s.save()

        self.u = User(username="loge1")
        self.u.save()

        self.l = Loge(libelle="Loge à Johnny", user=self.u)
        self.l.save()

    def test_save_add_serveur(self):
        s2 = Serveur(nom='a', prenom="a", dateNaissance="1992-08-26", adresse="700 Rue neuve", ville="Saint paul", codePostal="26750", tauxCommission=12.12)
        s2.save()

        # On occupe un serveur
        c = Commande(loge=self.l, serveur=self.s)
        c.save()
        c3 = Commande(loge=self.l, serveur=self.s)
        c3.save()

        c2 = Commande(loge=self.l)
        c2.save()

        self.assertEqual(c2.serveur.pk, s2.pk)


class LigneComTestCase(TestCase):

    def setUp(self):
        self.p = Produit(nom="pomme", description="Belle pomme rouge", prix=2, urlImg="http://google_une_pomme_pour_moi.com")
        self.p.save()

        self.p2 = Produit(nom="poire", description="Belle poire jaune", prix=4)
        self.p2.save()

        self.s = Serveur(nom='Ornottoobi', prenom="Toobi", dateNaissance="1992-08-26", adresse="700 Rue neuve", ville="Saint paul", codePostal="26750", tauxCommission=12.12)
        self.s.save()

        self.u = User(username="loge1")
        self.u.save()

        self.l = Loge(libelle="Loge à Johnny", user=self.u)
        self.l.save()

        self.i = Ingredient(libelle="Banane")
        self.i.save()

        self.i2 = Ingredient(libelle="Eau")
        self.i2.save()

        self.b = Boisson(nom="Pastis", description="Le petit jaune", prix=3.55, urlImg="http://google_une_pomme_pour_moi.com", degre=45)
        self.b.save()

        self.b2 = Boisson(nom="Jus de pomme", description="Belle pomme rouge", prix=2, urlImg="http://google_une_pomme_pour_moi.com")
        self.b2.save()

    def test_save_add_prix(self):
        c = Commande(loge=self.l)
        c.save()

        lc = LigneCom(produit=self.p, commande=c, quantite=4)
        lc.save()
        lc = LigneCom(produit=self.p2, commande=c, quantite=2)
        lc.save()

        self.assertEqual(Commande.objects.get(pk=c.pk).prixTTC, 16)

        for produit in c.produit.all():
            print(produit.nom)

# Ce test ne sert à rien: les manytomany sont déjà testée dans Django directement. Mais il permet de comprendre l'utilisation des many to many
    def test_save_ingredient(self):
        self.p.ingredients.add(self.i)

        self.assertEqual(self.p.ingredients.first().libelle, 'Banane')
        # deuxième option, moins jolie
        self.assertEqual(self.p.ingredients.all()[0].libelle, 'Banane')

    def test_save_boisson(self):
        self.assertEqual(self.b.alcool, True)
        self.assertEqual(self.b2.alcool, False)

    def test_user_loge(self):
        self.assertEqual(self.u.loge, self.l)

        if len(self.u.loge.commande_set.all()) == 0:
            print("gg")

        self.c = Commande(loge=self.u.loge)
        self.c.save()


class groupTest(TestCase):

    def test_group(self):
        u = User(username="tristan")
        u.save()

        g = Group(name="Serveur")
        g.save()
        u.groups.add(g)

        self.assertEqual(u.groups.first().name, "Serveur")
