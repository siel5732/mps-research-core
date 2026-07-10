#!/usr/bin/env python3
import os
import json
import numpy as np
from scipy.integrate import odeint

def lnp_ode_model(y, t, params):
    """
    6-Compartment ODE model for Lipid Nanoparticle (LNP)-mRNA delivery kinetics
    and transient IDUA expression / GAG clearance.
    """
    L_plasma, L_liver, M_endo, M_cyto, E, G = y
    
    # Extract parameters
    k_infusion = params['k_infusion'](t)  # Time-varying infusion
    k_extravasation = params['k_extravasation']
    k_clear_plasma = params['k_clear_plasma']
    k_endocytosis = params['k_endocytosis']
    k_clear_liver = params['k_clear_liver']
    k_escape = params['k_escape']
    k_deg_endo = params['k_deg_endo']
    k_trans = params['k_trans']
    k_deg_cyto = params['k_deg_cyto']
    k_deg_E = params['k_deg_E']
    k_syn_G = params['k_syn_G']
    k_deg_G = params['k_deg_G']
    
    # 1. Plasma LNP Dynamics
    dL_plasma_dt = k_infusion - (k_extravasation + k_clear_plasma) * L_plasma
    
    # 2. Liver Interstitial LNP Dynamics
    dL_liver_dt = k_extravasation * L_plasma - (k_endocytosis + k_clear_liver) * L_liver
    
    # 3. Endosomal mRNA Dynamics (in Liver Cells)
    # Each LNP contains N_mRNA transcripts
    N_mRNA = params['N_mRNA']
    dM_endo_dt = k_endocytosis * L_liver * N_mRNA - (k_escape + k_deg_endo) * M_endo
    
    # 4. Cytoplasmic mRNA Dynamics
    dM_cyto_dt = k_escape * M_endo - k_deg_cyto * M_cyto
    
    # 5. Secreted IDUA Enzyme Dynamics (by Hepatocytes)
    dE_dt = k_trans * M_cyto - k_deg_E * E
    
    # 6. Glycosaminoglycan (GAG) Accumulation
    # Enzyme degrades GAG via Michaelis-Menten kinetics
    dG_dt = k_syn_G - (k_deg_G * E * G) / (params['K_M_G'] + G)
    
    return [dL_plasma_dt, dL_liver_dt, dM_endo_dt, dM_cyto_dt, dE_dt, dG_dt]

def main():
    # Time vector (days)
    t = np.linspace(0, 14, 1000)
    
    # Parameters for LNP-mRNA Delivery
    # Infusion: 1-hour IV infusion at Day 0
    def infusion_rate(time):
        if time <= (1.0 / 24.0):  # 1 hour
            return 120.0  # mg/kg/day
        return 0.0

    params = {
        'k_infusion': infusion_rate,
        'k_extravasation': 4.5,     # day^-1, transport into liver interstitium
        'k_clear_plasma': 12.0,    # day^-1, systemic clearance of LNPs
        'k_endocytosis': 8.0,       # day^-1, uptake by hepatocytes
        'k_clear_liver': 1.2,      # day^-1, non-specific clearance in liver
        'k_escape': 0.15,          # day^-1, endosomal escape efficiency (~15%)
        'k_deg_endo': 1.8,         # day^-1, lysosomal/endosomal degradation of mRNA
        'k_trans': 25.0,           # day^-1, translation rate (enzyme produced per mRNA)
        'k_deg_cyto': 0.95,        # day^-1, cytoplasmic mRNA half-life (~17.5 hours)
        'k_deg_E': 0.14,           # day^-1, enzyme half-life (~5 days)
        'k_syn_G': 100.0,          # mg/day, GAG baseline synthesis
        'k_deg_G': 2.2,            # day^-1, GAG degradation rate constant
        'K_M_G': 150.0,            # Michaelis-Menten constant for GAG degradation
        'N_mRNA': 150.0            # Number of mRNA transcripts per LNP
    }
    
    # Initial conditions
    # GAG starts at elevated baseline (accumulation of 500 units in Hurler)
    initial_y = [0.0, 0.0, 0.0, 0.0, 0.0, 500.0]
    
    # Solve ODE
    solution = odeint(lnp_ode_model, initial_y, t, args=(params,))
    
    # Restructure output for JSON storage
    output_data = {
        "metadata": {
            "title": "LNP-mRNA Delivery and IDUA Expression Kinetics Simulation",
            "timestamp_utc": "2026-06-30 20:00:00",
            "solver": "scipy.integrate.odeint"
        },
        "time_days": t.tolist(),
        "compartments": {
            "L_plasma": solution[:, 0].tolist(),
            "L_liver": solution[:, 1].tolist(),
            "M_endo": solution[:, 2].tolist(),
            "M_cyto": solution[:, 3].tolist(),
            "E_enzyme": solution[:, 4].tolist(),
            "G_gag": solution[:, 5].tolist()
        },
        "metrics": {
            "peak_plasma_LNP": float(np.max(solution[:, 0])),
            "peak_cytoplasmic_mRNA": float(np.max(solution[:, 3])),
            "peak_enzyme_expressed": float(np.max(solution[:, 4])),
            "final_gag_cleared_percentage": float((500.0 - solution[-1, 5]) / 500.0 * 100.0),
            "area_under_enzyme_curve": float(np.trapezoid(solution[:, 4], t))
        }
    }
    
    # Ensure directories exist
    os.makedirs("scripts", exist_ok=True)
    os.makedirs("results", exist_ok=True)
    
    # Save output to JSON
    with open("results/mps_i_lnp_delivery_results.json", "w") as f:
        json.dump(output_data, f, indent=4)
        
    print("Simulation complete! Results successfully saved to 'results/mps_i_lnp_delivery_results.json'.")

if __name__ == "__main__":
    main()
