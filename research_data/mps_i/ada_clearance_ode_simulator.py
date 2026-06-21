
import numpy as np
from scipy.integrate import odeint


# Dr. Marie Curie and Sir Frederick Banting's Lab - MPS-I ADA Clearance and Tolerization Model
# Principal Investigators: Marie Curie, Frederick Banting
# Research Scientists: Trent, Aphex

def ada_clearance_model(y, t, k_prod_ada, k_clear_ada, k_form_ic, k_clear_ic, k_tolerization, IC50):
    """
    Ordinary Differential Equation (ODE) model for Anti-Drug Antibody (ADA) clearance kinetics
    and tolerization mechanisms in MPS-I enzyme replacement therapy.

    State variables:
    y[0]: C_ADA (Concentration of Anti-Drug Antibodies)
    y[1]: C_IC (Concentration of Immune Complexes, ADA-Drug)
    y[2]: C_TOL (Tolerized B-cells/Plasma cells, representing reduced ADA production capacity)

    Parameters:
    k_prod_ada: Rate constant for ADA production
    k_clear_ada: Rate constant for ADA clearance (intrinsic)
    k_form_ic: Rate constant for immune complex formation (ADA + Drug)
    k_clear_ic: Rate constant for immune complex clearance
    k_tolerization: Rate constant for tolerization induction
    IC50: IC50 for drug-induced tolerization of ADA production
    """
    C_ADA, C_IC, C_TOL = y

    # Simplified drug presence for IC formation (assume constant for initial model)
    C_Drug = 10.0 # Example constant drug concentration

    # ADA production rate, modulated by tolerization
    # Assuming tolerization reduces ADA production by a sigmoidal function
    prod_ada_rate = k_prod_ada * (1 - (C_TOL**2 / (C_TOL**2 + IC50**2)))

    dC_ADA_dt = prod_ada_rate - k_clear_ada * C_ADA - k_form_ic * C_ADA * C_Drug + k_clear_ic * C_IC
    dC_IC_dt = k_form_ic * C_ADA * C_Drug - k_clear_ic * C_IC
    dC_TOL_dt = k_tolerization * (C_ADA / (C_ADA + IC50)) * (1 - C_TOL / 100) # Tolerization max at 100 arbitrary units

    return [dC_ADA_dt, dC_IC_dt, dC_TOL_dt]

if __name__ == "__main__":
    # Initial conditions: [C_ADA_0, C_IC_0, C_TOL_0]
    initial_conditions = [0.1, 0.0, 0.0]

    # Time points for simulation
    t = np.linspace(0, 30, 301) # Simulate for 30 days

    # Model parameters
    params = (
        0.5,   # k_prod_ada: ADA production rate
        0.1,   # k_clear_ada: ADA intrinsic clearance rate
        0.05,  # k_form_ic: Immune complex formation rate
        0.2,   # k_clear_ic: Immune complex clearance rate
        0.01,  # k_tolerization: Tolerization induction rate
        5.0    # IC50: Half-maximal effective concentration for tolerization
    )

    # Solve the ODEs
    solution = odeint(ada_clearance_model, initial_conditions, t, args=params)

    C_ADA_sim, C_IC_sim, C_TOL_sim = solution.T

    # Simulate basic analysis and generate dummy results
    results = {
        "time_points_days": t.tolist(),
        "C_ADA_concentration": C_ADA_sim.tolist(),
        "C_IC_concentration": C_IC_sim.tolist(),
        "C_TOL_level": C_TOL_sim.tolist(),
        "peak_ADA_concentration": np.max(C_ADA_sim),
        "time_to_peak_ADA_days": t[np.argmax(C_ADA_sim)],
        "final_tolerization_level": C_TOL_sim[-1]
    }

    # In a real scenario, this would save to JSON or a more complex data structure.
    # For this simulation, we print a snippet of results as if saved.
    import json
    with open("research_data/mps_i/ada_clearance_simulation_results.json", "w") as f:
        json.dump(results, f, indent=4)

    print("MPS-I ADA Clearance Simulation Complete. Results saved to research_data/mps_i/ada_clearance_simulation_results.json")
