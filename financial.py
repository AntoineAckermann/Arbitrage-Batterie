import pandas as pd
#from numpy_financial import npv


def npv(r, cash):
    """Renvoie la valeur actualisée nette d'une série de flux de trésorerie"""
    return sum([cash[i]/(1+r)**i for i in range(len(cash))])


year = 2022  # choix du fichier de données
country = "DE"  # choix du pays

results = pd.read_csv(f"{country}_{str(year)}01010000-{str(year+1)}01010000_out.csv", sep=",")




E_max = 3900
n = 15
OPEX_escalation_rate = 0.02
OPEX = 10000  # €/MWh
profit_escalation_rate = 0.0
r = 0.04

profit = sum(results["Cash flow"])
profits = [(profit/(E_max/1000))*(1+profit_escalation_rate)**i for i in range(n)]  # per MWh

expenses = [OPEX*(1+OPEX_escalation_rate)**j for j in range(n)]

cash_flow = [profits[i] - expenses[i] for i in range(n)]

NPV = npv(r, cash_flow)

print(f"Yearly profit = {profit} €\n")
print(f"Net Present Value = {NPV} €/MWh")
