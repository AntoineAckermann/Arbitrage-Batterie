Tentative d'une mise en place d'une stratégie d'arbitrage sur les prix de l'électricité avec un BESS (Battery Energy Storage System) : optimisation de la charge et décharge à pas temporel pour maximiser le profit à partir des prix day ahead en France (utilisation des données de transparence d'ENTSOE pour les historiques de prix).

Le fichier "day_to_day.py" réalise l'optimisation sur des horizons de temps de 24h. Cela est rendu possible par la structure du marché day-ahead (les prix heure par heure sont connus à l'avance). On évite également par là d'utiliser un algorithme de prédiction des prix (j'ignore même si c'est possible). 

A améliorer/à creuser :  

 - Propreté du code
 - Calcul d'une NPV qui permettrait de déterminer un coût des batteries qui permettrait de rendre le projet rentable : pas facile de projeter les résultats dans le futur dans la mesure où les revenus annuels seront sans doute ammenés à changer (on peut imaginer que cela se fasse plutôt à la hausse, avec l'augmentation du taux de pénétration des EnR dans le mix et probablement une volatilité plus importante des prix)
 - Voir ce qu'il en est des autres pays EU (pas trop compliqué avec les données ENTSO-E)
 - Prise en compte de la dégradation de la batterie en fonction des stratégies de charge/décharge appliquées. Voir p.ex. https://www.sciencedirect.com/science/article/pii/S2352152X24019662#s0025
 - Utilisation des prix intraday ?
 - Prise en compte des services systèmes (Frequency Containment Reserve, aFRR et mFRR, i.e. réserves primaire/secondaire/tertiaire)




Quant à la rentabilité d'un projet concentré uniquement sur l'arbitrage sur le marché spot, globalement l'[étude citée](https://www.sciencedirect.com/science/article/pii/S2352152X24019662#bb0035) est assez claire :

>In summary, the profitability analysis shows that, even when assuming no degradation of the battery (LP scenario), the target break-even investment cost with a power-to-energy-ratio of 1 MW\/2MWh is 210 \$ \/kWh. Comparing these normalized NPVs to today's battery costs of 300–500 \$\/kWh  **demonstrates that investing in BESS for energy arbitrage services only is currently not profitable under the assumptions used in this case study**. Alternative locations with higher price volatility and considering a BESS that provides multiple grid services that generate additional revenue streams, could represent valuable strategies to make BESS profitable at today's costs. Furthermore, as projected by the IEA World Energy Outlook 2023 the total BESS investment costs for grid-level applications are forecasted to decrease to <185 \$ \/kWh by 2030 with a long-term goal of 140 \$ \/kWh by 2050. At this 2050 target, the BESS would be profitable at the selected location under the assumption used in this case study. In addition, price volatility in highly renewable electricity markets may increase, which would increase the NPV that BESS could achieve in these future markets even with degradation.

Cela invite toutefois à investiguer les apports des "additional revenue streams", càd les services systèmes fréquences, mécanisme d'ajustement et mécanisme de capacité. Aussi l'étude est basée sur les prix d'un noeud local aux US, donc à voir pour l'Europe.

