import pandas as pd
import random

# Charger les UE
ue = pd.read_csv("data/processed/ue.csv")

# Listes réservées aux enseignants
noms_enseignants = [
    "AGBOZO","HOUNKPATIN","DOSSOU","KPADONOU","AZON","TOTIN",
    "SOSSOU","ATCHADE","HOLOGO","ZANNOU","DEGUENON","FAVI",
    "KOSSOU","TOVIHOU","GUEDEGBE","HOUNGBEDJI","ADANLETE"
]

prenoms_enseignants = [
    "Bernard","Roger","Pascal","Luc","François","Alain",
    "Jean","Paul","Michel","Serge","Christophe","Jacques",
    "Thierry","Olivier","Eric","Didier","Patrice"
]

specialites = [
    "Génie Civil",
    "Génie Electrique",
    "Génie Mécanique",
    "Informatique",
    "Réseaux",
    "Intelligence Artificielle",
    "Mathématiques",
    "Physique"
]

# Toutes les combinaisons possibles NOM + PRENOM
combinaisons_possibles = [
    (n, p) for n in noms_enseignants for p in prenoms_enseignants
]

# Nombre souhaité (1 enseignant ≈ 5 UE)
nb_voulu = max(1, len(ue) // 5)

# Nombre réellement possible
nb_enseignants = min(nb_voulu, len(combinaisons_possibles))

# Tirage sans répétition
combinaisons = random.sample(combinaisons_possibles, nb_enseignants)
ids_enseignants = random.sample(range(100000, 999999), nb_enseignants)

enseignants = []

for i in range(nb_enseignants):
    nom, prenom = combinaisons[i]

    enseignants.append({
        "id_enseignant": ids_enseignants[i],
        "nom": nom,          # MAJUSCULE
        "prenom": prenom,
        "specialite": random.choice(specialites)
    })

df = pd.DataFrame(enseignants)
df.to_csv("data/processed/enseignants.csv", index=False)

print(f"✔ {len(df)} enseignants uniques générés")
