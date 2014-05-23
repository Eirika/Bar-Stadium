from django.contrib import admin
from shop.models import Boisson, Glace, Ingredient, Serveur, Loge, Commande

# Register your models here.


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('libelle',)
admin.site.register(Ingredient, IngredientAdmin)


class BoissonAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description', 'prix', 'alcool', 'degre', 'urlImg')
admin.site.register(Boisson, BoissonAdmin)


class GlaceAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description', 'prix', 'urlImg')
admin.site.register(Glace, GlaceAdmin)


class LogeAdmin(admin.ModelAdmin):
    list_display = ('libelle',)
admin.site.register(Loge, LogeAdmin)


class ServeurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'dateNaissance', 'adresse', 'ville', 'codePostal', 'tauxCommission')
admin.site.register(Serveur, ServeurAdmin)


class CommandeAdmin(admin.ModelAdmin):
    list_display = ('loge', 'serveur', 'get_produit', 'date', 'prixHT', 'prixTTC', 'servie', 'validee')

    def get_produit(self, obj):
        return "; ".join([p.nom for p in obj.produit.all()])
admin.site.register(Commande, CommandeAdmin)
