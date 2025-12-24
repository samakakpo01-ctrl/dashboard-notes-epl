import pandas as pd

ue = pd.read_csv("data/raw/ue_epl.csv", sep=";")

ue.columns = ["code_ue", "nom_matiere", "semestre", "id_parcours", "ue_id"]

ue["semestre"] = ue["semestre"].astype(int)
ue["id_parcours"] = ue["id_parcours"].astype(int)
ue["ue_id"] = ue["ue_id"].astype(int)

ue = ue.drop_duplicates(subset=["ue_id"])

ue.to_csv("data/processed/ue.csv", index=False)

print("✔ ue.csv généré avec succès")
