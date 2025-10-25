from flask import Flask, render_template, request, jsonify, session, send_file
import json
import os
import csv
from datetime import datetime, timedelta
import random
from io import StringIO, BytesIO
import requests
import hashlib
import hmac

app = Flask(__name__)
app.secret_key = 'leral_secret_key_2024'
app.config['SESSION_TYPE'] = 'filesystem'

# Configuration PayTech
class PayTechConfig:
    # Remplacez par vos vraies clés API PayTech
    API_KEY = "03c2e62e3f83d9c90bb4463df01a2e058c8e1fcb6a8d7821f89133e00dfd336d"
    API_SECRET = "7cb40bc26529bca209932715131e5e53aaf40e5e936ce3cc7e5491a6df377862" 
    BASE_URL = "https://paytech.sn"
    
    # URLs de callback - à adapter selon votre domaine
    SUCCESS_URL = "http://localhost:5000/api/payment/success"
    CANCEL_URL = "http://localhost:5000/api/payment/cancel"
    IPN_URL = "http://localhost:5000/api/payment/ipn"

class PayTechService:
    def __init__(self):
        self.api_key = PayTechConfig.API_KEY
        self.api_secret = PayTechConfig.API_SECRET
        self.base_url = PayTechConfig.BASE_URL
    
    def generate_signature(self, params):
        """Génère la signature HMAC pour l'API PayTech"""
        data = ''.join([str(params[k]) for k in sorted(params.keys())])
        return hmac.new(
            self.api_secret.encode('utf-8'),
            data.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    def initiate_payment(self, amount, currency, meter_id, customer_email, customer_name):
        """Initie un paiement avec PayTech"""
        
        # Paramètres de base pour PayTech
        params = {
            'item_name': f"Recharge compteur {meter_id}",
            'item_price': amount,
            'currency': currency,
            'command_name': f"Recharge Leral - {meter_id}",
            'ref_command': f"LERAL_{meter_id}_{int(datetime.now().timestamp())}",
            'env': 'test',  # 'prod' pour la production
            'ipn_url': PayTechConfig.IPN_URL,
            'success_url': PayTechConfig.SUCCESS_URL,
            'cancel_url': PayTechConfig.CANCEL_URL,
            'email': customer_email,
            'name': customer_name
        }
        
        # Ajouter la signature
        params['signature'] = self.generate_signature(params)
        
        # Headers
        headers = {
            'API_KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        
        try:
            # Faire l'appel à l'API PayTech
            response = requests.post(
                f"{self.base_url}/api/payment/request-payment",
                json=params,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success') == 1:
                    return {
                        'success': True,
                        'payment_url': data['redirect_url'],
                        'token': data['token'],
                        'payment_id': data['token']  # PayTech utilise 'token' comme ID
                    }
                else:
                    return {
                        'success': False,
                        'error': data.get('errors', 'Erreur inconnue de PayTech')
                    }
            else:
                return {
                    'success': False,
                    'error': f"Erreur HTTP {response.status_code}: {response.text}"
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f"Erreur de connexion: {str(e)}"
            }
    
    def verify_payment(self, token):
        """Vérifie le statut d'un paiement"""
        
        params = {
            'token': token
        }
        
        params['signature'] = self.generate_signature(params)
        
        headers = {
            'API_KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/payment/check",
                json=params,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'status': data.get('status'),
                    'amount': data.get('amount'),
                    'currency': data.get('currency'),
                    'customer': data.get('customer')
                }
            else:
                return {
                    'success': False,
                    'error': f"Erreur HTTP {response.status_code}"
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f"Erreur de connexion: {str(e)}"
            }

# Initialiser le service PayTech
paytech_service = PayTechService()

# Fonctions de génération de données (gardées de votre code précédent)
def generate_consumption_data(num_meters=100):
    """Génère des données de consommation simulées pour des compteurs"""
    data = {}
    
    # Noms de clients sénégalais réalistes
    senegalese_names = [
        "Diallo", "Ndiaye", "Diop", "Fall", "Sow", "Kane", "Sy", "Ba", "Gueye", "Touré",
        "Mbaye", "Faye", "Sarr", "Diagne", "Lo", "Thiam", "Camara", "Mbengue", "Seck", "Diaw"
    ]
    
    first_names = [
        "Moussa", "Fatou", "Abdoulaye", "Aminata", "Ibrahima", "Mariama", "Omar", "Khadija",
        "Cheikh", "Rokhaya", "Mamadou", "Aïssatou", "Modou", "Diarra", "Pape", "Sokhna"
    ]
    
    for i in range(1, num_meters + 1):
        meter_id = f"SENELEC_{str(i).zfill(6)}"
        
        # Générer un nom réaliste
        last_name = random.choice(senegalese_names)
        first_name = random.choice(first_names)
        customer_name = f"{first_name} {last_name}"
        
        # Villes du Sénégal
        cities = ["Dakar", "Thiès", "Saint-Louis", "Kaolack", "Ziguinchor", "Mbour", "Louga", "Tambacounda"]
        addresses = [
            f"Rue {random.randint(1, 100)}", 
            f"Avenue {random.choice(['Liberté', 'Faidherbe', 'Lamine Guèye', 'Blaise Diagne'])}",
            f"Villa N°{random.randint(1, 50)}",
            f"Cité {random.choice(['Sicap', 'HLM', 'Grand Dakar', 'Fass'])}"
        ]
        
        address = f"{random.choice(addresses)}, {random.choice(cities)}"
        
        # Génération de données horaires pour les dernières 24h
        hourly_data = []
        base_consumption = random.uniform(0.5, 3.0)  # kWh de base
        
        for hour in range(24):
            timestamp = (datetime.now() - timedelta(hours=23-hour)).strftime("%Y-%m-%d %H:%M:%S")
            
            # Variation selon l'heure de la journée
            if 6 <= hour <= 9:  # Matin
                consumption = base_consumption * random.uniform(1.2, 1.8)
            elif 18 <= hour <= 22:  # Soir
                consumption = base_consumption * random.uniform(1.5, 2.2)
            else:  # Nuit
                consumption = base_consumption * random.uniform(0.3, 0.8)
            
            # Ajouter un peu de bruit
            consumption += random.uniform(-0.2, 0.2)
            consumption = max(0.1, consumption)  # Éviter les valeurs négatives
            
            hourly_data.append({
                "timestamp": timestamp,
                "consumption_kwh": round(consumption, 2)
            })
        
        # Informations du compteur
        data[meter_id] = {
            "customer_name": customer_name,
            "address": address,
            "meter_type": random.choice(["Monophasé", "Triphasé"]),
            "contract_power": random.choice([3, 6, 9, 12]),
            "total_consumption": round(sum(hour["consumption_kwh"] for hour in hourly_data), 2),
            "current_balance": round(random.uniform(500, 5000), 2),
            "status": random.choice(["Actif", "Actif", "Actif", "En panne"]),  # 75% actif
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "hourly_data": hourly_data,
            "daily_data": generate_daily_data(30),  # 30 jours d'historique
            "monthly_data": generate_monthly_data(12)  # 12 mois d'historique
        }
    
    # Créer le dossier data s'il n'existe pas
    os.makedirs('data', exist_ok=True)
    
    # Sauvegarder les données avec gestion d'erreur
    try:
        with open('data/consumption_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Données générées pour {num_meters} compteurs")
        print("🎯 Compteurs de test recommandés :")
        print("   - SENELEC_000001")
        print("   - SENELEC_000042") 
        print("   - SENELEC_000099")
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde : {e}")
        return False

def generate_daily_data(days=30):
    """Génère des données quotidiennes pour X jours"""
    daily_data = []
    base = random.uniform(15, 45)  # Consommation quotidienne de base
    
    for i in range(days):
        date = (datetime.now() - timedelta(days=days-1-i)).strftime("%Y-%m-%d")
        
        # Variation selon le jour de la semaine
        day_of_week = (datetime.now() - timedelta(days=days-1-i)).weekday()
        if day_of_week >= 5:  # Weekend
            consumption = base * random.uniform(1.1, 1.4)
        else:
            consumption = base * random.uniform(0.9, 1.2)
        
        daily_data.append({
            "date": date,
            "consumption_kwh": round(consumption, 2),
            "cost": round(consumption * 110, 2)  # Prix approximatif en FCFA
        })
    
    return daily_data

def generate_monthly_data(months=12):
    """Génère des données mensuelles"""
    monthly_data = []
    base = random.uniform(400, 1200)  # Consommation mensuelle de base
    
    for i in range(months):
        date = (datetime.now() - timedelta(days=30*(months-1-i))).strftime("%Y-%m")
        
        # Variation saisonnière
        month = (datetime.now().month - (months-1-i)) % 12
        if month in [5, 6, 7]:  # Saison chaude
            consumption = base * random.uniform(1.2, 1.6)
        else:
            consumption = base * random.uniform(0.8, 1.2)
        
        monthly_data.append({
            "month": date,
            "consumption_kwh": round(consumption, 2),
            "cost": round(consumption * 110, 2)
        })
    
    return monthly_data

# Charger les données avec régénération automatique en cas d'erreur
def load_consumption_data():
    """Charge les données de consommation avec régénération automatique si nécessaire"""
    data_file = 'data/consumption_data.json'
    
    # Si le fichier n'existe pas, le générer
    if not os.path.exists(data_file):
        print("📊 Fichier de données non trouvé, génération...")
        if generate_consumption_data(100):
            print("✅ Données générées avec succès")
        else:
            print("❌ Échec de la génération des données")
            return {}
    
    # Essayer de charger le fichier
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ Données chargées avec succès ({len(data)} compteurs)")
        return data
    except json.JSONDecodeError as e:
        print(f"❌ Fichier JSON corrompu: {e}")
        print("🔄 Régénération des données...")
        if generate_consumption_data(100):
            # Recharger après régénération
            try:
                with open(data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print("✅ Données régénérées et chargées avec succès")
                return data
            except json.JSONDecodeError:
                print("❌ Échec du rechargement après régénération")
                return {}
        else:
            return {}
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return {}

def load_user_settings():
    """Charge les paramètres utilisateur"""
    try:
        with open('data/user_settings.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("❌ Fichier user_settings.json corrompu, création d'un nouveau")
        return {}

def save_user_settings(settings):
    """Sauvegarde les paramètres utilisateur"""
    os.makedirs('data', exist_ok=True)
    try:
        with open('data/user_settings.json', 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"❌ Erreur sauvegarde paramètres: {e}")
        return False

def calculate_consumption_metrics(meter_data):
    """
    Calcule les métriques de prédiction de durée du crédit
    """
    current_balance = meter_data['current_balance']
    cost_per_kwh = 110  # Prix du kWh en FCFA
    
    # Consommation moyenne sur 7 jours
    last_7_days = meter_data['daily_data'][-7:]
    avg_daily_consumption = sum(day['consumption_kwh'] for day in last_7_days) / len(last_7_days)
    
    # Calculs de prédiction
    daily_cost = avg_daily_consumption * cost_per_kwh
    days_remaining = current_balance / daily_cost if daily_cost > 0 else 0
    kwh_remaining = current_balance / cost_per_kwh
    
    # Niveau d'alerte
    if days_remaining < 2:
        alert_level = "critical"
        alert_message = "Crédit très faible"
    elif days_remaining < 5:
        alert_level = "warning" 
        alert_message = "Crédit faible"
    else:
        alert_level = "normal"
        alert_message = "Crédit suffisant"
    
    return {
        'current_balance': current_balance,
        'avg_daily_consumption': round(avg_daily_consumption, 2),
        'avg_daily_cost': round(daily_cost, 2),
        'days_remaining': round(days_remaining, 1),
        'kwh_remaining': round(kwh_remaining, 2),
        'alert_level': alert_level,
        'alert_message': alert_message,
        'cost_per_kwh': cost_per_kwh
    }

# Routes principales
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    meter_id = request.args.get('meter_id', '').strip().upper()
    consumption_data = load_consumption_data()
    
    if not meter_id:
        return render_template('dashboard.html', error="Veuillez entrer un numéro de compteur")
    
    if meter_id not in consumption_data:
        return render_template('dashboard.html', error="Compteur non trouvé")
    
    session['current_meter'] = meter_id
    meter_data = consumption_data[meter_id]
    
    # Calculer les métriques de prédiction
    consumption_metrics = calculate_consumption_metrics(meter_data)
    
    # Charger les paramètres utilisateur
    user_settings = load_user_settings()
    theme = user_settings.get(meter_id, {}).get('theme', 'light')
    
    return render_template('dashboard.html', 
                         meter_id=meter_id, 
                         meter_data=meter_data,
                         metrics=consumption_metrics,
                         theme=theme,
                         error=None)

@app.route('/history')
def history():
    meter_id = session.get('current_meter')
    if not meter_id:
        return render_template('history.html', error="Aucun compteur sélectionné")
    
    consumption_data = load_consumption_data()
    if meter_id not in consumption_data:
        return render_template('history.html', error="Compteur non trouvé")
    
    meter_data = consumption_data[meter_id]
    return render_template('history.html', 
                         meter_id=meter_id, 
                         meter_data=meter_data)

@app.route('/settings')
def settings():
    meter_id = session.get('current_meter')
    if not meter_id:
        return render_template('settings.html', error="Aucun compteur sélectionné")
    
    user_settings = load_user_settings()
    current_settings = user_settings.get(meter_id, {
        'theme': 'light',
        'notifications': True,
        'language': 'fr',
        'currency': 'XOF'
    })
    
    return render_template('settings.html', 
                         meter_id=meter_id,
                         settings=current_settings)

@app.route('/payment')
def payment():
    meter_id = session.get('current_meter')
    if not meter_id:
        return render_template('payment.html', error="Aucun compteur sélectionné")
    
    consumption_data = load_consumption_data()
    if meter_id not in consumption_data:
        return render_template('payment.html', error="Compteur non trouvé")
    
    meter_data = consumption_data[meter_id]
    return render_template('payment.html', 
                         meter_id=meter_id, 
                         meter_data=meter_data)

# API Routes - PayTech
@app.route('/api/initiate_payment', methods=['POST'])
def initiate_payment():
    data = request.json
    meter_id = session.get('current_meter')
    amount = data.get('amount')
    payment_method = data.get('payment_method')
    
    if not meter_id or not amount:
        return jsonify({"error": "Données manquantes"}), 400
    
    # Charger les données du compteur
    consumption_data = load_consumption_data()
    if meter_id not in consumption_data:
        return jsonify({"error": "Compteur non trouvé"}), 404
    
    meter_data = consumption_data[meter_id]
    
    # Utiliser le service PayTech réel
    result = paytech_service.initiate_payment(
        amount=amount,
        currency='XOF',
        meter_id=meter_id,
        customer_email=f"{meter_data['customer_name'].replace(' ', '.').lower()}@example.com",
        customer_name=meter_data['customer_name']
    )
    
    if result['success']:
        # Sauvegarder la transaction en session
        session['pending_payment'] = {
            'payment_id': result['payment_id'],
            'meter_id': meter_id,
            'amount': amount,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify({
            "success": True,
            "payment_data": {
                "payment_id": result['payment_id'],
                "payment_url": result['payment_url'],
                "amount": amount,
                "currency": "XOF",
                "status": "pending"
            },
            "message": "Paiement initié avec succès. Redirection vers PayTech..."
        })
    else:
        return jsonify({
            "success": False,
            "error": result['error']
        }), 400

# Routes de callback PayTech
@app.route('/api/payment/success')
def payment_success():
    """Callback appelé quand le paiement est réussi"""
    token = request.args.get('token')
    if not token:
        return render_template('payment_status.html', 
                             success=False, 
                             message="Token manquant")
    
    # Vérifier le paiement avec PayTech
    result = paytech_service.verify_payment(token)
    
    if result['success'] and result['status'] == 'success':
        # Récupérer les infos de la transaction en attente
        pending_payment = session.get('pending_payment')
        
        if pending_payment and pending_payment.get('payment_id') == token:
            # Mettre à jour le solde du compteur
            consumption_data = load_consumption_data()
            meter_id = pending_payment['meter_id']
            
            if meter_id in consumption_data:
                consumption_data[meter_id]['current_balance'] += pending_payment['amount']
                consumption_data[meter_id]['last_update'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Sauvegarder les données mises à jour
                try:
                    with open('data/consumption_data.json', 'w', encoding='utf-8') as f:
                        json.dump(consumption_data, f, indent=2, ensure_ascii=False)
                    
                    # Nettoyer la session
                    session.pop('pending_payment', None)
                    
                    return render_template('payment_status.html',
                                         success=True,
                                         message=f"Paiement de {pending_payment['amount']} FCFA confirmé avec succès!",
                                         new_balance=consumption_data[meter_id]['current_balance'],
                                         meter_id=meter_id)
                except Exception as e:
                    return render_template('payment_status.html',
                                         success=False,
                                         message=f"Erreur lors de la mise à jour: {str(e)}")
    
    return render_template('payment_status.html',
                         success=False,
                         message="Erreur lors de la confirmation du paiement")

@app.route('/api/payment/cancel')
def payment_cancel():
    """Callback appelé quand le paiement est annulé"""
    session.pop('pending_payment', None)
    return render_template('payment_status.html',
                         success=False,
                         message="Paiement annulé par l'utilisateur")

@app.route('/api/payment/ipn', methods=['POST'])
def payment_ipn():
    """Instant Payment Notification - Callback server-to-server"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "Données manquantes"}), 400
        
        token = data.get('token')
        
        if token:
            # Vérifier le statut du paiement
            result = paytech_service.verify_payment(token)
            
            if result['success'] and result['status'] == 'success':
                # Ici vous pouvez mettre à jour votre base de données
                # Cette route est appelée directement par PayTech
                print(f"📩 IPN: Paiement réussi pour le token {token}")
                print(f"💰 Montant: {result.get('amount')} {result.get('currency')}")
                
                # Logique pour mettre à jour votre système
                # (à adapter selon votre base de données)
                
                return jsonify({"status": "success", "message": "IPN traité"})
            else:
                return jsonify({"status": "error", "message": "Paiement non confirmé"}), 400
        else:
            return jsonify({"status": "error", "message": "Token manquant"}), 400
    
    except Exception as e:
        print(f"❌ Erreur IPN: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# Route pour vérifier manuellement un paiement
@app.route('/api/payment/status/<payment_id>')
def payment_status(payment_id):
    """Vérifie le statut d'un paiement"""
    result = paytech_service.verify_payment(payment_id)
    
    if result['success']:
        return jsonify({
            "success": True,
            "status": result['status'],
            "amount": result.get('amount'),
            "currency": result.get('currency'),
            "customer": result.get('customer')
        })
    else:
        return jsonify({
            "success": False,
            "error": result['error']
        }), 400

# Autres routes API
@app.route('/api/update_settings', methods=['POST'])
def update_settings():
    data = request.json
    meter_id = session.get('current_meter')
    
    if not meter_id:
        return jsonify({"error": "Aucun compteur sélectionné"}), 400
    
    user_settings = load_user_settings()
    if meter_id not in user_settings:
        user_settings[meter_id] = {}
    
    user_settings[meter_id].update(data)
    
    if save_user_settings(user_settings):
        return jsonify({"success": True, "message": "Paramètres mis à jour"})
    else:
        return jsonify({"error": "Erreur lors de la sauvegarde"}), 500

@app.route('/api/export_excel')
def export_excel():
    meter_id = session.get('current_meter')
    if not meter_id:
        return jsonify({"error": "Aucun compteur sélectionné"}), 400
    
    consumption_data = load_consumption_data()
    if meter_id not in consumption_data:
        return jsonify({"error": "Compteur non trouvé"}), 404
    
    meter_data = consumption_data[meter_id]
    
    # Créer un fichier CSV
    output = StringIO()
    writer = csv.writer(output)
    
    # Écrire l'en-tête pour les données quotidiennes
    writer.writerow(['Date', 'Consommation (kWh)', 'Coût (FCFA)'])
    for day in meter_data['daily_data']:
        writer.writerow([day['date'], day['consumption_kwh'], day['cost']])
    
    writer.writerow([])  # Ligne vide
    writer.writerow(['Mois', 'Consommation (kWh)', 'Coût (FCFA)'])
    for month in meter_data['monthly_data']:
        writer.writerow([month['month'], month['consumption_kwh'], month['cost']])
    
    writer.writerow([])  # Ligne vide
    writer.writerow(['Résumé'])
    writer.writerow(['Compteur', meter_id])
    writer.writerow(['Client', meter_data['customer_name']])
    writer.writerow(['Solde Actuel', f"{meter_data['current_balance']} FCFA"])
    writer.writerow(['Consommation Jour', f"{meter_data['total_consumption']} kWh"])
    writer.writerow(['Dernière Mise à Jour', meter_data['last_update']])
    
    # Convertir en bytes pour le téléchargement
    output_str = output.getvalue()
    output_bytes = BytesIO(output_str.encode('utf-8'))
    
    filename = f"rapport_{meter_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    return send_file(
        output_bytes,
        mimetype='text/csv',
        as_attachment=True,
        download_name=filename
    )

@app.route('/api/consumption/<meter_id>')
def api_consumption(meter_id):
    consumption_data = load_consumption_data()
    
    if meter_id not in consumption_data:
        return jsonify({"error": "Compteur non trouvé"}), 404
    
    return jsonify(consumption_data[meter_id])

# Route pour régénérer manuellement les données
@app.route('/api/regenerate_data')
def api_regenerate_data():
    """Régénère manuellement les données"""
    if generate_consumption_data(100):
        return jsonify({"success": True, "message": "Données régénérées avec succès"})
    else:
        return jsonify({"error": "Erreur lors de la régénération"}), 500

if __name__ == '__main__':
    # Chargement/regénération automatique des données
    consumption_data = load_consumption_data()
    
    if consumption_data:
        print(f"✅ {len(consumption_data)} compteurs prêts")
        print("🌐 Application accessible")
        print("🎯 Compteurs de test: SENELEC_000001, SENELEC_000042, SENELEC_000099")
    
    # En production sur Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
