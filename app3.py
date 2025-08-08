import streamlit as st
import pandas as pd
import plotly.express as px

# ===================== CONFIGURATION =====================
st.set_page_config(
    page_title="📘 Loi de Finances 2025 - Côte d'Ivoire",
    layout="wide",
    page_icon="📊"
)

# ===================== CHARGEMENT DES DONNÉES =====================
@st.cache_data
def load_data():
    df = pd.read_excel("Loi de finance 2025_2.xlsx", sheet_name="Budget")
    df.columns = df.columns.str.strip()  # nettoyer noms colonnes
    return df

df = load_data()

# ===================== TITRE ET DESCRIPTION =====================
st.title("📘 Loi de Finances 2025 - Côte d’Ivoire")
st.markdown("""
Analyse interactive et citoyenne du budget national : **recettes**, **dépenses** et **répartition par catégories**.
Utilisez les filtres à gauche pour explorer les données et répondre à vos questions.
""")

# ===================== BARRE LATERALE - FILTRES =====================
st.sidebar.header("🔎 Filtres interactifs")

type_choix = st.sidebar.multiselect(
    "Type de ligne budgétaire (Nom indicateur 2)",
    options=df["Nom indicateur 2"].dropna().unique(),
    default=df["Nom indicateur 2"].dropna().unique()
)

categorie_choix = st.sidebar.multiselect(
    "Catégorie budgétaire (Nom indicateur 5)",
    options=df["Nom indicateur 5"].dropna().unique(),
    default=df["Nom indicateur 5"].dropna().unique()
)

annee_choix = st.sidebar.multiselect(
    "Année",
    options=df["Annee"].dropna().unique(),
    default=df["Annee"].dropna().unique()
)

# ===================== APPLICATION DES FILTRES =====================
df_filtre = df[
    (df["Nom indicateur 2"].isin(type_choix)) &
    (df["Nom indicateur 5"].isin(categorie_choix)) &
    (df["Annee"].isin(annee_choix))
]

# ===================== KPI - INDICATEURS CLÉS =====================
total_budget = df_filtre["Valeur"].sum()
total_recettes = df_filtre[df_filtre["Nom indicateur 4"] == "RESSOURCES"]["Valeur"].sum()
total_depenses = df_filtre[df_filtre["Nom indicateur 4"] == "DEPENSES"]["Valeur"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Budget total", f"{total_budget:,.0f} FCFA")
col2.metric("📈 Total recettes", f"{total_recettes:,.0f} FCFA")
col3.metric("📉 Total dépenses", f"{total_depenses:,.0f} FCFA")

st.markdown("---")

# ===================== VISUALISATIONS =====================
col_g1, col_g2 = st.columns(2)

# Graphique 1 : Camembert par catégorie
with col_g1:
    fig1 = px.pie(
        df_filtre,
        names="Nom indicateur 5",
        values="Valeur",
        title="Répartition du budget par catégorie",
        color_discrete_sequence=px.colors.sequential.Blues
    )
    st.plotly_chart(fig1, use_container_width=True)

# Graphique 2 : Barres par sous-catégorie
with col_g2:
    fig2 = px.bar(
        df_filtre,
        x="Nom indicateur 6",
        y="Valeur",
        color="Nom indicateur 4",
        barmode="group",
        title="Répartition par sous-catégorie",
        color_discrete_map={"RESSOURCES": "#2ca02c", "DEPENSES": "#d62728"}
    )
    st.plotly_chart(fig2, use_container_width=True)

# ===================== COURBE PAR ANNÉE =====================
if len(df_filtre["Annee"].unique()) > 1:
    fig3 = px.line(
        df_filtre.groupby(["Annee", "Nom indicateur 4"])["Valeur"].sum().reset_index(),
        x="Annee",
        y="Valeur",
        color="Nom indicateur 4",
        markers=True,
        title="Évolution des ressources et dépenses par année"
    )
    st.plotly_chart(fig3, use_container_width=True)

# ===================== TABLEAU DETAIL =====================
st.subheader("🧾 Données détaillées")
st.dataframe(df_filtre)

# ===================== EXPORT CSV =====================
st.download_button(
    label="📥 Télécharger les données filtrées",
    data=df_filtre.to_csv(index=False).encode("utf-8"),
    file_name="donnees_filtrees.csv",
    mime="text/csv"
)

# ===================== SOURCE =====================
st.markdown("---")
st.markdown("**Source :** Loi de finance n° 2024-1109 du 18 décembre 2024")
