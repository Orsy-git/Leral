Léral c'est l'outil de Orsy :)

📊 Leral - Plateforme de Gestion Intelligente de l'Énergie
<div align="center">
https://img.shields.io/badge/version-1.0.0-blue.svg
https://img.shields.io/badge/python-3.8+-green.svg
https://img.shields.io/badge/flask-2.3.3-lightgrey.svg
https://img.shields.io/badge/license-MIT-yellow.svg

Solution innovante de monitoring et gestion de la consommation électrique

Présentation • Fonctionnalités • Installation • Utilisation • Structure • Contribuer

</div>
🎯 Présentation :
Leral (qui signifie "Énergie" en Wolof) est une plateforme web innovante développée dans le cadre d'un mémoire de maîtrise, visant à révolutionner la gestion de la consommation électrique au Sénégal.

Contexte du Projet :
Ce projet s'inscrit dans le cadre d'un mémoire de maîtrise en informatique, visant à adresser les défis de la gestion énergétique au Sénégal à travers une solution digitale moderne et accessible.

Objectifs Académiques :
- Démonstration des concepts avancés de développement web

- Implémentation d'architecture microservices

- Intégration de systèmes de paiement électronique

- Analyse et visualisation de données en temps réel

Fonctionnalités :
📈 Monitoring Intelligent
Tableau de bord interactif avec visualisation en temps réel

Prédiction de durée du crédit basée sur la consommation historique

Alertes intelligentes pour le suivi du solde

Graphiques dynamiques avec Plotly

Gestion des Paiements :
Intégration PayTech pour les recharges sécurisées

Simulation de recharge avec projection automatique

Historique complet des transactions

Multi-moyens de paiement (Orange Money, Free Money, Wave, Carte)

Expérience Utilisateur :
Design responsive adapté mobile et desktop

Mode sombre/clair selon les préférences

Interface intuitive et accessible

Export des données en format CSV

🔧 Fonctionnalités Techniques :
- Architecture modulaire et scalable

- Gestion de session sécurisée

- API RESTful complète

Simulation réaliste basée sur les données Senelec

🚀 Installation :
Prérequis
Python 3.8 ou supérieur

Pip (gestionnaire de packages Python)

📥 Installation Rapide
bash

# Créer un environnement virtuel
python -m venv venv

# Activer l'environnement
# Sur Windows :
venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
python app.py


🔧 Configuration
Variables d'environnement (optionnel) :

bash

Accéder à l'application :

http://localhost:5000


💻 Utilisation
🎯 Compteurs de Test
Pour tester l'application, utilisez ces identifiants de démonstration :

SENELEC_000001

SENELEC_000042

SENELEC_000099

📱 Navigation

Page d'accueil : Saisissez votre numéro de compteur

Tableau de bord : Visualisez votre consommation en temps réel

Section prédiction : Estimez la durée de votre crédit

Historique : Consultez votre consommation passée

Paiements : Rechargez votre compteur en toute sécurité

🏗️ Structure du Projet
text
leral/
├── app.py                          # Application principale Flask
├── requirements.txt                # Dépendances Python
├── README.md                       # Documentation
├── data/
│   ├── consumption_data.json      # Données de consommation
│   └── user_settings.json         # Préférences utilisateurs
├── static/
│   ├── css/
│   │   ├── style.css              # Styles principaux
│   │   └── dark-mode.css          # Mode sombre
│   └── js/
│       ├── dashboard.js           # Logique tableau de bord
│       ├── payments.js            # Gestion des paiements
│       └── settings.js            # Paramètres
└── templates/
    ├── base.html                  # Template de base
    ├── index.html                 # Page d'accueil
    ├── dashboard.html             # Tableau de bord
    ├── history.html               # Historique
    ├── payment.html               # Paiements
    ├── settings.html              # Paramètres
    └── payment_status.html        # Statut paiement

🔌 API Endpoints
📊 Données de Consommation
GET /api/consumption/<meter_id> - Données du compteur

POST /api/update_consumption - Mise à jour simulation

💳 Paiements
POST /api/initiate_payment - Initier un paiement

GET /api/payment/status/<id> - Statut du paiement

GET /api/payment/success - Callback succès

GET /api/payment/cancel - Callback annulation

⚙️ Configuration
POST /api/update_settings - Mettre à jour les paramètres

GET /api/export_excel - Exporter les données

🛠️ Développement
Technologies Utilisées
Backend : Flask, Python

Frontend : HTML5, CSS3, JavaScript, Plotly

Base de données : JSON (simulation)

Paiements : API PayTech

Visualisation : Plotly.js

🧪 Tests
bash
# Lancer l'application en mode développement
python app.py

# Accéder aux logs en temps réel
# Les données sont régénérées automatiquement si besoin
🔄 Personnalisation
Modifier les styles dans /static/css/

Adapter les templates dans /templates/

Configurer l'API PayTech dans app.py

🤝 Contribuer
Les contributions sont les bienvenues ! Pour contribuer :

Fork le projet

Créer une branche (git checkout -b feature/ma-fonctionnalite)

Commit les changements (git commit -am 'Ajouter une fonctionnalité')

Push sur la branche (git push origin feature/ma-fonctionnalite)

Ouvrir une Pull Request

📋 Guidelines
Suivre les standards PEP 8 pour le Python

Documenter le code新增的功能

Tester les modifications

Mettre à jour la documentation


Objectifs Pédagogiques
Architecture des applications web modernes

Intégration d'APIs tierces

Visualisation de données complexes

Expérience utilisateur optimisée

📄 Licence
Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

👥 Auteur
Orsy KEWOL

Étudiant en Maîtrise en BIG DATA & BUSINESS INTELLIGENCE

Email: kongokewol@gmail.com

LinkedIn: Orsy Kewol (https://www.linkedin.com/in/orsy-kewol-1116b0302/)

🙏 Remerciements
Senelec pour les données de référence

PayTech pour l'API de paiement

Communauté open-source pour les outils utilisés

<div align="center">
⚡ Leral - L'énergie intelligente pour tous ⚡

Développé avec ❤️ pour le Sénégal

</div>

📞 Support
Pour toute question ou support :

📧 Email : kongokewol@gmail.com

🐛 Issues : GitHub Issues

