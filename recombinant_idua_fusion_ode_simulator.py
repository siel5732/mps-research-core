
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import json

# Model parameters (example values, these would be experimentally derived)
params = {
    'k_infusion': 0.1,  # Systemic infusion rate (mg/hr)
    'V_sys': 5000,      # Systemic volume (mL)
    'k_elim': 0.05,     # Systemic elimination rate (1/hr)
    'k_on_LRP1': 0.1,   # LRP1 binding rate (1/nM/hr)
    'k_off_LRP1': 0.01, # LRP1 unbinding rate (1/hr)
    'LRP1_total': 100,  # Total LRP1 receptors on BBB (nM)
    'k_transcytosis': 0.02, # Transcytosis rate into brain ISF (1/hr)
    'k_brain_elim': 0.005, # Brain ISF elimination rate (1/hr)
    'k_uptake_cells': 0.05, # Uptake rate by neurons/astrocytes (1/hr)
    'k_degradation_lysosome': 0.01, # Lysosomal degradation rate (1/hr)
    'V_brain_isf': 10,  # Brain ISF volume (mL)
    'V_cells': 50       # Volume of neurons/astrocytes (mL)
}

# Initial conditions for the ODEs
# [Systemic_IDUA, LRP1_bound_IDUA, Brain_ISF_IDUA, Cellular_IDUA_Lysosome]
initial_conditions = [0, 0, 0, 0]

# Define the ODE system
def idua_fusion_model(y, t, p):
    Sys_IDUA, LRP1_IDUA, Brain_ISF_IDUA, Cellular_IDUA_Lysosome = y

    # Systemic compartment
    dSys_IDUA_dt = p['k_infusion'] - (p['k_elim'] * Sys_IDUA) - (p['k_on_LRP1'] * Sys_IDUA * (p['LRP1_total'] - LRP1_IDUA)) + (p['k_off_LRP1'] * LRP1_IDUA)

    # LRP1 bound compartment (on BBB)
    dLRP1_IDUA_dt = (p['k_on_LRP1'] * Sys_IDUA * (p['LRP1_total'] - LRP1_IDUA)) - (p['k_off_LRP1'] * LRP1_IDUA) - (p['k_transcytosis'] * LRP1_IDUA)

    # Brain ISF compartment
    dBrain_ISF_IDUA_dt = (p['k_transcytosis'] * LRP1_IDUA) - (p['k_brain_elim'] * Brain_ISF_IDUA) - (p['k_uptake_cells'] * Brain_ISF_IDUA)

    # Cellular lysosome compartment
    dCellular_IDUA_Lysosome_dt = (p['k_uptake_cells'] * Brain_ISF_IDUA) - (p['k_degradation_lysosome'] * Cellular_IDUA_Lysosome)

    return [dSys_IDUA_dt, dLRP1_IDUA_dt, dBrain_ISF_IDUA_dt, dCellular_IDUA_Lysosome_dt]

# Time points for simulation (e.g., 24 hours)
t = np.linspace(0, 24, 500)

# Solve the ODEs
solution = odeint(idua_fusion_model, initial_conditions, t, args=(params,))

# Extract results
Sys_IDUA = solution[:, 0]
LRP1_IDUA = solution[:, 1]
Brain_ISF_IDUA = solution[:, 2]
Cellular_IDUA_Lysosome = solution[:, 3]

# Store simulation results
simulation_results = {
    'time': t.tolist(),
    'Sys_IDUA': Sys_IDUA.tolist(),
    'LRP1_IDUA': LRP1_IDUA.tolist(),
    'Brain_ISF_IDUA': Brain_ISF_IDUA.tolist(),
    'Cellular_IDUA_Lysosome': Cellular_IDUA_Lysosome.tolist(),
    'parameters': params
}

# Save results to JSON
with open('research_data/mps_i/recombinant_idua_fusion_simulation_results.json', 'w') as f:
    json.dump(simulation_results, f, indent=4)

# Plotting (optional, for visualization)
plt.figure(figsize=(12, 8))
plt.plot(t, Sys_IDUA, label='Systemic IDUA-ApoE')
plt.plot(t, LRP1_IDUA, label='LRP1-bound IDUA-ApoE (BBB)')
plt.plot(t, Brain_ISF_IDUA, label='Brain ISF IDUA-ApoE')
plt.plot(t, Cellular_IDUA_Lysosome, label='Cellular Lysosomal IDUA-ApoE')
plt.xlabel('Time (hours)')
plt.ylabel('Concentration/Amount (nM or relative units)')
plt.title('Recombinant IDUA-ApoE Fusion Protein Transport across BBB')
plt.legend()
plt.grid(True)
plt.savefig('research_data/mps_i/recombinant_idua_fusion_simulation_plot.png')
# plt.show() # Don't show in automated environment

print("MPS-I simulation complete. Results saved to 'research_data/mps_i/recombinant_idua_fusion_simulation_results.json'")
