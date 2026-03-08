import os
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login
from .forms import CustomUserCreationForm, CustomAuthenticationForm, AvisForm, ArticleForm
from .models import Destination, Avis, Hotel, Article, Reservation
from django.core.mail import send_mail
from django.conf import settings
from .forms import CustomUserCreationForm
from django.contrib.auth import logout


def index(request):
    destinations = Destination.objects.filter(statut=True)[:3]
    avis = Avis.objects.filter(statut=True)[:5]
    return render(request, 'index.html', {'destinations': destinations, 'avis': avis})

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        form = AvisForm(request.POST)
        if form.is_valid():
            avis = form.save(commit=False)
            if request.user.is_authenticated:
                avis.nom_utilisateur = request.user.username
            avis.save()
            return redirect('index')
    else:
        form = AvisForm()
    return render(request, 'contact.html', {'form': form})

def destination(request):
    destinations = Destination.objects.filter(statut=True)
    return render(request, 'destination.html', {'destinations': destinations})


def destination_detail(request, destination_id):
    # Récupérer la destination demandée
    destination = get_object_or_404(Destination, id=destination_id, statut=True)
    
    # Récupérer des destinations similaires (même pays ou tags similaires)
    if destination.tags:
        # Si la destination a des tags, trouver d'autres destinations avec des tags similaires
        related_destinations = Destination.objects.filter(
            statut=True, 
            tags__icontains=destination.tags.split(',')[0]  # Utiliser le premier tag comme référence
        ).exclude(id=destination_id)[:3]
    else:
        # Sinon, trouver des destinations du même pays
        related_destinations = Destination.objects.filter(
            statut=True, 
            pays=destination.pays
        ).exclude(id=destination_id)[:3]
    
    # Si aucune destination similaire n'est trouvée, prendre simplement les dernières ajoutées
    if not related_destinations:
        related_destinations = Destination.objects.filter(
            statut=True
        ).exclude(id=destination_id).order_by('-date_ajout')[:3]
    
    context = {
        'destination': destination,
        'related_destinations': related_destinations,
    }
    
    return render(request, 'destination_detail.html', context)

def blog(request):
    articles = Article.objects.filter(statut=True).order_by('-date_publication')
    recent_articles = Article.objects.filter(statut=True).order_by('-date_publication')[:3]  # Get 3 most recent
    return render(request, 'blog.html', {'articles': articles, 'recent_articles': recent_articles})


def article_list(request):
    query = request.GET.get('q')
    if query:
        articles = Article.objects.filter(titre__icontains=query, statut=True)
    else:
        articles = Article.objects.filter(statut=True)

    return render(request, 'article_list.html', {'articles': articles, 'query': query})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Envoi de l'email de bienvenue avec pièce jointe
            subject = 'Bienvenue sur notre site!'
            # Utilisez un template HTML pour votre message
            html_message = f"""
            <html>
              <body>
                <h2>Bonjour {user.username},</h2>
                <p>Merci pour votre inscription sur notre site.</p>
                <p>Vous trouverez en pièce jointe notre guide d'utilisation.</p>
                <p>N'hésitez pas à nous contacter si vous avez des questions.</p>
                <p>Cordialement,<br>
                L'équipe du site</p>
              </body>
            </html>
            """
            
            # Version texte (pour les clients qui ne supportent pas l'HTML)
            text_message = f"""
            Bonjour {user.username},
            
            Merci pour votre inscription sur notre site.
            Vous trouverez en pièce jointe notre guide d'utilisation.
            
            Cordialement,
            L'équipe du site
            """
            
            email = EmailMessage(
                subject,
                text_message,
                f"Mon Site <{settings.DEFAULT_FROM_EMAIL}>",  # Format "Nom <email>"
                [user.email],
                reply_to=["support@monsiteweb.com"],  # Adresse de réponse
                headers={'X-MC-AutoText': 'true'},  # Aide à passer les filtres spam
            )
            
            # Ajout du contenu HTML
            email.content_subtype = "html"
            email.body = html_message
            
            # Chemin vers votre fichier (à compléter)
            guide_path = os.path.join(settings.BASE_DIR, 'static', 'docs', 'guide.pdf')
            if os.path.exists(guide_path):
                email.attach_file(guide_path)
            
            email.send(fail_silently=False)
            
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index') 

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})


def reservation(request, destination_id):
    destination = get_object_or_404(Destination, id=destination_id, statut=True)
    context = {
        'destination': destination,
    }
    return render(request, 'reservation.html', context)

def process_reservation(request):
    if request.method == 'POST':
        destination = get_object_or_404(Destination, id=request.POST.get('destination_id'))
        
        reservation = Reservation.objects.create(
            destination=destination,
            nom=request.POST.get('nom'),
            prenom=request.POST.get('prenom'),
            email=request.POST.get('email'),
            telephone=request.POST.get('telephone'),
            date_arrivee=request.POST.get('date_arrivee'),
            date_depart=request.POST.get('date_depart'),
            nb_adultes=int(request.POST.get('nb_adultes', 1)),
            nb_enfants=int(request.POST.get('nb_enfants', 0)),
            type_hebergement=request.POST.get('type_hebergement'),
            message=request.POST.get('message', ''),
        )
        
        return redirect('reservation_confirmation', reservation_id=reservation.id)
    
    # Si ce n'est pas un POST, rediriger vers la page d'accueil
    return redirect('index')

def reservation_confirmation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    context = {
        'reservation': reservation,
    }
    return render(request, 'reservation_confirmation.html', context)
