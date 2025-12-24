import pandas as pd
import random

# Charger les données
etudiants = pd.read_csv("data/processed/etudiants.csv")
ue = pd.read_csv("data/processed/ue.csv")

notes = []
id_note = 1

for _, etu in etudiants.iterrows():

    # UE correspondant au parcours ET au semestre de l'étudiant
    ue_filtrees = ue[
        (ue["semestre"] == etu["semestre"]) &
        (ue["id_parcours"] == etu["id_parcours"])
    ]

    for _, m in ue_filtrees.iterrows():
        note = round(random.triangular(0, 20, 12), 2)

        notes.append({
            "id_note": id_note,
            "id_etudiant": etu["id_etudiant"],
            "ue_id": m["ue_id"],     # NOM EXACT
            "note": note
        })

        id_note += 1

df_notes = pd.DataFrame(notes)
df_notes.to_csv("data/processed/notes.csv", index=False)

print(f"✔ {len(df_notes)} notes générées avec succès")
