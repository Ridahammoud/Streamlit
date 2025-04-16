import streamlit as st
import pandas as pd
import os

# ---------- CONFIG ----------
PASSWORD = "admin123"  # Change ce mot de passe !

CSV_PATH = "commandes.csv"

# ---------- FONCTIONS ----------
def charger_commandes():
    if os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH)
    return pd.DataFrame()

def enregistrer_commandes(df):
    df.to_csv(CSV_PATH, index=False)

# ---------- AUTH ----------
st.title("Interface Administrateur")

mdp = st.text_input("Mot de passe", type="password")
if mdp != PASSWORD:
    st.warning("Accès restreint. Entrez le bon mot de passe.")
    st.stop()

# ---------- CHARGEMENT ----------
df = charger_commandes()
if df.empty:
    st.info("Aucune commande enregistrée.")
    st.stop()

# ---------- FILTRAGE ----------
st.sidebar.header("Filtres")
produits = st.sidebar.multiselect("Produits", options=df["produit"].unique(), default=df["produit"].unique())
clients = st.sidebar.multiselect("Clients", options=df["nom"].unique(), default=df["nom"].unique())
paiement = st.sidebar.selectbox("Statut de paiement", ["Tous", "Payés", "Non payés"])

filtre = df[
    (df["produit"].isin(produits)) &
    (df["nom"].isin(clients))
]

if paiement == "Payés":
    filtre = filtre[filtre["payé"] == True]
elif paiement == "Non payés":
    filtre = filtre[filtre["payé"] == False]

# ---------- AFFICHAGE TABLE ----------
st.subheader("Commandes filtrées")
filtre["payé"] = filtre["payé"].astype(bool)
st.dataframe(filtre, use_container_width=True)

# ---------- GROUP BY ----------
st.subheader("Groupement")
group_option = st.selectbox("Grouper par", ["Aucun", "Client", "Produit"])

if group_option == "Client":
    group = filtre.groupby("nom")[["prix_total", "quantite"]].sum().reset_index()
    st.dataframe(group)
elif group_option == "Produit":
    group = filtre.groupby("produit")[["quantite", "prix_total"]].sum().reset_index()
    st.dataframe(group)

# ---------- MARQUER COMME PAYÉ ----------
st.subheader("Mettre à jour le statut de paiement")
with st.form("form_paiement"):
    commandes_a_marquer = st.multiselect("Commandes à marquer comme payées", options=filtre.index, format_func=lambda x: f"{filtre.loc[x, 'nom']} - {filtre.loc[x, 'produit']}")
    submit = st.form_submit_button("Mettre à jour")
    if submit:
        for i in commandes_a_marquer:
            df.loc[i, "payé"] = True
        enregistrer_commandes(df)
        st.success("Commandes mises à jour.")
