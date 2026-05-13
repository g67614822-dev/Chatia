import requests
import datetime

def envoyer_sms(numero, message):
    try:
        res = requests.post('https://textbelt.com/text', {
            'phone': numero,
            'message': message,
            'key': 'textbelt' # 1 SMS gratuit/jour
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
        ville = "Antananarivo" # change pour ta ville
        try:
            res = requests.get(f"https://wttr.in/{ville}?format=3&lang=fr", timeout=5)
            return res.text.strip()
        except:
            return "Impossible de récupérer la météo."

    elif "recherche" in msg:
        query = msg.replace("recherche", "").strip()
        if not query:
            return "Tape : recherche [ton sujet]"
        try:
            url = f"https://api.duckgo.com/?q={query}&format=json&no_html=1&kl=fr-fr"
            res = requests.get(url, timeout=5)
            data = res.json()

            if data.get("Abstract"):
                return data["Abstract"]
            elif data.get("RelatedTopics"):
                for item in data["RelatedTopics"]:
                    if "Text" in item:
                        return item["Text"]
                return "Trouvé mais pas de résumé dispo."
            else:
                return "Rien trouvé pour : " + query
        except Exception as e:
            return f"Erreur de recherche : {e}"

    elif msg.startswith("sms "):
        # Format: sms +261341234567 message ici
        try:
            parties = msg.split(" ", 2)
            if len(parties) < 3:
                return "Format: sms +261341234567 ton message"
            numero = parties[1]
            texte = parties[2]
            return envoyer_sms(numero, texte)
        except Exception as e:
            return f"Erreur: {e}"

    elif "quitter" in msg or "exit" in msg:
        return "bye"

    else:
        return "Commandes: heure, date, meteo, recherche [sujet], sms +261... message, quitter"

print("Bot info lancé. Tape ta commande.")
while True:
    user = input("Toi: ")
    rep = repondre(user)
    print("Bot:", rep)
    if rep == "bye":
        print("À plus!")
        break
