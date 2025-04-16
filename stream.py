import streamlit as st
import pandas as pd
from datetime import datetime
import os
import requests
import streamlit.components.v1 as components

client_id = "cc_classic_yYZ7nkTZeRyAgE2y5X8JkKyJ5rdg"
client_secret = "cc_sk_classic_DOxZ12IT3NqMNmPO90O7rrAIKoJ2zJOhnH8tQI6yL59EIHySPW"

response = requests.post(
    "https://api.sumup.com/token",
    auth=(client_id, client_secret),
    data={
        "grant_type": "client_credentials"
    }
)

if response.status_code == 200:
    token = response.json()["access_token"]
    print("ACCESS_TOKEN =", token)
else:
    print("Erreur :", response.status_code, response.text)


# Paramètres SumUp (à personnaliser)
ACCESS_TOKEN = ""  # 🔐 À remplacer par le tien
CALLBACK_URL = "https://api.sumup.com"  # 🔄 Redirection après paiement
SUMUP_EMAIL = "ton-email-sumup@example.com"  # 📧 Ton email marchand SumUp

# 🔗 Fonction pour créer le lien de paiement
def creer_lien_paiement(prix, nom_client):
    url = "https://api.sumup.com/v0.1/checkouts"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "checkout_reference": f"commande-{datetime.now().timestamp()}",
        "amount": prix,
        "currency": "EUR",
        "pay_to_email": SUMUP_EMAIL,
        "description": f"Commande de {nom_client}",
        "return_url": CALLBACK_URL
    }
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        return response.json()["checkout_url"]
    else:
        st.error("Erreur lors de la création du lien de paiement.")
        st.write(response.text)
        return None

# 🛒 Interface client
st.title("Formulaire de commande")

# Infos client
pseudo = st.text_input("Pseudo TikTok")
nom = st.text_input("Nom")
prenom = st.text_input("Prénom")
tel = st.text_input("Téléphone N°")
email = st.text_input("Email")
adresse = st.text_area("Adresse de livraison")

# Produits
produits = {
    "Produit A": 20,
    "Produit B": 30,
    "Produit C": 15
}
produit_choisi = st.selectbox("Produit", list(produits.keys()))
quantite = st.number_input("Quantité", min_value=1, value=1)

# ✅ Validation commande
if st.button("Valider la commande"):
    if not nom or not email or not adresse:
        st.warning("Merci de remplir tous les champs.")
    else:
        commande = {
            "datetime": datetime.now().isoformat(),
            "pseudo": pseudo,
            "nom": nom,
            "prenom": prenom,
            "tel": tel,
            "email": email,
            "adresse": adresse,
            "produit": produit_choisi,
            "quantite": quantite,
            "prix_total": produits[produit_choisi] * quantite,
            "payé": False
        }

        # 💾 Sauvegarde dans le CSV
        if os.path.exists("commandes.csv"):
            df = pd.read_csv("commandes.csv")
        else:
            df = pd.DataFrame()

        df = pd.concat([df, pd.DataFrame([commande])], ignore_index=True)
        df.to_csv("commandes.csv", index=False)

        # 🔗 Création lien SumUp
        lien_paiement = creer_lien_paiement(commande["prix_total"], nom)

        if lien_paiement:
            st.success("Commande enregistrée ! Redirection vers le paiement en cours...")
            components.html(f"""
                <script>
                    window.location.href = "{lien_paiement}";
                </script>
            """)
        else:
            st.error("Impossible de générer le lien de paiement.")
