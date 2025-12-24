import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# configuration
st.set_page_config(page_title="DASHBOARD EPL", layout="wide")

# chargement donnees
df_global = pd.read_csv("data/processed/dataset_notes_epl.csv")
df_global.columns = df_global.columns.str.lower()

# titre
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

    # indicateurs
    c1, c2, c3 = st.columns(3)
    c1.metric("Moyenne générale", round(df_f["note"].mean(), 2))
    c2.metric("Note minimale", df_f["note"].min())
    c3.metric("Note maximale", df_f["note"].max())

    # histogramme notes
    fig, ax = plt.subplots()
    ax.hist(df_f["note"], bins=20, color="skyblue", edgecolor="black")
    ax.set_xlabel("Notes")
    ax.set_ylabel("Effectif")
    st.pyplot(fig)

    # repartition parcours
    repartition = df_global.groupby("nom_parcours")["id_etudiant"].nunique()
    fig, ax = plt.subplots()
    ax.pie(repartition, labels=repartition.index, autopct="%1.1f%%")
    st.pyplot(fig)

# statistiques
elif menu == "Statistiques":

    # statistiques par matiere
    stats = (
        df_f.groupby("nom_matiere")["note"]
        .agg(["mean", "median", "std", "count"])
        .reset_index()
    )

    stats.columns = ["Matière", "Moyenne", "Médiane", "Écart-type", "Nombre de notes"]
    st.dataframe(stats)

    # export statistiques
    st.download_button(
        "📥 Télécharger les statistiques par matière (CSV)",
        stats.to_csv(index=False).encode("utf-8"),
        "statistiques_par_matiere.csv",
        "text/csv"
    )

    # histogramme notes
    fig, ax = plt.subplots()
    ax.hist(df_f["note"], bins=20, color="lightgreen", edgecolor="black")
    ax.set_xlabel("Notes")
    ax.set_ylabel("Effectif")
    st.pyplot(fig)

    # taux de reussite
    taux = (
        df_f.assign(reussi=df_f["note"] >= 10)
        .groupby("nom_matiere")["reussi"]
        .mean() * 100
    ).reset_index()

    taux.columns = ["Matière", "Taux de réussite (%)"]
    taux["Taux de réussite (%)"] = taux["Taux de réussite (%)"].round(2)
    st.dataframe(taux)

    # export taux
    st.download_button(
        "📥 Télécharger le taux de réussite (CSV)",
        taux.to_csv(index=False).encode("utf-8"),
        "taux_reussite_par_matiere.csv",
        "text/csv"
    )

# visualisations
elif menu == "Visualisations":

    # barres moyennes
    moyennes = (
        df_f.groupby("nom_matiere")["note"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(moyennes.index, moyennes.values, color=plt.cm.tab10(range(len(moyennes))))
    ax.set_ylabel("Moyenne")
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # boxplot
    fig, ax = plt.subplots(figsize=(12, 5))
    df_f[df_f["nom_matiere"].isin(moyennes.index)] \
        .boxplot(column="note", by="nom_matiere", ax=ax, rot=45)
    plt.suptitle("")
    st.pyplot(fig)

    # matrice de correlation
    df_corr = df_f.copy()
    df_corr["moyenne_matiere"] = df_corr.groupby("nom_matiere")["note"].transform("mean")
    df_corr["moyenne_enseignant"] = df_corr.groupby("nom_enseignant")["note"].transform("mean")

    corr = df_corr[["note", "moyenne_matiere", "moyenne_enseignant"]].corr()

    fig, ax = plt.subplots()
    cax = ax.matshow(corr, cmap="coolwarm")
    fig.colorbar(cax)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45)
    ax.set_yticklabels(corr.columns)
    st.pyplot(fig)

    # nuage de points
    fig, ax = plt.subplots()
    ax.scatter(
        df_corr["moyenne_matiere"],
        df_corr["note"],
        alpha=0.5
    )
    ax.set_xlabel("Moyenne de la matière")
    ax.set_ylabel("Note de l’étudiant")
    ax.set_title("Nuage de points : note vs moyenne par matière")
    st.pyplot(fig)

    # courbe cumulative
    notes_sorted = np.sort(df_f["note"])
    cumulative = np.arange(1, len(notes_sorted) + 1) / len(notes_sorted)

    fig, ax = plt.subplots()
    ax.plot(notes_sorted, cumulative)
    ax.set_xlabel("Note")
    ax.set_ylabel("Proportion cumulée")
    st.pyplot(fig)

# classements
elif menu == "Classements":

    # top 10 etudiants
    top10 = (
        df_f.groupby(["id_etudiant", "nom"])["note"]
        .mean()
        .reset_index()
        .sort_values("note", ascending=False)
        .head(10)
    )

    top10.columns = ["ID Étudiant", "Nom", "Moyenne"]
    st.dataframe(top10)

    # export top 10
    st.download_button(
        "📥 Télécharger le Top 10 des étudiants (CSV)",
        top10.to_csv(index=False).encode("utf-8"),
        "top_10_etudiants.csv",
        "text/csv"
    )

    # classement enseignants
    perf = (
        df_f.groupby("nom_enseignant")["note"]
        .mean()
        .reset_index()
        .sort_values("note", ascending=False)
    )

    perf.columns = ["Nom enseignant", "Moyenne"]
    st.dataframe(perf)

# espace etudiant
elif menu == "Espace étudiant":

    id_etu = st.text_input("Entrer votre identifiant étudiant")

    if id_etu:
        etu = df_global[df_global["id_etudiant"].astype(str) == id_etu]

        if etu.empty:
            st.error("Identifiant étudiant introuvable.")
        else:
            st.success("Étudiant trouvé")
            st.write(f"**Nom :** {etu.iloc[0]['nom']}")
            st.write(f"**Parcours :** {etu.iloc[0]['nom_parcours']}")

            notes_etu = etu[["nom_matiere", "note"]]
            notes_etu.columns = ["Matière", "Note"]
            st.dataframe(notes_etu)

            st.metric("Moyenne générale", round(etu["note"].mean(), 2))
            st.info(f"Nombre de notes disponibles : {len(notes_etu)}")
