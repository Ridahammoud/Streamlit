import streamlit as st
import pandas as pd
from datetime import datetime
import os
import requests

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
            "payé": False
        }

        # Enregistrement dans le CSV...
        # (code que tu as déjà mis pour ajouter la commande)

        # 🔐 Création du lien SumUp
        lien_paiement = creer_lien_paiement(commande["prix_total"], nom)

        if lien_paiement:
            st.success("Commande enregistrée ! Redirection vers le paiement en cours...")

            import streamlit.components.v1 as components
            components.html(f"""
                <script>
                    window.location.href = "{lien_paiement}";
                </script>
            """)


# Script pour redirection
js = f"""
<script>
    window.location.href = "{lien_paiement}";
</script>
"""
st.components.v1.html(js)

# Paramètres SumUp
ACCESS_TOKEN = "TON_ACCESS_TOKEN_SUMUP"  # remplace par le tien
CALLBACK_URL = "https://tonapp.com/merci"  # URL vers laquelle rediriger le client après paiement


