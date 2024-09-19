import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pyomo.environ import ConcreteModel, Var, Objective, Constraint, Reals, NonNegativeReals, Suffix, Set, Param, \
    ConstraintList, value, maximize
from pyomo.opt import SolverFactory

df = pd.read_csv("Day-ahead Prices_202301010000-202401010000.csv")
nb_hours = len(df["Day-ahead Price [EUR/MWh]"])


#PARAMETRES

Emax = 13.5 # kWh
Pmax = 5 # kW
conv_rate = 0.95

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

m.initCharge = Constraint(expr= m.Charge[0] == 0)
#m.initDischarge = Constraint(m.T, rule= m.Discharge[0] == 0)
#m.initSoC = Constraint(m.T, rule = m.SoC[0] == 0)

m.eq = Constraint(m.T, rule=lambda m, t: m.SoC[t+1]==m.SoC[t]+m.Charge[t]-m.Discharge[t] if t < nb_hours - 1 else Constraint.Skip)



# OBJECTIF

m.obj = Objective(expr = sum(m.Discharge[t]*m.Prices[t] for t in m.T)-sum(m.Charge[t]*m.Prices[t] for t in m.T), sense=maximize)

solver = SolverFactory('cplex').solve(m)

print("{} €".format(m.obj()))

results = pd.DataFrame(index=df.index)
results["SoC"] = [m.SoC[t].value for t in m.T]
results["Charge"] = [m.Charge[t].value for t in m.T]
results["Discharge"] = [-m.Discharge[t].value for t in m.T]

print(results)


fig, ax1 = plt.subplots()

# Plot SoC (State of Charge) with horizontal lines and markers on the primary y-axis
ax1.step(results.index, results["SoC"], where='mid', label='SoC', color='b')
ax1.set_xlabel('Time (hours)')
ax1.set_ylabel('State of Charge (kWh)', color='b')
ax1.tick_params(axis='y', labelcolor='b')

# Create a secondary y-axis for the prices
ax2 = ax1.twinx()
ax2.plot(results.index, m.Prices, label='Prices', color='r')  # Plot prices with a line
ax2.set_ylabel('Day-ahead Price (EUR/MWh)', color='r')
ax2.tick_params(axis='y', labelcolor='r')

# Add titles and legends
plt.title('State of Charge and Day-ahead Prices over Time')

# Show the plot
fig.tight_layout()  # Adjust layout to avoid overlap
plt.show()