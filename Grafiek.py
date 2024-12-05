import matplotlib as plt
from Zonnecel_experiment import ZonnecelExperiment

experiment = ZonnecelExperiment("ASRL4::INSTR")

voltages,currents,voltages_uncertainty,currents_uncertainty,= experiment.scan(n=1, start=40, stop=500)

plt.figure(figsize=(12, 6))  
plt.errorbar(voltages, currents, xerr=voltages_uncertainty, yerr=currents_uncertainty)
plt.show()
