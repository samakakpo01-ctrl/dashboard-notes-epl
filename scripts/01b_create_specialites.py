import pandas as pd

df = pd.read_csv("data/raw/parcours_specialites.csv", sep=";")
df.columns = ["nom_parcours", "nom_specialite", "id_parcours"]

df["statut"] = df["nom_specialite"].apply(
    lambda x: "ANCIEN" if "[ANCIEN]" in x else "ACTUEL"
)

df["nom_specialite"] = df["nom_specialite"].str.replace(
    r"\[ANCIEN\]\s*-\s*", "", regex=True
)

df.to_csv("data/processed/specialites.csv", index=False)

print("✔ specialites.csv créé")
