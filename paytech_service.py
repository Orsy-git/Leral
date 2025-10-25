# paytech_service.py
import requests
import json
import hashlib
import hmac
from config import Config

class PayTechService:
    def __init__(self):
        self.api_key = Config.PAYTECH_API_KEY
        self.api_secret = Config.PAYTECH_API_SECRET
        self.base_url = Config.PAYTECH_BASE_URL
    
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
        
        # Paramètres de base
        params = {
            'item_name': f"Recharge compteur {meter_id}",
            'item_price': amount,
            'currency': currency,
            'command_name': f"Recharge Leral - {meter_id}",
            'ref_command': f"LERAL_{meter_id}_{int(datetime.now().timestamp())}",
            'env': 'test',  # 'prod' pour la production
            'ipn_url': Config.PAYTECH_IPN_URL,
            'success_url': Config.PAYTECH_SUCCESS_URL,
            'cancel_url': Config.PAYTECH_CANCEL_URL,
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
                    'error': f"Erreur HTTP {response.status_code}"
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