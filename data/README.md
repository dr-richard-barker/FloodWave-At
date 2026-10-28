# Data

## Raw recordings (not in git)

There are 12 Zeiss ZEN `.czi` files, 5.17 GB in total, all acquired on 10 Jan 2020. Their current location is the external drive `Barker_2016`, at `Hyperspectral_UW-Botany_July 2016/Flood_DRB/`. A Zenodo deposit is planned. Per-file metadata, acquisition order and checksums-to-be are in `../INVENTORY.md` and `../metadata/`.

Each file is a single-channel time series: 692 × 520 px, 20.49 µm per pixel, GFP filter set 38 HE, a median of 1.212 s per frame, and 198–1140 frames.

## `derived_2020_videos/` (not in git; checksums in `SHA256SUMS`)

These are five Fiji exports made in April 2020 for the original "Flood Wave" deck. They were downloaded on 2026-10-28 from the Google Drive folder `Flooding_DRB_Shreya` (in Richard Barker's personal Google Drive). **All five derive from expt 8.**

| File | Frames | Size | Codec | Note |
|---|---|---|---|---|
| `Flood_DRB_Shreya_Flooding expt 8 … .avi` | 660 | 552×399 | PNG (lossless) | Blue LUT, burned-in "mm:ss Time" stamp |
| `Flood_DRB_Shreya_20fps_Flooding expt 8 … .avi` | 660 | 552×399 | raw BGR | Same, at 20 fps playback |
| `Smooth_Flooding expt 8 … .avi` | 660 | 552×399 | MJPEG | Smoothed, rainbow LUT |
| `Maxima_Flooding expt 8 … .avi` | 660 | 552×399 | MJPEG | Rainbow LUT; the 2020 deck calls it a "maximal project smoothed" |
| `Flood_Wave_Surface_Plot.avi` | 660 | 610×605 | MJPEG | Fiji 3-D surface plot over 11,311.8 × 8,176.5 µm |

Codec, size and frame counts come from ffprobe (`../results/video_match/ffprobe_2020_videos.txt`). The surface-plot axis lengths are read off one of its frames (`../results/video_match/surface_plot_frame300.png`).

How these frames map onto the raw run, checked by `analysis/match_video.py` (output in `../results/video_match/match_video_expt08.log`):
- **Time:** video frame *n* is raw frame *n* + 40. The first 40 frames (48.5 s) were dropped. The correlation of whole-frame means is 0.996.
- **Space:** each video frame is a 552 × 399 px crop at native resolution; the surface plot's axis lengths equal 552 × 399 px at 20.49 µm.
- **Clock:** the burned-in stamp counts 1 s per frame. Video frames 0/60/396/659 read 00:00/01:00/06:36/10:59. The true interval is 1.212 s, so the stamps understate elapsed time by 17.5 %.
