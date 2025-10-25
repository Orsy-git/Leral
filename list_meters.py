import json

def list_available_meters():
    try:
        with open('data/consumption_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("📊 COMPTEURS DISPONIBLES 📊")
        print("=" * 50)
        
        meters = list(data.keys())
        
        # Afficher les 10 premiers compteurs
        for i, meter_id in enumerate(meters[:10], 1):
            meter_data = data[meter_id]
            print(f"{i}. {meter_id}")
            print(f"   👤 Client: {meter_data['customer_name']}")
            print(f"   ⚡ Type: {meter_data['meter_type']}")
            print(f"   💰 Solde: {meter_data['current_balance']} FCFA")
            print(f"   🔌 Consommation: {meter_data['total_consumption']} kWh")
            print()
        
        print(f"📈 Total de {len(meters)} compteurs générés")
        print("\n💡 Conseil: Utilisez SENELEC_000001 pour tester")
        
    except FileNotFoundError:
        print("❌ Le fichier de données n'existe pas. Exécutez d'abord:")
        print("   python generate_data.py")

if __name__ == "__main__":
    list_available_meters()