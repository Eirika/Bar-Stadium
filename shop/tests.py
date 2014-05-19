# -*- coding: utf-8 -*-
from django.test import TestCase
from shop.models import Produit, Serveur, Loge, Commande, LigneCom


class CommandeTestCase(TestCase):

    def setUp(self):
        self.p = Produit(nom="pomme", description="Belle pomme rouge", prix=2, urlImg="http://google_une_pomme_pour_moi.com")
        self.p.save()

        self.s = Serveur(nom='Ornottoobi', prenom="Toobi")
        self.s.save()

        self.l = Loge(libelle="Loge à Johnny")
        self.l.save()

    def test_save_add_serveur(self):
        s2 = Serveur(nom='a', prenom="a")
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

        self.s = Serveur(nom='Ornottoobi', prenom="Toobi")
        self.s.save()

        self.l = Loge(libelle="Loge à Johnny")
        self.l.save()

    def test_save_add_prix(self):
        c = Commande(loge=self.l)
        c.save()

        lc = LigneCom(produit=self.p, commande=c, quantite=4)
        lc.save()
        lc = LigneCom(produit=self.p2, commande=c, quantite=2)
        lc.save()

        self.assertEqual(Commande.objects.get(pk=c.pk).prixTTC, 16)
