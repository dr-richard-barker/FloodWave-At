# FloodWave-At

A re-analysis, from the raw files, of a January 2020 experiment. The roots of *Arabidopsis thaliana* plants expressing GCaMP were flooded with water while the rosette was filmed from above. The question was whether a calcium signal reaches the leaves within seconds.

**Status:** first-pass analysis complete. Richard Barker's answers are recorded in `INVENTORY.md` §5a and §5c. The GCaMP line is still unconfirmed. The raw recordings are not yet deposited.

## What is here

| Path | Contents |
|---|---|
| `INVENTORY.md` | What the 12 raw `.czi` files contain, read from their own metadata; which facts are inferred; open questions |
| `metadata/` | Raw ZEN XML for every run, `file_table.csv` and `per_file_metadata.jsonl` |
| `previews/` | Frame montages and whole-field QC traces for each run (not results) |
| `analysis/` | `flood_wave.py` (per-run activation analysis), `roi2020.py` (2020 ROIs re-measured on raw data), `match_video.py` (2020 videos ↔ raw frames), `grid_acf.py` (mesh pitch), `deck_figs.py` (figures and the summary table), `make_clip.py` (expt 8 video clip), `run_all.sh` (reruns everything) |
| `results/` | Per-run maps, summaries and figures; `summary_all_runs.csv` |
| `data/` | Data README and the five 2020 Fiji videos (videos not in git) |
| `legacy/2020_Flood_Wave_deck/` | `ASSESSMENT.md` of the 2020 "Flood Wave" deck and two of its images made from the recordings. The deck's PDF and PPTX exports are kept locally, not in git, because they contain third-party figures |
| `legacy/2020_roi_workbook/` | The 2020 Fiji ROI measurement workbook (xlsx), summarised by `analysis/workbook2020_summary.py` |
| `scripts/` | Read-only metadata and preview extraction |
| `deck_2026/` | Slide sources of the new deck, "Flood Wave, revisited" |

Large files (raw `.czi`, the 2020 AVIs and the per-run `.npz` maps) and the 2020 deck exports stay out of git and are listed in `.gitignore`. They are for the planned Zenodo deposit.

## The data

The data are 12 single-channel time-lapses recorded on 10 Jan 2020 between 11:19 and 14:56. They were taken on a Zeiss stereo-zoom microscope: PlanApo Z 0.5× objective, AxioCam MRm camera with 2×2 binning, GFP filter set 38 HE, 20.49 µm per pixel, a median of 1.212 s per frame, and 4–23 min per run. The raw files (5.17 GB) are not in git. See `data/README.md`.

## Method (first pass)

`analysis/flood_wave.py` runs on each raw file, read-only, in seven steps:
1. Bin 2×2.
2. Register each frame rigidly to a late reference, using high-pass images so background changes don't drive the alignment.
3. Subtract an additive local background, estimated from off-plant pixels by normalised convolution. The model is checked on held-out background blocks.
4. Define a settle time: 3 frames after the last early registration step larger than 0.5 px, and at least 20 s.
5. For every plant pixel, measure the time its signal reaches half of its post-settle rise (t50).
6. Split the plant into an outer 80 µm margin, a control band 80–160 µm inside it, veins (ridge filter) and interior lamina.
7. Report which regions hold the earliest 5 % of t50 values, relative to their area.

ΔF/F₀ is not used. The pre-flood baseline is short and overlaps the arrival of water, and the plant is faint relative to its local background at that point.

## Main findings so far

Every figure and number comes from files in `results/`, produced by the scripts above.
- The 2020 deck's "All Flood Waves" traces are the **standard deviation** of pixels inside each ROI. Recomputing that SD from the raw data reproduces the 2020 chart (`results/figures/roi2020_reproduction.png`).
- The 2020 video time stamps assume 1 s per frame and start 48.5 s into the recording (`data/README.md`).
- Eight of 12 runs pass QC. `analysis/qc.json` plus the automatic motion and settle-step flags in `deck_figs.py` exclude expt 2 (motion), expts 3–4 (mask) and expt 10 (earliest pixels on the settle step).
- **Timing:** in every pooled run the GCaMP-channel signal rises over **minutes** after water arrives and motion settles. Median t50 is 323 s from the start of recording (range 194–520 s), and the median whole-plant peak is at 527 s (`results/pooled_summary.json`). The one seconds-scale jump (expt 10) is simultaneous across the field and could be optical.
- **Margins:** among the earliest 5 % of pixels, the outer margin is modestly over-represented (median 1.40×). The inner control band is not (0.93×). Margin exceeds inner band in 7 of 8 runs (sign test p = 0.07). This is weak support for the 2020 hydathode idea; hydathodes are not resolved at this pixel size.
- **No unflooded control run:** light exposure or handling could also drive the rise.

## Reproducing

Run `analysis/run_all.sh <folder with the 12 .czi files> <python>` with Python 3.11 and `czifile`, `imagecodecs`, `numpy`, `scipy`, `scikit-image`, `matplotlib`, `pillow` and `opencv-python-headless`. The outputs in `results/runs/` were produced by `analysis/flood_wave.py`. Expts 8 and 11 were run with `--qc analysis/qc.json`. For the other ten, the `--qc` code path is identical because they have no exclusion boxes.

## Archive

- **Code, metadata, results and docs:** this GitHub repository (public).
- **Raw recordings** (12 `.czi`, 5.17 GB) **and the 2020 videos** (5 `.avi`, 717 MB): a Zenodo deposit is prepared as a draft with metadata from `data/zenodo_raw_deposit.json`. All 17 files were uploaded on 2026-10-28, and every MD5 matches Zenodo's checksum (`data/zenodo_draft_upload_report.json`, made by `scripts/zenodo_draft_upload.py`). It is **not yet published**; its DOI will be added here and in `CITATION.cff` on publication. Checksums: `data/RAW_CZI_SHA256SUMS` and `data/derived_2020_videos/SHA256SUMS`.

## The new deck

"Flood Wave, revisited" is a 18-slide Claude Slides artifact, private to Richard: https://claude.ai/artifact/UFtgMKqHRoGHEK8AgNVB3D. Its slide sources are kept in `deck_2026/`.

## Credits

Shreya Godishala (University of Wisconsin–Madison at the time) ran the experiment, collected the data and did the imaging, with Richard Barker and Simon Gilroy (2020). Richard Barker's ORCID is 0000-0001-5681-9857. ORCIDs for Shreya Godishala and Simon Gilroy are still to be added (`CITATION.cff`).

## Licence

Code (`analysis/`, `scripts/`) is MIT (`LICENSE`). Data, metadata, results, figures, the video clip and the documentation are CC BY 4.0 (`LICENSE-DATA.md`). The exception is third-party figures reproduced inside the 2020 deck in `legacy/`, which stay with their owners.
