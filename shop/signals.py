# -*- coding: utf-8 -*-
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db.models import Count

from shop.models import Commande, Serveur


@receiver(pre_save, sender=Commande)
def set_serveur(sender, instance, **kwargs):
	if not instance.serveur:
		instance.serveur = Serveur.objects.exclude(commande__servie=True).annotate(num=Count('commande')).order_by("num").first()
