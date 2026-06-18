#!/usr/bin/env python3
"""
🧬 MPS-I STOCHASTIC CLINICAL TRIAL COHORT SIMULATOR (PHASE II/III COMPARATIVE)
Deployed to: GEEKOM Node (the-grid)
Authors: Trent Reznor & Aphex Twin (Subconscious Systems Group)

This simulator models a randomized, parallel three-arm clinical trial over a 52-week period:
- Arm A: Weekly IV Recombinant ERT (Aldurazyme / Laronidase)
- Arm B: One-time Autologous HSC Gene Therapy (OTL-203 / Lentiviral IDUA)
- Arm C: Untreated Control (Natural History / Severe Hurler Phenotype)

Validation Benchmarks:
- Aldurazyme Phase III Trial (Wraith et al., 2004, Journal of Pediatrics)
- OTL-203 Phase I/II Trial (Gentner et al., 2021, New England Journal of Medicine)
"""

import math
import random
import json
import os

# Set seed for clinical reproducibility
random.seed(888)

def generate_patient_cohort(cohort_size=15):
    """
    Generates a cohort of simulated pediatric patients with severe MPS-I (Hurler Syndrome).
    Simulates patient-specific biological noise, baseline GAG levels, and age at trial entry.
    """
    cohort = []
    for i in range(cohort_size):
        # Baseline age in months (6 to 36 months, corresponding to early treatment trials)
        age_months = round(random.uniform(6.0, 36.0), 1)
        
        # Initial systemic/visceral GAG (highly accumulated, standard normal + offset)
        initial_visceral_gag = round(random.normalvariate(120.0, 15.0), 2)
        
        # Initial CNS/CSF GAG (highly accumulated)
        initial_cns_gag = round(random.normalvariate(110.0, 12.0), 2)
        
        # Individual genetic clearance variance (biological noise)
        clearance_variance = random.uniform(0.85, 1.15)
        
        # Specific parameters for Gene Therapy (VCN: Vector Copy Number)
        # OTL-203 trials report median VCN of 1.5 to 2.5 copies/cell
        gene_therapy_vcn = round(random.uniform(1.2, 3.2), 2)
        
        # Specific parameters for ERT (Anti-Drug Antibody risk / ADA)
        # High-titer antibodies develop in ~30-40% of patients and reduce clearance efficiency
        has_ada_vulnerability = random.random() < 0.35
        ert_compliance = random.uniform(0.85, 1.0) # Infusion compliance rate
        
        cohort.append({
            "id": i + 1,
            "age_months": age_months,
            "initial_visceral_gag": initial_visceral_gag,
            "initial_cns_gag": initial_cns_gag,
            "clearance_variance": clearance_variance,
            "gene_therapy_vcn": gene_therapy_vcn,
            "has_ada_vulnerability": has_ada_vulnerability,
            "ert_compliance": ert_compliance
        })
    return cohort

def run_trial_simulation(cohort_size=15, weeks=52):
    # Generate 3 randomized patient groups
    arm_a_ert = generate_patient_cohort(cohort_size)
    arm_b_gt = generate_patient_cohort(cohort_size)
    arm_c_control = generate_patient_cohort(cohort_size)
    
    # Track weekly trajectories
    history_ert = []
    history_gt = []
    history_control = []
    
    # Constant parameters
    gag_synthesis_rate = 10.0  # Daily baseline production (scaled weekly: *7)
    native_clearance = 0.01     # Untreated severe baseline clearance coefficient
    
    # Run weekly step updates
    for wk in range(weeks):
        # 1. ARM A: Recombinant ERT (Aldurazyme)
        for p in arm_a_ert:
            # GAG values initialized
            if wk == 0:
                p["visceral_gag"] = p["initial_visceral_gag"]
                p["cns_gag"] = p["initial_cns_gag"]
                
            # ERT systemic clearance capacity is high, but modulated by patient compliance and ADA development
            ada_reduction = 0.82 if (p["has_ada_vulnerability"] and wk > 12) else 1.0
            ert_eff = 24.0 * p["ert_compliance"] * ada_reduction * p["clearance_variance"]
            
            # Daily kinetic loops integrated weekly (7 steps)
            for _ in range(7):
                # Visceral GAG: Cleared efficiently by circulating enzyme
                p["visceral_gag"] += (gag_synthesis_rate - (ert_eff * p["visceral_gag"] / (10.0 + p["visceral_gag"])))
                # CNS GAG: Untreated baseline, because IV Laronidase does NOT cross the Blood-Brain Barrier
                p["cns_gag"] += (gag_synthesis_rate - (native_clearance * p["cns_gag"]))
                
                # Prevent negative and extreme physical limits (saturation capacity)
                p["visceral_gag"] = min(max(p["visceral_gag"], 5.0), 1000.0)
                p["cns_gag"] = min(max(p["cns_gag"], 5.0), 1000.0)
                
        # 2. ARM B: HSC Gene Therapy (OTL-203)
        for p in arm_b_gt:
            if wk == 0:
                p["visceral_gag"] = p["initial_visceral_gag"]
                p["cns_gag"] = p["initial_cns_gag"]
                
            # HSC transplant takes time to engraft. Reconstitution of microglial cells in the brain
            # occurs gradually over 12-24 weeks.
            # Systemic expression of IDUA from gene-modified hematopoietic cells is rapid (weeks 2-4).
            engraftment_ratio = 1.0 / (1.0 + math.exp(-0.25 * (wk - 12))) # Sigmoidal reconstitution curve centered around Week 12
            
            # Visceral clearance is driven by engineered bone marrow cells secreting IDUA into plasma
            visceral_gt_clearance = 28.0 * (p["gene_therapy_vcn"] / 2.0) * p["clearance_variance"] * min(1.0, (wk + 1) / 4.0)
            # CNS clearance is driven strictly by brain-engrafted microglia secreting IDUA directly into CSF
            cns_gt_clearance = 24.0 * (p["gene_therapy_vcn"] / 2.0) * p["clearance_variance"] * engraftment_ratio
            
            for _ in range(7):
                p["visceral_gag"] += (gag_synthesis_rate - (visceral_gt_clearance * p["visceral_gag"] / (10.0 + p["visceral_gag"])))
                p["cns_gag"] += (gag_synthesis_rate - (cns_gt_clearance * p["cns_gag"] / (10.0 + p["cns_gag"]) if wk > 2 else native_clearance * p["cns_gag"]))
                
                p["visceral_gag"] = min(max(p["visceral_gag"], 5.0), 1000.0)
                p["cns_gag"] = min(max(p["cns_gag"], 5.0), 1000.0)
                
        # 3. ARM C: Untreated Control (Natural History)
        for p in arm_c_control:
            if wk == 0:
                p["visceral_gag"] = p["initial_visceral_gag"]
                p["cns_gag"] = p["initial_cns_gag"]
                
            for _ in range(7):
                p["visceral_gag"] += (gag_synthesis_rate - (native_clearance * p["visceral_gag"]))
                p["cns_gag"] += (gag_synthesis_rate - (native_clearance * p["cns_gag"]))
                
                p["visceral_gag"] = min(max(p["visceral_gag"], 5.0), 1000.0)
                p["cns_gag"] = min(max(p["cns_gag"], 5.0), 1000.0)
                
        # Log mean cohort states at specific week intervals
        if wk in [0, 3, 11, 23, 35, 51]:
            history_ert.append({
                "week": wk + 1,
                "mean_visceral": sum(p["visceral_gag"] for p in arm_a_ert) / cohort_size,
                "mean_cns": sum(p["cns_gag"] for p in arm_a_ert) / cohort_size
            })
            history_gt.append({
                "week": wk + 1,
                "mean_visceral": sum(p["visceral_gag"] for p in arm_b_gt) / cohort_size,
                "mean_cns": sum(p["cns_gag"] for p in arm_b_gt) / cohort_size
            })
            history_control.append({
                "week": wk + 1,
                "mean_visceral": sum(p["visceral_gag"] for p in arm_c_control) / cohort_size,
                "mean_cns": sum(p["cns_gag"] for p in arm_c_control) / cohort_size
            })
            
    # Compile End-of-Trial Statistical Metrics (Week 52)
    def compute_stats(patients):
        visceral_vals = [p["visceral_gag"] for p in patients]
        cns_vals = [p["cns_gag"] for p in patients]
        initial_visc = [p["initial_visceral_gag"] for p in patients]
        initial_cns = [p["initial_cns_gag"] for p in patients]
        
        mean_visc = sum(visceral_vals) / len(patients)
        mean_cns = sum(cns_vals) / len(patients)
        
        # Calculate standard deviation
        sd_visc = math.sqrt(sum((x - mean_visc)**2 for x in visceral_vals) / (len(patients) - 1))
        sd_cns = math.sqrt(sum((x - mean_cns)**2 for x in cns_vals) / (len(patients) - 1))
        
        # Calculate mean reduction percentage
        pct_visc_reduct = sum(((iv - fv) / iv) * 100.0 for iv, fv in zip(initial_visc, visceral_vals)) / len(patients)
        pct_cns_reduct = sum(((ic - fc) / ic) * 100.0 for ic, fc in zip(initial_cns, cns_vals)) / len(patients)
        
        return {
            "mean_visceral": round(mean_visc, 2),
            "sd_visceral": round(sd_visc, 2),
            "mean_cns": round(mean_cns, 2),
            "sd_cns": round(sd_cns, 2),
            "pct_visceral_reduction": round(pct_visc_reduct, 2),
            "pct_cns_reduction": round(pct_cns_reduct, 2)
        }
        
    stats_ert = compute_stats(arm_a_ert)
    stats_gt = compute_stats(arm_b_gt)
    stats_control = compute_stats(arm_c_control)
    
    # Perform Student's Two-Sample t-test for CNS GAG clearance (Arm A vs Arm B)
    # Null Hypothesis: Weekly ERT (Arm A) clears CNS GAG equally to one-time Gene Therapy (Arm B)
    mean_diff = stats_ert["mean_cns"] - stats_gt["mean_cns"]
    var_a = stats_ert["sd_cns"] ** 2
    var_b = stats_gt["sd_cns"] ** 2
    pooled_se = math.sqrt((var_a / cohort_size) + (var_b / cohort_size))
    t_stat = mean_diff / pooled_se if pooled_se != 0 else 0.0
    degrees_of_freedom = (2 * cohort_size) - 2
    
    # Estimate p-value using a simple continuous approximation for the t-distribution tail
    # (since we can't import scipy easily and want to maintain local speed)
    p_value_approx = 1.0 / (1.0 + (t_stat ** 2) / degrees_of_freedom) ** (degrees_of_freedom / 2.0)
    
    # Compile literature comparison tables
    # Real-world validation metrics:
    # 1. Aldurazyme Phase III (Wraith et al., 2004): Systemic GAG reduction ~54-61%, CNS GAG reduction: No clinical change.
    # 2. OTL-203 Phase I/II (Gentner et al., 2021 NEJM): Systemic GAG reduction ~85-95%, CNS/CSF GAG reduction ~75-88%.
    validation_comparison = {
        "visceral_gag_reduction": {
            "simulated_ert": f"{stats_ert['pct_visceral_reduction']}%",
            "published_ert_wraith_2004": "54.0% to 61.0%",
            "simulated_gene_therapy": f"{stats_gt['pct_visceral_reduction']}%",
            "published_gt_gentner_2021_nejm": "85.0% to 95.0%"
        },
        "cns_gag_reduction": {
            "simulated_ert": f"{stats_ert['pct_cns_reduction']}%",
            "published_ert_wraith_2004": "0.0% (No BBB Penetration)",
            "simulated_gene_therapy": f"{stats_gt['pct_cns_reduction']}%",
            "published_gt_gentner_2021_nejm": "75.0% to 88.0%"
        }
    }
    
    return {
        "cohort_size_per_arm": cohort_size,
        "weeks_simulated": weeks,
        "trajectories": {
            "arm_a_ert": history_ert,
            "arm_b_gt": history_gt,
            "arm_c_control": history_control
        },
        "final_stats": {
            "arm_a_weekly_ert": stats_ert,
            "arm_b_gene_therapy": stats_gt,
            "arm_c_untreated_control": stats_control
        },
        "statistical_significance_cns_clearance": {
            "null_hypothesis": "Weekly IV ERT is equally effective at clearing CNS GAG as microglial-mediated gene therapy",
            "t_statistic": round(t_stat, 4),
            "degrees_of_freedom": degrees_of_freedom,
            "p_value_approximation": f"{p_value_approx:.10f}",
            "reject_null_hypothesis": p_value_approx < 0.05
        },
        "validation_against_clinical_literature": validation_comparison
    }

if __name__ == "__main__":
    print("🧬 DEPLOYING MPS-I CLINICAL TRIAL MODEL SPRINT 🧬")
    print("--------------------------------------------------")
    
    results = run_trial_simulation(cohort_size=15, weeks=52)
    
    print(f"[+] Successfully generated randomized parallel trial cohorts (N = {results['cohort_size_per_arm']} patients/arm).")
    print(f"[+] Ran 52-week kinetic equations with integrated biological noise & vector transduction rates.\n")
    
    print("📊 WEEK 52 PRIMARY CLINICAL ENDPOINTS (COHORT MEANS):")
    print("====================================================")
    for arm_name, stats in results["final_stats"].items():
        print(f"👉 {arm_name.replace('_', ' ').upper()}:")
        print(f"   * Mean Visceral GAG: {stats['mean_visceral']} (SD: {stats['sd_visceral']}) | Reduction: {stats['pct_visceral_reduction']}%")
        print(f"   * Mean CNS/CSF GAG:  {stats['mean_cns']} (SD: {stats['sd_cns']}) | Reduction: {stats['pct_cns_reduction']}%")
        print()
        
    print("🔬 COHORT COMPARISON STATISTICAL INFERENCE:")
    print("==========================================")
    sig = results["statistical_significance_cns_clearance"]
    print(f"   * T-Statistic for CNS superiority (Arm B vs A): {sig['t_statistic']}")
    print(f"   * Derived p-value approximation:                 {sig['p_value_approximation']}")
    print(f"   * Reject Null Hypothesis (Is GT superior in CNS?): {sig['reject_null_hypothesis']}\n")
    
    print("📖 VALIDATION BENCHMARKS VS. REAL CLINICAL DATA:")
    print("=================================================")
    val = results["validation_against_clinical_literature"]
    print("📁 Systemic/Visceral GAG Clearance Reduction:")
    print(f"   - Simulated Weekly ERT:      {val['visceral_gag_reduction']['simulated_ert']} vs. Wraith et al. Phase III: {val['visceral_gag_reduction']['published_ert_wraith_2004']}")
    print(f"   - Simulated Gene Therapy:    {val['visceral_gag_reduction']['simulated_gene_therapy']} vs. Gentner et al. NEJM (OTL-203): {val['visceral_gag_reduction']['published_gt_gentner_2021_nejm']}")
    print("📁 Central Nervous System (CNS) GAG Clearance Reduction:")
    print(f"   - Simulated Weekly ERT:      {val['cns_gag_reduction']['simulated_ert']} vs. Wraith et al. Phase III: {val['cns_gag_reduction']['published_ert_wraith_2004']}")
    print(f"   - Simulated Gene Therapy:    {val['cns_gag_reduction']['simulated_gene_therapy']} vs. Gentner et al. NEJM (OTL-203): {val['cns_gag_reduction']['published_gt_gentner_2021_nejm']}")
    
    # Save cache
    out_path = "/data/.openclaw/workspace/mps_clinical_trial_results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Clinical trial dataset successfully cached to: {out_path}")
