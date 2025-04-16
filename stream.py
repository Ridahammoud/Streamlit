import streamlit as st
import pandas as pd
from datetime import datetime
import os

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
