import requests
import datetime

def repondre(message):
    msg = message.lower()

    if "heure" in msg:
        return f"Il est {datetime.datetime.now().strftime('%H:%M:%S')}"

    elif "date" in msg:
        return f"On est le {datetime.datetime.now().strftime('%d/%m/%Y')}"

    elif "météo" in msg:
        # Remplace Paris par ta ville
        ville = "Paris"
        try:
            res = requests.get(f"https://wttr.in/{ville}?format=3")
            return res.text.strip()
        except:
            return "Pas moyen de choper la météo."

    elif "recherche" in msg:
        # Ex: "recherche capitale france"
        query = msg.replace("recherche", "").strip()
        try:
            res = requests.get(f"https://api.duckgo.com/?q={query}&format=json&no_html=1")
            data = res.json()
            if data["Abstract"]:
                return data["Abstract"]
            elif data["RelatedTopics"]:
                return data["RelatedTopics"][0]["Text"]
            else:
                return "J'ai rien trouvé pour ça."
        except:
            return "Erreur de recherche."

    elif "exit" in msg:
        return "bye"

    else:
        return "Commandes: heure, date, météo, recherche [ta question], exit"

print("Bot info lancé. Exemples: météo, recherche capitale japon, heure")
while True:
    user = input("Toi: ")
    rep = repondre(user)
    print("Bot:", rep)
    if rep == "bye":
        break