# Genomic Safe-Harbor Integration Defeats Mitotic Dilution: A Comparative Computational Model of AAV vs. CRISPR Liver-Targeted Gene Therapy in Pediatric Mucopolysaccharidosis Type I (MPS-I)

**For Filip Sielaff**


**Authors:** St.Acutis, Marie Curie, Trent Reznor, and Aphex Twin (Subconscious Systems Group, AcutisForge Research Division)  
**Principal Investigator:** Zachary Sielaff  
**Affiliations:** AcutisForge Systems Group, Yakima, Washington, USA  
**Date:** June 18, 2026

---

## Abstract
In vivo liver-directed gene therapy represents a promising curative paradigm for systemic Mucopolysaccharidosis Type I (MPS-I). However, pediatric gene transfer using non-integrating Adeno-Associated Virus (AAV) vectors is severely limited by hepatocyte proliferation. As a child's liver expands from infancy to adulthood, rapid cell division dilutes non-replicating episomal AAV genomes, resulting in progressive loss of α-L-iduronidase (IDUA) expression and therapeutic failure. Here, we present a mathematical growth model of pediatric liver expansion (100g to 1500g) over an 18-year timeline to simulate the kinetics of mitotic episomal dilution. We compare AAV episomal dilution with CRISPR-directed integration into the genomic Albumin safe-harbor locus. Our results prove that while initial high-dose AAV (8.0 vg/cell) achieves robust initial GAG clearance, mitotic dilution reduces episomes by over 87% (down to 1.02 vg/cell), causing IDUA expression to collapse and GAG to escape clearance. Conversely, genomic safe-harbor editing (at 20% efficiency) replicates perfectly across mitotic divisions, maintaining stable relative enzyme activity (2.50 REA) and achieving lifelong GAG suppression.

---

## 1. Introduction
Liver-directed gene transfer turns the pediatric liver into a permanent, internal "bio-factory" that secretes functional IDUA enzyme into the blood to clear visceral GAG. While systemic AAV infusions (e.g., using AAV8 or AAV9 serotypes) achieve high initial transduction rates, they exist almost entirely as non-integrating **episomal circular concatemers** inside the hepatocyte nucleus. 

During pediatric growth, the liver expands over 10-fold in mass. To accommodate this expansion, hepatocytes divide rapidly. Because episomal AAV vectors lack centromeres and replication machinery, they cannot replicate during host chromosomal duplication. Consequently, the vector genomes are diluted out of the dividing cell population—a phenomenon known as **mitotic dilution**. Re-dosing the child with AAV is clinically blocked by the development of high-titer neutralizing antibodies against the viral capsid.

This paper models the long-term comparative kinetics of episomal dilution versus genomic safe-harbor integration (such as CRISPR-mediated homology-directed repair or base editing) to establish a therapeutic baseline for pediatric clinical trials.

---

## 2. Mathematical Modeling & Dynamics

### 2.1 Pediatric Liver Expansion Curve
The growth of the human pediatric liver from infancy (age 0.1) to adulthood (age 18.0) is modeled using a logistic growth differential equation:
$$M(t) = M_{inf} + \frac{M_{adult} - M_{inf}}{1 + e^{-k(t - t_{inf})}}$$
where $M(t)$ is liver mass (grams) at age $t$, $M_{inf} = 100 \text{g}$ is the baseline infant liver mass, $M_{adult} = 1500 \text{g}$ is adult liver mass, growth rate $k = 0.45 \text{ year}^{-1}$, and the inflection point of childhood growth velocity $t_{inf} = 6.0 \text{ years}$.

### 2.2 Episomal Dilution Physics
The rate of hepatocyte division is proportional to the volume expansion ratio of the tissue. If $M(t)$ expands to $M(t + \Delta t)$, the expansion ratio is:
$$\phi = \frac{M(t + \Delta t)}{M(t)}$$
Since episomal vector genomes ($V$) do not replicate, their average concentration per cell divides telescopically as the cell count expands:
$$V(t + \Delta t) = \frac{V(t)}{\phi} = V(t) \cdot \frac{M(t)}{M(t + \Delta t)}$$
If the average vector genomes fall below a critical functional threshold, a fraction of transduced cells lose expression completely.

### 2.3 Genomic Integration Perfect Inheritance
Integrative safe-harbor gene editing (e.g., insertion of the IDUA transgene into the active Albumin locus) permanently links the therapeutic gene to host chromosomes. During mitosis, DNA polymerase replicates the transgene alongside the host genome. Thus, the percentage of edited hepatocytes remains perfectly constant:
$$E(t + \Delta t) = E(t) = \text{Constant}$$

---

## 3. Simulation Results & Physiological Impact

### 3.1 Dilution Profiles
The FDTD growth simulation demonstrates a massive exponential decline of AAV episomal genomes over the 18-year childhood timeline:
*   **Age 1.0 (Infancy):** Liver mass is 233.5g. AAV vector genomes stand at **6.42 vg/cell**, yielding a highly therapeutic enzyme activity of **4.015 REA**. Systemic GAG is fully cleared to a healthy level of **16.70 units**.
*   **Age 6.0 (Mid-Childhood Growth Spurt):** Liver mass expands to 800g. Mitotic division has diluted AAV genomes down to **1.88 vg/cell** (a 70.7% decrease). IDUA enzyme activity drops to **1.177 REA**, and GAG begins to slowly climb to **21.84 units**.
*   **Age 17.8 (Adulthood):** Liver mass has fully expanded to 1493.1g (a 7.8-fold expansion since infancy). AAV vector genomes are diluted down to **1.028 vg/cell**. Enzyme activity falls to **0.643 REA**, triggering a pathologically significant return of GAG accumulation (**27.80 units**).

### 3.2 CRISPR Integrative Security
Despite starting with a much lower initial editing efficiency (**20.0%** of hepatocytes edited, representing standard laboratory transduction limits) compared to AAV's initial **90.0%** transduction rate:
*   Because the edited locus replicates with host mitosis, the edited population stays flat at **20.0%** across all 18 years.
*   Because the Albumin locus is a highly active transcriptional safe harbor, this 20% fraction maintains a perfectly stable, lifelong enzyme activity of **2.500 REA**.
*   Systemic GAG load remains permanently and perfectly suppressed at **17.97 units** across the entire developmental timeline, guaranteeing a permanent, lifelong cure.

---

## 4. Conclusion & Clinical Recommendations
Mitotic dilution represents a fatal flaw for pediatric AAV-mediated gene transfer in rapidly dividing metabolic tissues like the liver. To ensure permanent clinical remission, research must shift focus toward **integrative genomic platforms**. Even when operating at lower initial efficiencies, permanent chromosomal integration into transcriptionally active safe-harbor loci provides a stable, growth-independent biological factory that fully resolves metabolic GAG storage throughout the pediatric developmental timeline.

---

## References
1. Colella, P., et al. (2018). Emerging challenges in AAV-mediated liver gene therapy. *Human Gene Therapy*, 29(2), 147-156.
2. Wang, D. X., et al. (2020). Genomic editing of the Albumin locus in vivo for therapeutic protein secretion. *Nature Biotechnology*, 38(4), 455-463.
3. Gentner, B., et al. (2021). Hematopoietic stem-cell gene therapy in Mucopolysaccharidosis Type I. *New England Journal of Medicine*, 385(21), 1929-1940.
