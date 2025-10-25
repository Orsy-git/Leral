import json
import random
from datetime import datetime, timedelta
import os

# Sources officielles référencées
SOURCES = {
    "senelec_tarifs_2024": "https://www.senelec.sn/tarifs",
    "ansd_energie_2023": "https://www.ansd.sn/",
    "banque_mondiale_2023": "https://data.worldbank.org/country/SN"
}

def generer_donnees_credibles(nb_compteurs=100):

    
    donnees = {}
    
    for i in range(1, nb_compteurs + 1):
        compteur_id = f"SENELEC_{str(i).zfill(6)}"
        
        # Répartition réaliste basée sur les stats Sénégal
        est_urbain = random.random() < 0.65  # 65% de population urbaine
        localisation = random.choice(["Dakar", "Pikine", "Guediawaye", "Rufisque"]) if est_urbain else random.choice(["Thiès", "Mbour", "Kaolack", "Saint-Louis"])
        
        # Consommation basée sur les données ANSD
        if est_urbain:
            conso_mensuelle = random.normalvariate(50, 15)  # 50 kWh/mois ±15
        else:
            conso_mensuelle = random.normalvariate(35, 10)  # 35 kWh/mois ±10
            
        # Application des tarifs Senelec
        if conso_mensuelle <= 50:
            tarif_kwh = 110  # Tranche sociale
        elif conso_mensuelle <= 100:
            tarif_kwh = 125  # Tranche normale
        else:
            tarif_kwh = 145  # Tranche supérieure
            
        donnees[compteur_id] = {
            "metadata": {
                "source_donnees": "Modélisation basée sur Senelec 2024 & ANSD 2023",
                "localisation": localisation,
                "type_zone": "urbaine" if est_urbain else "rurale",
                "date_generation": datetime.now().strftime("%Y-%m-%d"),
                "references": SOURCES
            },
            "caracteristiques": {
                "puissance_souscrite": random.choice([3, 6, 9]),
                "type_compteur": random.choice(["Monophasé", "Triphasé"]),
                "consommation_mensuelle_moyenne": round(conso_mensuelle, 2),
                "tarif_kwh": tarif_kwh
            },
            "donnees_simulation": generer_historique_realiste(conso_mensuelle, tarif_kwh)
        }
    
    return donnees

def generer_historique_realiste(conso_mensuelle, tarif_kwh):
    """Génère un historique de consommation réaliste"""
    # Votre code existant mais calibré sur les données réelles
    # ...
def generate_consumption_data(num_meters=100):
    """
    Génère des données de consommation simulées pour des compteurs
    """
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
        
    except Exception as e:
        print(f"❌ Erreur lors de la sauvegarde : {e}")

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

if __name__ == "__main__":
    # Générer seulement 100 compteurs pour tester
    generate_consumption_data(100)