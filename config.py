# config.py
import os

class Config:
    # Configuration PayTech
    PAYTECH_API_KEY = os.getenv('PAYTECH_API_KEY', '03c2e62e3f83d9c90bb4463df01a2e058c8e1fcb6a8d7821f89133e00dfd336d')
    PAYTECH_API_SECRET = os.getenv('PAYTECH_API_SECRET', '7cb40bc26529bca209932715131e5e53aaf40e5e936ce3cc7e5491a6df377862')
    PAYTECH_BASE_URL = os.getenv('PAYTECH_BASE_URL', 'https://paytech.sn')
    
    # URLs de callback
    PAYTECH_SUCCESS_URL = os.getenv('PAYTECH_SUCCESS_URL', 'http://localhost:5000/api/payment/success')
    PAYTECH_CANCEL_URL = os.getenv('PAYTECH_CANCEL_URL', 'http://localhost:5000/api/payment/cancel')
    PAYTECH_IPN_URL = os.getenv('PAYTECH_IPN_URL', 'http://localhost:5000/api/payment/ipn')