from django.db import models
from django.contrib.auth import get_user_model
from django_ckeditor_5.fields import CKEditor5Field
from django.utils import timezone
from django.utils.text import slugify


User = get_user_model()

class Categorie(models.Model):
    class Meta:
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'

    nom = models.CharField(max_length=100)
    description = models.TextField()

    # Standards
    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Enlève `default=timezone.now`
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):        
        return self.nom



class Destination(models.Model):
    class Meta:
        verbose_name = 'Destination'
        verbose_name_plural = 'Destinations'

    # Champs de base existants
    nom = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='destinations/')
    pays = models.CharField(max_length=100)
    date_ajout = models.DateTimeField(auto_now_add=True)
    
    # Nouveaux champs pour informations détaillées
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    langue = models.CharField(max_length=100, default="Français, Anglais")
    monnaie = models.CharField(max_length=50, default="Euro (€)")
    visa_requis = models.BooleanField(default=False)
    
    # Périodes recommandées
    haute_saison_debut = models.CharField(max_length=20, blank=True, null=True)
    haute_saison_fin = models.CharField(max_length=20, blank=True, null=True)
    climat = models.CharField(max_length=50, blank=True, null=True)
    
    # Points d'intérêt (stockés sous forme de texte séparé par des virgules)
    points_interet = models.TextField(blank=True, null=True, 
                     help_text="Liste des points d'intérêt séparés par des virgules")
    
    # Champs pour galerie d'images supplémentaires
    image_2 = models.ImageField(upload_to='destinations/gallery/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='destinations/gallery/', blank=True, null=True)
    
    # Géolocalisation pour la carte
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    
    # Champs pour les tags
    tags = models.CharField(max_length=200, blank=True, null=True,
                            help_text="Tags séparés par des virgules")

    # Standards
    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom
    
    def save(self, *args, **kwargs):
        # Générer automatiquement un slug si non spécifié
        if not self.slug:
            self.slug = slugify(self.nom)
        super(Destination, self).save(*args, **kwargs)
    
    def get_points_interet_list(self):
        """Retourne la liste des points d'intérêt sous forme de liste"""
        if self.points_interet:
            return [point.strip() for point in self.points_interet.split(',')]
        return []
        
    def get_tags_list(self):
        """Retourne les tags sous forme de liste"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []


class Activite(models.Model):
    class Meta:
        verbose_name = 'Activité'
        verbose_name_plural = 'Activités'

    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    date_ajout = models.DateTimeField(auto_now_add=True)

    # Standards
    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Enlève `default=timezone.now`
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom


class Avis(models.Model):
    class Meta:
        verbose_name = 'Avis'    
        verbose_name_plural = 'Avis'

    destination = models.ForeignKey(Destination, related_name='avis', on_delete=models.CASCADE)
    nom_utilisateur = models.CharField(max_length=100)
    commentaire = models.TextField()
    note = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    date_ajout = models.DateTimeField(auto_now_add=True)

    # Standards
    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Enlève `default=timezone.now`
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Avis de {self.nom_utilisateur} sur {self.destination.nom}'


class Article(models.Model):
    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    titre = models.CharField(max_length=200)
    contenu = CKEditor5Field('Text', config_name='extends')
    image = models.ImageField(upload_to='articles/')
    # Dans models.py
    date_publication = models.DateTimeField(default=timezone.now)  # Remplace auto_now_add=True
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)

    # Standards
    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Enlève `default=timezone.now`
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titre


class Hotel(models.Model):
    class Meta:
        verbose_name = 'Hôtel'
        verbose_name_plural = 'Hôtels'

    nom = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='hotels/')
    adresse = models.CharField(max_length=255)
    prix_par_nuit = models.DecimalField(max_digits=10, decimal_places=2)
    destination = models.ForeignKey(Destination, related_name='hotels', on_delete=models.CASCADE)
    date_ajout = models.DateTimeField(auto_now_add=True)

    # Standards
    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Enlève `default=timezone.now`
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom


class Reservation(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    date_arrivee = models.DateField()
    date_depart = models.DateField()
    nb_adultes = models.PositiveIntegerField()
    nb_enfants = models.PositiveIntegerField(default=0)
    type_hebergement = models.CharField(max_length=50)
    message = models.TextField(blank=True, null=True)
    date_reservation = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, default='En attente', 
                             choices=[('En attente', 'En attente'), 
                                     ('Confirmée', 'Confirmée'), 
                                     ('Annulée', 'Annulée')])
    
    def __str__(self):
        return f"Réservation - {self.nom} {self.prenom} ({self.destination.nom})"


class Commande(models.Model):
    class Meta:
        verbose_name = 'Commande'
        verbose_name_plural = 'Commandes'

    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    date_ajout = models.DateTimeField(auto_now_add=True)

    # Standards
    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Enlève `default=timezone.now`
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):        
        return self.nom
    

class Panier(models.Model):
    class Meta:
        verbose_name = 'Panier'
        verbose_name_plural = 'Paniers'

    nom = models.CharField(max_length=100)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    date_ajout = models.DateTimeField(auto_now_add=True)

    # Standards
    statut = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Enlève `default=timezone.now`
    last_updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):        
        return self.nom
    

class Produit(models.Model):   
    nom = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField()
    detail = models.TextField()
    image = models.FileField(blank=True, null=True, upload_to="articles")
    old_price = models.FloatField()
    price = models.FloatField( blank=True, null=True)
    likes_count = models.PositiveIntegerField(default=0)

class Vote(models.Model):
    article = models.ForeignKey(Produit, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.BooleanField(default=True)
    

class Comment(models.Model):
   
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    
class CartArticle(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

class ContactForm(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    phone_number = models.CharField(max_length=20)
    website = models.URLField()


class Commentaire(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)






