import pandas as pd

# charger le fichier brut
df = pd.read_csv("data/raw/parcours_specialites.csv", sep=";")

# normaliser les colonnes
df.columns = ["nom_parcours", "nom_specialite", "id_parcours"]

# dédupliquer les parcours
parcours = df[["id_parcours", "nom_parcours"]].drop_duplicates()

# sauvegarde
parcours.to_csv("data/processed/parcours.csv", index=False)

print("✔ parcours.csv créé")
