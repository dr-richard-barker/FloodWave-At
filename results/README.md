# Results

Everything here is produced by scripts in `../analysis/` from the raw `.czi` files, which were read only. `../analysis/run_all.sh` reruns the lot. Nothing here is synthetic: none of the scripts use random numbers.

## Tables

| File | What it holds | Produced by |
|---|---|---|
| `summary_all_runs.csv` | One row per run: settle time, t50 percentiles, region t50 medians, earliest-5 % enrichment per region, rise, peak time, motion and QC flags, held-out background residual, fast 6-s step | `deck_figs.py` from `runs/*/expt*_summary.json` |
| `pooled_summary.json` | Medians and ranges over the QC-passing runs; margin-vs-inner-band sign test; which runs were excluded and why | `deck_figs.py` |
| `roi2020_expt08.json` | The seven 2020 ROIs registered onto raw expt 8 (NCC, position, radius), with per-frame SD, mean and background-subtracted mean, plus distance to the plant outline | `roi2020.py` |
| `runs/exptNN/exptNN_summary.json` | Per-run numbers | `flood_wave.py` |
| `runs/exptNN/exptNN_maps.npz` | Per-run arrays: t50, peak time, rise, region masks, traces, registration shifts. Not in git | `flood_wave.py` |

## Figures

| File | What it shows | Data |
|---|---|---|
| `figures/expt08_regions_t50.png` | Expt 8. Left: region masks (margin orange, inner control band grey, veins blue, lamina aqua) on the late registered reference image. Right: half-maximum rise time (t50) per plant pixel, lighter = earlier; white outline = earliest 5 %. 2 mm scale bars | `runs/expt08` |
| `figures/expt08_traces.png` | Expt 8. Mean signal above local background per region, from the settle time onwards, with the held-out background residual (flat line = background model is sound) | `runs/expt08` |
| `figures/roi2020_reproduction.png` | The seven 2020 ROIs. Left: standard deviation of raw counts inside each ROI, which reproduces the 2020 "All Flood Waves" chart. Right: background-subtracted mean inside the same ROIs. Colour = 2020 ROI label class | `roi2020_expt08.json` |
| `figures/all_runs_order_maps.png` | All 12 runs. Each plant pixel coloured by its t50 rank within its own run (light = first). Titles give the filename label and whether the run is pooled or why it is excluded | `runs/*` |
| `figures/enrichment_all_runs.png` | Earliest-5 % enrichment per region per run, log scale; 1× = no preference. Grey run labels are excluded from pooled numbers | `summary_all_runs.csv` |
| `figures/mask_qc_sheet.png` | Plant mask (red outline) over each run's late reference image; the basis for the by-eye decisions in `../analysis/qc.json` | `runs/*` |
| `runs/exptNN/exptNN_activation.png` | Per-run diagnostic: regions, t50 map, rise map, region traces, t50 histograms by region, registration shift | `flood_wave.py` |

## QC evidence

| File | What it holds |
|---|---|
| `qc/grid_pitch_expt08.log`, `.png` | Mesh period by autocorrelation of a grid-only patch of expt 8 (`grid_acf.py`) |
| `video_match/match_video_expt08.log` | Frame offset and spatial match between the 2020 video and raw expt 8 (`match_video.py`) |
| `video_match/ffprobe_2020_videos.txt` | Codec, size and frame count of the five 2020 videos |
| `video_match/burned_in_timestamps_frames_0_60_396_659.png` | The burned-in "mm:ss Time" stamps on four video frames (see the matching README) |
| `video_match/surface_plot_frame300.png` | One frame of the 2020 surface-plot video, showing its axis lengths |
