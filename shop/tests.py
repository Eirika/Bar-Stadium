# -*- coding: utf-8 -*-
from django.test import TestCase
from shop.models import Produit, Serveur, Loge, Commande


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

        self.assertEqual(c2.serveur, s2)
