from django.contrib import admin
from shop.models import Boisson, Glace, Ingredient, Serveur

# Register your models here.


class BoissonAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description', 'prix', 'alcool', 'degre', 'urlImg')
admin.site.register(Boisson, BoissonAdmin)


class GlaceAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description', 'prix', 'urlImg')
admin.site.register(Glace, GlaceAdmin)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('libelle',)
admin.site.register(Ingredient, IngredientAdmin)


class ServeurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'dateNaissance', 'adresse', 'ville', 'codePostal', 'tauxCommission')
admin.site.register(Serveur, ServeurAdmin)
