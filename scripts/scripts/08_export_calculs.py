import pandas as pd
import numpy as np
import os

# chemins
DATASET_PATH = "data/processed/dataset_notes_epl.csv"
EXPORT_PATH = "data/exports"

# creation dossier export
os.makedirs(EXPORT_PATH, exist_ok=True)

# chargement
df = pd.read_csv(DATASET_PATH)
df.columns = df.columns.str.lower()

# statistiques par matiere
stats_matiere = (
    df.groupby("nom_matiere")["note"]
    .agg(["mean", "median", "std", "count"])
    .reset_index()
)

stats_matiere.columns = [
    "matiere", "moyenne", "mediane", "ecart_type", "nombre_notes"
]

stats_matiere.to_csv(
    f"{EXPORT_PATH}/statistiques_par_matiere.csv",
    index=False
)

# taux de reussite par matiere
taux_reussite = (
    df.assign(reussi=df["note"] >= 10)
    .groupby("nom_matiere")["reussi"]
    .mean() * 100
).reset_index()

taux_reussite.columns = ["matiere", "taux_reussite"]

taux_reussite.to_csv(
    f"{EXPORT_PATH}/taux_reussite_par_matiere.csv",
    index=False
)

# moyenne par parcours
moyenne_parcours = (
    df.groupby("nom_parcours")["note"]
    .mean()
    .reset_index()
)

moyenne_parcours.columns = ["parcours", "moyenne"]

moyenne_parcours.to_csv(
    f"{EXPORT_PATH}/moyenne_par_parcours.csv",
    index=False
)

# top 10 etudiants
top10 = (
    df.groupby(["id_etudiant", "nom"])["note"]
    .mean()
    .reset_index()
    .sort_values("note", ascending=False)
    .head(10)
)

top10.columns = ["id_etudiant", "nom", "moyenne"]

top10.to_csv(
    f"{EXPORT_PATH}/top_10_etudiants.csv",
    index=False
)

# export numpy
np.save(
    f"{EXPORT_PATH}/moyennes_notes.npy",
    df["note"].values
)

print("exports termines avec succes")
