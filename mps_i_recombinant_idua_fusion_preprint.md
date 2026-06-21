# Recombinant IDUA-Apolipoprotein E Fusion Protein Transport across Blood-Brain Barrier (BBB): A Multi-Compartment PK/PD ODE Model

**In Honor of Cynthia Sielaff**

## Abstract

Mucopolysaccharidosis Type I (MPS I) is a lysosomal storage disorder caused by deficiency of α-L-iduronidase (IDUA), leading to glycosaminoglycan (GAG) accumulation. Neurological manifestations are a significant burden, yet systemic enzyme replacement therapy (ERT) is ineffective due to the blood-brain barrier (BBB). This preprint details a multi-compartment pharmacokinetic/pharmacodynamic (PK/PD) ordinary differential equation (ODE) model designed to simulate the transport and distribution of a recombinant IDUA-Apolipoprotein E (ApoE) fusion protein across the BBB, leveraging receptor-mediated transcytosis via low-density lipoprotein receptor-related protein 1 (LRP1) receptors. The model tracks systemic infusion, receptor-binding kinetics at the brain capillary endothelium, transcytosis rate, accumulation in brain parenchymal interstitial fluid (ISF), subsequent uptake by neurons and astrocytes, and target lysosomal GAG degradation. Our simulations provide insights into the dynamics of brain enzyme delivery and suggest optimal therapeutic strategies for neuroprotective outcomes in MPS I.

## 1. Introduction

MPS I is characterized by severe neurological symptoms in its most severe form (Hurler syndrome), including cognitive decline and developmental regression, primarily due to lysosomal GAG accumulation within central nervous system (CNS) cells. Current systemic ERT fails to adequately cross the BBB, necessitating novel approaches for CNS enzyme delivery. Fusion proteins designed to target endogenous BBB receptors, such as LRP1, offer a promising strategy. ApoE, a known ligand for LRP1, can be fused with therapeutic enzymes like IDUA to facilitate transport across the BBB. Understanding the complex pharmacokinetics and pharmacodynamics of such fusion proteins within the CNS is critical for effective drug design and dosing.

## 2. Model Formulation

Our model is a system of coupled ODEs describing the concentration or amount of the IDUA-ApoE fusion protein in four key compartments:

### 2.1 Systemic Circulation (Sys_IDUA)
This compartment represents the fusion protein in the plasma after intravenous infusion. It is influenced by the infusion rate, systemic elimination, and binding to LRP1 receptors on the BBB.

$\frac{dC_{Sys}}{dt} = k_{infusion} - k_{elim} \cdot C_{Sys} - k_{on_{LRP1}} \cdot C_{Sys} \cdot (LRP1_{total} - C_{LRP1\_bound}) + k_{off_{LRP1}} \cdot C_{LRP1\_bound}$

Where:
- $C_{Sys}$: Concentration of IDUA-ApoE in systemic circulation.
- $k_{infusion}$: Zero-order systemic infusion rate.
- $k_{elim}$: First-order systemic elimination rate constant.
- $k_{on_{LRP1}}$: Association rate constant for LRP1 binding.
- $k_{off_{LRP1}}$: Dissociation rate constant for LRP1 binding.
- $LRP1_{total}$: Total concentration of LRP1 receptors.
- $C_{LRP1\_bound}$: Concentration of LRP1-bound IDUA-ApoE on the BBB endothelium.

### 2.2 LRP1-Bound on BBB Endothelium (LRP1_bound_IDUA)
This compartment represents the fusion protein transiently bound to LRP1 receptors on the luminal side of brain capillary endothelial cells. This binding is a prerequisite for transcytosis.

$\frac{dC_{LRP1\_bound}}{dt} = k_{on_{LRP1}} \cdot C_{Sys} \cdot (LRP1_{total} - C_{LRP1\_bound}) - k_{off_{LRP1}} \cdot C_{LRP1\_bound} - k_{transcytosis} \cdot C_{LRP1\_bound}$

Where:
- $k_{transcytosis}$: First-order rate constant for transcytosis across the BBB.

### 2.3 Brain Interstitial Fluid (ISF) (Brain_ISF_IDUA)
After transcytosis, the fusion protein is released into the brain ISF. From here, it can be eliminated from the brain or taken up by brain cells.

$\frac{dC_{ISF}}{dt} = k_{transcytosis} \cdot C_{LRP1\_bound} - k_{brain\_elim} \cdot C_{ISF} - k_{uptake\_cells} \cdot C_{ISF}$

Where:
- $C_{ISF}$: Concentration of IDUA-ApoE in brain ISF.
- $k_{brain\_elim}$: First-order elimination rate constant from brain ISF.
- $k_{uptake\_cells}$: First-order rate constant for uptake by neurons/astrocytes.

### 2.4 Neuronal/Astrocytic Lysosomes (Cellular_IDUA_Lysosome)
This final compartment represents the accumulation of the fusion protein within the lysosomes of brain cells (neurons and astrocytes), where it can exert its therapeutic effect by degrading GAGs.

$\frac{dC_{Lysosome}}{dt} = k_{uptake\_cells} \cdot C_{ISF} - k_{degradation\_lysosome} \cdot C_{Lysosome}$

Where:
- $C_{Lysosome}$: Amount/concentration of IDUA-ApoE in cellular lysosomes.
- $k_{degradation\_lysosome}$: First-order rate constant for lysosomal degradation of the fusion protein itself (representing enzyme turnover).

## 3. Simulation and Neuroprotective Therapeutic Outcomes

The ODE system was solved numerically using `scipy.integrate.odeint` in Python. Initial conditions assumed no IDUA-ApoE fusion protein present in any compartment at time zero. Parameters were chosen to represent a plausible physiological scenario, though actual values would be determined experimentally.

Our simulations demonstrate the time-dependent transport of the IDUA-ApoE fusion protein. Key insights include:
- The systemic concentration provides the driving force for BBB binding.
- LRP1 receptor binding and transcytosis are critical rate-limiting steps for brain entry.
- Accumulation in brain ISF is followed by intracellular uptake and lysosomal localization.

These dynamics are crucial for predicting the neuroprotective therapeutic outcomes. Sustained levels of IDUA-ApoE within neuronal and astrocytic lysosomes are expected to reverse or halt GAG accumulation, thereby preventing neuronal damage, reducing neuroinflammation, and improving cognitive function. The model allows for the optimization of dosing regimens (e.g., infusion rate, frequency) to achieve and maintain target lysosomal enzyme levels, ultimately guiding the development of more effective treatments for the neurological manifestations of MPS I.

## 4. Conclusion

This multi-compartment PK/PD ODE model offers a robust framework for understanding and optimizing the delivery of LRP1-targeted IDUA-ApoE fusion proteins to the CNS in MPS I. By simulating the complex interplay of systemic pharmacokinetics, BBB transport, and intracellular distribution, this model serves as a powerful tool for rational drug design and development aimed at achieving significant neuroprotective therapeutic outcomes. Further experimental validation of parameters and model outputs will refine its predictive capabilities.
