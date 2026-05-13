import requests
import datetime

def envoyer_sms(numero, message):
    try:
        res = requests.post('https://textbelt.com/text', {
            'phone': numero,
            'message': message,
            'key': 'textbelt'  # 1 SMS gratuit/jour
        }, timeout=10)
        data = res.json()
        if data.get('success'):
            return f"SMS envoyé à {numero}. ID: {data.get('textId')}"
        else:
            return f"Echec: {data.get('error', 'Inconnu')}"
    except Exception as e:
        return f"Erreur réseau: {e}"

def repondre(message):
    msg = message.lower().strip()

    if "heure" in msg:
        return f"Il est {datetime.datetime.now().strftime('%H:%M:%S')}"

    elif "date" in msg:
        return f"On est le {datetime.datetime.now().strftime('%d/%m/%Y')}"

    elif "meteo" in msg:
        ville = "Antananarivo"  # change pour ta ville
        try:
            res = requests.get(f"https://wttr.in/{ville}?format=3&lang=fr", timeout=5)
            return res.text.strip()
       
