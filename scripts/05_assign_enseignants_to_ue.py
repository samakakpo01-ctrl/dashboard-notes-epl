import pandas as pd
import random

ue = pd.read_csv("data/processed/ue.csv")
enseignants = pd.read_csv("data/processed/enseignants.csv")

ue["id_enseignant"] = ue.apply(
    lambda _: random.choice(enseignants["id_enseignant"].tolist()),
    axis=1
)

ue.to_csv("data/processed/ue.csv", index=False)

print("✔ Enseignants affectés aux UE")
