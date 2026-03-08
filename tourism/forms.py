from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model
from .models import Avis, Reservation, Article

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Choisissez un nom d\'utilisateur',
            'required': 'required'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Entrez votre adresse email',
            'required': 'required'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Créez un mot de passe',
            'required': 'required'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Confirmez votre mot de passe',
            'required': 'required'
        })

# Formulaire de connexion personnalisé
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Nom d\'utilisateur ou email'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Mot de passe'
        })

# Formulaire de réinitialisation de mot de passe personnalisé
class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Votre adresse email'
        })

# Formulaire pour définir un nouveau mot de passe
class CustomSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Nouveau mot de passe'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-input',
            'placeholder': 'Confirmation du nouveau mot de passe'
        })

# Formulaire pour les avis
class AvisForm(forms.ModelForm):
    class Meta:
        model = Avis
        fields = ['nom_utilisateur', 'commentaire', 'note']
        
        widgets = {
            'nom_utilisateur': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Votre nom'
            }),
            'commentaire': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Votre commentaire',
                'rows': 4
            }),
            'note': forms.Select(attrs={
                'class': 'form-input'
            })
        }

# Formulaire pour les réservations
# class ReservationForm(forms.ModelForm):
#     class Meta:
#         model = Reservation
#         fields = ['hotel',  'nombre_de_personnes']
        
#         widgets = {
#             'hotel': forms.Select(attrs={
#                 'class': 'form-input'
#             }),
#             'date_debut': forms.DateInput(attrs={
#                 'class': 'form-input',
#                 'type': 'date'
#             }),
#             'date_fin': forms.DateInput(attrs={
#                 'class': 'form-input',
#                 'type': 'date'
#             }),
#             'nombre_de_personnes': forms.NumberInput(attrs={
#                 'class': 'form-input',
#                 'min': 1
#             })
#         }

# Formulaire pour les articles de blog
class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['titre', 'contenu', 'image']
        
        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Titre de l\'article'
            }),
            'contenu': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Contenu de l\'article',
                'rows': 10
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-input'
            })
        }