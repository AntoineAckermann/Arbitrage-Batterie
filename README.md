Tentative d'une mise en place d'une stratégie d'arbitrage sur les prix de l'électricité avec un BESS (Battery Energy Storage System) : optimisation de la charge et décharge à pas temporel pour maximiser le profit à partir des prix day ahead en France (utilisation des données de transparence d'ENTSOE pour les historiques de prix).

Le fichier "day_to_day.py" réalise l'optimisation sur des horizons de temps de 24h. Cela est rendu possible par la structure du marché day-ahead (les prix heure par heure sont connus à l'avance). On évite également par là d'utiliser un algorithme de prédiction des prix (j'ignore même si c'est possible). 

A améliorer/à creuser :  

 - Propreté du code
 - Prise en compte de la dégradation de la batterie en fonction des stratégies de charge/décharge appliquées. Voir p.ex https://www.sciencedirect.com/science/article/pii/S2352152X24019662#s0025
 - Utilisation des prix intraday ?
 - Prise en compte des services systèmes (Frequency Containment Reserve, aFRR et mFRR, i.e. réserves primaire/secondaire/tertiaire)

Globalement, l'[étude citée](https://www.sciencedirect.com/science/article/pii/S2352152X24019662#bb0035) indique :

>In summary, the profitability analysis shows that, even when assuming no degradation of the battery (LP scenario), the target break-even investment cost with a power-to-energy-ratio of 1 MW\/2MWh is 210 \$ \/kWh. Comparing these normalized NPVs to today's battery costs of 300–500 \$\/kWh  **demonstrates that investing in BESS for energy arbitrage services only is currently not profitable under the assumptions used in this case study**. Alternative locations with higher price volatility and considering a BESS that provides multiple grid services that generate additional revenue streams, could represent valuable strategies to make BESS profitable at today's costs. Furthermore, as projected by the IEA World Energy Outlook 2023 the total BESS investment costs for grid-level applications are forecasted to decrease to <185 \$ \/kWh by 2030 with a long-term goal of 140 \$ \/kWh by 2050. At this 2050 target, the BESS would be profitable at the selected location under the assumption used in this case study. In addition, price volatility in highly renewable electricity markets may increase, which would increase the NPV that BESS could achieve in these future markets even with degradation.



