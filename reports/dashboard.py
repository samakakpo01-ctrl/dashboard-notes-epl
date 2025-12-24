import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# configuration
st.set_page_config(page_title="DASHBOARD EPL", layout="wide")

# chargement
df_global = pd.read_csv("data/processed/dataset_notes_epl.csv")

# normalisation
df_global.columns = df_global.columns.str.lower()

# titre principal
st.title("📊 DASHBOARD D’ANALYSE DES NOTES DE L’EPL")

# menu
menu = st.sidebar.radio(
    "Menu",
    [
        "Vue globale",
        "Statistiques",
        "Visualisations",
        "Classements",
        "Espace étudiant"
    ]
)

# filtres
st.sidebar.subheader("Filtres")

parcours_select = st.sidebar.selectbox(
    "Parcours",
    ["Tous"] + sorted(df_global["nom_parcours"].dropna().unique().tolist())
)

df_f = df_global.copy()
if parcours_select != "Tous":
    df_f = df_f[df_f["nom_parcours"] == parcours_select]

# vue globale
if menu == "Vue globale":

    st.subheader("Indicateurs clés")

    c1, c2, c3 = st.columns(3)
    c1.metric("Moyenne générale", round(df_f["note"].mean(), 2))
    c2.metric("Note minimale", df_f["note"].min())
    c3.metric("Note maximale", df_f["note"].max())

    st.subheader("Histogramme global des notes")

    fig, ax = plt.subplots()
    ax.hist(df_f["note"], bins=20)
    ax.set_xlabel("Notes")
    ax.set_ylabel("Effectif")
    st.pyplot(fig)

    st.subheader("Répartition des étudiants par parcours")

    repartition = df_global.groupby("nom_parcours")["id_etudiant"].nunique()
    fig, ax = plt.subplots()
    ax.pie(repartition, labels=repartition.index, autopct="%1.1f%%")
    st.pyplot(fig)

# statistiques
elif menu == "Statistiques":

    st.subheader("Statistiques descriptives par matière")

    stats = (
        df_f.groupby("nom_matiere")["note"]
        .agg(["mean", "median", "std", "count"])
        .reset_index()
    )

    stats.columns = [
        "Matière", "Moyenne", "Médiane", "Écart-type", "Nombre de notes"
    ]

    st.dataframe(stats)

    st.subheader("Histogramme des notes (statistiques)")

    fig, ax = plt.subplots()
    ax.hist(df_f["note"], bins=20)
    ax.set_xlabel("Notes")
    ax.set_ylabel("Effectif")
    st.pyplot(fig)

    st.subheader("Taux de réussite par matière (%)")

    taux = (
        df_f.assign(reussi=df_f["note"] >= 10)
        .groupby("nom_matiere")["reussi"]
        .mean() * 100
    ).reset_index()

    taux.columns = ["Matière", "Taux de réussite (%)"]
    taux["Taux de réussite (%)"] = taux["Taux de réussite (%)"].round(2)

    st.dataframe(taux)

# visualisations
elif menu == "Visualisations":

    st.subheader("Histogramme des notes")

    fig, ax = plt.subplots()
    ax.hist(df_f["note"], bins=20)
    st.pyplot(fig)

    st.subheader("Boxplot des notes par matière (Top 10)")

    top_matieres = (
        df_f.groupby("nom_matiere")["note"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .index
    )

    fig, ax = plt.subplots(figsize=(12, 5))
    df_f[df_f["nom_matiere"].isin(top_matieres)] \
        .boxplot(column="note", by="nom_matiere", ax=ax, rot=45)

    plt.suptitle("")
    st.pyplot(fig)

    st.subheader("Diagramme en barres – Moyenne par matière (Top 10)")

    moyennes = (
        df_f.groupby("nom_matiere")["note"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(12, 5))
    moyennes.plot(kind="bar", ax=ax)
    ax.set_ylabel("Moyenne")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.subheader("Nuage de points – Notes par étudiant")

    fig, ax = plt.subplots()
    ax.scatter(df_f["id_etudiant"], df_f["note"], alpha=0.4)
    ax.set_xlabel("Étudiants")
    ax.set_ylabel("Notes")
    st.pyplot(fig)

# classements
elif menu == "Classements":

    st.subheader("Top 10 des étudiants")

    top10 = (
        df_f.groupby(["id_etudiant", "nom"])["note"]
        .mean()
        .reset_index()
        .sort_values("note", ascending=False)
        .head(10)
    )

    top10.columns = ["ID Étudiant", "Nom", "Moyenne"]
    st.dataframe(top10)

    st.subheader("Classement des enseignants")

    perf = (
        df_f.groupby("nom_enseignant")["note"]
        .mean()
        .reset_index()
        .sort_values("note", ascending=False)
    )

    perf.columns = ["Nom enseignant", "Moyenne"]
    st.dataframe(perf)

# espace étudiant
elif menu == "Espace étudiant":

    st.subheader("Consultation individuelle des notes")

    id_etu = st.text_input("Entrer votre identifiant étudiant")

    if id_etu:
        etu = df_global[df_global["id_etudiant"].astype(str) == id_etu]

        if etu.empty:
            st.error("Identifiant étudiant introuvable.")
        else:
            st.success("Étudiant trouvé")

            st.write(
                f"**Nom :** {etu.iloc[0]['nom']}  \n"
                f"**Parcours :** {etu.iloc[0]['nom_parcours']}"
            )

            notes_etu = etu[["nom_matiere", "note"]]
            notes_etu.columns = ["Matière", "Note"]
            st.dataframe(notes_etu)

            st.metric(
                "Moyenne générale",
                round(etu["note"].mean(), 2)
            )

            st.info(f"Nombre de notes disponibles : {len(notes_etu)}")
