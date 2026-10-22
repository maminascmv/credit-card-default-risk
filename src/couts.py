"""Hypothèses de coût du notebook 03.

Ce sont des HYPOTHÈSES, à valider avec la banque. Les sources sont citées
dans le notebook 03 (partie 2).
Elles sont regroupées ici pour pouvoir les changer à un seul endroit.
"""

# 1 € = 40,0 TWD : moyennes 2005 de la Réserve fédérale (release G.5A du 3 janvier 2006),
# 1,2449 dollar pour 1 € et 32,131 TWD pour 1 dollar.
TAUX_CHANGE = 40.0

# Part de la facture finalement perdue quand un défaut n'est pas anticipé.
# Beaucoup de clients en retard régularisent (FICO, 2019), mais une créance passée
# en perte n'est récupérée qu'à 10-15 % (Fed de Philadelphie, 2012).
PERTE = 0.10

# Part de cette perte évitée grâce à un appel préventif.
# Les rappels étudiés (SMS, application) réduisent les retards de 4 à 7 % (Campbell et al., 2022).
EFFICACITE = 0.10

# Coût d'un appel en € : environ 10 minutes de conseiller (une heure de centre d'appels
# interne coûte 50 à 60 € à une entreprise, AFRC citée par la Banque des Territoires, 2010).
COUT_APPEL = 10.0

# Le jeu de test (6 000 clients) représente 1/5 d'un portefeuille de 30 000 clients,
# et la décision est prise chaque mois : on multiplie donc par 5 x 12 pour avoir une année.
FACTEUR_ANNUEL = 5 * 12

# Coût du projet la 1re année, en € : 30 000 de développement (environ 56 jours de data scientist à 533 €),
# 15 000 d'intégration et 10 000 d'exploitation.
COUT_PROJET = 55_000


def cout_total(appele, defaut, montant, perte=PERTE, efficacite=EFFICACITE, cout_appel=COUT_APPEL):
    """Coût d'une politique d'appel, en €.

    appele, defaut : tableaux de True / False (un élément par client)
    montant        : montant à risque de chaque client, en €

    - défaut non appelé  : on perd perte x montant
    - défaut appelé      : l'appel coûte cout_appel, et on perd encore perte x montant x (1 - efficacite)
    - client sain appelé : l'appel coûte cout_appel
    """
    defaut_manque = ~appele & defaut
    defaut_trouve = appele & defaut
    return (montant[defaut_manque].sum() * perte
            + montant[defaut_trouve].sum() * perte * (1 - efficacite)
            + appele.sum() * cout_appel)
