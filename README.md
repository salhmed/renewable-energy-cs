# Dimensionnement solaire, éolien et batteries

Version officielle : français  
English version: [README.en.md](README.en.md)

## Objectif

Ce projet estime le dimensionnement d'un système hybride :

- production éolienne ;
- production solaire photovoltaïque ;
- stockage par batteries ;
- consommation électrique horaire.

L'objectif principal est d'identifier la période la plus défavorable de l'année, puis de dimensionner économiquement le nombre de panneaux solaires et de batteries nécessaires pour couvrir cette période critique.

## Données utilisées

Le fichier principal utilisé est :

```text
Power_conso_farm_projet_good_calcul_anne_cleaned.csv
```

Colonnes principales :

- `local_time` : date et heure ;
- `wind_electricity_kW` : production éolienne horaire ;
- `solar_electricity_kW` : production solaire de référence pour 290 panneaux ;
- `consommation_kW` : consommation horaire.

Comme les données sont horaires, les valeurs `kW` sommées sur une heure sont utilisées comme des `kWh`.

## Méthode

### 1. Identification de la période critique

Le notebook calcule des sommes glissantes sur 15 jours pour repérer les plus faibles périodes de production.

La période critique retenue est :

```text
03/12/2019 au 17/12/2019
```

Elle correspond à la période de 15 jours consécutifs la plus défavorable dans l'analyse.

### 2. Dimensionnement économique sur la période critique

Le dimensionnement final est fait sur cette période critique uniquement.

Coûts utilisés :

```text
Coût d'un panneau solaire : 139,66 EUR
Coût d'une batterie       : 449,99 EUR
```

Caractéristiques batterie :

```text
Capacité nominale d'une batterie : 2,40 kWh
État de charge autorisé          : 20% à 90%
Capacité utilisable              : 70%
Capacité utilisable par batterie : 1,68 kWh
```

Pour chaque nombre de panneaux testé, le notebook :

1. calcule la production solaire horaire ;
2. calcule le bilan horaire :

```text
bilan = production éolienne + production solaire - consommation
```

3. simule la recharge et la décharge des batteries heure par heure ;
4. calcule le nombre minimal de batteries nécessaire ;
5. calcule le coût total :

```text
coût total = panneaux * 139,66 + batteries * 449,99
```

La solution retenue est celle qui minimise ce coût total.

## Résultats principaux

Solution économique retenue sur la période critique :

```text
Nombre de panneaux : 1189
Nombre de batteries : 924
Capacité nominale batteries : 2217,60 kWh
Capacité utilisable batteries : 1552,32 kWh
Coût panneaux : 166055,74 EUR
Coût batteries : 415790,76 EUR
Coût total : 581846,50 EUR
```

Simulation sur la période critique, avec les batteries initialement chargées à 90% :

```text
SOC minimum : 20%
SOC maximum : 90%
Énergie non servie : 0 kWh
Énergie écrêtée : 3474,95 kWh
```

## Vérification sur l'année complète

Le couple `1189 panneaux / 924 batteries` a ensuite été simulé sur toute l'année.

Résultat annuel :

```text
Consommation annuelle : 329595,00 kWh
Production éolienne : 165722,39 kWh
Production solaire : 334941,68 kWh
Production totale : 500664,07 kWh
Bilan avant stockage : +171069,07 kWh
Énergie non servie : 142,70 kWh
Énergie écrêtée : 172013,47 kWh
SOC minimum : 20%
SOC maximum : 90%
```

Point important : le système a été optimisé sur les 15 jours critiques, pas sur toute l'année. En simulation annuelle chronologique, il reste donc une petite énergie non servie de `142,70 kWh`, car les batteries ne sont pas forcément à 90% au début de la période critique.

## Graphiques produits

Graphique annuel :

```text
plot_annee_energie_batterie_generation.png
```

Il montre :

- l'énergie consommée chaque jour ;
- l'énergie générée chaque jour ;
- l'énergie stockée dans les batteries ;
- l'énergie écrêtée ;
- l'énergie non servie.

Graphique des journées typiques par saison :

```text
plot_journees_typiques_saisons.png
```

Journées représentatives sélectionnées automatiquement :

```text
Hiver     : 13/02/2019
Printemps : 21/05/2019
Été       : 28/06/2019
Automne   : 27/09/2019
```

## Fichiers importants

```text
solar_wind_estimation.ipynb
```

Notebook principal contenant les calculs, simulations et graphiques.

```text
low_15_day_windows.csv
```

Résumé des pires fenêtres de 15 jours.

```text
dimensionnement_panneaux_batteries_periode_critique.csv
```

Résultats de la recherche économique sur la période critique.

```text
periode_critique_with_battery.csv
```

Simulation horaire de la période critique avec état des batteries.

```text
simulation_annuelle_1189p_924b.csv
```

Simulation horaire annuelle avec `1189` panneaux et `924` batteries.

## Reproduire les résultats

1. Ouvrir `solar_wind_estimation.ipynb`.
2. Exécuter les cellules dans l'ordre.
3. Les CSV et graphiques sont régénérés automatiquement.

Dépendances principales :

- Python ;
- pandas ;
- matplotlib ;
- Jupyter Notebook ou JupyterLab.

## Limites et hypothèses

- La colonne solaire est considérée comme un profil de référence pour `290` panneaux.
- La production solaire pour `N` panneaux est calculée proportionnellement :

```text
solaire_N = solaire_290 * N / 290
```

- Les batteries sont modélisées simplement, sans rendement de charge/décharge ni vieillissement.
- Le dimensionnement économique final est optimisé sur la période critique de 15 jours.
- L'état initial des batteries influence fortement le résultat. La période critique est couverte si les batteries commencent à `90%`.
