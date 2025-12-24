# Tableau de bord d’analyse des notes de l’EPL

## Objectif
Ce projet a pour objectif d’analyser les performances académiques des étudiants de l’EPL
à partir de données simulées, à travers un tableau de bord interactif développé avec Streamlit.

Il permet de produire des statistiques descriptives, des visualisations graphiques
et des classements afin de faciliter l’interprétation des résultats académiques.

## Données
Les données utilisées sont générées artificiellement et organisées sous forme de fichiers CSV.
Elles représentent :
- les parcours académiques
- les unités d’enseignement (UE)
- les matières
- les enseignants
- les étudiants
- les notes

Un dataset final consolidé est également produit :
- **dataset_notes_epl.csv** : dataset global des notes des étudiants, prêt pour l’analyse et la visualisation

## Outils utilisés
- Python
- Pandas
- NumPy
- Streamlit
- Matplotlib

## Fonctionnalités
Le tableau de bord permet :
- le chargement et l’exploitation du dataset des notes
- le calcul des statistiques descriptives (moyenne, médiane, écart-type)
- la visualisation graphique des données :
  - histogrammes
  - diagrammes en barres
  - boxplots
  - diagrammes circulaires
  - nuages de points
- le calcul du taux de réussite par matière (en pourcentage)
- le filtrage des données par parcours
- la consultation individuelle des notes et de la moyenne d’un étudiant
- le classement des étudiants (Top 10)
- l’évaluation des performances des enseignants
- l’export des résultats de calculs :
  - fichiers CSV
  - fichiers NumPy (.npy)

## Exports des données
Le projet permet l’export :
- des datasets consolidés au format CSV
- des résultats de calculs statistiques au format NumPy (.npy)

Ces fichiers peuvent être réutilisés pour d’autres analyses ou modèles.

## Exécution du projet

Installer les dépendances :
```bash
pip install -r requirements.txt

Lancer le tableau de bord Streamlit :
streamlit run reports/dashboard.py

## Structure du projet
```text
Projet_EPL/
├── data/
│   ├── processed/
│   └── dataset_notes_epl.csv
├── reports/
│   └── dashboard.py
├── scripts/
│   └── scripts de génération et d’export
├── requirements.txt
└── README.md
