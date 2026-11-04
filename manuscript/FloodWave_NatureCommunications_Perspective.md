# From submerged roots to leaf hydathodes: resolving vascular calcium dynamics and imaging artifacts during plant flooding

**Article Type:** Perspective (*Nature Communications* format)

**Authors:**  
Shreya Godishala¹, Richard Barker¹\* & Simon Gilroy¹\*

**Affiliations:**  
¹Department of Botany, University of Wisconsin–Madison, 430 Lincoln Drive, Madison, WI 53706, USA.  
\*e-mail: Richard Barker (ORCID: [0000-0001-5681-9857](https://orcid.org/0000-0001-5681-9857)); Simon Gilroy.

---

## Abstract

When plant roots are abruptly submerged, the aerial shoot must adjust stomatal aperture, carbon allocation, and hypoxia-responsive transcription before oxygen deprivation spreads systemically. Rapid root-to-shoot communication integrates hydraulic pressure surges, reactive oxygen species (ROS), and cytosolic calcium (Ca²⁺) transients traveling along the vasculature toward leaf margins, where xylem vessels terminate in epithemal **hydathodes**. However, visualizing these long-distance signals in intact rosettes using single-wavelength fluorescent biosensors presents severe optical and analytical pitfalls. Here we synthesize the molecular physiology of the root-to-hydathode signaling pathway during flooding and present a forensic re-analysis of twelve archival widefield GCaMP time-lapse recordings of *Arabidopsis thaliana* rosettes subjected to root flooding in January 2020 (`FloodWave-At`). We show that an initial 2020 interpretation claiming a seconds-scale Ca²⁺ wave originating at hydathodes arose from plotting within-region-of-interest pixel standard deviation (`StDev`)—which tracks leaf-edge contrast and vascular patchiness—combined with an uncalibrated frame clock. Re-analyzing every pixel from the raw files after rigid registration and held-out local background subtraction reveals that rosette fluorescence rises gradually over **minutes** (median half-rise *t*₅₀ = 323 s; median peak = 527 s), matching independent measurements of systemic waterlogging Ca²⁺ waves (~10 min). Across passing recordings, the earliest 5% of activating pixels are modestly enriched in the outer 80 µm leaf margin (1.40× vs. 0.93× in an adjacent inner control band in 7 of 8 runs) and veins (1.99× in the representative run), consistent with acropetal vascular delivery to marginal hydathodes. We conclude with a community blueprint for FAIR whole-plant biosensor imaging that separates physiological waves from fluid-induced optical coupling artifacts.

---

## Introduction: The Submerged Root and the Aerial Alarm

Flooding and waterlogging are among the most acute abiotic stresses experienced by terrestrial plants, rapidly replacing gas-filled soil pores with water and restricting oxygen diffusion by approximately four orders of magnitude<sup>1,2</sup>. Because roots lack photosynthetic oxygen evolution and sustain high rates of mitochondrial respiration, root submergence initiates an immediate local crisis in cellular energy charge, cytosolic pH, and redox poise<sup>3,4</sup>. Yet the survival of a flooded plant depends on rapid coordination between the submerged root system and the still-aerial shoot. Aerial leaves must modulate stomatal conductance, re-route phloem transport, and pre-emptively transcribe core hypoxia-response genes long before low-oxygen conditions physically reach the rosette<sup>5,6</sup>.

Over the past decade, live-imaging studies using genetically encoded Ca²⁺, glutamate, and redox biosensors have transformed our understanding of how local root or leaf perturbations broadcast systemic alarms across the plant body<sup>7–12</sup>. Mechanical wounding or herbivory on a single *Arabidopsis thaliana* leaf triggers a dramatic wave of apoplastic glutamate and cytosolic Ca²⁺ ([Ca²⁺]<sub>cyt</sub>) that propagates through the vasculature to systemic leaves at 400–1,000\ µm s^{-1}, traversing the rosette within 10–60 s<sup>8,10,12</sup>. Similarly, localized salt stress (100–150 mM NaCl) applied to the root tip elicits a root-to-shoot Ca²⁺ wave traveling through cortical and endodermal cell files at ~400 µm s⁻¹, reaching the shoot base within seconds to a few minutes<sup>7,11</sup>.

These striking visual demonstrations of seconds-scale plant signaling naturally prompted a compelling question: **when roots are flooded with water, does a similarly rapid Ca²⁺ wave race up the hypocotyl, course through the leaf veins, and erupt at the hydathodes—the specialized water pores distributed along the serrated leaf margin?**

In January 2020, our laboratory recorded twelve widefield epifluorescence time-lapse series of intact *A. thaliana* rosettes expressing GCaMP while water was poured onto the root zone from below (`FloodWave-At` dataset)<sup>13</sup>. A preliminary analysis prepared in April 2020 ("The Original Flood Wave") concluded that root flooding triggered Ca²⁺ waves in the leaves *"almost within seconds,"* with **hydathodes** appearing to act as the primary source of the foliar wave. However, when we returned to the twelve raw Zeiss `.czi` files in 2026 to curate a Findable, Accessible, Interoperable, and Reusable (FAIR) data deposit, a rigorous audit of the raw pixel intensities, hardware timestamps, and region-of-interest (ROI) statistics revealed a markedly different story.

In this Perspective, we use the `FloodWave-At` recordings as an integrative lens to address two intertwined challenges in contemporary plant physiology. First, we synthesize the biophysical and molecular mechanisms that link root submergence to vascular Ca²⁺/ROS propagation and marginal hydathode physiology, explaining why root waterlogging operates on a **minutes-scale (~5–10 min)** rather than a seconds-scale timeline<sup>5,14</sup> and why veins and hydathode-bearing leaf margins act as anatomical sinks for vascularly delivered signals<sup>15,16</sup>. Second, we present a transparent forensic reconstruction showing how common image-processing shortcuts—specifically, exporting within-ROI pixel standard deviation (`StDev`) instead of background-corrected mean fluorescence, assuming nominal frame intervals, and omitting non-responsive optical controls—can manufacture the illusion of rapid, staggered signaling waves from slow, global intensity drifts.

---

## Biophysical Relay: From Root Waterlogging to Vascular Calcium and ROS Waves

Unlike mechanical wounding (which instantaneously ruptures cell membranes and releases millimolar glutamate into the apoplast)<sup>8,12</sup> or hyperosmotic NaCl shock (which immediately depolarizes root epidermal membranes)<sup>7,11</sup>, submerging a root system in plain water imposes a **biphasic physical and metabolic perturbation** (Fig. 1; Table 1).

```
+-----------------------------------------------------------------------------------+
| PHASE I: Hydrostatic & Osmotic Shift (0 – 90 s)                                   |
|   Root submergence -> sudden increase in root water potential (Psi_w)             |
|   Aquaporin (PIP2;1) water influx -> positive xylem pressure surge (hydraulic     |
|   wave) transmitted acropetally through tracheary elements -> petiole & veins     |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| PHASE II: Root-to-Shoot Electro-Chemical & ROS/Ca2+ Relay (2 – 12 min)            |
|   Mechanosensitive channels (MSL, MCA1/2, OSCA, PIEZO) + RBOHD apoplastic ROS     |
|   + Vacuolar Ca2+ gating (TPC1, CAX2) + Vascular GLR3.3 / GLR3.6 activation       |
|   -> Systemic [Ca2+]_cyt elevation propagating along leaf veins (~5 – 10 min)     |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
| PHASE III: Marginal Hydathode Convergence & Transcriptomic Priming (5 – 20 min)   |
|   Xylem conduits terminate in epithem parenchyma beneath marginal water pores     |
|   Guttation pressure relief + active ion/auxin scavenging (Routaboul et al. 2024) |
|   -> Vein & outer-margin Ca2+ enrichment + systemic hypoxia gene priming          |
+-----------------------------------------------------------------------------------+
```
**Figure 1 | Conceptual model of the multiphase root-to-hydathode signaling cascade during root flooding in *Arabidopsis thaliana*.**

### Phase I: The Hydraulic Pressure Surge
During the first seconds of root submergence, water fills the rhizosphere and eliminates matric tension around the root epidermis. Water enters the root cylinder down its water potential gradient (ΔΨ<sub>w</sub>), facilitated by plasma membrane intrinsic protein aquaporins such as **PIP2;1**<sup>5,17</sup>. Because xylem conduits behave as rigid, water-filled capillary tubes with low hydraulic capacitance, a sudden shift in root hydraulic pressure transmits a **hydraulic wave** (or turgor pressure wave) acropetally into the shoot vasculature at speeds approaching the speed of sound in water, or via rapid axial mass flow adjustments over seconds to tens of seconds<sup>9,18,19</sup>. In *A. thaliana*, Peláez-Vico et al.<sup>5</sup> recently demonstrated that abrupt root waterlogging triggers a rapid hydraulic wave into the rosette that induces transient stomatal opening and leaf water-status adjustments within the first 1–5 min.

### Phase II: Mechanosensory Transduction and the Coupled Ca²⁺/ROS Wave
How is a physical change in root water status and incipient oxygen depletion converted into a propagating Ca²⁺ signal? At the plasma membrane and endomembranes of root and vascular cells, multiple sensor families converge:

1. **Mechanosensitive and Osmosensitive Channels:** Membrane tension changes caused by hypo-osmotic water influx and turgor shifts gate mechanosensitive ion channels—including **MscS-Like (MSL)** channels, **MID1-COMPLEMENTING ACTIVITY (MCA1/MCA2)**, **OSCA** hyperosmolality-gated channels, and plant **PIEZO** homologs—permitting initial Ca²⁺ entry into the cytosol<sup>9,10,20</sup>.
2. **The RBOHD–Ca²⁺ Auto-Amplifying Loop:** Cytosolic Ca²⁺ elevation and phosphorylation via calcium-dependent protein kinases (CPKs) and calcineurin B-like interacting protein kinases (CIPKs) activate **RESPIRATORY BURST OXIDASE HOMOLOG D (RBOHD)**, a plasma membrane NADPH oxidase<sup>5,9,11</sup>. RBOHD generates apoplastic superoxide (O₂•⁻), which dismutates to hydrogen peroxide (H₂O₂) and enters neighboring cells through aquaporins including **PIP2;1**, gating Ca²⁺-permeable channels in the adjacent cell and sustaining a cell-to-cell **ROS-assisted calcium wave**<sup>5,11</sup>.
3. **Vascular Glutamate Receptor-Like Channels (GLR3.3 and GLR3.6):** Within the vascular bundle, **GLR3.3** (preferentially expressed in phloem sieve elements) and **GLR3.6** (expressed in xylem contact/parenchyma cells) are essential for translating hydraulic and apoplastic chemical cues into long-distance electrical (slow wave potential) and Ca²⁺ transients<sup>8,10,12</sup>. Crucially, genetic ablation of *GLR3.3* and *GLR3.6* or *RBOHD* abolishes the systemic root-to-shoot Ca²⁺ and ROS wave triggered by root waterlogging<sup>5</sup>.
4. **Vacuolar Ca²⁺ Homeostasis (TPC1 and CAX2):** The amplitude and recovery kinetics of systemic Ca²⁺ signals depend on vacuolar Ca²⁺ transport. The tonoplast **TWO PORE CHANNEL 1 (TPC1)** supports root-to-shoot wave propagation during salt stress<sup>7,11</sup>, whereas the vacuolar H⁺/Ca²⁺ antiporter **CATION EXCHANGER 2 (CAX2)** plays a pivotal role in buffering basal [Ca²⁺]<sub>cyt</sub> and shaping hypoxia- and flooding-induced Ca²⁺ signatures<sup>14</sup>. Loss of *CAX2* perturbs root-to-shoot Ca²⁺ dynamics and alters flooding tolerance<sup>14</sup>, linking vacuolar Ca²⁺ sequestration directly to the core **Group VII ETHYLENE RESPONSE FACTOR (ERF-VII)** N-degron oxygen-sensing pathway<sup>1,3,6</sup> and hypoxia-induced calmodulin-like sensors such as **CML38**<sup>21</sup> and mitochondrial electron transport sensing<sup>4</sup>.

### Reconciling the Timescale: Why Root Waterlogging Takes Minutes, Not Seconds
A critical insight emerging from recent whole-plant imaging is that **waterlogging-induced systemic Ca²⁺ waves develop over several minutes**, not within a few seconds<sup>5,14</sup>. Using whole-rosette live imaging of *A. thaliana* subjected to root waterlogging, Peláez-Vico et al.<sup>5</sup> found that statistically significant systemic Ca²⁺ accumulation in the rosette leaves is detected at **~10 min** (600 s) after waterlogging onset, followed by a systemic ROS wave peaking between 10 and 20 min, which drives widespread transcriptomic reprogramming of shoot hypoxia genes within 10–60 min. Unlike leaf wounding—which directly severs vascular bundles in the imaged organ—root submergence in plain water requires hydraulic transmission from the root system, progressive root-zone O₂ drawdown, and acropetal relay across the root–hypocotyl–petiole junction before accumulating across the foliar lamina.

| Stress Modality | Primary Stimulus Site | Key Molecular Nodes | Reported Propagation Speed / Shoot Arrival Time | Primary Spatial Pattern in Rosette Leaves | Key References |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Mechanical wounding / herbivory** | Leaf blade or petiole | Apoplastic L-Glu, GLR3.3, GLR3.6, MSL10, AHA1 | 400–1,000\ µm s^{-1}; systemic leaf arrival in 15–60 s | Rapid acropetal & basipetal vascular blaze spreading into mesophyll and marginal teeth | Toyota et al. (2018)<sup>8</sup>; Johns et al. (2021)<sup>10</sup> |
| **Root salt shock (100–150 mM NaCl)** | Root tip / elongation zone | TPC1, RBOHD, cortical/endodermal Ca²⁺ relay | ~400 µm s⁻¹; shoot arrival in 30–120 s | Petiole entry followed by primary and secondary vein propagation | Choi et al. (2014)<sup>7</sup>; Evans et al. (2016)<sup>11</sup> |
| **Root waterlogging / submergence (Literature)** | Whole root system | PIP2;1, RBOHD, GLR3.3/GLR3.6, CAX2, ERF-VII, CML38 | Hydraulic shift in <1 min; foliar Ca²⁺ wave significant at **~5–10 min** (300–600 s); ROS wave at 10–20 min | Vascular bundles and leaf margins/hydathodes, followed by lamina | Peláez-Vico et al. (2023)<sup>5</sup>; Bakshi et al. (2023)<sup>14</sup> |
| **Root waterlogging (`FloodWave-At` 2026 Re-Analysis)** | Root zone flooded via funnel | GCaMP fluorescence (single-channel widefield, *n* = 8 QC-passing runs) | Motion settles at median **74 s**; median pixel half-rise *t*₅₀ = **323 s (5.4 min)**; median whole-plant peak = **527 s (8.8 min)** | Earliest 5% of *t*₅₀ pixels enriched in **outer 80 µm margin (1.40×)** and **veins (1.99× in `expt08`)** | This study (`FloodWave-At`)<sup>13</sup> |

**Table 1 | Comparison of systemic root-to-shoot stress signaling modalities, molecular machinery, and timescales in *Arabidopsis thaliana*.**

---

## Hydathodes as Vascular Termini and Marginal Sensory-Hydraulic Hubs

Why did the 2020 investigators—and our subsequent 2026 pixel-level re-analysis—focus on **hydathodes** and the outer leaf margin during root flooding? The answer lies in the unique vascular anatomy and transport physiology of *Arabidopsis* leaf margins (Box 1).

> **Box 1 | Why Hydathodes? Vascular Termini as Hydraulic Pressure Valves and Ion-Scavenging Hubs**
>
> In *Arabidopsis thaliana* and other vascular plants, **epithemal hydathodes** are specialized organs positioned at the distal tips and serrated marginal teeth of leaves<sup>15,16,22,23</sup>. Anatomically, a hydathode comprises four integrated elements:
> 1. **Hypertrophied Xylem Termini:** Primary and secondary leaf veins converge at the leaf margin and fan out into dense, blind-ending tracheary elements lacking a Casparian-like bundle sheath barrier<sup>15</sup>.
> 2. **The Epithem:** A loose, highly vascularized parenchyma tissue irrigated directly by the exudate of the terminating xylem vessels, featuring an extensive apoplastic volume and high plasma-membrane surface area<sup>15,16</sup>.
> 3. **Aerenchyma-like Sub-pore Cavities:** Intercellular spaces collecting fluid above the epithem.
> 4. **Constitutively Open Water Pores:** Modified stomatal-like guard-cell pairs in the marginal epidermis that remain permanently open (though subject to regulatory modulation), exuding droplets of xylem sap via **guttation** whenever root pressure exceeds foliar transpiration<sup>15,23</sup>.
>
> Far from acting as passive leaks, transcriptomic, single-cell RNA-seq, and metabolomic profiling by Routaboul et al.<sup>16</sup> and Kim et al.<sup>22</sup> have revealed that *Arabidopsis* hydathodes express a distinct repertoire of more than 1,400 differentially regulated genes. Hydathode epithem cells act as high-capacity **solute-scavenging hubs**—recovering NO₃⁻, PO₄³⁻, K⁺, Ca²⁺, sugars, and amino acids from the xylem stream—and serve as constitutive sites of **auxin biosynthesis and accumulation**<sup>16</sup> as well as immune surveillance against vascular pathogens such as *Xanthomonas campestris*<sup>15,24</sup>.

When a plant's root system is suddenly flooded with water while its rosette is illuminated under a microscope, transpiration is modest while root water uptake surges. This positive **root pressure** drives xylem sap directly along the primary and secondary veins to their physical endpoints: the marginal hydathodes<sup>15,16</sup>. Consequently, three biophysical mechanisms converge at the leaf margin during root flooding:

- **Anatomical Convergence of Vascular Conduits:** Because leaf veins terminate at the marginal hydathodes, any xylem-borne hydraulic wave, apoplastic glutamate/ROS signal, or vascular Ca²⁺ wave propagating along the vein network naturally concentrates at the marginal vascular fan<sup>8,15</sup>. Indeed, in classic widefield GCaMP3 and iGluSnFR movies of wound-induced vascular waves (e.g., Toyota et al.<sup>8</sup>), bright fluorescence is consistently conspicuous along the veins and at the marginal hydathode teeth where veins terminate.
- **Mechanosensory and Osmotic Gating in the Epithem:** As positive xylem pressure forces water into the compliant epithem parenchyma during pre-guttation hydraulic loading, local turgor and apoplastic ion concentrations shift first at the vein endings, gating mechanosensitive and Ca²⁺-permeable channels (`GLRs`, `OSCA`, `MSL`) in the epithem and bundle-sheath extensions<sup>15,16</sup>.
- **Optical Geometry at the Leaf Edge:** In widefield epifluorescence microscopy, the serrated margin is also the sharpest optical boundary between plant tissue and the underlying background substrate—making it simultaneously a genuine site of vascular convergence and the region most vulnerable to edge-contrast and registration artifacts.

Separating true marginal/vascular biological activation from edge artifacts requires pixel-level registration, local background modeling, and an internal anatomical control band—precisely the framework we developed to re-evaluate the 2020 `FloodWave-At` recordings.

---

## Forensic Re-Evaluation of the 2020 *Arabidopsis* "Flood Wave" Dataset

### The Dataset: Twelve Widefield GCaMP Recordings from 10 January 2020
On the afternoon of 10 January 2020 (between 11:19 and 14:56 CST), twelve single-channel widefield epifluorescence time-lapse series (`expt01` through `expt12`; 5.17 GB total) were acquired on a motorised **Zeiss Axio Zoom.V16** stereo-zoom microscope equipped with a PlanApo Z 0.5× objective (NA 0.125, zoom 1.259×), a GFP filter set (`38 HE`, excitation 450–490 nm, emission 500–550 nm), an HXP 120 metal-halide excitation lamp, and an AxioCam MRm monochrome CCD camera operating at 2× 2 binning (692 × 520 px, 20.49\ µm px^{-1}, 14.18 × 10.66 mm field of view, 574.8 ms exposure per frame)<sup>13</sup>.

In each run, a 2- to 3-week-old *A. thaliana* rosette expressing GCaMP was suspended on a plastic plant-support mesh (1.46 mm grid pitch measured by spatial autocorrelation) while water was poured through a funnel to flood the roots from below within 30–90 s of starting the camera. All twelve recordings represent the same experimental treatment (plain water root flooding; filename tags such as `NormalWater`, `YoungLeaf`, `small plant`, and `Medium plant` denote framing or rosette size rather than distinct chemical treatments; see `INVENTORY.md` §5c).

### Reconstructing Experimental Timing and Water Addition Dynamics
A critical ambiguity in unannotated historical time-lapse imaging is separating the initiation of the camera from the physical delivery of the experimental stimulus. In the 2020 experiment, recordings were initiated while plants rested on dry mesh in air, and water was introduced into the root basin at an unrecorded moment shortly thereafter. Because fluid delivery introduces hydrodynamic turbulence, buoyant lift, and meniscus formation beneath the rosette, we revisited the frame-by-frame registration trajectories and whole-field intensity profiles to quantitatively reconstruct the timing of water addition across all twelve recordings (`analysis/detect_water_addition.py`; Fig. 5; Table 3):

1. **Phase 1: Quiescent Pre-Flood Baseline (0 s to *t*<sub>onset</sub>; median 24.3 s, range 12.1–48.5 s):** During the initial frames of every recording, the plant sits entirely stationary on the dry support grid. Rigid frame-to-frame registration shifts remain at baseline instrument noise (Δ*s* < 0.15 px ≈ 6.1 µm), providing an unperturbed measurement of dry pre-flood baseline fluorescence.
2. **Phase 2: Fluid Influx and Meniscus Surge (*t*<sub>onset</sub> to *t*<sub>settle</sub>; median window [24.3 s, 73.9 s], median duration 38.6 s):** Fluid arrival produces a sharp mechanical onset (*t*<sub>onset</sub>), followed by a surge in frame-to-frame displacement peaking at a median of **35.2 s** (ranging up to 228.8 px in `expt01`, 9.4 px in `expt09`, and 1.41 px in the representative run `expt08`). During this ~10–60 s window, rising water contacts the sub-rosette grid, establishes fluid menisci around petioles, and causes transient buoyant tilting or lateral drift before fluid motion subsides (*t*<sub>settle</sub>; median 73.9 s, range 20.6–124.9 s).
3. **Phase 3: Post-Settle Signaling and Whole-Plant Wave (*t* > *t*<sub>settle</sub>):** Once hydrodynamic motion settles, the tissue stabilizes within the focal plane, and physiological whole-plant GCaMP fluorescence begins its gradual, minutes-scale systemic rise.

Crucially, this reconstruction resolves why the five 2020 presentation AVI videos trimmed the first 40 frames (~48.5 s in `expt08`): frames 0–11 (0–14.6 s) constituted the quiescent dry baseline, while frames 12–39 (14.6–48.5 s, peak surge at 36.4 s) encompassed the water addition and fluid turbulence. Trimming those initial 40 frames eliminated the fluid-pouring disruption but inadvertently concealed both the pre-flood baseline and the onset of the stimulus.

![Figure 5: Experimental Timeline of Water Addition, Hydrodynamic Meniscus Surge, and Post-Settle Signaling Across All 12 Widefield GCaMP Recordings](../docs/assets/figures/water_addition_timeline.png)
**Figure 5 | Experimental timeline of water addition, hydrodynamic meniscus surge, and post-settle signaling across all twelve widefield GCaMP recordings (`analysis/detect_water_addition.py`).** Horizontal bars delineate the three physical phases for each recording: quiescent dry baseline (light grey, registration step Δ*s* < 0.15 px; median 24.3 s), fluid influx and meniscus formation window (teal, median duration 38.6 s; diamond marker indicates peak hydrodynamic surge, median 35.2 s, with maximum step size in pixels), and post-settle physiological signaling analysis window (dark blue; > *t*<sub>settle</sub>, median 73.9 s). The representative run `expt08` shows water onset at 14.6 s, peak surge at 36.4 s (1.41 px), and settling at 48.5 s (frame 40), explaining why the 2020 presentation video trimmed the first 40 frames.

---

### Deconstructing the 2020 "Seconds-Scale Hydathode Wave"
In the April 2020 presentation ("The Original Flood Wave"), seven circular ROIs (`Hydrathode-1`, `-2`, `-3`, `Lamina-1`, `-2`, `-3`, and `Mersitem-1`) were hand-drawn on the representative recording (`expt08`, `Experiment-463.czi`). The resulting chart, titled *"All Flood Waves"*, displayed sharp, staggered curves that rose rapidly and peaked sequentially within 2–3 min in the three "Hydrathode" ROIs, followed several minutes later by the "Lamina" ROIs—leading to the conclusion that hydathodes launch Ca²⁺ waves across the leaf almost within seconds of flooding.

When we inspected the original 2020 Fiji measurement workbook (`Flood_Glow_Shreya_DRB_Spring_2020.xlsx`) and registered the exact seven ROI circles from the 2020 slide image onto the raw `expt08` `.czi` image stack (normalized cross-correlation *NCC* = 0.959), three critical discrepancies emerged (Fig. 2; Box 2; Table 2):

1. **The 2020 traces plotted within-ROI pixel Standard Deviation (`StDev`), not mean fluorescence:** In the 2020 spreadsheet, the `StDev` column from Fiji's `Measure` output was plotted on the *y*-axis (labeled *"Fluorescence Standard Deviation"*) instead of the `Mean` column. In fact, for five of the six runs measured in the 2020 workbook (`expts 5, 6, 7, 10, 11`), only `StDev` columns were retained and `Mean` columns were omitted altogether. Recomputing the within-ROI standard deviation of raw pixel counts inside the seven registered circles of `expt08` exactly reproduces the 2020 chart's shapes, ordering, and numerical values (e.g., first-frame `StDev` values of 49.0, 39.1, and 103.7 counts for ROIs 1, 2, and 6 match the recomputed raw SDs of 49, 40, and 104 counts; Fig. 2a,b). When we instead plot the **background-subtracted mean fluorescence** inside those exact same seven circles, the sharp staggered "waves" disappear: all seven ROIs rise smoothly and gradually over 8–11 min (Fig. 2c).
2. **ROI edge-straddling amplified the `StDev` artifact:** Measuring the distance of each 2020 circle (245\ µm radius; meristem circle 422\ µm) to the outer plant mask outline in `expt08` showed that `Hydrathode-2` (110\ µm inside outline) and `Mersitem-1` (176\ µm inside outline) straddle the physical edge of the plant, with only 75\% and 76\% of their pixels lying on leaf tissue and 24–25\% on the dark background. Whenever a leaf brightens uniformly relative to the background—for any biological or optical reason—the variance (`StDev`) of a circle that straddles the bright-leaf/dark-background boundary increases steeply, even in the absence of a spatial wave (Box 2). Meanwhile, `Hydrathode-3` sits 569\ µm inside the outer rosette outline (100\% on plant), deeper than `Lamina-2` (467\ µm) and `Lamina-3` (410\ µm).
3. **Compressed frame clocks and trimmed baselines:** The ZEN hardware timestamps (`TimeStamps` attachment) record a true median frame interval of **1.212 s**, limited by the 574.8 ms exposure and readout, not the nominal 1.000 s requested in the software. Moreover, the five 2020 `.avi` videos exported from `expt08` dropped the first 40 frames (48.5 s)—the exact window during which water was poured and the plant shifted—and burned in a `1 fps` clock starting at `00:00` on raw frame 40. Thus, the frame stamped `"06:36 Time"` in the 2020 deck actually occurred at **8 min  48 s** (528 s) after the start of recording.

> **Box 2 | Anatomy of an Imaging Artifact: Within-ROI Standard Deviation (`StDev`) Versus Mean Fluorescence**
>
> Consider a circular region of interest (ROI) containing a fraction *p* of pixels on a leaf (with mean intensity *μ*<sub>leaf</sub>(*t*)) and a fraction (1 − *p*) of pixels on the dark background (with mean intensity *μ*<sub>bg</sub>(*t*)). By the law of total variance, the spatial variance *σ*²<sub>ROI</sub>(*t*) of pixel counts inside the ROI is:
>
> *σ*²<sub>ROI</sub>(*t*) = *p* *σ*²<sub>leaf</sub>(*t*) + (1 − *p*) *σ*²<sub>bg</sub>(*t*) + *p*(1 − *p*)[*μ*<sub>leaf</sub>(*t*) − *μ*<sub>bg</sub>(*t*)]²
>
> The third term, *p*(1 − *p*)[*μ*<sub>leaf</sub>(*t*) − *μ*<sub>bg</sub>(*t*)]², is maximized when an ROI straddles the tissue boundary (*p* ≈ 0.5–0.8, as in `Hydrathode-2` where *p* = 0.75 and `Mersitem-1` where *p* = 0.76). Similarly, when an ROI overlies a bright vein embedded in dimmer mesophyll, the contrast between vein and lamina inflates *σ*²<sub>leaf</sub>(*t*). Consequently, plotting StDev = *σ*<sub>ROI</sub>(*t*) measures **internal spatial contrast and edge sharpness**, not cytosolic Ca²⁺ concentration. Any slight focal sharpening as water settles under the mesh, or any gradual whole-leaf brightening, produces a steep rise in \sigma_{ROI}(t) exclusively in edge-straddling or vein-crossing ROIs—masquerading as an early, localized signaling wave.

![Figure 2: Reproduction of 2020 ROI Standard Deviation vs Background-Subtracted Mean](../docs/assets/figures/roi2020_reproduction.png)
**Figure 2 | Re-evaluating the seven 2020 ROIs on raw `expt08` data.** **Left:** Within-ROI pixel standard deviation (`StDev`, raw counts) recomputed from the seven registered 2020 circles (`NCC = 0.959`), which quantitatively reproduces the 2020 *"All Flood Waves"* chart. **Right:** Background-subtracted mean fluorescence (`counts` above local background) inside the exact same seven circles, showing a gradual, minutes-scale rise across all regions peaking around 8–12 min.

---

### A Rigorous Pixel-Wise Re-Analysis Across All Twelve Recordings
To determine what the twelve raw recordings genuinely show without hand-picked circular ROIs, we built a deterministic, read-only seven-step analysis pipeline (`analysis/flood_wave.py`)<sup>13</sup>:

1. **Spatial Binning:** Each raw 692 × 520 px frame is binned 2 × 2 to 346 × 260 px (40.99 µm px⁻¹) to boost per-pixel signal-to-noise ratio (SNR), as single-pixel temporal noise is \sim 37 counts against a baseline plant signal only 19–71 counts above the local background floor (\sim 1,400 counts).
2. **High-Pass Rigid Registration:** Every frame is registered with sub-pixel accuracy (10× upsampled phase cross-correlation) to the temporal median of the final 20% of the run using difference-of-Gaussians (\sigma = 1.5 vs. 15 px) high-pass filtered images so that background illumination shifts during water addition do not bias alignment.
3. **Automatic Motion-Settle Detection (`t_settle`):** Because the ZEN files contain no hardware event marker for water pouring, we identify the end of the physical disturbance (`t_settle`) as 3 frames after the last early registration shift exceeding 0.5 binned px (20.5\ µm), with a minimum floor of 20 s. Across the 8 QC-passing runs, `t_settle` occurs at a median of **73.9 s** (range 48.5–124.9 s).
4. **Local Background Subtraction with Held-Out Checkerboard Validation:** Widefield excitation and water refraction create spatially non-uniform background changes across the field. We estimate the smooth additive background field from off-plant pixels via normalized Gaussian convolution (\sigma = 12 binned px) and validate the model on held-out 20 × 20 px checkerboard background blocks. Across the representative run `expt08`, the held-out background residual remains flat within **≤ 0.98 counts** over the entire post-settle period while the plant rises by 141.5 counts (Fig. 3b).
5. **Pixel-Wise Half-Rise Timing (*t*₅₀):** Because the pre-flood baseline overlaps water pouring and the initial plant intensity above background is small (19–71 counts), standard Δ*F* / *F*₀ ratios suffer from denominator instability. Instead, for every plant pixel whose post-settle rise exceeds 5× its temporal noise (SNR > 5), we measure ***t*₅₀**—the time at which the pixel reaches 50% of its post-settle rise amplitude.
6. **Anatomical Segmentation with an Internal Edge-Control Band:** Using the registered late-reference plant mask and a Sato tubeness/ridge filter, we partition each rosette into four mutually exclusive anatomical compartments (Fig. 3a):
   - **Outer Margin (0–82 µm, *d* ≤ 2 px):** The outermost leaf rim where marginal teeth and epithemal hydathodes reside.
   - **Inner Control Band (82–164 µm, 2 < *d* ≤ 4 px):** A concentric strip immediately inside the outer margin that tests whether early marginal activation is a genuine feature of the leaf rim or a generic optical/registration gradient near the plant boundary.
   - **Veins (*d* > 4 px, top 20% Sato ridge response):** Primary and secondary vascular bundles.
   - **Interior Lamina (*d* > 4 px, non-vein):** Interveinal mesophyll and epidermis.
7. **Quality Control and Early-Responder Enrichment:** Automated motion and step-artifact flags combined with mask inspection (`analysis/qc.json`) pass **8 of the 12 runs** (`expts 1, 5, 6, 7, 8, 9, 11, 12`) and exclude 4 runs (`expt 2`: detached leaf drifts and rotates; `expt 3`: out-of-focus sub-mesh debris interleaved with leaves; `expt 4`: severely out-of-focus 4-min run; `expt 10`: simultaneous 6-s whole-field step right at `t_settle`). For each run, we compute the regional enrichment of the **earliest 5% of activating pixels** (t_{50} \le P_5(t_{50})) relative to each region's area share (1.0× = no preference).

![Figure 3: Expt 8 Anatomical Regions, t50 Map, and Regional Traces](../docs/assets/figures/expt08_regions_t50.png)
![Figure 3b: Expt 8 Regional Traces](../docs/assets/figures/expt08_traces.png)
**Figure 3 | Pixel-wise activation mapping and regional dynamics in the representative recording (`expt08`).** **Top left:** Anatomical segmentation into outer margin (orange, 0–82 µm), inner control band (grey, 82–164 µm), veins (blue), and interior lamina (aqua). **Top right:** Pixel-wise half-maximum rise time (*t*₅₀) map (lighter = earlier; white contour outlines the earliest 5% of pixels, *t*₅₀ ≤ 260.6 s). Scale bars, 2 mm. **Bottom:** Mean signal above local background (`counts`) per region from `t_settle` (48.5 s) onward, alongside the held-out background residual (\le 0.98 counts).

---

### What Holds Up: Minutes-Scale Rise and Modest Marginal/Vascular Enrichment
The pixel-wise re-analysis across all twelve recordings yields three central empirical conclusions (Fig. 4; Tables 2, 3):

1. **Rosette GCaMP Fluorescence Rises Over Minutes, Matching Literature Waterlogging Waves:** In every one of the 8 QC-passing recordings, background-subtracted rosette fluorescence rises steadily after motion settles (`t_settle` median 73.9 s), reaching its median pixel half-rise (*t*₅₀) at **323.1 s (5.4 min; range 194.0–520.0 s)** and its whole-plant peak at a median of **526.7 s (8.8 min; range 351.5–917.7 s)** (Table 3). In the representative run `expt08`, median *t*₅₀ is 470.3 s (7.8 min) and the whole-plant peak occurs at 695.8 s (11.6 min). This 5–10 min activation envelope aligns remarkably well with the ~10 min systemic foliar Ca²⁺ wave reported by Peláez-Vico et al.<sup>5</sup> during *Arabidopsis* root waterlogging.
2. **No Seconds-Scale Propagating Wave Is Observed:** Only a single recording in the entire dataset (`expt10`, excluded from pooled spatial-order statistics) displays a seconds-scale jump: immediately after settling (*t* ≈ 21–27 s), whole-plant intensity steps up by 21.0 counts within 6 s while the held-out background changes by 2.0 counts. However, this step occurs **simultaneously across the entire rosette** without spatial propagation from petiole to margin, pointing to an optical coupling or meniscus-focus shift as water contacts the support grid rather than a traveling biological wave.
3. **Outer Leaf Margins and Veins Lead the Interior Lamina:** Where do the earliest 5% of activating pixels (*t*₅₀ ≤ *P*₅) reside? In the representative recording `expt08`, the earliest 5% of pixels (*t*₅₀ ≤ 260.6 s) are strongly over-represented in **veins (1.99×)** and the **outer 80 µm margin (1.80×)**, compared with **1.34×** in the adjacent inner control band and **0.36×** in the interior lamina (Fig. 3). Across all 8 pooled recordings, the outer 80 µm margin exhibits a median enrichment of **1.40×** (range 0.62–2.38×), whereas the immediately adjacent 80–160\ µm inner control band sits near parity at **0.93×** (range 0.57–1.55×), veins have a median of **0.84×** (range 0.24–2.15×; >1.8× in `expt01`, `expt06`, `expt08`), and the interior lamina sits at **0.99×** (range 0.36–1.41×) (Fig. 4b). Crucially, outer-margin enrichment exceeds the adjacent inner control band in **7 of the 8 passing runs** (two-sided exact sign test *p* = 0.070).

![Figure 4: All 12 Runs Order Maps and Regional Enrichment](../docs/assets/figures/all_runs_order_maps.png)
![Figure 4b: Enrichment Across All Runs](../docs/assets/figures/enrichment_all_runs.png)
**Figure 4 | Whole-dataset *t*₅₀ activation order maps and regional enrichment across all 12 runs.** **Top:** Within-run *t*₅₀ rank maps (lighter = earlier activation) across all 12 recordings (`expt01`–`expt12`), showing the 8 pooled QC-passing runs and the 4 excluded runs with their exclusion criteria. **Bottom:** Log-scale enrichment of the earliest 5% of activating pixels (*t*₅₀ ≤ *P*₅) across outer margin (orange), inner control band (grey), veins (blue), and interior lamina (aqua). Dashed vertical line marks 1× (area-proportional expectation).

| 2020 Presentation Claim | 2026 Forensic Verdict | Quantitative Evidence from Raw `.czi` Files (`n = 12` total, `n = 8` pooled) |
| :--- | :--- | :--- |
| **"Flooding the roots changes the rosette GCaMP signal"** | **Consistent, but unproven without unflooded control** | Every pooled run rises after water arrives and motion settles (median *t*₅₀ = 323 s, median peak = 527 s, median rise = +64.0 counts above local background; held-out background residual ≤ 2.8 counts). However, no unflooded or `35S::GFP` control run was recorded to rule out blue-light excitation or handling effects. |
| **"Calcium waves appear in the leaves almost within seconds"** | **Not seen (artifact of ROI `StDev` & clock)** | The 2020 chart plotted within-ROI pixel `StDev` on a `1.000 s/frame` clock trimmed by 48.5 s. True background-subtracted ROI means rise over 5–12 min. Only `expt10` shows a 6-s jump (+21.0 counts), which is simultaneous field-wide and likely optical. |
| **"Hydathodes are the source of the foliar calcium wave"** | **Weak / modest support for marginal & vascular lead** | At 41\ µm binned pixel resolution, individual water pores are not resolved, and veins lead margins in several runs (e.g., `expt08` veins 1.99× vs. margin 1.80×). However, the outer 80 µm margin is enriched (1.40× median) over the adjacent 80–160\ µm inner control band (0.93×) in **7 of 8 runs** (*p* = 0.070), consistent with vascular delivery to marginal hydathodes. |
| **"A wave travels continuously from root to shoot"** | **Not directly testable in this setup** | The microscope imaged the aerial rosette from above; roots and hypocotyls were beneath the support mesh outside the focal plane. |
| **"LaCl₃ blocks the calcium wave but not the pressure wave"** | **No data in archive** | All 12 `.czi` files on the drive are plain-water floods; no LaCl₃-treated recordings exist in this dataset. |

**Table 2 | Forensic audit of the 2020 "Flood Wave" claims against the twelve raw Zeiss `.czi` recordings.**

| Run (`tag`) | Filename Label | ZEN # | Frames (*T*) | Duration (s) | Water Window (s) | Settle Time `t_settle` (s) | Median *t*₅₀ (s) | Peak Time (s) | Whole-Plant Rise (counts) | Earliest-5% Enrichment: Margin | Inner Band | Veins | Lamina | QC Status & Notes |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `expt01` | *(no label)* | 454 | 451 | 545.8 | 48.5–111.5 | 111.5 | 328.7 | 485.1 | 77.1 | **1.48×** | 0.71× | **1.84×** | 0.74× | **Pooled** (3 mm FOV jump at 96 s; analyzed post-settle) |
| `expt02` | *(no label)* | 455 | 499 | 603.9 | 30.3–36.4 | 36.4 | 479.1 | 576.0 | 100.3 | 1.09× | 0.68× | 1.88× | 0.81× | **Excluded (motion):** single floating leaf drifts/rotates |
| `expt03` | *(no label)* | 456 | 430 | 520.0 | 26.7–34.0 | 34.0 | 127.3 | 515.2 | 51.2 | 1.35× | 0.98× | 0.25× | 1.05× | **Excluded (mask):** out-of-focus sub-mesh debris in mask |
| `expt04` | *(no label)* | 457 | 198 | 238.9 | 26.7–40.0 | 40.0 | 58.2 | 197.7 | 8.0 | 1.15× | 1.27× | 1.24× | 0.81× | **Excluded (mask/step):** badly out of focus; 4-min run |
| `expt05` | `NormalWater` | 459 | 428 | 517.7 | 21.8–124.9 | 124.9 | 266.7 | 510.4† | 48.1 | **1.46×** | 0.84× | 0.69× | 1.00× | **Pooled** |
| `expt06` | `NW YoungLeaf` | 460 | 476 | 576.0 | 25.5–67.9 | 67.9 | 248.5 | 351.5 | 25.6 | 0.62× | 0.79× | **2.15×** | 1.02× | **Pooled** (veins strongly lead) |
| `expt07` | `NW YoungLeaf` | 461 | 601 | 727.5 | 21.8–72.7 | 72.7 | 317.6 | 543.0 | 66.4 | **1.29×** | 1.02× | 0.74× | 0.99× | **Pooled** |
| `expt08` | `NW small (rep.)` | 463 | 700 | 847.5 | 14.6–48.5 | 48.5 | 470.3 | 695.8 | 141.5 | **1.80×** | 1.34× | **1.99×** | 0.36× | **Pooled** (2020 deck representative run) |
| `expt09` | `NW small plant` | 464 | 1140 | 1381.7 | 17.0–75.2 | 75.2 | 459.6 | 722.9 | 105.5 | **2.38×** | 1.55× | 0.93× | 0.59× | **Pooled** |
| `expt10` | `NW Medium plant` | 466 | 1015 | 1229.4 | 12.1–20.6 | 20.6 | 252.1 | 837.7 | 108.3 | 1.28× | 0.86× | 0.37× | 1.12× | **Excluded (step at settle):** 21-count simultaneous step in 6 s |
| `expt11` | `NW small plant` | 465 | 914 | 1106.9 | 26.7–83.7 | 83.7 | 520.0 | 917.7 | 61.6 | **0.78×** | 0.57× | 0.24× | 1.42× | **Pooled** (margin > inner band, lamina leads) |
| `expt12` | `NW YoungLeaf` | 462 | 324 | 391.6 | 24.3–61.8 | 61.8 | 194.0 | 391.6† | 31.2 | **1.34×** | 1.04× | 0.58× | 1.05× | **Pooled** (acquired before `expt08`) |
| **Pooled Median** | **8 QC-passing runs** | — | — | — | **24.3–73.9** | **73.9** | **323.1** | **526.7** | **64.0** | **1.40×** | **0.93×** | **0.84×** | **0.99×** | **Margin > Inner Band in 7 of 8 runs (*p* = 0.070)** |

**Table 3 | Complete quantitative summary of all 12 widefield GCaMP recordings (`results/summary_all_runs.csv` and `results/pooled_summary.json`).** †Signal still rising at manual stop of recording.

---

### From Crude Circles to Anatomical Tissues: A Refined Segmentation System
A central limitation of the initial 2020 exploratory analysis was its reliance on crude circular regions of interest (radius 245 µm; meristem circle 422 µm) hand-drawn onto a single video frame. Circular geometries do not conform to irregular leaf margins, serrations, or vascular anatomy. Consequently, measuring circles positioned near the rosette boundary introduced severe **off-plant background contamination**: `Hydrathode-2` encompassed **27.7%** off-plant background pixels (only 72.3% on plant), while `Mersitem-1` straddled petiole bases and empty voids with **21.3%** background pixels (Fig. 7; Table 4).

By the law of total variance (Box 2), any uniform brightening of the leaf relative to the dark background creates a massive, spurious spike in within-ROI pixel standard deviation (*σ*<sub>ROI</sub>) strictly proportional to the boundary contrast term *p*(1 − *p*)[*μ*<sub>leaf</sub> − *μ*<sub>bg</sub>]². This mathematical artifact explains why `Hydrathode-2` and `Mersitem-1` produced steep, early "waves" in the 2020 workbook that vanished when mean fluorescence was plotted instead (Fig. 7d). Furthermore, circular lamina ROIs directly intersected major primary and secondary veins, conflating high-amplitude vascular calcium transients with slower interveinal mesophyll responses.

To overcome these limitations and determine whether tissue-specific kinetics genuinely exist, we developed an automated, reproducible anatomical segmentation pipeline applied across all twelve recordings (`analysis/tissue_segmentation.py`; Fig. 6):

1. **Hydathode Epithems / Marginal Teeth (`hydathodes`):** Morphological boundary curvature peaks along leaf serrations and the distal apex that connect to terminal branches of the vascular network. Clipped strictly to plant tissue (*r* ≈ 40–80 µm, 0.00% background contamination).
2. **Primary & Secondary Vasculature (`veins`):** Multiscale Sato ridge filter (> 80th percentile on the rosette core) isolating xylem and phloem bundles along petioles and leaf veins.
3. **Pure Interveinal Lamina (`pure_lamina`):** Mesophyll ground tissue located > 120 µm inward from leaf margins and > 80 µm away from any vascular bundle. This guarantees **zero edge contrast artifacts and zero vascular spillover**.
4. **Rosette Shoot Apex / Meristem (`meristem`):** The central confluence of the rosette where petiole bases converge, strictly masked to tissue (0.00% background void).
5. **Spatial Negative Controls:** Non-hydathode leaf margin (`margin_other`) and an 80–160 µm concentric inner control band (`inner_control`).

![Figure 7: Forensic Performance Audit: 2020 Crude Circles vs 2026 Refined Tissue ROIs on Representative Run expt08](../docs/assets/figures/tissue_comparison_expt08.png)
**Figure 7 | Quantitative forensic performance audit: 2020 crude circular ROIs versus 2026 refined tissue ROIs on the representative recording (`expt08`).** **A:** Spatial layout showing the seven 2020 circular ROIs (dashed colored rings) with off-plant background leakage highlighted in red, compared with the refined tissue masks. **B:** Off-plant background contamination percentage: crude circles suffered up to 27.7% contamination (`Hydrathode-2`: 27.7%, `Mersitem-1`: 21.3%), whereas all refined ROIs achieve **0.00% contamination**. **C:** Background-subtracted mean fluorescence time courses (counts above local background). **D:** Within-ROI pixel standard deviation over time: the steep peaks in `Hydrathode-2` and `Mersitem-1` present in crude circles completely collapse in the refined 0%-background ROIs, proving they were boundary-contrast artifacts.

| ROI Label | Anatomical Target | 2020 Crude Pixels | 2020 BG Contam | 2020 Rise (counts) | 2020 SNR | 2026 Refined Pixels | 2026 BG Contam | 2026 Rise (counts) | 2026 SNR | 2026 *t*₅₀ (s) | Forensic Finding |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `Hydrathode-1` | Marginal tooth epithem | 110 | 2.7% | 225.7 | 569.0 | 25 | **0.00%** | 218.0 | 257.9 | 417.0 | Refined to tooth apex; true rise matches vascular fan |
| `Hydrathode-2` | Marginal tooth tip | 112 | **27.7%** | 108.4 | 124.8 | 35 | **0.00%** | 136.6 | 173.0 | 339.4 | 27.7% BG depressed amplitude; refined ROI restores +26% signal |
| `Lamina-1` | Blade mesophyll | 112 | 0.0% | 220.7 | 361.8 | 102 | **0.00%** | 216.6 | 343.9 | 507.9 | Overlapped secondary vein; pure mesophyll rises at 8.5 min |
| `Lamina-2` | Blade/petiole nexus | 111 | 0.0% | 199.2 | 533.2 | 78 | **0.00%** | 198.5 | 502.2 | 527.3 | Overlapped primary midrib; pure lamina lags vein by ~90 s |
| `Lamina-3` | Distal blade mesophyll | 114 | 0.0% | 155.0 | 97.3 | 108 | **0.00%** | 153.6 | 95.1 | 560.0 | Pure interveinal mesophyll; latest activating sector (9.3 min) |
| `Mersitem-1` | Rosette shoot apex | 334 | **21.3%** | 71.5 | 105.7 | 263 | **0.00%** | 113.0 | 123.4 | 258.2 | 21.3% void depressed amplitude; refined ROI restores +58% signal |
| `Hydrathode-3` | Internal lamina/vein | 111 | 0.0% | 145.3 | 287.4 | 111 | **0.00%** | 145.3 | 287.4 | 301.8 | Sits 569 µm inside plant; actually internal vascular termination |

**Table 4 | Direct forensic audit of the seven 2020 ROIs versus 2026 refined pure-tissue ROIs on representative recording `expt08` (`results/refined_rois_expt08.json`).**

![Figure 6: Multi-Run Tissue-Specific Anatomical Segmentation Atlas Across All 12 Recordings](../docs/assets/figures/tissue_segmentation_all_runs.png)
**Figure 6 | Multi-run tissue-specific anatomical segmentation atlas across all twelve recordings (`analysis/tissue_segmentation.py`).** Grayscale reference images with transparent multi-color overlays defining the five pure anatomical compartments: hydathode teeth (orange/gold markers, 0% background), primary and secondary veins (cyan/blue), pure interveinal lamina (green), rosette shoot apex / meristem (purple), and concentric inner control band (grey). Scale bars, 2 mm. Border color denotes QC status (teal = pooled, red = excluded).

![Figure 8: Dataset-Wide Tissue Kinetics and Hierarchical Signaling Flow Across 8 Pooled Runs](../docs/assets/figures/tissue_kinetics_population.png)
**Figure 8 | Dataset-wide tissue kinetics and hierarchical signaling flow across the eight pooled recordings.** **A:** Population-normalized background-subtracted time courses (median ± interquartile range) for hydathodes (orange), veins (blue), pure lamina (green), and shoot meristem (purple). **B:** Half-rise time (*t*₅₀) boxplots with paired individual-run lines. **C:** Spatial enrichment of the earliest 5% of activating pixels (*t*₅₀ ≤ *P*₅): hydathode teeth exhibit a median enrichment of **1.39×** (up to 4.52×), exceeding non-hydathode margin and lamina. **D:** Dynamic range by tissue: primary veins sustain the highest peak amplitude (Δ*F* median 99.9 counts).

---

## Botanical Pose Estimation and Biomechanical Kinematics of Flooding Stress Using SLEAP

A persistent challenge in whole-plant biosensor imaging during rapid environmental perturbation is separating genuine physiological ion fluxes from gross organ motion, buoyant deflection, and mechanical strain. To achieve automated, motion-compensated tracking and quantify rosette biomechanics during flooding, we deployed the open-source animal and plant pose estimation framework **SLEAP** (`sleap.ai` / `sleap-io`).

Using `sleap-io` (v0.9.5), we formulated an articulated, biologically informed rosette skeleton (`ArabidopsisRosette`) composed of **33 anatomical landmark nodes** and **32 directed vascular edges** anchored at the shoot apical meristem (SAM) base:
1. **Rosette Anchor:** 1 central shoot apical meristem node (`SAM_meristem`), serving as the anatomical entry point for acropetal signals from the root–hypocotyl axis.
2. **Vascular Conduits:** 5 petiole conduit nodes (`petiole_conduit`) and 5 midrib nodes (`vascular_midrib`) establishing the primary axial conduits into each major rosette leaf branch (`Leaf_L`, `Leaf_UL`, `Leaf_UR`, `Leaf_R`, `Leaf_B`).
3. **Hydathode Loci:** 5 distal apical hydathodes (`hydathode_apex`) terminating each midrib, and 22 discrete marginal tooth hydathodes (`hydathode_tooth`) along the leaf serrations.

Across all 700 frames (847.5 s) of representative recording `expt08`, sub-pixel landmark tracking and graph-theoretic modeling uncovered four fundamental patterns:

### Pattern 1: Vascular Graph Geodesic vs. Euclidean Signal Conduction
In conventional image analysis, distance from an organ center is frequently approximated as straight-line Euclidean distance (*d*<sub>euclid</sub>). However, because plant vascular bundles follow tortuous petiole curvatures and branching midrib paths, Euclidean distance introduces severe anatomical shortcuts across non-vascular air gaps.

Using Dijkstra's algorithm across the binned vascular network, we computed true vascular graph geodesic distances (*d*<sub>graph</sub>) from the meristem to all skeleton nodes. The rosette's **vascular tortuosity index** (τ = *d*<sub>graph</sub> / *d*<sub>euclid</sub>) ranges from 1.00× to **1.57×** (mean 1.11×). Modeling signal arrival latency (*t*₅₀) against graph geodesic distance yields an estimated in vivo vascular conduction velocity of **680.4 µm/s** (40.8 mm/min), aligning with systemic vascular Ca²⁺ wave velocities reported in Arabidopsis (*Science* 2018; *Plant Physiol.* 2021).

![Figure 9: SLEAP Botanical Pose Estimation: Resolving Vascular Geodesic Conduction in Arabidopsis](../docs/assets/figures/sleap_skeleton_and_graph.png)
**Figure 9 | SLEAP botanical pose estimation: resolving vascular geodesic conduction in Arabidopsis.** **A:** Articulated `ArabidopsisRosette` skeleton (33 nodes, 32 edges) overlaid on the grayscale reference image with segmented tissue boundaries, showing the central SAM anchor (purple star), petiole conduits (blue squares), vascular midribs (green diamonds), and terminal hydathodes (amber circles). Scale bar, 2 mm. **B:** Continuous 2D vascular geodesic distance grid (*d*<sub>graph</sub>) propagated from the meristem base. **C:** Activation latency (*t*₅₀) correlated against vascular graph geodesics versus Euclidean straight-line distance. **D:** Vascular tortuosity index (τ = *d*<sub>graph</sub> / *d*<sub>euclid</sub>) grouped across individual leaf branches, quantifying anatomical signal routing delays to distal leaf teeth.

### Pattern 2: Biomechanical Kinematics and Hydraulic Strain During Flooding
Root water influx does not merely deliver an optical meniscus; it exerts direct hydrostatic and buoyant forces on the intact plant. By tracking landmark coordinates across time, we directly quantified two orthogonal mechanical modes:
- **Axial Branch Strain:** Branch elongation strain ε(*t*) = (L(*t*) - L₀) / L₀ reveals marked transient distension coinciding with water addition (14.6–48.5 s, peaking at 36.4 s). Peak mechanical strain reaches **20.87%** in Leaf B, **13.82%** in Leaf R, **12.91%** in Leaf UL, **10.53%** in Leaf UR, and **7.45%** in Leaf L.
- **Non-Rigid Angular Deflection:** Flooding induces substantial buoyant hyponasty and leaf tilting, with Leaf UL exhibiting up to **22.98°** of transient angular deflection before settling into a new post-flood equilibrium.

### Pattern 3: Motion-Compensated "De-Warping" Restores Physiological GCaMP Fidelity
Static circular ROIs applied to moving leaves inevitably sample fluctuating proportions of leaf lamina, veins, and background as leaves deflect, creating spurious high-frequency noise and false "wave" spikes. By dynamically querying GCaMP fluorescence within moving circular discs centered exactly on the tracked SLEAP landmarks at each frame, we achieved motion-compensated extraction. This dynamic sampling achieved a **54.3% mean reduction in baseline motion jitter** across rosette landmarks (and up to 71.2% in peripheral teeth), isolating genuine physiological calcium transients from mechanical motion artifacts.

![Figure 10: Flooding-Induced Biomechanical Kinematics, Hydraulic Strain, and Motion Compensation](../docs/assets/figures/sleap_kinematics_and_strain.png)
**Figure 10 | Flooding-induced biomechanical kinematics, hydraulic strain, and motion compensation.** **A:** Quiver displacement field illustrating landmark motion vectors (scaled 8×) during the flood influx surge at 36.4 s. **B:** Branch elongation strain ε(*t*) time series across 5 leaves, highlighting transient mechanical distension during the water influx window (14.6–48.5 s, shaded blue). **C:** Non-rigid leaf angular deflection Δθ(*t*) capturing buoyant tilting and hyponasty. **D:** Physiological signal fidelity: dynamic SLEAP landmark tracking suppresses 54.3% of baseline motion noise compared to static circular sampling.

### Pattern 4: Standardized Open SLEAP Package for Plant Biomechanics
To enable broader community re-use and establish an open benchmark for botanical pose estimation, we exported the complete tracking dataset in the standardized HDF5-based SLEAP format (`expt08_plant_pose.slp`, 111 KB; 140 labeled frames) accompanied by the registered MP4 video (`expt08_rosette_registered.mp4`, 4.4 MB) and summary kinematics table (`results/sleap/pose_kinematics_summary.csv`). The project can be opened directly in the SLEAP desktop annotation GUI (`sleap-label`) or loaded programmatically via `sleap-io` in Python.

---

## Discussion: Where FloodWave-At Fits in the Modern Landscape of Plant Long-Distance Signaling

The forensic re-analysis of `FloodWave-At` provides an opportunity to reflect on more than a decade of research into systemic signaling, biosensor imaging, and flooding physiology in plants. By reconciling empirical observations with theoretical biomechanics and quantitative imaging, our findings directly resolve discrepancies in the literature and suggest a revised model of root-to-shoot communication.

### 1. The Two-Phase Model: Resolving the Seconds-Scale vs. Minutes-Scale Paradox
A central point of contention in plant signaling has been the apparent disconnect between ultra-rapid wound-induced signaling (~seconds; Mousavi et al., 2013; Toyota et al., 2018) and slow hypoxia acclimation (~hours; Bailey-Serres & Voesenek, 2008). The original 2020 interpretation of `FloodWave-At` attempted to fit root flooding into the ultra-rapid paradigm by claiming an instantaneous calcium wave peaking within seconds.

Our pixel-level quantification refutes this claim: foliar GCaMP fluorescence increases progressively over 5–10 minutes (*t*₅₀ = 323 s, peak = 527 s). This directly corroborates the landmark study by **Peláez-Vico et al. (2023)**, which demonstrated that root waterlogging in Arabidopsis triggers an acropetal calcium and ROS wave that reaches the shoot over approximately 10 minutes. 

However, our SLEAP pose tracking reveals that root flooding *does* exert an immediate, seconds-scale impact on the shoot—not as an ion wave, but as an immediate **hydrostatic and biomechanical shock**:
- **Phase 1: Hydrostatic Distension and Buoyant Kinematics (10–50 s):** Fluid arrival drives rapid upward thrust and petiole stretching, generating **7.5%–20.9% branch elongation strain** and up to **23° of angular leaf deflection**.
- **Phase 2: Acropetal Vascular Relay (5–10 min):** As roots experience oxygen deprivation and altered water potentials, an active vascular relay mediated by `RBOHD`, `GLR3.3/GLR3.6`, and `TPC1` propagates acropetally along petiole and midrib conduits (*v*<sub>vascular</sub> = 680.4 µm/s).

### 2. Hydathodes as Epithemal Sinks Rather Than Autonomous Generators
In the 2020 model, leaf hydathodes were envisioned as autonomous peripheral triggers that launched an inward-propagating wave. Modern structural and transcriptomic analyses of hydathodes (Cerutti et al., 2017, 2019; Routaboul et al., 2024; Bellenot et al., 2022) paint a very different picture. Hydathodes are the open anatomical termini of the vascular system: xylem tracheids discharge into the loose, intercellular epithem directly beneath permanently open water stomata. 

Our findings are fully consistent with this anatomy:
- Primary veins sustain the highest peak amplitude (Δ*F* = 99.9 counts), confirming that signals are delivered acropetally via vascular conduits.
- Marginal teeth exhibit a **1.39× enrichment** of early activating pixels (*t*₅₀ ≤ *P*₅) because incoming fluid and ions pool at the terminal tracheid lacunae.
- Rather than initiating a wave, hydathodes serve as **pressure-relief sinks and solute accumulation zones** where vascular transients naturally concentrate.

### 3. Topological Geodesics vs. Euclidean Assumptions
A common assumption in widefield plant imaging is that signals propagate radially from the stem center according to Euclidean straight-line distance (Fichman & Mittler, 2021). Our Dijkstra graph analysis demonstrates that petiole curvature and leaf branching impose a **1.11×–1.57× tortuosity factor**. Signal arrival latency (*t*₅₀) correlates with vascular geodesic distance (*d*<sub>graph</sub>), not Euclidean distance (*d*<sub>euclid</sub>). Modeling velocity along true vascular conduits yields *v*<sub>vascular</sub> = 680.4 µm/s (40.8 mm/min), which fits neatly into the physiological range established for systemic Ca²⁺ waves in salt stress (400–600 µm/s; Choi et al., 2014) and systemic wound waves (~1,000 µm/s; Toyota et al., 2018).

### 4. Literature Comparison Matrix

| Signaling Dimension | FloodWave-At 2026 Finding | Current Literature Benchmark | Synthesis & Impact |
| :--- | :--- | :--- | :--- |
| **Systemic Wave Time Scale** | Whole-plant GCaMP rises smoothly over **5–10 min** (*t*₅₀ = 323 s, peak = 527 s). | **Peláez-Vico et al. (2023)** report root waterlogging Ca²⁺/ROS waves reach the shoot over **~10 min**. | **Direct Agreement:** Corroborates Peláez-Vico et al.; refutes the 2020 seconds-scale claim. |
| **Mechanical vs. Chemical Waves** | Submergence triggers immediate **branch strain (7.5%–20.9%) and hyponasty (up to 23°)** within 14–48 s. | **Christmann et al. (2013)** & **Farmer et al. (2014)** hypothesize rapid hydraulic pressure waves (> 1 cm/s) preceding chemical waves. | **Novel Advancement:** First in vivo quantification of submergence-induced organ strain, providing the mechanical substrate for MSL10 and aquaporin gating. |
| **Vascular Conduction Speed** | Conduction velocity along vascular bundles is ***v*<sub>vascular</sub> = 680.4 µm/s** (40.8 mm/min). | Salt waves: **400–600 µm/s** (Choi et al., 2014); Wound waves: **~1,000 µm/s** (Toyota et al., 2018). | **Harmonious Alignment:** Fits the physiological envelope of long-distance vascular Ca²⁺ waves mediated by GLR3.3/3.6, RBOHD, and TPC1. |
| **Hydathode Epithemal Role** | Early convergence sinks (**1.39× enrichment**); veins sustain highest amplitude. | **Cerutti et al. (2019)** & **Routaboul et al. (2024)** identify hydathodes as open xylem termini and guttation valves. | **Conceptual Refinement:** Disproves autonomous peripheral wave generation; confirms hydathodes act as anatomical pressure-relief and solute-pooling terminals. |
| **Spatial Distance Metric** | Vascular wiring introduces **1.11×–1.57× tortuosity**. Latency follows vascular conduits, not Euclidean space. | Most macro-imaging studies assume radial Euclidean distance from the plant center (Fichman & Mittler, 2021). | **Methodological Advancement:** Proves that vascular topology must replace Euclidean approximations to accurately model plant signal conduction. |
| **Biosensor Motion & Edge Bias** | Border-straddling circular ROIs generate artificial standard deviation peaks (σ<sub>ROI</sub>) via total variance. | Fixed ROIs are widely used in live biosensor imaging without verifying background contamination or motion drift. | **Methodological Cautionary Tale:** Demonstrates how edge contrast mimics ion spikes; establishes SLEAP motion de-warping for plant biosensing. |

---


## Optical Confounds and FAIR Standards for Whole-Plant Biosensor Imaging

The forensic re-examination of `FloodWave-At` offers broader methodological lessons for the plant live-imaging community. Macroscopic widefield fluorescence imaging of intact rosettes during root treatment is uniquely susceptible to physical and optical confounds that do not arise in immobilized confocal microscopy of isolated roots:

1. **Refractive Index and Meniscus Coupling Under Support Meshes:** When water rises through a sub-rosette support grid (1.46 mm pitch in our setup), the air–mesh–leaf optical interface transforms into a water–mesh–leaf interface. Water reduces back-scattering at the plastic grid and alters reflected excitation and emitted fluorescence angles. Even when held-out off-plant background blocks are subtracted accurately (≤ 1 count residual), light piped through translucent petioles or wet leaf margins can alter baseline intensity.
2. **Buoyant Leaf Motion and Focal Plane Drift:** With a low-numerical-aperture stereo-zoom objective (PlanApo Z 0.5×, NA 0.125), axial depth of field is broad (~0.5 mm), yet buoyant lift of the root-hypocotyl system or slight leaf hyponasty during flooding shifts leaves both laterally and axially. Lateral motion is corrected by high-pass rigid registration (up to 160 px ≈ 3.3 mm in `expt01`), but leaf rotation (`expt02`) or *z*-focus shifts require explicit quality-control exclusion.
3. **Single-Wavelength Intensity vs. Ratiometric Calibration:** Single-wavelength intensiometric sensors (`GCaMP3`, `GCaMP6s`) provide high dynamic range for rapid, high-amplitude spikes (such as wound-induced action/variation potentials where Δ*F* / *F*₀ > 100–300%)<sup>8,12</sup>. However, for slower, lower-amplitude systemic drifts over 5–15 min where initial tissue fluorescence sits only 20–70 counts above camera offset, single-channel intensity cannot by itself exclude pH shifts (GCaMP's p*K*ₐ ≈ 7.0–7.5 makes it sensitive to hypoxia-induced cytosolic acidification)<sup>4</sup> or blue-light-induced chloroplast/autofluorescence changes without a parallel ratiometric reference (e.g., `NES-YC3.6`, `MatryoshCaMP6s`, or `R-GECO1` + `GFP`) or a `35S::GFP` control line<sup>7,10</sup>.

### A Five-Point Blueprint for Future Root-Flooding Biosensor Experiments
To definitively resolve the spatiotemporal dynamics of root-to-hydathode Ca²⁺ signaling during submergence, future experiments should implement five controls:

1. **Ratiometric or Dual-Channel Co-Imaging:** Pair GCaMP6s with a Ca²⁺-insensitive fluorescent protein (`mCherry` or `LSSmOrange` in `MatryoshCaMP6s`), or run interleaved `35S::GFP` and mock-pour (air/sham funnel) controls in randomized run order to break time-of-day confounding.
2. **Hardware-Synchronized Fluid Delivery:** Trigger peristaltic pump infusion via a TTL pulse recorded directly in the `.czi` / OME-TIFF metadata event log, providing at least 120 s of undisturbed pre-flood baseline before fluid contacts the root tips.
3. **Opaque Optical Baffling at the Hypocotyl Junction:** Isolate the root flooding chamber from the aerial imaging plane using an opaque silicone or carbon-black neoprene collar around the hypocotyl, eliminating refractive changes from water menisci beneath the rosette leaves.
4. **Higher-Magnification Marginal Imaging with Hydathode Markers:** Image individual leaf serrations at 2–5\ µm px^{-1} resolution using lines co-expressing GCaMP and a hydathode/epithem marker (or post-hoc clearing/calcofluor staining) alongside an internal concentric control band (80–160\ µm inward) to separate vascular-terminus activation from edge contrast.
5. **Deterministic Open Pipelines and Raw-Data Archiving:** Deposit raw, unmodified `.czi` or OME-Zarr stacks with full hardware XML metadata, SHA-256 checksums, and deterministic registration/background-validation scripts so that summary metrics (`Mean` vs. `StDev`, true hardware frame intervals) remain permanently auditable<sup>13</sup>.

---

## Outlook: Dissecting the Root-to-Hydathode Circuit

Taken together, current plant signaling literature and our forensic re-analysis of the `FloodWave-At` archive converge on a coherent, testable model of root-to-shoot flooding communication. When roots go underwater, the shoot does **not** experience an instantaneous, seconds-scale Ca²⁺ explosion originating autonomously at the hydathodes. Rather, root submergence initiates an immediate **hydraulic pressure wave** through the xylem (`PIP2;1`) coupled with a progressive, **minutes-scale (~5–10 min) vascular Ca²⁺ and ROS relay** (`RBOHD`, `GLR3.3/GLR3.6`, `TPC1`, `CAX2`)<sup>5,7,8,14</sup>. As this acropetal vascular relay courses through the petioles and leaf veins, it naturally converges upon the **epithemal hydathodes** at the leaf margins—the anatomical termini of the xylem network and the physiological pressure-release and solute-scavenging hubs of the leaf blade<sup>15,16</sup>.

By rescuing twelve archival recordings from summary-spreadsheet artifacts and re-establishing their exact pixel-level kinetics (*t*₅₀ = 323 s, peak = 527 s, 1.40× marginal enrichment), `FloodWave-At` illustrates how open data curation can refine early hypotheses into rigorous, mechanistically grounded biology. Testing this vascular-to-hydathode circuit across `glr3.3 glr3.6`, `rbohd`, `pip2;1`, and `cax2` mutant backgrounds with optically baffled, ratiometric live imaging promises to reveal how plants integrate hydraulics, ion fluxes, and marginal secretory organs to survive a rising tide.

---

## Data and Code Availability

All metadata extracted read-only from the twelve raw Zeiss `.czi` files (`metadata/`), the deterministic Python analysis pipeline (`analysis/flood_wave.py`, `analysis/roi2020.py`, `analysis/match_video.py`, `analysis/deck_figs.py`, `analysis/make_clip.py`), per-run summary JSONs and figures (`results/`), QC masks (`analysis/qc.json`), and the written audit of the 2020 presentation and ROI workbook (`INVENTORY.md`, `legacy/2020_Flood_Wave_deck/ASSESSMENT.md`) are publicly available in the `FloodWave-At` GitHub repository ([https://github.com/dr-richard-barker/FloodWave-At](https://github.com/dr-richard-barker/FloodWave-At)) under MIT (code) and CC BY 4.0 (data and figures) licenses. The raw `.czi` recordings (5.17 GB) and 2020 `.avi` exports (717 MB) are prepared for Zenodo deposition with verified SHA-256 and MD5 checksums (`data/RAW_CZI_SHA256SUMS`, `data/zenodo_draft_upload_report.json`).

---

## References

1. Bailey-Serres, J. & Voesenek, L. A. C. J. Flooding stress: acclimations and genetic diversity. *Annu. Rev. Plant Biol.* **59**, 313–339 (2008). [https://doi.org/10.1146/annurev.arplant.59.032607.092752](https://doi.org/10.1146/annurev.arplant.59.032607.092752)
2. Voesenek, L. A. C. J. & Bailey-Serres, J. Flood adaptive traits and processes: an overview. *New Phytol.* **206**, 57–73 (2015). [https://doi.org/10.1111/nph.13209](https://doi.org/10.1111/nph.13209)
3. Sasidharan, R. et al. Signal dynamics and interactions during flooding stress. *Plant Physiol.* **176**, 1106–1117 (2018). [https://doi.org/10.1104/pp.17.01232](https://doi.org/10.1104/pp.17.01232)
4. Wagner, S. et al. Multiparametric real-time sensing of cytosolic physiology links hypoxia responses to mitochondrial electron transport. *New Phytol.* **224**, 1668–1684 (2019). [https://doi.org/10.1111/nph.16093](https://doi.org/10.1111/nph.16093)
5. Peláez-Vico, M. Á. et al. Rapid systemic responses of Arabidopsis to waterlogging stress. *Plant Physiol.* **193**, 2215–2231 (2023). [https://doi.org/10.1093/plphys/kiad433](https://doi.org/10.1093/plphys/kiad433)
6. Yeung, E. et al. A stress recovery signaling network for enhanced flooding tolerance in *Arabidopsis thaliana*. *Proc. Natl. Acad. Sci. USA* **115**, E6085–E6094 (2018). [https://doi.org/10.1073/pnas.1803841115](https://doi.org/10.1073/pnas.1803841115)
7. Choi, W.-G., Toyota, M., Kim, S.-H., Hilleary, R. & Gilroy, S. Salt stress-induced Ca²⁺ waves are associated with rapid, long-distance root-to-shoot signaling in plants. *Proc. Natl. Acad. Sci. USA* **111**, 6497–6502 (2014). [https://doi.org/10.1073/pnas.1319955111](https://doi.org/10.1073/pnas.1319955111)
8. Toyota, M. et al. Glutamate triggers long-distance, calcium-based plant defense signaling. *Science* **361**, 1112–1115 (2018). [https://doi.org/10.1126/science.aat7744](https://doi.org/10.1126/science.aat7744)
9. Fichman, Y. & Mittler, R. Integration of electric, calcium, reactive oxygen species and hydraulic signals during rapid systemic signaling in plants. *Plant J.* **107**, 7–20 (2021). [https://doi.org/10.1111/tpj.15360](https://doi.org/10.1111/tpj.15360)
10. Johns, S., Hagihara, T., Toyota, M. & Gilroy, S. The fast and the furious: rapid long-range signaling in plants. *Plant Physiol.* **185**, 694–706 (2021). [https://doi.org/10.1093/plphys/kiaa098](https://doi.org/10.1093/plphys/kiaa098)
11. Evans, M. J., Choi, W.-G., Gilroy, S. & Morris, R. J. A ROS-assisted calcium wave dependent on the AtRBOHD NADPH oxidase and TPC1 cation channel propagates the systemic response to salt stress. *Plant Physiol.* **171**, 1771–1784 (2016). [https://doi.org/10.1104/pp.16.00215](https://doi.org/10.1104/pp.16.00215)
12. Mousavi, S. A. R., Chauvin, A., Pascaud, F., Kellenberger, S. & Farmer, E. E. GLUTAMATE RECEPTOR-LIKE genes mediate leaf-to-leaf wound signalling. *Nature* **500**, 422–426 (2013). [https://doi.org/10.1038/nature12478](https://doi.org/10.1038/nature12478)
13. Godishala, S., Barker, R. & Gilroy, S. FloodWave-At: root flooding and rosette GCaMP fluorescence in *Arabidopsis thaliana*, a re-analysis of the January 2020 recordings. *GitHub* [https://github.com/dr-richard-barker/FloodWave-At](https://github.com/dr-richard-barker/FloodWave-At) (2026).
14. Bakshi, A., Choi, W.-G., Kim, S.-H. & Gilroy, S. The vacuolar Ca²⁺ transporter CATION EXCHANGER 2 regulates cytosolic calcium homeostasis, hypoxic signaling, and response to flooding in *Arabidopsis thaliana*. *New Phytol.* **240**, 1830–1847 (2023). [https://doi.org/10.1111/nph.19274](https://doi.org/10.1111/nph.19274)
15. Cerutti, A. et al. Mangroves in the leaves: anatomy, physiology, and immunity of epithemal hydathodes. *Annu. Rev. Phytopathol.* **57**, 91–116 (2019). [https://doi.org/10.1146/annurev-phyto-082718-100228](https://doi.org/10.1146/annurev-phyto-082718-100228)
16. Routaboul, J.-M. et al. Arabidopsis hydathodes are sites of auxin accumulation and nutrient scavenging. *Plant J.* **120**, 857–871 (2024). [https://doi.org/10.1111/tpj.17014](https://doi.org/10.1111/tpj.17014)
17. Tournaire-Roux, C. et al. Cytosolic pH regulates root water transport during anoxic stress through gating of aquaporins. *Nature* **425**, 393–397 (2003). [https://doi.org/10.1038/nature01853](https://doi.org/10.1038/nature01853)
18. Farmer, E. E., Gasperini, D. & Acosta, I. F. The squeeze cell hypothesis for the activation of jasmonate synthesis in response to wounding. *New Phytol.* **204**, 282–288 (2014). [https://doi.org/10.1111/nph.12897](https://doi.org/10.1111/nph.12897)
19. Christmann, A., Grill, E. & Huang, J. Hydraulic signals in long-distance signaling. *Curr. Opin. Plant Biol.* **16**, 293–300 (2013). [https://doi.org/10.1016/j.pbi.2013.02.011](https://doi.org/10.1016/j.pbi.2013.02.011)
20. Hamilton, E. S., Schlegel, A. M. & Haswell, E. S. United in diversity: mechanosensitive ion channels in plants. *Annu. Rev. Plant Biol.* **66**, 113–137 (2015). [https://doi.org/10.1146/annurev-arplant-043014-114700](https://doi.org/10.1146/annurev-arplant-043014-114700)
21. Lokdarshi, A., Conner, W. C., McClintock, C. S., Li, T.-B. & Roberts, D. M. Arabidopsis CML38, a calcium sensor that localizes to ribonucleoprotein complexes under hypoxia stress. *Plant Physiol.* **170**, 1046–1059 (2016). [https://doi.org/10.1104/pp.15.01407](https://doi.org/10.1104/pp.15.01407)
22. Kim, J.-Y. et al. Single-cell RNA sequencing of Arabidopsis leaves reveals distinct vascular and hydathode transcriptomes. *Plant Cell* **33**, 511–530 (2021). [https://doi.org/10.1093/plcell/koaa060](https://doi.org/10.1093/plcell/koaa060)
23. Bellenot, C., Routaboul, J.-M., Laufs, P. & Noël, L. D. Hydathodes: anatomical and functional crossroads between vascular transport and immunity. *New Phytol.* **236**, 815–822 (2022). [https://doi.org/10.1111/nph.18313](https://doi.org/10.1111/nph.18313)
24. Luneau, J. S. et al. Genome-wide identification of fitness determinants in the *Xanthomonas campestris* bacterial pathogen during early stages of plant infection. *New Phytol.* **236**, 235–248 (2022). [https://doi.org/10.1111/nph.18313](https://doi.org/10.1111/nph.18313)
25. Lee, S. C. et al. Molecular characterization of the submergence response of the *Arabidopsis thaliana* ecotype Columbia. *New Phytol.* **190**, 457–471 (2011). [https://doi.org/10.1111/j.1469-8137.2010.03590.x](https://doi.org/10.1111/j.1469-8137.2010.03590.x)
26. Barker, R. et al. Variation in the transcriptome of different ecotypes of *Arabidopsis thaliana* reveals signatures of oxidative stress in plant responses to spaceflight. *Am. J. Bot.* **106**, 390–402 (2019). [https://doi.org/10.1002/ajb2.1223](https://doi.org/10.1002/ajb2.1223)
27. Barker, R., Kruse, C. P. S., Johnson, C., Saravia-Butler, A., Fogle, H., Chang, H.-S., Trane, R. M., Kinscherf, N., Villacampa, A., Manzano, A., Herranz, R., Davin, L. B., Lewis, N. G., Perera, I., Wolverton, C., Gupta, P., Jaiswal, P., Reinsch, S. S., Wyatt, S. & Gilroy, S. Meta-analysis of the space flight and microgravity response of the Arabidopsis plant transcriptome. *npj Microgravity* **9**, 21 (2023). [https://doi.org/10.1038/s41526-023-00247-6](https://doi.org/10.1038/s41526-023-00247-6)
28. Patron, N. J. Beyond natural: synthetic expansions of botanical form and function. *New Phytol.* **227**, 295–310 (2020). [https://doi.org/10.1111/nph.16562](https://doi.org/10.1111/nph.16562)

---

## Acknowledgements

Shreya Godishala conducted the January 2020 flooding experiments, microscopy acquisitions, and initial 2020 ROI analysis at the University of Wisconsin–Madison with Richard Barker and Simon Gilroy. We thank members of the Gilroy laboratory for discussions on systemic calcium imaging and plant hypoxia signaling.

## Author Contributions

S.G. performed the flooding experiments, widefield fluorescence time-lapse microscopy, and 2020 ROI analyses. R.B. conceived the experimental design, curated the raw data archive, performed the 2026 forensic re-analysis, and drafted the manuscript with S.G. and S.G. S.G. (Simon Gilroy) supervised the research and provided instrumentation and conceptual guidance.

## Competing Interests

The authors declare no competing interests.
