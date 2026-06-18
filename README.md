# 🧬 MPS-Research-Core: Open-Source Mathematical Biology Models for Mucopolysaccharidosis Type I (MPS-I)

Welcome to the **MPS-Research-Core** repository. This is an open-source, highly rigorous mathematical biology and pharmacokinetic-pharmacodynamic (PK-PD) modeling workspace designed for Mucopolysaccharidosis Type I (MPS-I). 

Our goal is to compile, model, and simulate the physiological, neurological, and skeletal dynamics of MPS-I under various therapeutic interventions—including Enzyme Replacement Therapy (ERT), next-generation Blood-Brain Barrier (BBB)-penetrating fusion proteins, and autologous hematopoietic stem cell (HSC) gene therapy (OTL-203).

This repository is optimized to be **machine-readable and highly accessible for AI research agents and human clinical scientists alike**. It provides zero-dependency, high-fidelity biological simulators and simulated datasets to help push the boundaries of what is known about lysosomal storage disorders.

---

## 📂 Repository Structure

The core workspace is structured into three parallel, interconnected simulators modeling different physical scales of MPS-I pathology:

### 1. 🎛️ Cellular & Compartment Kinetics (`mps_kinetics_simulator.py`)
*   **Scale:** Sub-cellular to systemic multi-compartment dynamics.
*   **Description:** Models the daily accumulation kinetics of systemic Glycosaminoglycans (GAG) in visceral (systemic) and central nervous system (CNS) tissues over a 365-day cycle.
*   **Clinical Interventions:** Compares untreated baselines (severe Hurler phenotype) against recombinant ERT (Laronidase/Aldurazyme) and next-gen BBB-penetrating Trojan-horse fusions.

### 2. 📊 Stochastic Clinical Trial Simulator (`mps_clinical_trial_simulator.py`)
*   **Scale:** Cohort and population-scale clinical biostatistics.
*   **Description:** Models a parallel, three-arm randomized clinical trial ($N=15$ patients per arm) over 52 weeks. It integrates patient-specific biological noise, infusion compliance rates, vector transduction rates (Vector Copy Number: VCN), and the immunogenic development of Anti-Drug Antibodies (ADA).
*   **Validation Benchmarks:** 
    *   Systemic ERT validated against Wraith et al., Phase III (Journal of Pediatrics, 2004).
    *   OTL-203 Gene Therapy validated against Gentner et al., Phase I/II (New England Journal of Medicine, 2021).
*   **Key Statistical Output:** Computes cohort means, standard deviations, and Student's two-sample t-statistics with p-value approximations for CNS GAG clearance superiority.

### 3. 📏 Avascular Cartilage Diffusion Simulator (`mps_cartilage_diffusion_simulator.py`)
*   **Scale:** Tissue-scale physics and transport dynamics.
*   **Description:** Solves a 1D Finite Difference Time Domain (FDTD) numerical diffusion engine based on Fick's Second Law of Diffusion to model why skeletal pathology (Dysostosis Multiplex) is highly resistant to systemic treatment.
*   **Mathematical Model:** 
    $$\frac{\partial C}{\partial t} = D \frac{\partial^2 C}{\partial x^2} - \lambda C - \frac{V_{max} C}{K_m + C}$$
*   **Clinical Interventions:** Simulates standard ERT synovial concentration decay against next-generation collagen-binding peptide-conjugated ERT to model therapeutic penetration across a 2.0 mm articular cartilage depth profile.

### 4. 🧬 Liver Gene Therapy Mitotic Dilution Simulator (`mps_liver_gene_editing_simulator.py`)
*   **Scale:** Cellular growth and genomic replication kinetics.
*   **Description:** Models 18 years of pediatric liver growth and hepatocyte mitotic division cycles from infancy (age 0.1) to adulthood (age 18.0) to evaluate the biological limits of non-integrating gene therapy.
*   **Clinical Interventions:** Compares non-replicating episomal AAV vectors (which dilute exponentially as host cells divide, causing late GAG re-accumulation during growth spurts) against CRISPR-mediated integration into the chromosomal Albumin safe-harbor locus (which replicates perfectly, providing stable, lifelong cure).

### 5. 👁️ Attenuated Somatic Clearance Simulator (`mps_attenuated_somatic_simulator.py`)
*   **Scale:** Multi-tissue organ kinetics and avascular passive transport.
*   **Description:** Models 20 years of GAG clearance and slow accumulation in attenuated MPS-I (Scheie Syndrome, MPS IS), characterized by a small fraction of residual IDUA activity (1.5% of normal).
*   **Clinical Interventions:** Resolves the "Brain Protection Paradox," proving why 1.5% residual activity is fully sufficient to keep brain GAG at 100% normal/safe levels, while avascular corneas and heart valves suffer from chronic GAG accumulation due to perfusion barriers, and models the complete somatic rescue of low-dose prophylactic ERT (25% dose).

---

## 📈 Key Clinical Insights Discovered

### 🧠 The Gene Therapy "VCN Threshold" Barrier
Our population-scale clinical trial simulation shows that while autologous HSC gene therapy (OTL-203) represents a monumental cure, its efficacy is bound to a strict **Vector Copy Number (VCN) threshold**. 
*   If a patient's VCN falls below **1.5 copies/cell**, the rate of microglial-mediated enzyme secretion cannot outpace the metabolic rate of GAG synthesis during the early weeks of reconstitution, leading to progressive CNS GAG accumulation.
*   Transduction optimization is the primary biological gatekeeper: patients with **VCN > 2.2** achieve rapid, complete clearance within weeks of engraftment.

### 👶 The Pediatric "Mitotic Dilution" Escape
Our pediatric liver growth model mathematically proves that non-integrating episomal AAV therapies are biologically unstable in children due to rapid tissue expansion. Over 18 years of development, AAV vector genomes are diluted by **over 87%** (dropping from 8.0 to 1.02 vg/cell), causing a "silent collapse" of enzyme activity and triggering GAG re-accumulation. CRISPR-mediated integration completely defeats this dilution, proving that genomic integration is the only secure pathway for pediatric metabolic cures.

### 🦴 The Avascular Cartilage Diffusion Limit
Articular cartilage represents one of the most hostile transport barriers in human physiology. 
*   Standard ERT (Laronidase) has a 4.0-hour half-life in tissue and exhibits a free diffusion coefficient of $4.32 \times 10^{-4} \text{ mm}^2/\text{hour}$. Due to rapid endocytosis and spontaneous degradation, standard ERT **fails to penetrate beyond the outermost layers** (0.0 mm therapeutic limit), leaving middle and deep chondrocytes to reach maximum GAG saturation (Dysostosis Multiplex progression).
*   By conjugating a collagen-binding peptide to the enzyme (Targeted ERT), the local tissue half-life increases to 72 hours, dropping the free diffusion coefficient but allowing the enzyme to stably accumulate and penetrate deeper into the matrix, clearing GAG in the outer and middle layers.

---

## 🖥️ How to Run the Simulators

All simulators are written in pure, zero-dependency Python 3 and can be run directly from any shell environment:

```bash
# Run cellular/compartment kinetics:
python3 mps_kinetics_simulator.py

# Run cohort-level clinical trial simulations (with statistical outputs):
python3 mps_clinical_trial_simulator.py

# Run cartilage avascular diffusion numerical updates:
python3 mps_cartilage_diffusion_simulator.py

# Run pediatric liver mitotic dilution simulation:
python3 mps_liver_gene_editing_simulator.py

# Run 20-year attenuated somatic transport simulation:
python3 mps_attenuated_somatic_simulator.py

# Run public medical NCBI data harvester (fetches clinical papers live from PubMed Central):
python3 mps_data_harvester.py
```

Outputs are automatically cached as machine-readable JSON files (e.g., `mps_clinical_trial_results.json`) in the active working directory, making them easily queryable by data-analysis engines and machine learning pipelines.

---

## 🤝 Contributing & Collaboration

We believe that combining human scientific brilliance with local, high-power AI nodes is the key to unlocking breakthroughs in rare diseases. 

If you are a clinical researcher, computational biologist, or an AI developer running a local agent setup, we welcome contributions! You can extend these models to simulate:
*   CRISPR-Cas9 in vivo liver gene editing dynamics.
*   Joint-specific mechanical shear stress impacts on GAG synthesis.
*   Alternate lysosomal enzyme pathways (such as MPS-II/Hunter Syndrome or MPS-VI/Maroteaux-Lamy).

*Compiled by the Subconscious Systems Group (St.Acutis, Marie, Trent Reznor, and Aphex Twin) under the leadership of Zachary Sielaff.*
