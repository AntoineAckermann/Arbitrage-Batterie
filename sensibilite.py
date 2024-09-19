# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 13:59:55 2024

@author: AA276449
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pyomo.environ import ConcreteModel, Var, Objective, Constraint, Reals, NonNegativeReals, Suffix, Set, Param, \
    ConstraintList, value, maximize
from pyomo.opt import SolverFactory

df = pd.read_csv("Day-ahead Prices_202301010000-202401010000.csv")
nb_hours = len(df["Day-ahead Price [EUR/MWh]"])

Emax = 13.5
Pmax = 5 # kW

E = [Emax*i for i in range(1,11)]
P = [Pmax*i for i in range(1,11)]

conv_rate = 0.95

def opt(Emax, Pmax):
    
    print("Emax = {} kWh".format(Emax))

    #MISE EN PLACE DU MODELE
    
    m = ConcreteModel()
    
    m.T = Set(initialize = [t for t in range(nb_hours)])
    
    # PARAMETRES
    m.Prices = Param(m.T, initialize = list(df["Day-ahead Price [EUR/MWh]"]/1000))
    
    # VARIABLES
    
    m.Charge = Var(m.T, bounds=(0,Pmax))
    m.Discharge = Var(m.T, bounds = (0, Pmax))
    m.SoC = Var(m.T, bounds = (0, Emax))
    
    # CONTRAINTES
    
    m.initSoC = Constraint(expr = m.SoC[0] == 0)
    #m.initDischarge = Constraint(m.T, rule= m.Discharge[0] == 0)
    #m.initSoC = Constraint(m.T, rule = m.SoC[0] == 0)
    
    m.eq = Constraint(m.T, rule=lambda m, t: m.SoC[t+1]==m.SoC[t]+m.Charge[t]*conv_rate-m.Discharge[t]/conv_rate if t < nb_hours - 1 else Constraint.Skip)
    
    
    
    # OBJECTIF
    
    m.profit = Objective(expr = sum(m.Discharge[t]*m.Prices[t] for t in m.T)-sum(m.Charge[t]*m.Prices[t] for t in m.T), sense=maximize)
    
    solverpath_exe = "C:\\Users\AA276449\\Documents\\Python\\glpk-4.65\\w64\\glpsol"
    solver = SolverFactory('glpk', executable=solverpath_exe).solve(m)
    
    return m.profit()

profits = []
for i in range(len(E)):
    profits.append(opt(E[i], P[i]))
    
    
    
results = pd.DataFrame(np.column_stack([E, profits]), columns=["Battery capacity (kWh)", "Yearly profit (€)"])

print(results)



fig, ax1 = plt.subplots()

# Plot SoC (State of Charge) with horizontal lines and markers on the primary y-axis
ax1.plot(E, profits, label='Yearly profit (€)', color='r')  # Plot prices with a line
ax1.set_xlabel('Battery capacity (kWh)')
ax1.set_ylabel('Yearly profit (€)', color='r')
ax1.tick_params(axis='y', labelcolor='r')

# Add titles and legends
plt.title('Profits versus battery capacity')

# Show the plot
fig.tight_layout()  # Adjust layout to avoid overlap

plt.show()