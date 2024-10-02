import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pyomo.environ import ConcreteModel, Var, Objective, Constraint, Suffix, Set, Param, \
    ConstraintList, value, maximize, Binary
from pyomo.opt import SolverFactory

interval = "202401010000-202501010000"

df = pd.read_csv(f"Day-ahead Prices_{interval}.csv")
df.drop(df[df["Day-ahead Price [EUR/MWh]"] == "-"].index, inplace = True)
df["Day-ahead Price [EUR/MWh]"] = df["Day-ahead Price [EUR/MWh]"].astype(float)
df["Day-ahead Price [EUR/MWh]"].fillna((df["Day-ahead Price [EUR/MWh]"].shift() + df["Day-ahead Price [EUR/MWh]"].shift(-1))/2, inplace=True)
df["Day-ahead Price [EUR/MWh]"] = df["Day-ahead Price [EUR/MWh]"]/1000

nb_hours = len(df["Day-ahead Price [EUR/MWh]"])
nb_days = int(nb_hours/24)

hours_per_day = 24

def opt(E0, prices):
    
    #PARAMETRES
    
    Emax = 3900 # kWh
    EtP_ratio = 5 #hours
    Pmax = Emax/EtP_ratio # kW
    conv_rate = 0.95
    
    
    #MISE EN PLACE DU MODELE
    
    m = ConcreteModel()
    
    m.T = Set(initialize = [t for t in range(hours_per_day)])
    
    # PARAMETRES
    m.Prices = Param(m.T, initialize = prices)
    
    # VARIABLES
    
    m.Charge = Var(m.T, bounds=(0,Pmax))
    m.Discharge = Var(m.T, bounds = (0, Pmax))
    m.ChargeStatus = Var(m.T, bounds = (0,1), domain=Binary) # 0 = discharge ; 1 = charge
    m.SoC = Var(m.T, bounds = (0, Emax))

    
    # CONTRAINTES

    m.eq = Constraint(m.T, rule=lambda m, t: m.SoC[t] == m.SoC[t-1]+m.Charge[t]*conv_rate-m.Discharge[t]/conv_rate if t>=1 else m.SoC[0] == E0+m.Charge[0]*conv_rate-m.Discharge[0]/conv_rate)
    m.charge_status1 = Constraint(m.T, rule= lambda m, t: m.Charge[t] <= Pmax*m.ChargeStatus[t])
    m.charge_status2 = Constraint(m.T, rule=lambda m, t: m.Discharge[t] <= Pmax*(1-m.ChargeStatus[t]))

    # OBJECTIF
    
    m.profit = Objective(expr = sum(m.Discharge[t]*m.Prices[t] for t in m.T)-sum(m.Charge[t]*m.Prices[t] for t in m.T), sense=maximize)
    
    #solverpath_exe = "C:\\Users\AA276449\\Documents\\Python\\glpk-4.65\\w64\\glpsol"
    solver = SolverFactory('cplex').solve(m)
    
    return m
    

E0 = 0
results = pd.DataFrame()


for day_of_year in range(int(nb_days)):
    print(day_of_year, E0)

    daily_prices = list(df["Day-ahead Price [EUR/MWh]"].iloc[day_of_year*24:(day_of_year+1)*24])
    
   
    m = opt(E0, daily_prices)

    daily_results = pd.DataFrame()
    daily_results["SoC"] = [m.SoC[t].value for t in m.T]
    daily_results["Charge"] = [m.Charge[t].value for t in m.T]
    daily_results["Discharge"] = [m.Discharge[t].value for t in m.T]
    daily_results["Status"] = [m.ChargeStatus[t].value for t in m.T]
    daily_results["Energy prices"] = daily_prices
    daily_results["Cash flow"] = daily_results["Energy prices"]*daily_results["Discharge"] - daily_results["Energy prices"]*daily_results["Charge"] 

    temp = pd.concat([results, daily_results], copy=False, ignore_index=True)
    results.drop(results.index[0:], inplace=True)
    results[temp.columns] = temp
    
    E0 = m.SoC[23].value

    
    
    
print(results)
print(list(results["Cash flow"]))
results.to_csv(f"{interval}_out.csv", sep=";")
profit = sum(results["Cash flow"])
print("Profit = {} €\nProfit per day = {}€".format(profit, profit/nb_days))
    


fig, ax1 = plt.subplots()

# Plot SoC (State of Charge) with horizontal lines and markers on the primary y-axis
ax1.step(results.index, results["SoC"], where='mid', label='SoC', color='b')
ax1.set_xlabel('Time (hours)')
ax1.set_ylabel('State of Charge (kWh)', color='b')
ax1.tick_params(axis='y', labelcolor='b')

# Create a secondary y-axis for the prices
ax2 = ax1.twinx()
ax2.plot(results.index, list(df["Day-ahead Price [EUR/MWh]"]/1000)[:nb_days*hours_per_day] , label='Prices', color='r')  # Plot prices with a line
ax2.set_ylabel('Day-ahead Price (EUR/MWh)', color='r')
ax2.tick_params(axis='y', labelcolor='r')

# Add titles and legends
plt.title('State of Charge and Day-ahead Prices over Time')

# Show the plot
fig.tight_layout()  # Adjust layout to avoid overlap

plt.savefig("fig.png")
plt.show()