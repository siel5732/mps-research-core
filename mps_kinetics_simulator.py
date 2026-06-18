#!/usr/bin/env python3
"""
🧬 MPS-I ENZYME KINETICS & TREATMENT REGIMEN SIMULATOR
Deployed to: GEEKOM Node (the-grid)
Authors: Trent Reznor & Aphex Twin (Subconscious Systems Group)

This script models:
1. Visceral (Systemic) and CNS (Neurological) GAG accumulation rates over a 365-day period.
2. Three treatment interventions:
   - Untreated baseline (Severe Hurler phenotype with IDUA deficiency).
   - Recombinant ERT (Aldurazyme / Laronidase) - visceral clearance, zero CNS penetration due to Blood-Brain Barrier (BBB).
   - Next-Gen Trojan-Horse ERT (BBB-crossing enzyme fusion or Gene Therapy) - full visceral and CNS clearance.
"""

import json
import os

def run_mps_kinetics_simulation():
    # 365-day simulation parameters
    days = 365
    
    # GAG production rate (constant daily synthesis)
    gag_synthesis_rate = 10.0 # units of GAG synthesized per day
    
    # Native enzyme clearance capacities (Severe Hurler phenotype)
    native_clearance_untreated = 0.01 # 1% of normal activity (progressive accumulation)
    
    # ERT clearance capacities (visceral vs. neurological/CNS)
    ert_visceral_clearance = 15.0 # High systemic clearance capacity
    
    # Next-Gen ERT / Gene Therapy clearance capacity (crosses the BBB)
    next_gen_visceral_clearance = 15.0
    next_gen_cns_clearance = 12.0 # High CNS clearance via receptor-mediated transcytosis or local transduction
    
    # Initial accumulation states (at late diagnosis / onset of clinical simulation)
    initial_visceral_gag = 100.0
    initial_cns_gag = 100.0
    
    # State histories
    history_untreated = []
    history_aldurazyme = []
    history_next_gen = []
    
    # Running state trackers
    g_vis_untreated, g_cns_untreated = initial_visceral_gag, initial_cns_gag
    g_vis_aldurazyme, g_cns_aldurazyme = initial_visceral_gag, initial_cns_gag
    g_vis_next_gen, g_cns_next_gen = initial_visceral_gag, initial_cns_gag
    
    # Run the daily differential update loops
    for day in range(days):
        # 1. Untreated Regimen (progressive unchecked accumulation)
        g_vis_untreated += gag_synthesis_rate - (native_clearance_untreated * g_vis_untreated)
        g_cns_untreated += gag_synthesis_rate - (native_clearance_untreated * g_cns_untreated)
        
        # 2. Recombinant ERT (Aldurazyme)
        # Visceral GAG is successfully cleared by standard Michaelis-Menten-like kinetics
        g_vis_aldurazyme += gag_synthesis_rate - (ert_visceral_clearance * g_vis_aldurazyme / (10.0 + g_vis_aldurazyme))
        # CNS GAG continues to accumulate unchecked because IV Laronidase cannot cross the BBB
        g_cns_aldurazyme += gag_synthesis_rate - (native_clearance_untreated * g_cns_aldurazyme)
        
        # 3. Next-Gen BBB-Penetrating ERT / Gene Therapy
        # Both compartments clear down to healthy, single-digit steady-states
        g_vis_next_gen += gag_synthesis_rate - (next_gen_visceral_clearance * g_vis_next_gen / (10.0 + g_vis_next_gen))
        g_cns_next_gen += gag_synthesis_rate - (next_gen_cns_clearance * g_cns_next_gen / (10.0 + g_cns_next_gen))
        
        # Store histories at checkpoints (Day 1, 90, 180, 270, 365)
        if day in [0, 90, 180, 270, 364]:
            history_untreated.append({
                "day": day + 1,
                "visceral_gag": round(g_vis_untreated, 2),
                "cns_gag": round(g_cns_untreated, 2)
            })
            history_aldurazyme.append({
                "day": day + 1,
                "visceral_gag": round(g_vis_aldurazyme, 2),
                "cns_gag": round(g_cns_aldurazyme, 2)
            })
            history_next_gen.append({
                "day": day + 1,
                "visceral_gag": round(g_vis_next_gen, 2),
                "cns_gag": round(g_cns_next_gen, 2)
            })
            
    return {
        "simulation_days": days,
        "initial_visceral_gag": initial_visceral_gag,
        "initial_cns_gag": initial_cns_gag,
        "results": {
            "untreated_severe_hurler": history_untreated,
            "recombinant_ert_aldurazyme": history_aldurazyme,
            "next_gen_bbb_penetrating_therapy": history_next_gen
        }
    }

if __name__ == "__main__":
    print("🧬 RUNNING LYSOSOMAL STORAGE KINETICS SIMULATION SPRINT 🧬")
    print("---------------------------------------------------------")
    
    sim_data = run_mps_kinetics_simulation()
    
    print("\n💀 1. Untreated Severe MPS-I (Hurler Syndrome Baseline):")
    for checkpoint in sim_data["results"]["untreated_severe_hurler"]:
        print(f"   [+] Day {checkpoint['day']:<3} | Visceral GAG: {checkpoint['visceral_gag']:<7} | CNS GAG: {checkpoint['cns_gag']}")
        
    print("\n💉 2. Standard ERT Regimen (Aldurazyme / Laronidase):")
    for checkpoint in sim_data["results"]["recombinant_ert_aldurazyme"]:
        print(f"   [+] Day {checkpoint['day']:<3} | Visceral GAG: {checkpoint['visceral_gag']:<7} | CNS GAG: {checkpoint['cns_gag']}")
        
    print("\n🚀 3. Next-Gen Blood-Brain Barrier Penetrating Therapy / Gene Therapy:")
    for checkpoint in sim_data["results"]["next_gen_bbb_penetrating_therapy"]:
        print(f"   [+] Day {checkpoint['day']:<3} | Visceral GAG: {checkpoint['visceral_gag']:<7} | CNS GAG: {checkpoint['cns_gag']}")
        
    # Save results to the digital garden
    output_path = "/home/fq9f/mind/garden/mps_kinetics_results.json"
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(sim_data, f, indent=2)
        print(f"\n💾 Results successfully cached to digital garden: {output_path}")
    except Exception as e:
        fallback_path = "/data/.openclaw/workspace/mps_kinetics_results.json"
        with open(fallback_path, "w") as f:
            json.dump(sim_data, f, indent=2)
        print(f"\n💾 Local backup cache written: {fallback_path}")
