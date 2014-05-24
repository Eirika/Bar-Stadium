# -*- coding: utf-8 -*-
from django.test import TestCase
from shop.models import Produit, Serveur, Loge, Commande, LigneCom, Ingredient, Boisson
from django.contrib.auth.models import User, Group


class CommandeTestCase(TestCase):

    def setUp(self):
        self.p = Produit(nom="pomme", description="Belle pomme rouge", prix=2, urlImg="http://google_une_pomme_pour_moi.com")
        self.p.save()

        self.s = Serveur(nom='Ornottoobi', prenom="Toobi", dateNaissance="1992-08-26", adresse="700 Rue neuve", ville="Saint paul", codePostal="26750", tauxCommission=10)
        self.s.save()

        self.u = User(username="loge1")
        self.u.save()

        self.l = Loge(libelle="Loge à Johnny", user=self.u)
        self.l.save()

        self.p = Boisson(nom="Pastis", description="Le petit jaune", prix=10, urlImg="http://google_une_pomme_pour_moi.com", degre=45)
        self.p.save()

        self.p2 = Boisson(nom="Jus de pomme", description="Belle pomme rouge", prix=20, urlImg="http://google_une_pomme_pour_moi.com")
        self.p2.save()

    def test_save_add_serveur(self):
        s2 = Serveur(nom='a', prenom="a", dateNaissance="1992-08-26", adresse="700 Rue neuve", ville="Saint paul", codePostal="26750", tauxCommission=10)
        s2.save()

        # On occupe un serveur
        c = Commande(loge=self.l, serveur=self.s)
        c.save()
        c3 = Commande(loge=self.l, serveur=self.s)
        c3.save()

        c2 = Commande(loge=self.l)
        c2.save()

        print Commande.objects.get(pk=c2.pk)

        self.assertEqual(Commande.objects.get(pk=c2.pk).serveur.pk, s2.pk)

    def test_commission_serveur(self):
        c = Commande(loge=self.l, serveur=self.s)
        c.save()

        lc = LigneCom(produit=self.p, commande=c, quantite=10)
        lc.save(self.l)
        lc = LigneCom(produit=self.p2, commande=c, quantite=10)
        lc.save(self.l)

        self.assertEqual(Commande.objects.get(pk=c.pk).prixTTC, 300)

        c.validee = True
        c.servie = True
        c.save()

        self.assertEqual(Commande.objects.get(pk=c.pk).prixTTC, 300)

        self.assertEqual(self.s.get_commissions(), 30)


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

        for ligneCom in c.lignecom_set.all():
            if ligneCom.produit.pk == 1:
                ligneCom.quantite = 2
            print(ligneCom.produit.nom)
            print(ligneCom.quantite)
            print(ligneCom.produit.pk)
        print(self.p.pk)

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

        self.assertEqual(u.groups.first(), g)
# compare directement les objets quand tu peux :)

        self.assertRaises(Loge.DoesNotExist, lambda: u.loge)


class excludeTest(TestCase):

    def setUp(self):
        self.s = Serveur(nom='Ornottoobi', prenom="Toobi", dateNaissance="1992-08-26", adresse="700 Rue neuve", ville="Saint paul", codePostal="26750", tauxCommission=12.12)
        self.s.save()

        self.u = User(username="loge1")
        self.u.save()

        self.u2 = User(username="loge2")
        self.u2.save()

        self.l = Loge(libelle="Loge à Johnny", user=self.u)
        self.l.save()

        self.l2 = Loge(libelle="La Loge 2", user=self.u2)
        self.l2.save()

        self.c = Commande(loge=self.l, validee=True)
        self.c.save()

        self.c2 = Commande(loge=self.l2)
        self.c2.save()

    def test_exclude_querie(self):
        commande1 = Commande.objects.exclude(validee=True).exclude(servie=True).filter(loge=self.l).first()

        commande2 = Commande.objects.exclude(validee=True).filter(loge=self.l).first()

        commande3 = Commande.objects.exclude(validee=True, servie=True).filter(loge=self.l2).first()

        self.assertEqual(commande1, None)  # résultat attendu : None car c.validee = True
                                            # résultat obtenu error car il renvoie c1

        self.assertEqual(commande2, None)  # résutlat attendu : None car c.valide = True
                                                # résultat obtenu None OK ! (car il prend bien en compte le exclude)

        self.assertEqual(commande3, self.c2)  # résultat attendu : c2 car c2.validee = False
                                            # résultat obtenu c2 OK !