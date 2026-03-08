from django.contrib import admin
from .models import Destination, Activite, Avis, Article, Hotel, Reservation, Categorie, Commande, Panier



class DestinationAdmin(admin.ModelAdmin):
    list_display = ('nom', 'pays', 'date_ajout', 'statut')
    list_filter = ('statut', 'pays')
    search_fields = ('nom', 'description', 'pays')
    prepopulated_fields = {'slug': ('nom',)}
    fieldsets = (
        ('Informations principales', {
            'fields': ('nom', 'slug', 'description', 'pays', 'image')
        }),
        ('Informations détaillées', {
            'fields': ('langue', 'monnaie', 'visa_requis', 'points_interet')
        }),
        ('Période et climat', {
            'fields': ('haute_saison_debut', 'haute_saison_fin', 'climat')
        }),
        ('Galerie', {
            'fields': ('image_2', 'image_3')
        }),
        ('Localisation', {
            'fields': ('latitude', 'longitude')
        }),
        ('Catégorisation', {
            'fields': ('tags',)
        }),
        ('Paramètres', {
            'fields': ('statut',)
        }),
    )

class ActiviteAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix', 'created_at', 'statut')  # Ajout de 'statut'
    list_display_links = ['nom']
    list_filter = ('prix', 'statut')  # Ajout de filtre sur 'statut'
    search_fields = ('nom',)
    date_hierarchy = 'created_at'
    ordering = ['nom']
    list_per_page = 10
    fieldsets = [
        ('Informations', {'fields': ['nom', 'description', 'prix', 'statut']})  # Ajout de 'statut'
    ]

class AvisAdmin(admin.ModelAdmin):
    list_display = ('nom_utilisateur', 'destination', 'note', 'created_at', 'statut')  # Ajout de 'statut'
    list_display_links = ['nom_utilisateur']
    list_filter = ('destination', 'note', 'statut')  # Ajout de filtre sur 'statut'
    search_fields = ('nom_utilisateur', 'commentaire')
    date_hierarchy = 'created_at'
    ordering = ['created_at']
    list_per_page = 10
    fieldsets = [
        ('Informations', {'fields': ['destination', 'nom_utilisateur', 'commentaire', 'note', 'statut']})  # Ajout de 'statut'
    ]

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'date_publication', 'statut')  # Ajout de 'statut'
    list_display_links = ['titre']
    search_fields = ('titre', 'contenu')
    list_filter = ('statut',)  # Ajout de filtre sur 'statut'
    date_hierarchy = 'date_publication'
    ordering = ['date_publication']
    list_per_page = 10
    fieldsets = [
        ('Informations générales', {'fields': ['titre', 'contenu', 'image', 'statut']}),  # Ajout de 'statut'
        ('Publication', {'fields': ['date_publication', 'auteur']})
    ]

class HotelAdmin(admin.ModelAdmin):
    list_display = ('nom', 'destination', 'prix_par_nuit', 'created_at', 'statut')  # Ajout de 'statut'
    list_display_links = ['nom']
    list_filter = ('destination', 'statut')  # Ajout de filtre sur 'statut'
    search_fields = ('nom',)
    date_hierarchy = 'created_at'
    ordering = ['nom']
    list_per_page = 10
    fieldsets = [
        ('Informations', {'fields': ['nom', 'description', 'image', 'adresse', 'prix_par_nuit', 'destination', 'statut']})  # Ajout de 'statut'
    ]


class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        'nom_prenom',  # Méthode personnalisée pour afficher nom + prénom
        'destination', 
        'date_arrivee', 
        'date_depart', 
        'statut',
        'type_hebergement'
    )
    
    list_display_links = ['nom_prenom']
    
    list_filter = (
        'destination',
        'statut',
        'type_hebergement',
        'date_arrivee'
    )
    
    search_fields = (
        'nom',
        'prenom',
        'email',
        'destination__nom'
    )
    
    date_hierarchy = 'date_arrivee'
    ordering = ['date_arrivee']
    list_per_page = 10
    
    fieldsets = [
        ('Informations client', {
            'fields': [
                'nom',
                'prenom',
                'email',
                'telephone'
            ]
        }),
        ('Détails de la réservation', {
            'fields': [
                'destination',
                'date_arrivee',
                'date_depart',
                'nb_adultes',
                'nb_enfants',
                'type_hebergement',
                'statut'
            ]
        }),
        ('Autres informations', {
            'fields': [
                'message',
                'date_reservation'
            ],
            'classes': ['collapse']
        })
    ]
    
    def nom_prenom(self, obj):
        return f"{obj.nom} {obj.prenom}"

class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'created_at', 'statut')  # Ajout de 'statut'
    list_display_links = ['nom']
    search_fields = ('nom',)
    list_filter = ('statut',)  # Ajout de filtre sur 'statut'
    date_hierarchy = 'created_at'
    ordering = ['nom']
    list_per_page = 10
    fieldsets = [
        ('Informations', {'fields': ['nom', 'description', 'statut']})  # Ajout de 'statut'
    ]

class CommandeAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix', 'date_ajout', 'statut')  # Ajout de 'statut'
    list_display_links = ['nom']
    list_filter = ('statut',)  # Ajout de filtre sur 'statut'
    search_fields = ('nom',)
    date_hierarchy = 'date_ajout'
    ordering = ['date_ajout']
    list_per_page = 10
    fieldsets = [
        ('Informations', {'fields': ['nom', 'description', 'prix', 'statut']})  # Ajout de 'statut'
    ]

class PanierAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix', 'date_ajout', 'statut')  # Ajout de 'statut'
    list_display_links = ['nom']
    list_filter = ('statut',)  # Ajout de filtre sur 'statut'
    search_fields = ('nom',)
    date_hierarchy = 'date_ajout'
    ordering = ['date_ajout']
    list_per_page = 10
    fieldsets = [
        ('Informations', {'fields': ['nom', 'description', 'prix', 'statut']})  # Ajout de 'statut'
    ]

# Enregistrement des modèles avec leurs classes d'administration
admin.site.register(Destination, DestinationAdmin)
admin.site.register(Activite, ActiviteAdmin)
admin.site.register(Avis, AvisAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Hotel, HotelAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Categorie, CategorieAdmin)
admin.site.register(Commande, CommandeAdmin)
admin.site.register(Panier, PanierAdmin)