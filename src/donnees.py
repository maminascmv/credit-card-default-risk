"""Chargement et préparation des données (utilisé par les 3 notebooks)."""
from pathlib import Path

import pandas as pd

# Le fichier de données est dans le dossier data/, à côté du dossier src/
FICHIER = Path(__file__).parent.parent / "data" / "default_credit_card_clients.csv"

# Noms explicites pour les colonnes du fichier UCI (X1 à X23, Y) selon le site de sources
NOUVEAUX_NOMS = {
    "ID": "id_client",
    "X1": "plafond_credit",
    "X2": "sexe",
    "X3": "education",
    "X4": "statut_marital",
    "X5": "age",
    "X6": "retard_sep", "X7": "retard_aou", "X8": "retard_jul",
    "X9": "retard_jun", "X10": "retard_mai", "X11": "retard_avr",
    "X12": "facture_sep", "X13": "facture_aou", "X14": "facture_jul",
    "X15": "facture_jun", "X16": "facture_mai", "X17": "facture_avr",
    "X18": "paiement_sep", "X19": "paiement_aou", "X20": "paiement_jul",
    "X21": "paiement_jun", "X22": "paiement_mai", "X23": "paiement_avr",
    "Y": "defaut",
}

RETARDS = ["retard_sep", "retard_aou", "retard_jul", "retard_jun", "retard_mai", "retard_avr"]
FACTURES = ["facture_sep", "facture_aou", "facture_jul", "facture_jun", "facture_mai", "facture_avr"]
PAIEMENTS = ["paiement_sep", "paiement_aou", "paiement_jul", "paiement_jun", "paiement_mai", "paiement_avr"]
NOUVELLES = ["nb_mois_retard", "taux_utilisation", "taux_remboursement"]

# Variables données au modèle : ni identifiant, ni sexe, ni âge, ni situation familiale
VARIABLES_MODELE = ["plafond_credit"] + FACTURES + PAIEMENTS + RETARDS + NOUVELLES


def charger_donnees():
    """Lit le fichier UCI et renomme les colonnes (les valeurs ne changent pas)."""
    df = pd.read_csv(FICHIER)
    return df.rename(columns=NOUVEAUX_NOMS)


def regrouper_codes(df):
    """Regroupe les codes non documentés avec la modalité « autre »."""
    df = df.copy()
    df["education"] = df["education"].replace({0: 4, 5: 4, 6: 4})
    df["statut_marital"] = df["statut_marital"].replace({0: 3})
    return df


def ajouter_variables(df):
    """Ajoute les 3 variables construites (notebook 01, partie 9)."""
    df = df.copy()
    # nombre de mois (sur 6) avec au moins un mois de retard
    df["nb_mois_retard"] = (df[RETARDS] >= 1).sum(axis=1)
    # part du plafond utilisée par la facture de septembre
    df["taux_utilisation"] = df["facture_sep"] / df["plafond_credit"]
    # part de la facture d'août payée en septembre, entre 0 et 1
    # (1 si la facture d'août était nulle ou négative : il n'y avait rien à payer)
    taux = df["paiement_sep"] / df["facture_aou"]
    taux[df["facture_aou"] <= 0] = 1
    df["taux_remboursement"] = taux.clip(0, 1)
    return df


def preparer_donnees():
    """Les trois étapes à la suite (utilisé par les notebooks 02 et 03)."""
    return ajouter_variables(regrouper_codes(charger_donnees()))
