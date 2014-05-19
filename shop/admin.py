from django.contrib import admin
from shop.models import Boisson, Glace

# Register your models here.


class BoissonAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description', 'prix', 'alcool', 'degree', 'urlImg')
admin.site.register(Boisson, BoissonAdmin)


class GlaceAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description', 'prix', 'parfum', 'urlImg')
admin.site.register(Glace, GlaceAdmin)
