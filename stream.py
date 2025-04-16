import streamlit as st
import pandas as pd
from datetime import datetime
import os
import requests

st.title("Formulaire de commande")

# Données du client
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

# Bouton de validation
if st.button("Valider la commande"):
    if not nom or not email or not adresse:
        st.warning("Merci de remplir tous les champs.")
    else:
        commande = {
            "datetime": datetime.now().isoformat(),
            "nom": nom,
            "email": email,
            "adresse": adresse,
            "produit": produit_choisi,
            "quantite": quantite,
            "prix_total": produits[produit_choisi] * quantite,
            "payé": False  # Par défaut
        }

        # Création du fichier CSV si nécessaire
        path_csv = "commandes.csv"
        if os.path.exists(path_csv):
            df = pd.read_csv(path_csv)
        else:
            df = pd.DataFrame()

        df = pd.concat([df, pd.DataFrame([commande])], ignore_index=True)
        df.to_csv(path_csv, index=False)

        st.success("Commande enregistrée ! Vous allez être redirigé vers le paiement ensuite.")

# Paramètres SumUp
ACCESS_TOKEN = "TON_ACCESS_TOKEN_SUMUP"  # remplace par le tien
CALLBACK_URL = "https://tonapp.com/merci"  # URL vers laquelle rediriger le client après paiement

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
        "pay_to_email": "ton-email-sumup@example.com",  # ton email marchand SumUp
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

