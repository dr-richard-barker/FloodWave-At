# Assessment of the 2020 "Flood Wave" deck

**Source:** Google Slides "Flood Wave" (in Richard Barker's personal Google Drive; created 2020-04-28, last modified 2022-02-17), exported 2026-10-28 as `Flood_Wave_2020.pptx` and `Flood_Wave_2020.pdf` (checksums in `SHA256SUMS`). Title slide: "The Original Flood Wave — Shreya Godishala, DRB, & Gilroy Lab et al., 2020". 78 slides.

**Companion videos:** five Fiji exports in the Drive folder `Flooding_DRB_Shreya` (dated 28–29 Apr 2020), now in `data/derived_2020_videos/`. Every one of them is derived from **expt 8** (`Flooding expt 8 NormalWater small plant representative 10012020.czi`).

Everything below was checked against the raw `.czi` data. The scripts are in `analysis/`.

## 1. What the deck contains

| Slides | Content | Relation to the 2020 flooding data |
|---|---|---|
| 1 | Title | — |
| 2–46 | Background and speculation: plants as computers (cites Patron 2020, *New Phytol.* 227:295–310, doi:10.1111/nph.16562, verified on Crossref); µXRF metal and Ca maps in *N. caerulescens*, pepper and *A. halleri* leaves; iGluSnFR glutamate imaging; trichomes "like the tip of a nerve"; an OMA/Metascape orthology analysis of 171 touch∩hypoxia loci; syntaxins and PEN1; eFP images; a neuron analogy ("Crazy DRB Model") | None. These are not results from this dataset. |
| 47–51 | Experimental design: funnel and water, 2–3-week-old plants, focus on rosette leaves, roots flooded in 30–60 s; hypotheses (a Ca²⁺ wave from roots to shoot, then along the petiole and across leaves) | Describes this dataset |
| 52–59 | Results, all from expt 8: representative frames ("06:36 Time", "06:40 Time"), 7 hand-drawn ROIs, "All Flood Waves" chart, "Timing of hydrathode/lamina response" | Tested below |
| 60–61 | Discussion: "2 experimental groups: 2 week old, 3 week old"; "Hydathodes appear to be the source of Calcium waves in the leaves almost within seconds of flooding the roots" | Tested below |
| 62–63 | Root pressure figure; "Calcium waves can be blocked with LaCl. But pressure waves are not?!" | No LaCl₃ data in this dataset |
| 64–66 | "Conclusion" (empty) and two blank slides | — |
| 67–78 | Root-hair development and root-zone anatomy | Unrelated; apparently carried over from another talk |

Only 17 of the 78 slides (47–63) are about the flooding experiment.

## 2. Problems found, each checked against the raw data

1. **The "All Flood Waves" traces are within-ROI standard deviations, not fluorescence.** The y-axis label is "Fluorescence Standard Deviation". Taking the SD of raw counts inside the same seven ROIs (registered from the slide image onto raw expt 8 with NCC 0.959) reproduces the 2020 chart's shapes, ordering and values: "Hydrathode-1" peaks at ~114 by ~3 min on the 2020 axis, "Hydrathode-2" at ~112, "Hydrathode-3" at ~99, lamina ROIs at 66–91 around 7–8 min, and "Mersitem" starts at 104 and reaches 127. SD measures heterogeneity inside a circle. It rises when part of an ROI brightens, or when an ROI straddles the leaf edge and the leaf brightens against the background. It is not a calcium measure. The ROI **means** rise gradually and much more alike (`results/figures/roi2020_reproduction.png`).
2. **The burned-in time stamps assume 1 s per frame.** The camera ran at a median 1.212 s per frame, and each video starts at raw frame 40, 48.5 s after recording began. Video frames 0/60/396/659 are stamped 00:00/01:00/06:36/10:59. So "06:36 Time" is really 8 min 48 s after the start of recording. The chart's own axis (0.02 min per frame ≈ 1.2 s) is close to the true rate, but it starts at the video's start, not the recording's.
3. **"Hydrathode" ROIs are not all at the leaf margin.** Measured to the outer plant outline, the ROI centres sit 222, 110 and 569 µm inside it (Hydrathode-1, -2, -3). The lamina ROIs sit 410–779 µm in. Hydrathode-2 and the meristem ROI straddle the plant edge: only 75–76 % of their pixels are on the plant. Caveat: leaves overlap at the top of the rosette, so an inner leaf margin may lie under another leaf. The legend-to-ROI-number mapping (series order = ROI number) is my reading of the slide.
4. **One plant.** "All Flood Waves" shows the seven ROIs of expt 8 only. The other 11 runs were not analysed in the deck.
5. **Claims without data here.** Nothing on this drive records the "2 experimental groups: 2 week old, 3 week old"; the filenames say small/medium plant and young leaf. The LaCl₃ blocking claim (slide 63) has no matching recordings in this set.
6. **Errors in the background slides.** "SAM: Root Apical Meristem" (slides 9 and 50) should be RAM. Slide 37 headed "PEN1!" describes AT4G15340, the pentacyclic triterpene synthase also named PEN1, while the slides around it are about the syntaxin PEN1/SYP121 (AT3G11820): a gene-symbol collision. Typos include "Hydrathode", "Mersitem", "cooringates", "experimanal" and "Technology show's".
7. **Third-party figures** (µXRF panels, review figures "Adapted from …") carry partial or no citations. A public FAIR version should not reuse them without full references and permission.

## 3. What the re-analysis says about the 2020 conclusions

See `results/` and the new deck ("Flood Wave, revisited"). Eight of the 12 runs pass QC; `analysis/qc.json` and `results/pooled_summary.json` give the reasons for the four exclusions. In brief:
- **"Flooding changes the rosette signal":** consistent, but unproven. Every pooled run rises after the water arrives and motion settles. Median t50 is 323 s from the start of recording (range 194–520 s), and the whole-plant peak is at a median 527 s (352–918 s). No unflooded run exists, so light exposure or handling cannot be ruled out as a driver.
- **"Within seconds":** not seen. Only one run, expt 10, has a seconds-scale jump: the plant rises 21 counts in about 6 s while the held-out background moves 2. The jump is simultaneous across the field and could be optical.
- **"Hydathodes are the source":** weak support. Among the earliest 5 % of pixels to reach half-rise, the outer 80 µm margin is over-represented (median 1.40×, range 0.62–2.38). The control band just inside it is not (0.93×). Margin exceeds inner band in 7 of 8 runs (sign test p = 0.07). Veins lead in some runs; in expt 8 they are 1.99×, against 1.80× for the margin. Hydathodes themselves are not resolved at 41 µm per binned pixel.
- **The setup description** (funnel flooding, rosette focus, 2–3-week-old plants) is the best record of the protocol and is carried into the new deck as the 2020 account.
