# Flood_DRB: inventory of 12 Zeiss `.czi` files (10 Jan 2020)

**Source:** `/Volumes/Barker_2016/Hyperspectral_UW-Botany_July 2016/Flood_DRB/`, 12 files, 5.17 GB in total. I read them read-only and wrote nothing to the volume.
**Inspected:** 2026-10-28, using `czifile` 2019.7.2.3, `imagecodecs` 2026.3.6, `numpy` 2.4.6 and `matplotlib` 3.11.2 (the scripts are in `scripts/`).
**Status:** inventory only. Nothing in this folder is an analysis result.

Each statement below is marked as one of:
- **[metadata]**: read directly from the file's embedded ZEN XML or its attachments.
- **[pixels]**: computed from the image data (whole-field statistics only; no ROIs).
- **[observed]**: seen in the preview images in `previews/`.
- **[inference]**: my interpretation. Richard should confirm or correct it.

---

## 1. What the files are

These are **not confocal data**. The working folder was first called `Flood_DRB_confocal`; it was renamed to the `FloodWave-At` repo on 2026-10-28. Every file is a single-channel, widefield epifluorescence time-lapse from a Zeiss motorised stereo-zoom system **[metadata]**. There are no Z-stacks, tiles, scenes or extra channels: the axes are B=1, T=198–1140, C=1, Y=520, X=692 **[metadata]**.

All 12 files share the same acquisition settings **[metadata]**:

| Item | Value (as stored) |
|---|---|
| Software | ZEN 2012 (blue edition) 1.1.2.0. Windows user `zeiss`. Saved as `C:\Users\zeiss\Pictures\temp\Experiment-4NN.czi` and renamed later. |
| Microscope entry | `EMS3/SyCoP3`. Zoom optovar `Wega.Zoom_mot` (motorised). |
| Objective | PlanApo Z 0.5x, NA 0.125, air |
| Zoom | 1.259× (theoretical total magnification at the camera 0.6295×) |
| Camera | AxioCam MRm (model string `AxioCamMRm3`), 1x camera adapter, 6.45 µm pixels, **2×2 binning** → 692 × 520 px |
| Bit depth | 12-bit data in a 16-bit container (Gray16) |
| Pixel size | **20.49 µm** (X = Y) → field of view **14.18 × 10.66 mm** |
| Channel | ZEN dye-database entry `EGFP` (nominal ex 488 / em 509) |
| Filter set | Reflector `38 HE Green Fluorescent Prot`: excitation 450–490 nm, dichroic 495 nm, emission 500–550 nm |
| Illumination | Epifluorescence. The instrument block lists one light source, `CL 9000 LED/CL 6000 LED`, at 60 % intensity. The acquisition track's shutter device is `MTBHXP120Shutter`. The "Before [EGFP]" hardware setting opens the HXP 120 shutter and "After [EGFP]" closes it. So the excitation was most likely the HXP 120, but the two entries conflict and Richard should confirm. |
| Exposure | 574.8 ms per frame, no auto-exposure |
| Storage | Uncompressed (`IsCompressWithJpegXr=false`), so file size scales with frame count |
| Time series | Requested interval 1 s, duration "as long as possible", interactive mode. The actual median interval is **1.212 s** (limited by exposure). |
| End of run | Every file has exactly one event: a `MARKER` reading "Stopped Execution", so every run was **stopped by hand**. |
| Notes and annotations | Description, comments, custom attributes and annotation layers are all **empty** in every file. There are no user event markers, so the files do not record when a treatment was applied. |

The stand is a **Zeiss Axio Zoom.V16**. Richard confirmed this on 2026-10-28 (§5c). It is consistent with the PlanApo Z objective and the SyCoP3 control panel in the metadata, but the file itself never names the stand.

The document timestamps carry a UTC−06:00 offset **[metadata]**. That matches US Central Standard Time in January. Where the microscope was is not recorded.

## 2. Per-file table

The **ZEN #** column is the internal counter from the original save name (`Experiment-NNN.czi`). It gives the **true acquisition order**, which differs from the "expt N" labels. Times are local (UTC−06:00) **[metadata]**. Focus is the raw `MTBFocus` position; the metadata gives no unit.

| Run order | expt # (file label) | Label words in filename | ZEN # | Start | Stop | Frames | Duration (s) | Size (MB) | Focus |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1 | *(none)* | 454 | 11:19:58 | 11:29:05 | 451 | 545.8 | 325.1 | 136768 |
| 2 | 2 | *(none)* | 455 | 11:39:09 | 11:49:14 | 499 | 603.9 | 359.7 | 126334 |
| 3 | 3 | *(none)* | 456 | 11:53:38 | 12:02:20 | 430 | 520.0 | 310.0 | 125830 |
| 4 | 4 | *(none)* | 457 | 12:09:36 | 12:13:37 | 198 | 238.9 | 142.9 | 125830 |
| — | — | **not on drive** | **458** | (gap 12:13–12:24) | | | | | |
| 5 | 5 | NormalWater | 459 | 12:24:26 | 12:33:05 | 428 | 517.7 | 308.5 | 126293 |
| 6 | 6 | NormalWater YoungLeaf | 460 | 12:38:50 | 12:48:28 | 476 | 576.0 | 343.1 | 116549 |
| 7 | 7 | NormalWater YoungLeaf | 461 | 12:54:05 | 13:06:14 | 601 | 727.5 | 433.1 | 122762 |
| 8 | **12** | NormalWater YoungLeaf | 462 | 13:12:55 | 13:19:29 | 324 | 391.6 | 233.6 | 122581 |
| 9 | **8** | NormalWater small plant *representative* | 463 | 13:25:38 | 13:39:48 | 700 | 847.5 | 504.4 | 115140 |
| 10 | **9** | NormalWater small plant | 464 | 13:44:29 | 14:07:32 | 1140 | 1381.7 | 821.5 | 116492 |
| 11 | **11** | NormalWater small plant | 465 | 14:12:35 | 14:31:03 | 914 | 1106.9 | 658.6 | 117910 |
| 12 | **10** | NormalWater Medium plant | 466 | 14:36:16 | 14:56:47 | 1015 | 1229.4 | 731.5 | 117910 |

The same table is in `metadata/file_table.csv`, and the full extracted fields are in `metadata/per_file_metadata.jsonl`. The raw ZEN XML for each file is in `metadata/*.xml`.

Provenance points **[metadata]**:
- **Experiment-458 is missing.** There is an 11-minute gap between expt 4 and expt 5. That run was either not saved under a "Flooding expt" name or was discarded.
- The labels **expt 8–12 do not follow acquisition order.** expt 12 was acquired before expt 8, and expt 11 before expt 10. Files were evidently renamed after acquisition.
- Two pairs share an identical focus value: expts 3 and 4 (125830), and expts 11 and 10 (117910). This only shows the focus was not changed between those runs. It does not show they are the same plant, and 11 and 10 carry different plant-size labels.

## 3. What was imaged

Whole-field pixel statistics **[pixels]** (`metadata/qc_stats.json`):
- In every file the minimum pixel value is about 1,370–1,430 counts. This is a large offset or background floor, and there is no dark or reference frame in the files.
- Plant signal in the previews mostly sits around 1,550–2,200 counts.
- The mean absolute difference between consecutive frames is about 42 counts in every file. If that is pure Gaussian noise, the per-pixel SD is that figure ÷ (2/√π), i.e. 42 ÷ 1.128 ≈ 37 counts per frame. Against a plant signal only a few hundred counts above the floor, a single pixel's SNR is low. ROI or region averaging is needed.
- Six files reach 4,095 (saturation) somewhere: expts 2, 5, 8, 9, 10 and 12. Only expts 2, 10 and 12 have a noticeable saturated area, at most 0.14 % of the field (expt 2). In their previews it falls on bright off-plant objects **[observed]**. In the other three, under 0.001 % of pixels saturate.

From the previews **[observed]** (`previews/exptNN_frames.png`: frames at 0, ¼, ½, ¾ and the end of each run on one shared display range, plus a max-over-time projection):
- The samples are **small rosette plants seen from above**: petiolate, rounded leaf blades roughly 2–7 mm across, filling most of the 14 × 11 mm field. expt 2 is the exception: its field centres on a **single leaf** that drifts and rotates across the frame over the run.
- In most runs a **regular dark grid or mesh** is visible behind the plant. Examples are expts 3, 5–10 and 12. In expt 8, autocorrelation along x of a grid-only patch of the mid-run frame gives a period of 71 px, i.e. **1.46 mm** **[pixels]** (`analysis/grid_acf.py` → `results/qc/grid_pitch_expt08.log` and `.png`). Along y the patch spans only about two cells and the period it reports (106 px) is not reliable. By eye the cells look roughly square and the dark bars a fraction of a millimetre wide **[observed]**.
- The GFP-channel signal is strongest in **veins, leaf margins and the rosette centre or youngest leaves**. Bright **local foci** appear on some leaves during the run (for example expt 1 at about 136 s and expt 5 at about 130 s).
- In several runs the **t = 0 frame is hazier and lower in contrast than later frames**. The grid is faint at t = 0 and sharp later in expts 3, 5, 8, 9, 10 and 12.
- On a fixed display range, **vein signal looks brighter in later frames than at t = 0** in expts 7, 8 and 9, and less clearly in others. Because the t = 0 frames are also optically different (see the previous point), this is **not evidence of a biological response** until it is checked with background-corrected ROIs.
- The max-over-time projections show motion streaks in expts 1, 2 and 5: the plant or leaf moved during the run.

Whole-field QC traces **[pixels]** (`previews/exptNN_qc_traces.png`: whole-field mean, 99th percentile and consecutive-frame difference; these are not results):

| expt | Peak consecutive-frame difference (counts; noise ≈ 42) | at t (s) |
|---|---|---|
| 1 | 52.7 | 96 |
| 2 | 58.0 | 588 (also spikes near 90 and 165) |
| 3 | 43.3 | 98 |
| 4 | 42.2 | — (none above noise) |
| 5 | 45.1 | 69 |
| 6 | 47.5 | 58 |
| 7 | 46.9 | 34 |
| 8 | 43.0 | — (none above noise) |
| 9 | 57.7 | 70 |
| 10 | 46.0 | 42 |
| 11 | 46.4 | 69 |
| 12 | 42.8 | — (none above noise), but whole-field mean steps up at about 40–60 s |

Eight of the 12 runs show a distinct motion spike, seven of them between 34 and 96 s after the run started.

**[inference]** Taken together (manual start, a disturbance about 0.5–1.5 min in, optical change after t = 0, manual stop), it looks as if each run was started first and the sample was **then disturbed, probably by adding water**. The files do not record this. Only Richard can say when, and whether, water was applied.

**[inference]** The emission band is 500–550 nm, which blocks chlorophyll fluorescence. So the signal is either from a GFP-based reporter or from green autofluorescence. Its vein and margin pattern and its brightening in some runs fit a GFP-based biosensor line (for example a calcium or redox reporter) imaged for systemic signalling. **That is a guess. The genotype is not recorded anywhere in the files.**

## 4. Which conditions pair up (from filenames only)

The design below is **[inference]** from the filenames. The metadata has no condition field.

| Group (by filename) | Files | Acquired |
|---|---|---|
| No condition word | expt 1, 2, 3, 4 (n = 4) | 11:19–12:13 |
| "NormalWater" (no size word) | expt 5 | 12:24 |
| "NormalWater YoungLeaf" | expt 6, 7, 12 (n = 3) | 12:38–13:19 |
| "NormalWater small plant" | expt 8 (marked *representative*), 9, 11 (n = 3) | 13:25–14:31 |
| "NormalWater Medium plant" | expt 10 (n = 1) | 14:36 |

There are two readings, and I cannot choose between them from the files:
- **(a)** expts 1–4 are the **flooding treatment** and expts 5–12 are the **"NormalWater" control**, split by plant size or field of view. That gives n = 4 vs n = 8.
- **(b)** expts 1–4 are **pilot or setup runs**, and the condition labels were added once the protocol was settled. In that case all 12 may be one condition.

Under reading (a), **treatment is completely confounded with time of day and run order**: every unlabelled run comes before every NormalWater run. Analysis cannot undo this; it can only state it.

"YoungLeaf" runs use the same zoom as the others **[metadata]**, so "YoungLeaf" describes framing (the field centred on the young leaves or rosette centre), not a magnification change **[observed/inference]**.

No file pairs a before/after or a treated/control on the **same plant** in any way the metadata shows.

## 5. Facts only Richard can supply

1. **Species, ecotype and genotype or reporter line.** What does the GFP channel report: GCaMP, roGFP, HyPer, a promoter::GFP line, or wild-type autofluorescence?
2. **Plant age and growth system.** What is the mesh or grid under the plants: hydroponic mesh, a pot insert, a support grid? How old were the plants, and what were "small", "medium" and "young leaf" plants?
3. **Flooding protocol.** What happened to expts 1–4 versus 5–12? Does "NormalWater" mean the control (plain water, versus a flooding solution such as hypoxic, deoxygenated or temperature-shifted water), or something else? How much water was added, at what temperature, and when relative to the start of each recording?
4. **Missing run Experiment-458** (about 12:13–12:24): was it a failed or test run? Does it exist anywhere else?
5. **expt 8 "representative"**: was it picked as a figure example? Was a figure or talk ever made from this data?
6. **Who acquired it and where.** The instrument, the lab, and whether the HXP 120 or the CL LED source supplied the excitation. Is there a lab-notebook page for 10 Jan 2020?
7. **Other replicates.** Are there other days, or a non-reporter or GFP-only control line imaged the same way?
8. **Sharing.** May the raw `.czi` files be deposited publicly (for example on Zenodo), and are any co-authors or collaborators involved?

### 5a. Clarifications received 2026-10-28 and how they are recorded

Richard pasted a set of clarifications. Apart from the species, they are written as general Gilroy-lab practice ("typically", "commonly", "often"), and several end with "Richard should verify". So I have recorded them as **unconfirmed context**, not as facts about these 12 runs. Each item is checked against the files below.

| Item | What the clarification says | Status here |
|---|---|---|
| Species | *Arabidopsis thaliana* | **Accepted.** Consistent with the previews. |
| Reporter | "Commonly" UBQ10::GCaMP3 in Col-0, or GCaMP6 / NES-YC3.6; cytosolic Ca²⁺. Construct to be verified. | **Unconfirmed.** A single GFP-channel acquisition is consistent with GCaMP. It rules out ratiometric NES-YC3.6 imaging, which would need two emission channels, and none were recorded. The line is still unknown. |
| Growth system | Nylon/nitex or steel mesh, "commonly 100–200 µm" pore, over 0.5–1× MS agar | **Conflicts with the files.** The grid in the images has a measured pitch of 1.46 mm along x (§3), at least seven times coarser. What the grid is remains open. |
| Plant stages | Small = 7–10 dpg with cotyledons and first leaf primordia; medium = 12–14 dpg with 4–6 leaves; young leaf = leaves 3–5 | **Unconfirmed.** Given as typical stages. The "small plant" runs (expts 8, 9, 11) already show four or more expanded, petiolate leaf blades, which is more than cotyledons plus primordia. |
| "NormalWater" | Control flooding with plain water or unsupplemented dilute MS | **Unconfirmed** ("or"). It still doesn't say what expts 1–4 received. |
| Timing | 60–120 s baseline, then liquid added to the root zone | **Unconfirmed but compatible.** The motion spikes fall at 34–96 s (§3), and some are shorter than the stated 60 s. The application time still has to be estimated from each run. |
| Experiment-458 | "Often" a skipped test or alignment run; Richard to check | **Still open.** |
| Microscope | "Typically" Axio Zoom.V16 or SteREO Discovery.V20, with AxioCam or Hamamatsu Orca Flash; filter set 38 HE or 46 HE | **Settled by the metadata.** AxioCam MRm and filter set 38 HE (§1). The stand is an Axio Zoom.V16 (Richard, §5c). |
| Light source | HXP 120 excites; CL LED is transmitted/ambient light | **Accepted.** Matches the HXP 120 shutter opening for the EGFP track (§1). |
| Replicates and GFP-only control | "Typically" run on other days or in parallel | **Unconfirmed.** No such files have been found on this drive. |
| Sharing | Generally CC-BY 4.0 on Zenodo or OSDR "once authorized by the PI"; mentions BRIC-19 follow-ups | **Open.** It needs an explicit yes from the PI. Nothing in the files links these runs to BRIC-19. |

From the review of the analysis plan, I've adopted Cliff's delta or Hedges' g as effect sizes, and an F₀ window of 30–60 pre-flood frames where the pre-flood period is that long. I have **not** adopted the quoted propagation speeds (">1 mm/s" in veins, "<0.1 mm/s" in mesophyll), because they come without a source. Any speed used for comparison will need a citation that has been checked.

### 5b. The 2020 deck and videos (imported 2026-10-28)

Richard pointed to the Google Slides deck "Flood Wave" ("The Original Flood Wave — Shreya Godishala, DRB, & Gilroy Lab et al., 2020") and to the Drive folder `Flooding_DRB_Shreya`, which holds five AVIs. All are now in the repo:
- `legacy/2020_Flood_Wave_deck/` holds `ASSESSMENT.md` and two slide images made from the recordings. The PPTX and PDF exports are kept locally, outside git, because they contain third-party figures.
- `data/derived_2020_videos/` holds the AVIs; see `data/README.md`.

The deck is first-hand evidence for parts of the protocol: GCaMP, 2–3-week-old plants, water through a funnel, roots flooded in 30–60 s, focus on the rosette. It confirms that "NormalWater" runs used water. It does **not** say what expts 1–4 received. Its "2 experimental groups: 2 week old, 3 week old" does not match the filename labels.

The deck **shows expt 8 only**; the 2020 ROI workbook (§5c) also measured expts 5, 6, 7, 10 and 11. `ASSESSMENT.md` documents what the raw data show about its analysis: the traces were within-ROI SD, the time stamps assumed 1 s per frame, and not every "hydathode" ROI sits on a margin.

### 5c. Second set of answers (2026-10-28) and the 2020 ROI workbook

Richard supplied a second set of answers. They are recorded below with how each one stands against the files.

| Topic | Answer | Status here |
|---|---|---|
| Microscope stand | Zeiss Axio Zoom.V16 | **Accepted** (Richard's confirmation; consistent with §1) |
| Expts 1–4 vs "NormalWater" | Same setup: roots flooded with water from below. The "NormalWater" label distinguishes plain-water floods from possible osmotic or chemical controls, none of which are in this set | **Accepted.** All 12 runs are one treatment, a water flood, so there is no treatment contrast in this set |
| Unflooded control | None; the frames before water arrives are the baseline | **Accepted.** Matches §3 and the re-analysis |
| GCaMP line | "Typically" 35S::GCaMP3 or GCaMP6s | **Still unconfirmed** (TODO) |
| Experiment-458 | Not an independent dataset; an aborted or unsaved run | **Accepted as Richard's account.** Consistent with the files: every one of the 12 runs maps to a different ZEN counter value (454–466) and none maps to 458. The answer's mention of "Expts 1–10" is a slip; there are 12 runs |
| Mesh | Standard plastic plant-support mesh suspending the plants | **Recorded.** The measured pitch (1.46 mm, §3) stands; the material is not checked |
| Pour time | Can be read off the data. The answer says the trace "holds steady until an immediate, steep rise", citing `Flood_Glow_Shreya_DRB_Spring_2020` | **Contradicted by that workbook and by the raw data** (below). The re-analysis uses the motion-settle time as its stand-in for water arrival |
| Authorship | Shreya Godishala (UW–Madison at the time; data collection and imaging), Richard Barker, Simon Gilroy | **Accepted** and applied in `CITATION.cff` and README |
| Licences | MIT for code; CC BY 4.0 for data, figures and videos | **Applied** (`LICENSE`, `LICENSE-DATA.md`), with third-party figures in the 2020 deck excluded |
| 2018–19 hyperspectral data | Belongs in a separate AstroBotany hyperspectral repo | **Consistent:** §6 lists it only as related and none of it is used here |

**The 2020 ROI workbook.** `Flood_Glow_Shreya_DRB_Spring_2020` is a Google Sheet in Richard's personal Drive. Its xlsx export was imported on 2026-10-28 to `legacy/2020_roi_workbook/` (checksum alongside). The numbers below come from `analysis/workbook2020_summary.py` → `results/workbook2020_summary.json`.
- **Contents:** 9 tabs. One (`DRB_example_Original_data`) holds expt 8's Fiji ROI measurements: Mean, StDev, Mode, Min and Max for 7 ROIs over 660 frames labelled "Time (1fps)". The tabs for expts 5, 6, 7, 10 and 11 hold StDev columns and **no Mean columns** (Flood5 also has Area, Min and Max). Row counts match each run's frame count: 428, 476, 601, 1015 and 914. The `Flood 6` tab names its source file, `Flooding expt 6 NormalWater YoungLeaf 10012020.czi`.
- **It corrects this repo:** the 2020 work **measured 6 of the 12 runs**, not one; the deck shows only expt 8. Every 2020 trace is a within-ROI SD, and every tab counts time at 1 s per frame. Flood10 ends at "16.92 min", against a true 20.5 min.
- **No sudden rise in expt 8's own Mean columns.** The steepest rise over any 10 frames is 13–23 counts, and the ROI means peak at frames 411–554 (roughly 8–11 min). That matches the slow rise in §3 and `results/`.
- **The SD finding is confirmed directly.** The workbook's first-frame StDev values (for example 49.0, 39.1 and 103.7 for ROIs 1, 2 and 6) match the SDs recomputed from raw data in `results/roi2020_expt08.json` (49, 40, 104).

## 6. Related files elsewhere on the drive (not examined)

A read-only filename search of `/Volumes/Barker_2016` found **other flooding-named data from 2015–2016**, apparently a separate experiment. The full list is in `metadata/drive_flood_related_files.txt`.
- `Organized/2015/2015-03/Flooding_cropped_3fps_Pi03.avi`
- `Organized/2015/2015-05/Cropped_Flooding_Pi1_*.jpg`: 186 files, which is 180 numbered frames plus 6 copies with hash suffixes. The one checked is 2294 × 1178 px.
- `Organized/2015/2015-12/` and `Organized/2016/2016-01/`: `Col-0_flood_*`, `Ler-0_flood_*`, `Cvi-0_flood_*`, `WS_flood_*` and `WS-2_flood_*` crops (the two checked are 304 × 319 and 333 × 321 px), plus `WS-2_Flood_01.avi` and `Grey-scale_WS-2_1_Flood_.avi`

These are RGB or greyscale photographs of named Arabidopsis accessions, not Zeiss fluorescence files. Nothing in the 2020 `.czi` metadata links the two. I have **not** used them to infer the species or protocol of the 2020 data.

Richard's personal Google Drive also holds 2015–2019 hyperspectral water-stress and flooding material, found by another session and listed by title only: the folders "Hyperspec_plant_data" (Dec 2018) and "Hyperspectral - DRB" (May 2018), a deck "Arabidopsis Hyper spectral water stress", and "Report_Hyper spectral imaging_March_2015". According to that session's summary (I have not opened the report), the 2015 report lists the ecotypes Col, WS, Ler and Cvi plus cml24-2 and cml24-4. Those match the accession names in the drive photos above. One item was read, read-only, on 2026-10-28: "HyperSpec Flood Response", which is a Google Sheet, not a Doc. It is a planning sheet with tentative dates from 8 Feb to 23 Mar 2019. It lists 2–3-week-old plants, trays of 18, 32 flooded and 32 control plants, a day-by-day sampling schedule, and stress lasting up to 4 weeks. The sheet was read in place and no copy is kept in this repo. That is a chronic, weeks-long design measured by reflectance. It says nothing about the January 2020 GCaMP runs, the reporter line or the pour time.

## 7. Proposed analysis plan (not started; waiting for answers to §5)

1. **Archive first.** Record SHA-256 checksums for the 12 originals. Convert losslessly to OME-TIFF or OME-Zarr, carrying the ZEN XML across. Plan a Zenodo deposit for the 5.2 GB of raw data; it is too large for git.
2. **Preprocess.** Subtract the offset and background using an off-plant ROI, because no dark frame was recorded. Mask the saturated off-plant objects. Register each frame rigidly to a reference, and track the leaf in expt 2 separately because it drifts and rotates. Flag any frames that registration cannot fix.
3. **Define ROIs.** Build a plant mask from the temporal median. Draw per-leaf ROIs, labelling leaf age, and split each leaf into vein and lamina sub-masks using a vesselness filter, because the signal is vein-enriched. Keep a background ROI and, ideally, a non-responsive reference region in every run.
4. **Measure the signal.** For each ROI compute ΔF/F₀. F₀ is the baseline before water was applied: use Richard's application times, or, failing those, the detected motion event, clearly flagged as a proxy. Extract onset, peak, time-to-peak and area under the curve. If a propagating signal is present, add kymographs along petiole → lamina and estimate wave speed.
5. **Check the confounds.** This is a single-wavelength intensity reporter imaged widefield through a changing water layer, so focus and optical changes alone can raise or lower intensity. Check whether background and grid regions shift with the plant signal. If a GFP-only control line exists, use it.
6. **Compare groups**, only if Richard confirms the design. Use the plant as the unit; with n = 4 vs 8 that means effect sizes with bootstrap CIs and a permutation test. State the run-order and time-of-day confound explicitly.
7. **Package.** Build a FAIR repo whose README draws only on this metadata and on Richard's answers: OME data plus a Zenodo DOI, notebooks and figure scripts. Run `/abai check` before anything is published.
8. ~~Rename the project folder.~~ Done: the folder is now `~/Documents/FloodWave-At`, named after the 2020 deck.

Steps 2–4 have since been run as a first pass (`analysis/flood_wave.py`, results in `results/`). Because the pre-flood baseline is too short for reliable ΔF/F, the analysis uses half-maximum rise times (t50) after motion settles, not ΔF/F₀.

## 8. Files in this folder

- `INVENTORY.md`: this file.
- `metadata/`: the raw ZEN XML for each file, `file_table.csv`, `per_file_metadata.jsonl` and `qc_stats.json`.
- `previews/`: for each run, `exptNN_frames.png` (5 timepoints plus the max over time, 2 mm scale bar) and `exptNN_qc_traces.png`.
- `scripts/`: the read-only extraction and preview scripts used here. They were run with Python 3.11 in a throwaway venv.
- `analysis/`: the first-pass activation analysis, the 2020-ROI reproduction, video-to-raw matching and grid measurement.
- `results/`: per-run maps and summaries, `summary_all_runs.csv`, and the figures used in the new deck.
- `data/`: the data README and the 2020 videos (videos not in git).
- `legacy/2020_Flood_Wave_deck/`: the original deck plus `ASSESSMENT.md`.
