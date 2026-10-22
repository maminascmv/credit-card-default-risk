# Défaut de paiement sur carte de crédit : qui appeler en priorité ?

Projet de Science des données (module S7MOI1, ECAM-EPMI, 2AE), réalisé seul.

## Le problème

Une banque appelle chaque mois une partie de ses clients pour prévenir un défaut de paiement sur leur carte de crédit (rappel d'échéance, proposition d'échéancier). Aujourd'hui, elle appelle les clients déjà en retard sur leur dernière facture. Cela représente 22.7% (environ 23% ) des clients.

Ma question : **avec le même nombre d'appels, peut-on mieux choisir les clients à appeler pour réduire les pertes ?**

## Résultats clés

- Modèle retenu : une Random Forest qui prédit la probabilité de défaut le mois suivant. AUC de 0,786 ± 0,005 en validation croisée et de 0,778 sur le test, contre 0,678 pour la règle actuelle.
- Décision : je garde le même nombre d'appels, mais j'appelle d'abord les clients dont la **perte attendue** (probabilité de défaut × montant de la facture) est la plus forte.
- Sur le test, le modèle couvre **80,3 % des montants qui partent en défaut**, contre 55,3 % pour la règle actuelle. Le critère de succès fixé au départ (au moins 70 %) est atteint.
- **ROI** : environ 252 000 € de gain par an pour un coût de projet de 55 000 €, soit un ROI de 358 % la 1re année et un retour en 2,6 mois. Dans 90 % des tirages du bootstrap, le gain reste entre 197 000 et 309 000 €.
- Scénario défavorable (5 % de perte, 5 % d'efficacité des appels) : 63 000 € de gain par an, le projet reste juste rentable. Il est remboursé dès que les appels évitent 2,2 % des pertes.

Ces gains reposent sur des hypothèses de coût (perte, efficacité d'un appel, coût d'un appel), sourcées dans le notebook 03 et regroupées dans `src/couts.py`. **Ma recommandation est un pilote de 3 mois avec un groupe témoin** pour mesurer l'efficacité réelle des appels avant de généraliser.

![Part des montants en défaut couverts selon le nombre de clients appelés](reports/figures/couverture%20montant.png)

*À nombre d'appels égal, trier les clients par perte attendue couvre beaucoup plus de montants que la règle actuelle ou que le tri par probabilité seule.*

## Démarche

| Notebook | Contenu | Axes |
|---|---|---|
| `01_cadrage_eda.ipynb` | cadrage métier, type de problème, qualité des données, audit de fuite, analyse exploratoire, règle actuelle (baseline), variables construites | 1, 2, 3 |
| `02_modelisation.ipynb` | split stratifié 80/20, pipeline, 3 modèles (régression logistique, arbre de décision, Random Forest) réglés par validation croisée à 5 plis, sur-apprentissage, importance des variables, analyse des erreurs, évaluation finale sur le test | 4, 5 |
| `03_decision_roi.ipynb` | calibration des probabilités, hypothèses et matrice de coûts, règle de décision, matrices de confusion, ROI, bootstrap, sensibilité aux hypothèses, équité, registre des risques, recommandation | 6, 7, 9 |

Le jeu de test (20 % des clients) n'est utilisé qu'une seule fois, pour évaluer le modèle final.

## Données
- **Jeu de données** : *Default of Credit Card Clients* (UCI Machine Learning Repository, id 350) : 30 000 clients d'une banque de Taïwan, 23 variables (plafond, données personnelles, retards, factures et paiements d'avril à septembre 2005), et la cible : défaut de paiement le mois suivant.
- **Lien** : https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients
- **Citation** : Yeh, I. (2009). *Default of Credit Card Clients* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C55S3H
- **Licence** : CC BY 4.0
- **Date de consultation** : 09-10-2026

Le fichier brut (2,8 Mo) est inclus dans `data/`. Les détails sont dans `data/SOURCE.md`.

## Comment lancer le projet

Le projet a été exécuté avec Python 3.9.6 et les versions de `requirements.txt`. Ces versions s'installent avec Python 3.9 à 3.12 (elles n'existent pas pour Python 3.13 et plus).

```bash
git clone https://github.com/maminascmv/credit-card-default-risk
cd credit-card-default-risk
python3 -m pip install -r requirements.txt
python3 -m jupyterlab
```

Puis ouvrir les notebooks dans l'ordre **01 → 02 → 03** et lancer *Kernel → Restart Kernel and Run All Cells* sur chacun. Le notebook 02 enregistre le modèle final dans `models/` (ce dossier n'est pas versionné), et le notebook 03 en a besoin. Le notebook 02 prend quelques minutes à cause de la recherche des hyperparamètres.

Tous les aléas sont fixés (`random_state=42`) et les chemins sont relatifs. Avec d'autres versions de scikit-learn ou de pandas, les résultats peuvent varier légèrement.

## Structure du dépôt

```
credit-card-default-risk/
├── README.md
├── requirements.txt          # versions des librairies
├── data/
│   ├── default_credit_card_clients.csv   # données brutes UCI
│   └── SOURCE.md                         # source, licence, date
├── notebooks/
│   ├── 01_cadrage_eda.ipynb
│   ├── 02_modelisation.ipynb
│   └── 03_decision_roi.ipynb
├── src/
│   ├── donnees.py            # chargement, nettoyage des codes, variables construites
│   └── couts.py              # hypothèses de coût et calcul du coût d'une politique d'appel
└── reports/
    ├── RAPPORT SM7OI1 DATA.pdf   # rapport de synthèse
    ├── Slides_soutenance.pdf     # support de la soutenance
    ├── figures/                  # graphiques produits par les notebooks
    └── metriques_modele.json     # métriques du modèle final (notebook 02)
```

## Limites

- Les données datent de 2005, en pleine crise des cartes de crédit à Taïwan. Le modèle devra être réentraîné sur les données récentes de la banque avant tout usage.
- Les hypothèses de coût, surtout l'efficacité d'un appel, ne sont pas mesurées sur cette banque : seul un pilote avec groupe témoin peut les confirmer.
- Les défauts de clients qui n'ont jamais été en retard restent difficiles à prévoir avec ces seules variables (notebook 02).

## Usage de l'IA generative

Conformément aux consignes, je déclare avoir utilisé **Claude (Anthropic)** comme assistant pendant le projet, sur :
- Verificztion technique ;
- Assistance en codage ;
- recherche d’un jeu de données selon critères ;
- Orientation dans le plan financier ;
- Reverifaction apres chaque étape
- Aide à la rédaction et à la mise en forme du rapport

