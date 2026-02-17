import os
import requests
import logging

logger = logging.getLogger(__name__)

def send_order_email(order_number, customer_name, customer_email, customer_address, customer_zip, customer_city, quantity, price):
    """
    Sendet eine Bestellbestätigung über Mailgun an den Admin
    
    Args:
        order_number: Bestellnummer
        customer_name: Name des Kunden
        customer_email: E-Mail des Kunden
        customer_address: Adresse des Kunden
        customer_zip: PLZ des Kunden
        customer_city: Stadt des Kunden
        quantity: Menge bestellt
        price: Preis pro Artikel
        
    Returns:
        dict: Status und Nachricht
    """
    try:
        mailgun_api_key = os.environ.get('MAILGUN_API_KEY')
        mailgun_domain = os.environ.get('MAILGUN_DOMAIN')
        mailgun_from = os.environ.get('MAILGUN_FROM')
        flask_env = os.environ.get('FLASK_ENV', 'production')
        
        logger.info(f"Starting email send: API_KEY={'***' if mailgun_api_key else 'MISSING'}, Domain={mailgun_domain}, Admin Email={mailgun_from}")
        
        if not mailgun_api_key or not mailgun_domain or not mailgun_from:
            error_msg = f'Mailgun-Konfiguration fehlt: Key={bool(mailgun_api_key)}, Domain={bool(mailgun_domain)}, Email={bool(mailgun_from)}'
            logger.error(error_msg)
            return {
                'success': False,
                'message': error_msg
            }
        
        # Mailgun API URL
        url = f"https://api.mailgun.net/v3/{mailgun_domain}/messages"
        
        # Gesamtpreis berechnen
        total_price = quantity * price
                
        # Modernes HTML E-Mail Design
        email_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 0; background: linear-gradient(180deg, #0d0d0d 0%, #1a1a1a 100%); font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0" style="padding: 60px 20px;">
        <tr>
            <td align="center">
                <!-- Main Container -->
                <table width="520" cellpadding="0" cellspacing="0" style="background: linear-gradient(145deg, #141414 0%, #0a0a0a 100%); border-radius: 24px; overflow: hidden; border: 1px solid rgba(245, 136, 0, 0.15);">
                    
                    <!-- Logo Section -->
                    <tr>
                        <td style="padding: 50px 40px 30px 40px; text-align: center;">
                            <div style="display: inline-block; background: linear-gradient(135deg, #F58800 0%, #ff9500 50%, #F58800 100%); padding: 16px 32px; border-radius: 50px;">
                                <span style="color: #000000; font-size: 20px; font-weight: 800; letter-spacing: 4px;">DESKDUNK</span>
                            </div>
                        </td>
                    </tr>
                    
                    <!-- Success Icon -->
                    <tr>
                        <td style="text-align: center; padding: 10px 40px;">
                            <div style="width: 80px; height: 80px; margin: 0 auto; background: linear-gradient(135deg, rgba(245, 136, 0, 0.2) 0%, rgba(245, 136, 0, 0.05) 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center;">
                                <span style="font-size: 40px; line-height: 80px;">✓</span>
                            </div>
                        </td>
                    </tr>
                    
                    <!-- Greeting -->
                    <tr>
                        <td style="padding: 30px 40px 10px 40px; text-align: center;">
                            <h1 style="margin: 0; color: #ffffff; font-size: 28px; font-weight: 600; letter-spacing: -0.5px;">Bestellung bestätigt!</h1>
                        </td>
                    </tr>
                    
                    <tr>
                        <td style="padding: 10px 40px 30px 40px; text-align: center;">
                            <p style="margin: 0; color: #888888; font-size: 15px; line-height: 1.6;">
                                Hey {customer_name}, danke für deine Bestellung.<br>Wir machen uns direkt an die Arbeit! 🚀
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Order Number Card -->
                    <tr>
                        <td style="padding: 0 40px 25px 40px;">
                            <table width="100%" cellpadding="0" cellspacing="0" style="background: linear-gradient(135deg, #F58800 0%, #ff6b00 100%); border-radius: 16px;">
                                <tr>
                                    <td style="padding: 25px; text-align: center;">
                                        <p style="margin: 0 0 8px 0; color: rgba(0,0,0,0.6); font-size: 11px; text-transform: uppercase; letter-spacing: 2px; font-weight: 600;">Bestellnummer</p>
                                        <p style="margin: 0; color: #000000; font-size: 32px; font-weight: 700; letter-spacing: 1px;">#{order_number}</p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Order Summary -->
                    <tr>
                        <td style="padding: 0 40px 25px 40px;">
                            <table width="100%" cellpadding="0" cellspacing="0" style="background: rgba(255,255,255,0.03); border-radius: 16px; border: 1px solid rgba(255,255,255,0.06);">
                                <tr>
                                    <td style="padding: 20px 25px 15px 25px;">
                                        <p style="margin: 0; color: #666666; font-size: 11px; text-transform: uppercase; letter-spacing: 2px; font-weight: 600;">Zusammenfassung</p>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding: 0 25px;">
                                        <table width="100%" cellpadding="0" cellspacing="0">
                                            <tr>
                                                <td style="padding: 12px 0; color: #999999; font-size: 14px; border-bottom: 1px solid rgba(255,255,255,0.05);">Artikel</td>
                                                <td style="padding: 12px 0; color: #ffffff; font-size: 14px; text-align: right; border-bottom: 1px solid rgba(255,255,255,0.05);">{quantity}× DeskDunk</td>
                                            </tr>
                                            <tr>
                                                <td style="padding: 12px 0; color: #999999; font-size: 14px; border-bottom: 1px solid rgba(255,255,255,0.05);">Einzelpreis</td>
                                                <td style="padding: 12px 0; color: #ffffff; font-size: 14px; text-align: right; border-bottom: 1px solid rgba(255,255,255,0.05);">€{price:.2f}</td>
                                            </tr>
                                            <tr>
                                                <td style="padding: 18px 0 20px 0; color: #ffffff; font-size: 16px; font-weight: 600;">Gesamt</td>
                                                <td style="padding: 18px 0 20px 0; color: #F58800; font-size: 22px; font-weight: 700; text-align: right;">€{total_price:.2f}</td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Shipping Address -->
                    <tr>
                        <td style="padding: 0 40px 40px 40px;">
                            <table width="100%" cellpadding="0" cellspacing="0" style="background: rgba(255,255,255,0.03); border-radius: 16px; border: 1px solid rgba(255,255,255,0.06);">
                                <tr>
                                    <td style="padding: 20px 25px 15px 25px;">
                                        <p style="margin: 0; color: #666666; font-size: 11px; text-transform: uppercase; letter-spacing: 2px; font-weight: 600;">📦 Lieferung an</p>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding: 0 25px 20px 25px;">
                                        <p style="margin: 0; color: #ffffff; font-size: 15px; line-height: 1.7; font-weight: 500;">{customer_name}</p>
                                        <p style="margin: 5px 0 0 0; color: #888888; font-size: 14px; line-height: 1.6;">{customer_address}<br>{customer_zip} {customer_city}</p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Divider -->
                    <tr>
                        <td style="padding: 0 40px;">
                            <div style="height: 1px; background: linear-gradient(90deg, transparent 0%, rgba(245,136,0,0.3) 50%, transparent 100%);"></div>
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="padding: 35px 40px 45px 40px; text-align: center;">
                            <p style="margin: 0 0 15px 0; color: #555555; font-size: 13px;">
                                Fragen? Einfach auf diese Mail antworten.
                            </p>
                            <p style="margin: 0; color: #333333; font-size: 11px;">
                                © 2026 DESKDUNK · Made with 🏀 in Switzerland
                            </p>
                        </td>
                    </tr>
                    
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
"""
        
        # API-Request absenden
        logger.info(f"Sending POST request to: {url}")
        response = requests.post(
            url,
            auth=("api", mailgun_api_key),
            data={
                "from": f"DESKDUNK <noreply@{mailgun_domain}>",
                "to": customer_email,
                "subject": f"Bestellbestätigung #{order_number} - DESKDUNK",
                "html": email_html,
                "reply-to": mailgun_from
            }
        )
        
        logger.info(f"Response Status: {response.status_code}")
        logger.info(f"Response Body: {response.text}")
        
        if response.status_code == 200:
            logger.info(f"✅ Email sent successfully for order #{order_number}")
            return {
                'success': True,
                'message': 'Bestellbestätigung versendet'
            }
        else:
            error_msg = f'Fehler beim Versenden: {response.status_code} - {response.text}'
            logger.error(error_msg)
            return {
                'success': False,
                'message': error_msg
            }
            
    except Exception as e:
        error_msg = f'Exception: {str(e)}'
        logger.error(error_msg)
        return {
            'success': False,
            'message': error_msg
        }

