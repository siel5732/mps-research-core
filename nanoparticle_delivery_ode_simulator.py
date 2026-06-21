import numpy as np
from scipy.integrate import solve_ivp
import json

# MPS-I Core Focus: Intrathecal Nanoparticle Enzyme Delivery Kinetics across Spinal Cord Barriers

# Parameters (example values - these would be determined experimentally/clinically)
params = {
    "dose_it": 1000.0,  # Intrathecal dose of nanoparticles (e.g., nM)
    "k_inj_abs": 0.1,   # Rate of nanoparticle absorption from injection site into CSF (1/hr)
    "k_transcytosis_bsb": 0.05, # Rate of nanoparticle transcytosis across BSB (1/hr)
    "k_efflux_csf": 0.02, # Rate of nanoparticle efflux from CSF (1/hr)
    "k_uptake_chondro": 0.01, # Rate of uptake by spinal chondrocytes (1/hr)
    "k_uptake_meningeal": 0.005, # Rate of uptake by meningeal cells (1/hr)
    "k_degradation_chondro": 0.001, # Rate of GAG degradation in chondrocytes (1/hr)
    "k_degradation_meningeal": 0.0005, # Rate of GAG degradation in meningeal cells (1/hr)
    "V_csf": 150.0, # Volume of CSF (mL)
    "V_chondro": 100.0, # Effective volume of spinal chondrocytes (mL)
    "V_meningeal": 50.0, # Effective volume of meningeal cells (mL)
    "initial_gag_chondro": 10000.0, # Initial GAG concentration in chondrocytes
    "initial_gag_meningeal": 5000.0, # Initial GAG concentration in meningeal cells
}

def mps_i_ode_model(t, y, params):
    """
    ODE model for intrathecal nanoparticle enzyme delivery.
    y = [NP_CSF, NP_Chondrocytes, NP_Meningeal, GAG_Chondrocytes, GAG_Meningeal]
    """
    NP_CSF, NP_Chondrocytes, NP_Meningeal, GAG_Chondrocytes, GAG_Meningeal = y

    # Differential equations
    # d(NP_CSF)/dt: Nanoparticles in Cerebrospinal Fluid (CSF)
    # - Influx from injection site (simplified as absorption into CSF)
    # - Efflux from CSF
    # - Uptake by chondrocytes
    # - Uptake by meningeal cells
    dNP_CSF_dt = (params["dose_it"] * params["k_inj_abs"] * np.exp(-params["k_inj_abs"] * t) / params["V_csf"]) - \
                 (params["k_efflux_csf"] * NP_CSF) - \
                 (params["k_uptake_chondro"] * NP_CSF) - \
                 (params["k_uptake_meningeal"] * NP_CSF)

    # d(NP_Chondrocytes)/dt: Nanoparticles in Spinal Chondrocytes
    # - Uptake from CSF
    # - Loss due to degradation (simplified for enzyme activity)
    dNP_Chondrocytes_dt = (params["k_uptake_chondro"] * NP_CSF) - \
                          (params["k_degradation_chondro"] * NP_Chondrocytes) # Simplified loss

    # d(NP_Meningeal)/dt: Nanoparticles in Meningeal Cells
    # - Uptake from CSF
    # - Loss due to degradation (simplified for enzyme activity)
    dNP_Meningeal_dt = (params["k_uptake_meningeal"] * NP_CSF) - \
                       (params["k_degradation_meningeal"] * NP_Meningeal) # Simplified loss

    # d(GAG_Chondrocytes)/dt: Glycosaminoglycans (GAGs) in Chondrocytes
    # - Degradation by nanoparticles in chondrocytes
    dGAG_Chondrocytes_dt = - (params["k_degradation_chondro"] * NP_Chondrocytes * GAG_Chondrocytes / params["V_chondro"]) # Assuming enzyme activity proportional to NP concentration

    # d(GAG_Meningeal)/dt: Glycosaminoglycans (GAGs) in Meningeal Cells
    # - Degradation by nanoparticles in meningeal cells
    dGAG_Meningeal_dt = - (params["k_degradation_meningeal"] * NP_Meningeal * GAG_Meningeal / params["V_meningeal"]) # Assuming enzyme activity proportional to NP concentration

    return [dNP_CSF_dt, dNP_Chondrocytes_dt, dNP_Meningeal_dt, dGAG_Chondrocytes_dt, dGAG_Meningeal_dt]

# Initial conditions
# [NP_CSF, NP_Chondrocytes, NP_Meningeal, GAG_Chondrocytes, GAG_Meningeal]
y0 = [0.0, 0.0, 0.0, params["initial_gag_chondro"], params["initial_gag_meningeal"]]

# Time span for simulation (e.g., 7 days = 168 hours)
t_span = (0, 168)
t_eval = np.linspace(t_span[0], t_span[1], 500) # Evaluate at 500 points

# Solve the ODEs
sol = solve_ivp(mps_i_ode_model, t_span, y0, args=(params,), dense_output=True, t_eval=t_eval)

# Store results
simulation_results = {
    "time_hours": sol.t.tolist(),
    "NP_CSF": sol.y[0].tolist(),
    "NP_Chondrocytes": sol.y[1].tolist(),
    "NP_Meningeal": sol.y[2].tolist(),
    "GAG_Chondrocytes": sol.y[3].tolist(),
    "GAG_Meningeal": sol.y[4].tolist(),
    "parameters": params
}

# Save results to JSON
output_file = 'research_data/mps_i/nanoparticle_delivery_simulation_results.json'
with open(output_file, 'w') as f:
    json.dump(simulation_results, f, indent=4)

print(f"MPS-I simulation completed and results saved to {output_file}")
