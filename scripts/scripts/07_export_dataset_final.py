import pandas as pd

# charger les fichiers
etudiants = pd.read_csv("data/processed/etudiants.csv")
parcours = pd.read_csv("data/processed/parcours.csv")
ue = pd.read_csv("data/processed/ue.csv")
enseignants = pd.read_csv("data/processed/enseignants.csv")
notes = pd.read_csv("data/processed/notes.csv")

# harmonisation colonnes etudiants
etudiants = etudiants.rename(columns={
    "nom_etudiant": "nom",
    "prenom_etudiant": "prenom"
})

# harmonisation enseignants
enseignants = enseignants.rename(columns={
    "nom": "nom_enseignant",
    "nom_complet": "nom_enseignant"
})

# harmonisation ue
ue = ue.rename(columns={
    "Semestre": "semestre",
    "semestre_ue": "semestre"
})

# notes + etudiants
df = notes.merge(
    etudiants,
    on="id_etudiant",
    how="left"
)

# + ue
df = df.merge(
    ue,
    on="ue_id",
    how="left"
)

# normaliser id_parcours
if "id_parcours_y" in df.columns:
    df["id_parcours"] = df["id_parcours_y"]
    df = df.drop(columns=["id_parcours_x", "id_parcours_y"], errors="ignore")

# + enseignants
df = df.merge(
    enseignants,
    on="id_enseignant",
    how="left"
)

# + parcours
df = df.merge(
    parcours,
    on="id_parcours",
    how="left"
)

# colonnes finales (sécurisé)
colonnes_finales = [
    c for c in [
        "id_etudiant",
        "nom",
        "prenom",
        "nom_parcours",
        "semestre",
        "code_ue",
        "nom_matiere",
        "nom_enseignant",
        "note"
    ]
    if c in df.columns
]

df_final = df[colonnes_finales]

# export final
df_final.to_csv(
    "data/processed/dataset_notes_epl.csv",
    index=False
)

print("dataset simulé final généré avec succès")
