from django.conf.urls import patterns, url

urlpatterns = patterns('shop.views',
    url(r'^$', 'home'),
    url(r'^boutique/$', 'produits'),
    url(r'^boissons/$', 'boissons'),
    url(r'^glaces/$', 'glaces'),
    url(r'^connexion/$', 'connexion'),
    url(r'^deconnexion/$', 'deconnexion', name='deconnexion'),
    url(r'^service/$', 'gestionService'),
)
