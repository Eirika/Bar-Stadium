# -*- coding: utf-8 -*-
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models import Count

from shop.models import Commande, Serveur

# A chaque reception d'un save() sur l'objet commande le signal suivant s'execute


@receiver(pre_save, sender=Commande)
def set_serveur(sender, instance, **kwargs):
    if not instance.serveur:    # Si notre instance de commande n'a pas de serveur
                                # Alors on lui attribue le serveur possédant le moins de commande en cours
        instance.serveur = Serveur.objects.exclude(commande__servie=True).annotate(num=Count('commande')).order_by("num").first()
