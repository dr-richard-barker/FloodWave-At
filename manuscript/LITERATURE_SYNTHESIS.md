# Literature Synthesis & Scientific Context: Where FloodWave-At Fits in Modern Plant Signaling

**Authors:** Shreya Godishala, Richard Barker & Simon Gilroy  
**Affiliation:** Department of Botany, University of Wisconsin–Madison  
**Repository:** [https://github.com/dr-richard-barker/FloodWave-At](https://github.com/dr-richard-barker/FloodWave-At)  
**Date:** November 2026  

---

## Executive Summary

The `FloodWave-At` project provides a comprehensive, pixel-level re-evaluation of twelve macroscopic widefield GCaMP fluorescence recordings acquired during root submergence in *Arabidopsis thaliana* (January 2020). By coupling automated computer vision, sub-pixel image registration, held-out local background subtraction, tissue-specific anatomical segmentation, and deep-learning pose estimation via SLEAP (`sleap.ai`), we have resolved the physical, optical, and physiological events that unfold when an intact root system is flooded.

Here, we review the full spectrum of empirical findings from `FloodWave-At` and reflect systematically on the plant long-distance signaling and flooding physiology literature. We delineate:
1. **Where our results agree with and corroborate modern literature** (e.g., Peláez-Vico et al., 2023; Bakshi et al., 2023; Wagner et al., 2019; Cerutti et al., 2019; Routaboul et al., 2024).
2. **Where our results challenge, refute, or correct earlier claims and common assumptions** (the 2020 "instantaneous seconds-scale" hypothesis, circular ROI edge-straddling artifacts, and Euclidean straight-line distance approximations).
3. **The novel conceptual and methodological frameworks we contribute to the field** (the Two-Phase Hydrostatic-Vascular Relay Model, the first in vivo quantification of submergence-induced organ strain, and motion-compensated biosensor tracking).

---

## 1. Consolidated Review of Project Results

### A. The 2020 Forensic Audit: Deconstructing the "Within Seconds" Artifact
* **The Root of the Misinterpretation:** The April 2020 slide deck (*Slide 55: "All Flood Waves"*) reported a dramatic calcium wave peaking "within seconds" specifically at leaf hydathodes. Our forensic audit of the raw 2020 ImageJ/Excel workbooks revealed that the plotted curve was **not mean fluorescence**, but the **within-ROI standard deviation (`StDev`)** of pixel intensities.
* **The Law of Total Variance:** In the 2020 analysis, circular ROIs were stamped over leaf serrations, straddling bright leaf tissue and dark background (e.g., **27.7% background** in `Hydathode-2` and **21.3%** in `Meristem-1`). By the law of total variance:
  *σ*²<sub>ROI</sub>(*t*) = *p* *σ*²<sub>leaf</sub>(*t*) + (1 − *p*) *σ*²<sub>bg</sub>(*t*) + *p*(1 − *p*)[*μ*<sub>leaf</sub>(*t*) − *μ*<sub>bg</sub>(*t*)]²
  Because *p*(1 − *p*) is maximized near *p* ≈ 0.5, any uniform rise in leaf tissue intensity (*μ*<sub>leaf</sub>) against a static dark background (*μ*<sub>bg</sub>) generates a steep, quadratic surge in within-ROI standard deviation. When refined to pure anatomical compartments (*p* = 1.0), this artificial standard deviation peak completely collapses.
* **Clock Skew and Missing Frames:** The 2020 AVI videos burned in a 1.000 fps timestamp and dropped the first 40 frames (48.5 s), compressing time by 21.2% (true hardware frame interval = 1.212 s).

### B. Fluid Delivery Telemetry & Influx Detection
* **Unrecorded Delay:** In the 2020 experiment, video acquisition commenced prior to manual water pouring into the root funnel.
* **Automated Telemetry:** Across all 12 recordings, sub-pixel frame-to-frame registration shifts and cross-correlation tracking identified an initial undisturbed baseline of **10–30 s**.
* **Influx Window in Representative Run (`expt08`):** Fluid arrival began at **14.6 s** (frame 12), reached maximum meniscus surge velocity at **36.4 s** (frame 30), and settled into a mechanical steady state at **48.5 s** (frame 40).
* **Quality Control Classification:** 8 runs passed strict mechanical QC (`expt01, 05, 06, 07, 08, 09, 11, 12`), while 4 runs exhibited disqualifying physical perturbations (`expt02` leaf rotation, `expt03` large translation, `expt04` focus drift/no water, `expt10` focal plane drift).

### C. Quantitative Tissue Segmentation & Signaling Hierarchy (Figures 6–8)
* **0.00% Background Contamination:** Automated multi-scale anatomical segmentation isolated five pure botanical compartments: (1) Epithemal Hydathode Teeth, (2) Primary & Secondary Veins, (3) Pure Interveinal Lamina, (4) Shoot Apical Meristem (SAM), and (5) Concentric Inner Control Band (80–160 µm inward).
* **Population Kinetics (8 Pooled Runs):**
  - **Median Activation Latency:** Half-maximum rise time *t*₅₀ = 323 s (~5.4 min; range 194–520 s); whole-plant fluorescence peaks at **527 s (~8.8 min)**.
  - **Early Responder Enrichment (*E*<sub>tissue</sub>):** Discrete hydathode teeth exhibit a **1.39× median enrichment** of the earliest 5% of activating pixels (*t*₅₀ ≤ *P*₅, up to **4.52×** in `expt12`), significantly exceeding adjacent non-tooth leaf margins (1.26×) and pure lamina (0.85×).
  - **Dynamic Range:** Primary and secondary veins sustain the highest peak amplitude (Δ*F* = 99.9 counts median).
  - **Lamina Lag:** Pure interveinal mesophyll activates significantly later than primary conduits (*t*₅₀ = 503–560 s in `expt08`), reflecting progressive radial diffusion from vascular bundles.

### D. SLEAP Botanical Pose Estimation & Biomechanics (Figures 9–10)
* **Articulated Botanical Skeleton:** We formulated an articulated 33-node skeleton (`ArabidopsisRosette`) with 32 hierarchical edges linking the SAM base anchor, 5 petiole conduits, 5 midribs, 5 apices, and 22 discrete marginal teeth.
* **Vascular Graph Geodesics:** Dijkstra shortest-path modeling along the vascular network reveals an anatomical tortuosity index *τ* = *d*<sub>graph</sub> / *d*<sub>euclid</sub> = 1.11×–1.57×. Signal arrival latency correlates strongly with vascular path distance, yielding an in vivo vascular conduction velocity of ***v*<sub>vascular</sub> = 680.4 µm/s (40.8 mm/min)**.
* **Transient Hydraulic Branch Strain:** Sub-pixel landmark tracking uncovered substantial mechanical distension during the water influx window (14.6–48.5 s):
  - Leaf B: **20.87%** peak strain *ε*(*t*) = Δ*L* / *L*₀
  - Leaf R: **13.82%** peak strain
  - Leaf UL: **12.91%** peak strain
  - Leaf UR: **10.53%** peak strain
  - Leaf L: **7.45%** peak strain
* **Non-Rigid Angular Tilting:** Flooding induces rapid buoyant hyponasty, with Leaf UL exhibiting up to **22.98°** of transient angular deflection.
* **Motion-Compensated De-Warping:** Querying GCaMP fluorescence within moving discs dynamically centered on SLEAP landmarks suppresses **54.3% of baseline motion jitter** (up to 71.2% in peripheral teeth), isolating true physiological signals from physical movement.

---

## 2. Literature Synthesis & Reflection Matrix

| Biological Domain | Prior State of the Art / Common Assumptions | FloodWave-At Findings (2026) | Literature Fit & Scientific Synthesis |
| :--- | :--- | :--- | :--- |
| **Systemic Submergence Signaling Dynamics** | **A:** 2020 initial report claimed an instantaneous, seconds-scale wave.<br>**B:** Conflicting reports between rapid wound waves (~seconds) and slow hypoxia acclimation (~hours). | True pixel-level GCaMP rises slowly over **5–10 min** (*t*₅₀ = 323 s, peak = 527 s). | **Confirms Peláez-Vico et al. (2023):** Directly corroborates their observation of a ~10-minute waterlogging systemic Ca²⁺/ROS wave. Completely **refutes** the 2020 seconds-scale claim. |
| **Mechanical Shock vs. Ion Waves** | Debate over whether rapid systemic signaling is primarily hydraulic (> 1–10 cm/s) or chemical/electric (~1 mm/s) (Christmann et al. 2013; Farmer et al. 2014; Fichman & Mittler 2021). | Discovers a **Two-Phase Model**: Phase 1 is an immediate **hydrostatic shock** (7.5%–20.9% branch strain within 14–48 s); Phase 2 is an **acropetal vascular Ca²⁺ relay** (5–10 min). | **Advances the Field:** Uncovers the first direct biomechanical proof of immediate organ strain during root flooding, bridging the gap between hydraulic pressure transmission and downstream ion channels. |
| **Vascular Conduction Mechanics** | Wound-induced Ca²⁺ waves travel at ~1,000 µm/s (Toyota et al. 2018); salt-induced waves travel at 400–600 µm/s (Choi et al. 2014; Evans et al. 2016). | Conduction velocity along rosette vascular bundles is ***v*<sub>vascular</sub> = 680.4 µm/s (40.8 mm/min)**. | **Harmonious Alignment:** Fits squarely into the physiological velocity envelope of long-distance vascular Ca²⁺ waves mediated by GLR3.3/3.6, RBOHD, and TPC1. |
| **Hydathode Epithemal Biology** | Hydathodes are hypothesized to be autonomous sensory "trigger zones" for foliar calcium waves. | Hydathodes are **early convergence sinks (1.39× enrichment)**, while primary veins sustain highest total amplitude. | **Refines Cerutti et al. (2019) & Routaboul et al. (2024):** Hydathodes are the open anatomical termini of the xylem; signals converge and pool at the epithem as a natural consequence of acropetal vascular flow and pressure release. |
| **Spatial Distance Modeling in Leaves** | Widefield studies typically model signal latency as radial Euclidean distance from the plant center (Fichman & Mittler 2021). | Petiole and midrib curvatures impose a **1.11×–1.57× tortuosity factor**. Signal timing correlates with vascular network geodesics, not Euclidean distance. | **Challenges Conventional Practice:** Demonstrates that vascular graph geometry must replace Euclidean approximations to accurately model plant signal conduction. |
| **Biosensor Motion & Boundary Artifacts** | Fixed circular ROIs are widely used to measure fluorescence in moving organs without registration or background subtraction. | Circular ROIs straddling boundaries create false standard deviation peaks through the law of total variance; motion creates up to 71% noise jitter. | **Methodological Breakthrough:** Establishes a five-point FAIR imaging blueprint and introduces SLEAP pose estimation for automated motion de-warping in plant biology. |

---

## 3. In-Depth Reflection: Key Scientific Themes

### Theme 1: The Two-Phase Model — Resolving the Seconds vs. Minutes Dilemma
A long-standing debate in plant stress biology concerns the velocity of systemic communication. In wounding and herbivory, mechanical damage ruptures cells, releasing apoplastic glutamate that gates `GLR3.3` and `GLR3.6` channels to launch an action-potential-like wave propagating through the phloem and xylem parenchyma at approximately 1,000 µm/s (Mousavi et al., 2013; Toyota et al., 2018). In contrast, abiotic stresses like salinity and root waterlogging take substantially longer: salt-induced root-to-shoot waves travel at 400–600 µm/s (Choi et al., 2014), and waterlogging-induced systemic signals peak after ~10 minutes (Peláez-Vico et al., 2023).

The initial 2020 interpretation of `FloodWave-At` claimed that root flooding provoked a seconds-scale response similar to wounding. Our re-analysis reveals that this was a conflation of two fundamentally different phenomena:
1. **Phase 1: The Instantaneous Hydrostatic Shock (10–50 s):** When water enters the root zone, it rapidly alters the root water potential (ΔΨ<sub>w</sub>) and displaces air in the root chamber. This generates an immediate hydrostatic pressure surge transmitted through the continuous water columns of the xylem, accompanied by physical buoyant forces. Our SLEAP tracking captures this directly: leaf branches undergo **7.5% to 20.9% axial elongation strain** and up to **23° of angular deflection** within 30 seconds of water arrival.
2. **Phase 2: The Acropetal Vascular Ca²⁺ Relay (3–10 min):** The subsequent increase in GCaMP fluorescence does not peak in seconds; it rises gradually over several minutes (*t*₅₀ = 323 s, peak = 527 s). This fits the kinetics of an active biochemical relay mediated by reactive oxygen species (ROS) production via `RBOHD`, calcium influx via `GLR3.3/GLR3.6` and `TPC1`, and intracellular mobilization via `CAX2` (Evans et al., 2016; Bakshi et al., 2023).

By disentangling Phase 1 (mechanical strain) from Phase 2 (calcium flux), `FloodWave-At` reconciles the rapid physical response of plants to submergence with the progressive biochemical activation of systemic defense pathways.

---

### Theme 2: Biomechanical Kinematics — Hydrostatic Shock as the Physiological Precursor to Ion Fluxes
How does an underwater root communicate with aerial leaves? In the classical "hydraulic squeeze" hypothesis (Farmer et al., 2014; Christmann et al., 2013), sudden changes in turgor pressure transmit a physical shock wave through the plant vascular system at velocities exceeding meters per second. This rapid pressure change is hypothesized to deform plasma membranes in distal organs, activating mechanosensitive ion channels.

Until now, quantitative in vivo evidence of organ-scale deformation during submergence has been lacking. Our deployment of SLEAP pose tracking provides the first direct empirical demonstration that root flooding induces measurable, organ-scale mechanical strain in the aerial rosette:
- **Axial Branch Elongation:** All five primary leaf lobes undergo rapid elongation during the flood influx surge (peaking at 36.4 s), with the most distended leaf branch (`Leaf_B`) experiencing **+20.87% strain**.
- **Angular Hyponastic Tilting:** Buoyancy and hydrostatic influx force leaves upward and outward, driving up to **22.98° of angular deflection** in young expanding leaves (`Leaf_UL`).

This physical strain provides the exact physiological input required to activate mechanosensitive ion channels such as the **MscS-like (MSL)** family (e.g., `MSL10`; Hamilton et al., 2015) and stretch-activated calcium channels (Haswell lab). Furthermore, rapid cell turgor shifts gate plasma membrane aquaporins (`PIP2;1`; Tournaire-Roux et al., 2003). Thus, biomechanical deformation is not an artifact to be ignored; it is the physical precursor that couples root inundation to downstream calcium signaling.

---

### Theme 3: Epithemal Hydathodes — Open Vascular Sinks, Pressure Relief, and Ion Traps
In the 2020 slide deck, hydathodes were envisioned as autonomous "spark plugs" that initiated a reverse calcium wave propagating inward toward the petiole. Modern anatomical and molecular studies provide a radically different picture (Cerutti et al., 2017, 2019; Routaboul et al., 2024; Bellenot et al., 2022).

Hydathodes are specialized organs located at leaf serrations where xylem tracheids terminate into a loose parenchyma called the **epithem**, situated beneath permanently open **water pores** (modified stomata lacking functional occluding mechanisms). Hydathodes serve two primary roles:
1. **Hydraulic Pressure Relief (Guttation):** When root pressure exceeds transpirational demand (as occurs during root flooding or high humidity), water and solutes are forced out of the xylem termini through the water pores as guttation droplets.
2. **Nutrient and Solute Retrieval:** Epithem cells express high densities of ion transporters, peptide scavengers, and aquaporins to reclaim valuable solutes from the xylem sap before it is lost in guttation fluid (Routaboul et al., 2024).

Our quantitative tissue kinetics corroborate this anatomical reality:
- Primary and secondary veins exhibit the highest dynamic range (Δ*F* = 99.9 counts), confirming that signals course acropetally along the vascular bundles.
- Hydathode teeth exhibit a **1.39× enrichment** of the earliest activating pixels (*t*₅₀ ≤ *P*₅). Because xylem tracheids terminate in open lacunae at the epithem, acropetally transported fluid and ions naturally pool at the leaf margin.
- Rather than being autonomous wave generators, hydathodes are **anatomical pressure-relief sinks** where incoming vascular waves accumulate, concentrate, and discharge hydrostatic tension.

---

### Theme 4: Vascular Topology — Why Geodesic Routing Governs Long-Distance Propagation
A pervasive limitation in plant macro-imaging literature is the reliance on Euclidean 2D distance to model signal velocity (e.g., measuring radial distance from the rosette center). Because leaves are planar organs connected to a 3D stem through curved, flexible petioles, Euclidean straight lines routinely take impossible shortcuts across air gaps between neighboring leaves.

By applying Dijkstra's algorithm to the segmented vascular skeleton, we established that:
- Rosette vascular tortuosity (*τ* = *d*<sub>graph</sub> / *d*<sub>euclid</sub>) ranges from **1.00× to 1.57×** (mean **1.11×**).
- Conduction latency (*t*₅₀) correlates with vascular geodesic distance, not Euclidean proximity.
- Modeling velocity through vascular geodesics yields ***v*<sub>vascular</sub> = 680.4 µm/s**, establishing that calcium signals are strictly constrained to the continuous vascular architecture of the petiole and midrib before symplastically diffusing into the lamina.

---

### Theme 5: Methodological Guidelines for Biosensors — Avoiding the "StDev" Trap
The forensic history of `FloodWave-At` provides a cautionary tale for the biosensing and plant imaging communities. Why did skilled researchers conclude in 2020 that a seconds-scale hydathode wave existed?

1. **The Trap of Fixed Circular ROIs on Moving Organs:** When an intact plant is flooded, leaves move. A circular ROI stamped over a leaf margin will inevitably capture varying proportions of tissue and background.
2. **The Law of Total Variance:** Plotting the standard deviation of pixel intensities within a border-straddling ROI creates an artificial peak that mimics an action potential. As tissue brightens, contrast against the dark background surges, producing a peak in *σ*<sub>ROI</sub> even when mean tissue fluorescence rises monotonically.
3. **The Necessity of Motion De-Warping:** We demonstrate that deep-learning pose estimation via SLEAP can track moving anatomical landmarks with sub-pixel precision across hundreds of frames, reducing baseline motion jitter by **54.3%**.

---

## 4. Testable Genetic Predictions for Future Experiments

Based on our synthesis of the literature and empirical findings, we propose specific genetic tests to dissect the root-to-hydathode circuit during submergence:

1. **`pip2;1` Aquaporin Mutants:**
   - *Prediction:* If Phase 1 branch strain and Phase 2 vascular Ca²⁺ relay depend on root hydraulic conductivity and xylem pressure transmission, `pip2;1` knockout lines should exhibit attenuated mechanical strain (*ε* < 5%) and delayed foliar Ca²⁺ arrival (*t*₅₀ > 500 s).
2. **`glr3.3 glr3.6` Double Mutants:**
   - *Prediction:* Phase 1 mechanical strain will remain intact (hydrostatic shock occurs regardless of channel activity), but the Phase 2 vascular Ca²⁺ wave will be severely blunted or abolished along the petioles and midribs.
3. **`rbohd` NADPH Oxidase Mutants:**
   - *Prediction:* Apoplastic ROS generation is required for systemic wave propagation. In `rbohd`, local root activation will occur, but acropetal propagation to leaf hydathodes will fail to sustain velocity (*v* ≪ 600 µm/s).
4. **`msl10` Mechanosensitive Channel Mutants:**
   - *Prediction:* If the rapid hydraulic strain detected in Phase 2 gates stretch-activated channels, `msl10` mutants will show normal mechanical distension but impaired immediate electrical/calcium triggering in leaf margins.
5. **`cax2` Cation Exchanger Mutants:**
   - *Prediction:* CAX2 regulates vacuolar Ca²⁺ sequestration and hypoxic tolerance (Bakshi et al., 2023). `cax2` plants should exhibit altered baseline GCaMP resting levels and aberrant decay kinetics following flood settlement.

---

## References

1. **Bailey-Serres, J. & Voesenek, L. A. C. J.** Flooding stress: acclimations and genetic diversity. *Annu. Rev. Plant Biol.* **59**, 313–339 (2008). [doi:10.1146/annurev.arplant.59.032607.092752](https://doi.org/10.1146/annurev.arplant.59.032607.092752)
2. **Bakshi, A., Choi, W.-G., Kim, S.-H. & Gilroy, S.** The vacuolar Ca²⁺ transporter CATION EXCHANGER 2 regulates cytosolic calcium homeostasis, hypoxic signaling, and response to flooding in *Arabidopsis thaliana*. *New Phytol.* **240**, 1830–1847 (2023). [doi:10.1111/nph.19274](https://doi.org/10.1111/nph.19274)
3. **Barker, R. et al.** Meta-analysis of the space flight and microgravity response of the Arabidopsis plant transcriptome. *npj Microgravity* **9**, 21 (2023). [doi:10.1038/s41526-023-00247-6](https://doi.org/10.1038/s41526-023-00247-6)
4. **Bellenot, C., Routaboul, J.-M., Laufs, P. & Noël, L. D.** Hydathodes: anatomical and functional crossroads between vascular transport and immunity. *New Phytol.* **236**, 815–822 (2022). [doi:10.1111/nph.18313](https://doi.org/10.1111/nph.18313)
5. **Cerutti, A. et al.** Mangroves in the leaves: anatomy, physiology, and immunity of epithemal hydathodes. *Annu. Rev. Phytopathol.* **57**, 91–116 (2019). [doi:10.1146/annurev-phyto-082718-100228](https://doi.org/10.1146/annurev-phyto-082718-100228)
6. **Choi, W.-G., Toyota, M., Kim, S.-H., Hilleary, R. & Gilroy, S.** Salt stress-induced Ca²⁺ waves are associated with rapid, long-distance root-to-shoot signaling in plants. *Proc. Natl. Acad. Sci. USA* **111**, 6497–6502 (2014). [doi:10.1073/pnas.1319955111](https://doi.org/10.1073/pnas.1319955111)
7. **Christmann, A., Grill, E. & Huang, J.** Hydraulic signals in long-distance signaling. *Curr. Opin. Plant Biol.* **16**, 293–300 (2013). [doi:10.1016/j.pbi.2013.02.011](https://doi.org/10.1016/j.pbi.2013.02.011)
8. **Evans, M. J., Choi, W.-G., Gilroy, S. & Morris, R. J.** A ROS-assisted calcium wave dependent on the AtRBOHD NADPH oxidase and TPC1 cation channel propagates the systemic response to salt stress. *Plant Physiol.* **171**, 1771–1784 (2016). [doi:10.1104/pp.16.00215](https://doi.org/10.1104/pp.16.00215)
9. **Farmer, E. E., Gasperini, D. & Acosta, I. F.** The squeeze cell hypothesis for the activation of jasmonate synthesis in response to wounding. *New Phytol.* **204**, 282–288 (2014). [doi:10.1111/nph.12897](https://doi.org/10.1111/nph.12897)
10. **Fichman, Y. & Mittler, R.** Integration of electric, calcium, reactive oxygen species and hydraulic signals during rapid systemic signaling in plants. *Plant J.* **107**, 7–20 (2021). [doi:10.1111/tpj.15360](https://doi.org/10.1111/tpj.15360)
11. **Hamilton, E. S., Schlegel, A. M. & Haswell, E. S.** United in diversity: mechanosensitive ion channels in plants. *Annu. Rev. Plant Biol.* **66**, 113–137 (2015). [doi:10.1146/annurev-arplant-043014-114700](https://doi.org/10.1146/annurev-arplant-043014-114700)
12. **Johns, S., Hagihara, T., Toyota, M. & Gilroy, S.** The fast and the furious: rapid long-range signaling in plants. *Plant Physiol.* **185**, 694–706 (2021). [doi:10.1093/plphys/kiaa098](https://doi.org/10.1093/plphys/kiaa098)
13. **Kim, J.-Y. et al.** Single-cell RNA sequencing of Arabidopsis leaves reveals distinct vascular and hydathode transcriptomes. *Plant Cell* **33**, 511–530 (2021). [doi:10.1093/plcell/koaa060](https://doi.org/10.1093/plcell/koaa060)
14. **Lokdarshi, A., Conner, W. C., McClintock, C. S., Li, T.-B. & Roberts, D. M.** Arabidopsis CML38, a calcium sensor that localizes to ribonucleoprotein complexes under hypoxia stress. *Plant Physiol.* **170**, 1046–1059 (2016). [doi:10.1104/pp.15.01407](https://doi.org/10.1104/pp.15.01407)
15. **Mousavi, S. A. R., Chauvin, A., Pascaud, F., Kellenberger, S. & Farmer, E. E.** GLUTAMATE RECEPTOR-LIKE genes mediate leaf-to-leaf wound signalling. *Nature* **500**, 422–426 (2013). [doi:10.1038/nature12478](https://doi.org/10.1038/nature12478)
16. **Peláez-Vico, M. Á. et al.** Rapid systemic responses of Arabidopsis to waterlogging stress. *Plant Physiol.* **193**, 2215–2231 (2023). [doi:10.1093/plphys/kiad433](https://doi.org/10.1093/plphys/kiad433)
17. **Pereira, T. D. et al.** SLEAP: A deep learning system for multi-animal pose tracking. *Nat. Methods* **19**, 486–495 (2022). [doi:10.1038/s41592-022-01426-1](https://doi.org/10.1038/s41592-022-01426-1)
18. **Routaboul, J.-M. et al.** Arabidopsis hydathodes are sites of auxin accumulation and nutrient scavenging. *Plant J.* **120**, 857–871 (2024). [doi:10.1111/tpj.17014](https://doi.org/10.1111/tpj.17014)
19. **Sasidharan, R. et al.** Signal dynamics and interactions during flooding stress. *Plant Physiol.* **176**, 1106–1117 (2018). [doi:10.1104/pp.17.01232](https://doi.org/10.1104/pp.17.01232)
20. **Tournaire-Roux, C. et al.** Cytosolic pH regulates root water transport during anoxic stress through gating of aquaporins. *Nature* **425**, 393–397 (2003). [doi:10.1038/nature01853](https://doi.org/10.1038/nature01853)
21. **Toyota, M. et al.** Glutamate triggers long-distance, calcium-based plant defense signaling. *Science* **361**, 1112–1115 (2018). [doi:10.1126/science.aat7744](https://doi.org/10.1126/science.aat7744)
22. **Voesenek, L. A. C. J. & Bailey-Serres, J.** Flood adaptive traits and processes: an overview. *New Phytol.* **206**, 57–73 (2015). [doi:10.1111/nph.13209](https://doi.org/10.1111/nph.13209)
23. **Wagner, S. et al.** Multiparametric real-time sensing of cytosolic physiology links hypoxia responses to mitochondrial electron transport. *New Phytol.* **224**, 1668–1684 (2019). [doi:10.1111/nph.16093](https://doi.org/10.1111/nph.16093)
24. **Yeung, E. et al.** A stress recovery signaling network for enhanced flooding tolerance in *Arabidopsis thaliana*. *Proc. Natl. Acad. Sci. USA* **115**, E6085–E6094 (2018). [doi:10.1073/pnas.1803841115](https://doi.org/10.1073/pnas.1803841115)
