import pandas as pd
import random

# Charger les parcours
parcours = pd.read_csv("data/processed/parcours.csv")

# Listes larges pour limiter répétitions
noms = [
    "AKAKPO","MENSAH","LAWSON","ADJOVI","AMOUZOU","SODJI",
    "TCHALLA","ATAKORA","KOUASSI","TRAORE","DIALLO",
    "BARRY","SANOGO","OUATTARA","KONATE","GBETO",
    "HOUNGBEDJI","ASSOGBA","AGBODJAN","HOUEGNON"
]

prenoms = [
    "Kossi","Yaw","Kodjo","Komi","Afi","Akossiwa","Essowè",
    "Sena","Yawa","Mawuli","Dodzi","Abla","Eyram","Edem",
    "Kwame","Yawovi","Ayélé","Aminata","Fatou","Salifou",
    "Issa","Mariam","Awa","Ibrahim"
]

etudiants = []

# Génération d'ID étudiants uniques à 6 chiffres
ids_etudiants = random.sample(range(100000, 999999), 1000)

for i in range(1000):
    id_etudiant = ids_etudiants[i]

    nom = random.choice(noms)
    prenom = random.choice(prenoms)

    parcours_row = parcours.sample(1).iloc[0]

    etudiants.append({
        "id_etudiant": id_etudiant,
        "nom": nom,
        "prenom": prenom,
        "id_parcours": parcours_row["id_parcours"],
        "semestre": random.choice([1, 2, 3, 4, 5, 6])
    })

df = pd.DataFrame(etudiants)

df.to_csv("data/processed/etudiants.csv", index=False)

print("✔ 1000 étudiants générés (ID aléatoire à 6 chiffres)")
