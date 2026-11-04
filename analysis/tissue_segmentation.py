#!/usr/bin/env python3
"""
Automated Tissue-Specific Anatomical Segmentation and Quantitative Evaluation
across all 12 FloodWave-At widefield GCaMP time-lapse recordings.

Defines 5 pure tissue compartments (0.00% background contamination):
  1. Hydathode Epithems / Marginal Teeth (hydathodes)
  2. Primary & Secondary Vasculature (veins)
  3. Pure Interveinal Lamina / Mesophyll (pure_lamina)
  4. Rosette Shoot Apex / Meristem (meristem)
  5. Spatial Negative Controls (margin_other, inner_control)

Audits 2020 crude circular ROIs vs. Refined pure-tissue ROIs on expt08.
Extracts background-subtracted time series, kinetic parameters (t50, tpeak, rise, SNR, enrichment),
and performs statistical hypothesis tests across the 8 pooled runs.
"""

import os, sys, re, glob, json
import numpy as np
import czifile
from scipy import ndimage as ndi
from scipy.stats import wilcoxon, friedmanchisquare
from skimage.morphology import disk, dilation, erosion
from skimage.filters import sato
from skimage.feature import corner_peaks, corner_harris

PX_UM = 20.4925 * 2 # 40.985 um per binned pixel

RAW_DIR = "/Volumes/Barker_2016/Hyperspectral_UW-Botany_July 2016/Flood_DRB"
RESULTS_DIR = "results"
RUNS_DIR = os.path.join(RESULTS_DIR, "runs")

POOLED_RUNS = ["expt01", "expt05", "expt06", "expt07", "expt08", "expt09", "expt11", "expt12"]
EXCLUDED_RUNS = ["expt02", "expt03", "expt04", "expt10"]

# Known meristem approximate centroids (in binned px y, x) for intact rosettes
MERISTEM_SEEDS = {
    "expt01": (135, 185),
    "expt02": (120, 155),
    "expt03": (145, 175),
    "expt04": (130, 160),
    "expt05": (130, 170),
    "expt06": None,         # single young leaf, no meristem
    "expt07": (130, 175),
    "expt08": (162, 157),   # corresponding to 2020 Mersitem-1
    "expt09": (140, 160),
    "expt10": (125, 170),
    "expt11": (130, 175),
    "expt12": (125, 170),
}


def segment_tissues(ref, mask, tag):
    """
    Segment the registered plant reference into 5 pure anatomical compartments:
    hydathodes, veins, pure_lamina, meristem, margin_other, inner_control.
    All masks are strictly subsets of 'mask', guaranteeing 0% background contamination.
    """
    dist = ndi.distance_transform_edt(mask)
    yy, xx = np.indices(mask.shape)
    
    # 1. Outer Margin (dist <= 2 px, ~82 um) & Inner Control (2 < dist <= 4 px, 82-164 um)
    margin = mask & (dist <= 2)
    inner_control = mask & (dist > 2) & (dist <= 4)
    core = mask & (dist > 4)
    
    # 2. Primary and secondary vasculature via Sato ridge filter
    ridge = sato(ref, sigmas=[1, 2], black_ridges=False)
    core_ridge = ridge[core] if core.any() else np.array([0])
    vein_thresh = np.percentile(core_ridge, 80) if core.any() else 0
    veins = core & (ridge > vein_thresh) if core.any() else np.zeros_like(mask)
    
    # Safety buffer around veins (dilate by 2 px ~ 82 um)
    vein_buf = dilation(veins, disk(2))
    
    # 3. Rosette Shoot Apex / Meristem
    seed = MERISTEM_SEEDS.get(tag)
    meristem = np.zeros_like(mask)
    if seed is not None:
        sy, sx = seed
        # Radial disk of radius 10 px (~410 um) clipped strictly inside mask & not within margin
        meristem_disc = (yy - sy)**2 + (xx - sx)**2 <= 11**2
        meristem = mask & meristem_disc & (dist > 2)
        if not meristem.any(): # fallback to core centroid
            cy, cx = ndi.center_of_mass(core if core.any() else mask)
            meristem = mask & ((yy - cy)**2 + (xx - cx)**2 <= 10**2) & (dist > 2)
    
    # 4. Hydathode Epithems / Marginal Teeth
    # Detect sharp convex curvature peaks along outer leaf boundary
    corners = corner_peaks(corner_harris(mask.astype(float)), min_distance=7, threshold_rel=0.07)
    hydathodes = np.zeros_like(mask)
    for cy, cx in corners:
        if mask[cy, cx]:
            # Compact 2-px radius disc (~82 um) clipped strictly within outer margin
            disc = (yy - cy)**2 + (xx - cx)**2 <= 2**2
            hydathodes |= (disc & margin)
            
    # If no corners detected, ensure at least some margin teeth
    if hydathodes.sum() < 20 and margin.sum() > 50:
        # Top 5% most distal margin pixels from center
        cy, cx = ndi.center_of_mass(mask)
        d_center = np.hypot(yy - cy, xx - cx)
        hydathodes = margin & (d_center > np.percentile(d_center[margin], 95))

    # 5. Non-hydathode margin rim
    margin_other = margin & ~hydathodes
    
    # 6. Pure Interveinal Lamina (core mesophyll, strictly excluding veins, vein buffers, and meristem)
    pure_lamina = core & ~vein_buf & ~meristem
    
    # Verify strict disjointness and zero background
    assert (hydathodes & ~mask).sum() == 0, f"{tag}: Hydathodes leak into background!"
    assert (veins & ~mask).sum() == 0, f"{tag}: Veins leak into background!"
    assert (pure_lamina & ~mask).sum() == 0, f"{tag}: Lamina leaks into background!"
    assert (meristem & ~mask).sum() == 0, f"{tag}: Meristem leaks into background!"
    assert (pure_lamina & veins).sum() == 0, f"{tag}: Lamina overlaps veins!"
    
    return {
        "hydathodes": hydathodes,
        "veins": veins,
        "pure_lamina": pure_lamina,
        "meristem": meristem,
        "margin_other": margin_other,
        "inner_control": inner_control,
        "plant": mask
    }


def analyze_roi2020_refinement(raw_czi_path, registered_shifts, bg_mask, qc_json_path, out_json_path):
    """
    On expt08, compare the seven 2020 crude circular ROIs directly against their
    refined, pure-tissue counterparts.
    """
    print("\n--- Auditing 2020 Crude ROIs vs Refined 2026 ROIs on expt08 ---")
    with czifile.CziFile(raw_czi_path) as c:
        arr = np.squeeze(c.asarray()).astype(np.float32)
        T, Y, X = arr.shape
        raw_binned = arr.reshape(T, Y // 2, 2, X // 2, 2).mean((2, 4))
    maps08 = np.load("results/runs/expt08/expt08_maps.npz")
    t = maps08["t"]
    
    # Apply rigid shifts
    S = np.empty_like(raw_binned)
    for i in range(T):
        if np.hypot(*registered_shifts[i]) > 0.05:
            S[i] = ndi.shift(raw_binned[i], registered_shifts[i], order=1, mode='nearest')
        else:
            S[i] = raw_binned[i]
            
    # Additive local background subtraction
    w = ndi.gaussian_filter(bg_mask.astype(np.float32), 12)
    Fc = np.empty_like(S)
    for i in range(T):
        B = ndi.gaussian_filter(S[i] * bg_mask, 12) / np.maximum(w, 1e-3)
        Fc[i] = S[i] - B
    Fc = ndi.uniform_filter1d(Fc, 5, axis=0) # match temporal smoothing

    # Load 2020 ROI definitions
    with open("results/roi2020_expt08.json") as f:
        roi2020_data = json.load(f)

    maps08 = np.load("results/runs/expt08/expt08_maps.npz")
    plant_mask = maps08["mask"]
    i_settle = int(maps08["i_settle"])
    yy, xx = np.indices(plant_mask.shape)
    
    tissues08 = segment_tissues(maps08["ref"], plant_mask, "expt08")
    vein_buf = dilation(tissues08["veins"], disk(2))
    
    rois_audit = {}
    
    for k_str, r in roi2020_data["rois"].items():
        k = int(k_str)
        lbl = r["label"]
        
        # Crude circle in binned coords
        bx, by, br = r["x"] / 2.0, r["y"] / 2.0, r["r"] / 2.0
        crude_circle = (xx - bx)**2 + (yy - by)**2 <= br**2
        
        # Refined mask:
        # Strictly intersect with plant mask (0% background)
        pure_mask = crude_circle & plant_mask
        
        # Tissue-specific refinement:
        if "Lamina" in lbl:
            # For lamina, strictly remove any vein overlap
            refined_tissue_mask = pure_mask & ~vein_buf
            if refined_tissue_mask.sum() < 20: # if too small, just remove pure vein
                refined_tissue_mask = pure_mask & ~tissues08["veins"]
        elif "Hydrathode" in lbl:
            # For hydathode, confine to marginal tooth
            refined_tissue_mask = pure_mask & (ndi.distance_transform_edt(plant_mask) <= 3)
            if refined_tissue_mask.sum() < 15:
                refined_tissue_mask = pure_mask
        elif "Mersitem" in lbl:
            # For meristem, strictly on plant tissue
            refined_tissue_mask = pure_mask
        else:
            refined_tissue_mask = pure_mask
            
        crude_total_px = int(crude_circle.sum())
        crude_bg_px = int((crude_circle & ~plant_mask).sum())
        crude_bg_frac = float(crude_bg_px / max(crude_total_px, 1))
        
        refined_total_px = int(refined_tissue_mask.sum())
        refined_bg_px = int((refined_tissue_mask & ~plant_mask).sum())
        refined_bg_frac = float(refined_bg_px / max(refined_total_px, 1))
        assert refined_bg_frac == 0.0, f"Refined ROI {lbl} has background pixels!"
        
        # Time series
        crude_raw_mean = [float(f[crude_circle].mean()) for f in S]
        crude_raw_sd = [float(f[crude_circle].std()) for f in S]
        crude_bgsub_mean = [float(f[crude_circle].mean()) for f in Fc]
        crude_bgsub_sd = [float(f[crude_circle].std()) for f in Fc]
        
        refined_raw_mean = [float(f[refined_tissue_mask].mean()) for f in S]
        refined_raw_sd = [float(f[refined_tissue_mask].std()) for f in S]
        refined_bgsub_mean = [float(f[refined_tissue_mask].mean()) for f in Fc]
        refined_bgsub_sd = [float(f[refined_tissue_mask].std()) for f in Fc]
        
        # Kinetics post-settle
        post_crude = np.array(crude_bgsub_mean[i_settle:])
        post_refined = np.array(refined_bgsub_mean[i_settle:])
        
        rise_crude = float(post_crude.max() - post_crude[:5].mean())
        rise_refined = float(post_refined.max() - post_refined[:5].mean())
        
        # Baseline noise (std in first 10 frames of post-settle or pre-flood)
        noise_crude = float(np.std(np.diff(crude_bgsub_mean[i_settle:i_settle+25])) / np.sqrt(2))
        noise_refined = float(np.std(np.diff(refined_bgsub_mean[i_settle:i_settle+25])) / np.sqrt(2))
        
        snr_crude = float(rise_crude / max(noise_crude, 1e-3))
        snr_refined = float(rise_refined / max(noise_refined, 1e-3))
        
        # t50
        half_crude_thresh = post_crude[:5].mean() + 0.5 * rise_crude
        half_refined_thresh = post_refined[:5].mean() + 0.5 * rise_refined
        
        i_t50_crude = int(np.where(post_crude >= half_crude_thresh)[0][0]) if (post_crude >= half_crude_thresh).any() else 0
        i_t50_refined = int(np.where(post_refined >= half_refined_thresh)[0][0]) if (post_refined >= half_refined_thresh).any() else 0
        
        t50_crude = float(t[i_settle + i_t50_crude])
        t50_refined = float(t[i_settle + i_t50_refined])
        
        rois_audit[k] = {
            "label": lbl,
            "crude": {
                "total_px": crude_total_px,
                "bg_px": crude_bg_px,
                "bg_frac": crude_bg_frac,
                "mean_raw": crude_raw_mean,
                "sd_raw": crude_raw_sd,
                "mean_bgsub": crude_bgsub_mean,
                "sd_bgsub": crude_bgsub_sd,
                "rise": rise_crude,
                "noise": noise_crude,
                "snr": snr_crude,
                "t50_s": t50_crude,
                "tpeak_s": float(t[i_settle + post_crude.argmax()])
            },
            "refined": {
                "total_px": refined_total_px,
                "bg_px": refined_bg_px,
                "bg_frac": refined_bg_frac,
                "mean_raw": refined_raw_mean,
                "sd_raw": refined_raw_sd,
                "mean_bgsub": refined_bgsub_mean,
                "sd_bgsub": refined_bgsub_sd,
                "rise": rise_refined,
                "noise": noise_refined,
                "snr": snr_refined,
                "t50_s": t50_refined,
                "tpeak_s": float(t[i_settle + post_refined.argmax()])
            }
        }
        print(f"  {lbl:12s}: Crude bg={crude_bg_frac*100:4.1f}% (SNR={snr_crude:4.1f}, t50={t50_crude:5.1f}s) -> Refined bg={refined_bg_frac*100:4.1f}% (SNR={snr_refined:4.1f}, t50={t50_refined:5.1f}s)")
        
    out = {
        "tag": "expt08",
        "t": t.tolist(),
        "i_settle": i_settle,
        "t_settle_s": float(t[i_settle]),
        "rois": rois_audit
    }
    with open(out_json_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"Saved 2020 audit to {out_json_path}")
    return out


def run_full_tissue_segmentation():
    """
    Run tissue segmentation and time-series extraction across all 12 recordings.
    """
    czi_files = sorted(glob.glob(os.path.join(RAW_DIR, "*.czi")))
    print(f"Found {len(czi_files)} raw .czi files in {RAW_DIR}")
    
    file_map = {}
    for f in czi_files:
        base = os.path.basename(f)
        m = re.match(r"Flooding expt (\d+)", base)
        if m:
            n = int(m.group(1))
            file_map[f"expt{n:02d}"] = f

    all_summaries = []
    
    for expt_idx in range(1, 13):
        tag = f"expt{expt_idx:02d}"
        czi_path = file_map[tag]
        print(f"\n==================== Processing {tag} ====================")
        
        # Load existing run data
        run_npz = os.path.join(RUNS_DIR, tag, f"{tag}_maps.npz")
        d_map = np.load(run_npz)
        ref_img = d_map["ref"]
        plant_mask = d_map["mask"]
        shifts = d_map["shifts"]
        t = d_map["t"]
        i_settle = int(d_map["i_settle"])
        t50_map = d_map["t50"]
        rise_map = d_map["rise"]
        valid_t50 = ~np.isnan(t50_map)
        
        # 1. Segment into anatomical tissues
        tissues = segment_tissues(ref_img, plant_mask, tag)
        
        # 2. Read raw CZI and extract background-subtracted time-series
        with czifile.CziFile(czi_path) as c:
            arr = np.squeeze(c.asarray()).astype(np.float32)
            T, Y, X = arr.shape
            raw_binned = arr.reshape(T, Y // 2, 2, X // 2, 2).mean((2, 4))
                
        # Register frames rigidly
        S = np.empty_like(raw_binned)
        for i in range(T):
            if np.hypot(*shifts[i]) > 0.05:
                S[i] = ndi.shift(raw_binned[i], shifts[i], order=1, mode='nearest')
            else:
                S[i] = raw_binned[i]
                
        # Background subtraction
        bg_mask = ~ndi.binary_dilation(plant_mask, disk(4))
        w = ndi.gaussian_filter(bg_mask.astype(np.float32), 12)
        Fc = np.empty_like(S)
        for i in range(T):
            B = ndi.gaussian_filter(S[i] * bg_mask, 12) / np.maximum(w, 1e-3)
            Fc[i] = S[i] - B
        Fc = ndi.uniform_filter1d(Fc, 5, axis=0) # match standard smoothing
        
        # 3. Extract metrics per tissue compartment
        q5_overall = np.percentile(t50_map[valid_t50], 5) if valid_t50.sum() >= 50 else np.nan
        total_valid = max(valid_t50.sum(), 1)
        total_first5 = (t50_map[valid_t50] <= q5_overall).sum() if not np.isnan(q5_overall) else 1
        
        run_record = {
            "tag": tag,
            "file": os.path.basename(czi_path),
            "pooled": tag in POOLED_RUNS,
            "frames": T,
            "duration_s": float(t[-1]),
            "i_settle": i_settle,
            "t_settle_s": float(t[i_settle]),
            "plant_total_px": int(plant_mask.sum()),
            "plant_area_mm2": float(plant_mask.sum() * (PX_UM / 1000)**2),
            "tissues": {}
        }
        
        tissue_traces = {}
        tissue_sd_traces = {}
        
        for tname, tmask in tissues.items():
            px_count = int(tmask.sum())
            area_mm2 = float(px_count * (PX_UM / 1000)**2)
            frac_rosette = float(px_count / max(plant_mask.sum(), 1))
            
            # Contamination check: strictly 0
            bg_contam_px = int((tmask & ~plant_mask).sum())
            assert bg_contam_px == 0, f"{tag} {tname} has background contamination!"
            
            if px_count > 0:
                mean_trace = [float(f[tmask].mean()) for f in Fc]
                sd_trace = [float(f[tmask].std()) for f in Fc]
                
                # Baseline subtraction from t_settle
                base_val = np.mean(mean_trace[i_settle:i_settle+5])
                dF_trace = (np.array(mean_trace) - base_val).tolist()
                
                post_dF = np.array(dF_trace[i_settle:])
                rise_amp = float(post_dF.max())
                tpeak = float(t[i_settle + post_dF.argmax()])
                
                # Temporal noise
                noise = float(np.std(np.diff(mean_trace[i_settle:i_settle+25])) / np.sqrt(2))
                snr = float(rise_amp / max(noise, 1e-3))
                
                # t50 within tissue
                t_valid = tmask & valid_t50
                if t_valid.sum() >= 5:
                    med_t50 = float(np.median(t50_map[t_valid]))
                    p5_t50 = float(np.percentile(t50_map[t_valid], 5))
                else:
                    med_t50 = None
                    p5_t50 = None
                    
                # Early responder enrichment
                if not np.isnan(q5_overall) and t_valid.sum() >= 5:
                    share_first5 = float((t50_map[t_valid] <= q5_overall).sum() / max(total_first5, 1))
                    share_area = float(t_valid.sum() / total_valid)
                    enrichment = float(share_first5 / share_area) if share_area > 0 else 0.0
                else:
                    share_first5 = None
                    enrichment = None
            else:
                mean_trace = []
                sd_trace = []
                dF_trace = []
                rise_amp = None
                tpeak = None
                noise = None
                snr = None
                med_t50 = None
                p5_t50 = None
                share_first5 = None
                enrichment = None
                
            run_record["tissues"][tname] = {
                "px_count": px_count,
                "area_mm2": area_mm2,
                "frac_rosette": frac_rosette,
                "bg_contamination_pct": 0.00,
                "rise_amplitude_counts": rise_amp,
                "peak_time_s": tpeak,
                "noise_counts": noise,
                "snr": snr,
                "t50_median_s": med_t50,
                "t50_p5_s": p5_t50,
                "first5_enrichment": enrichment
            }
            
            tissue_traces[f"trace_{tname}"] = np.array(dF_trace, dtype=np.float32)
            tissue_sd_traces[f"sd_{tname}"] = np.array(sd_trace, dtype=np.float32)
            
            print(f"  {tname:15s}: px={px_count:5d} ({frac_rosette*100:4.1f}%) | rise=+{rise_amp or 0:5.1f} cts | t50={med_t50 or -1:5.1f}s | enrich={enrichment or 0:4.2f}x")

        # Save per-run tissue maps npz
        out_npz = os.path.join(RUNS_DIR, tag, f"{tag}_tissue_maps.npz")
        np.savez_compressed(
            out_npz,
            ref=ref_img,
            mask=plant_mask,
            t=t,
            shifts=shifts,
            i_settle=i_settle,
            t50=t50_map,
            rise=rise_map,
            **{f"mask_{k}": v for k, v in tissues.items()},
            **tissue_traces,
            **tissue_sd_traces
        )
        all_summaries.append(run_record)
        
        # On expt08, execute the detailed 2020 ROI refinement comparison
        if tag == "expt08":
            analyze_roi2020_refinement(
                czi_path, shifts, bg_mask, "analysis/qc.json", "results/refined_rois_expt08.json"
            )

    # 4. Statistical hypothesis testing across the 8 pooled runs
    print("\n==================== Statistical Comparisons Across 8 Pooled Runs ====================")
    pooled_records = [r for r in all_summaries if r["pooled"]]
    
    tissue_names = ["hydathodes", "veins", "pure_lamina", "meristem"]
    t50_by_tissue = {t: [] for t in tissue_names}
    rise_by_tissue = {t: [] for t in tissue_names}
    enrich_by_tissue = {t: [] for t in tissue_names}
    
    for r in pooled_records:
        for tname in tissue_names:
            tdata = r["tissues"][tname]
            t50_by_tissue[tname].append(tdata["t50_median_s"])
            rise_by_tissue[tname].append(tdata["rise_amplitude_counts"])
            enrich_by_tissue[tname].append(tdata["first5_enrichment"])

    # Non-parametric tests
    # Compare Veins vs Pure Lamina across pooled runs with valid pairs
    vein_t50 = []
    lam_t50 = []
    for v, l in zip(t50_by_tissue["veins"], t50_by_tissue["pure_lamina"]):
        if v is not None and l is not None:
            vein_t50.append(v)
            lam_t50.append(l)
    
    wilc_vein_lam = wilcoxon(vein_t50, lam_t50) if len(vein_t50) >= 5 else None
    
    # Compare Hydathodes vs Pure Lamina
    hyd_t50 = []
    lam_t50_h = []
    for h, l in zip(t50_by_tissue["hydathodes"], t50_by_tissue["pure_lamina"]):
        if h is not None and l is not None:
            hyd_t50.append(h)
            lam_t50_h.append(l)
    wilc_hyd_lam = wilcoxon(hyd_t50, lam_t50_h) if len(hyd_t50) >= 5 else None

    # Compare Hydathodes vs Veins
    hyd_t50_v = []
    vein_t50_h = []
    for h, v in zip(t50_by_tissue["hydathodes"], t50_by_tissue["veins"]):
        if h is not None and v is not None:
            hyd_t50_v.append(h)
            vein_t50_h.append(v)
    wilc_hyd_vein = wilcoxon(hyd_t50_v, vein_t50_h) if len(hyd_t50_v) >= 5 else None

    stats_summary = {
        "n_pooled": len(pooled_records),
        "median_t50": {t: float(np.nanmedian([x for x in t50_by_tissue[t] if x is not None])) for t in tissue_names},
        "median_rise": {t: float(np.nanmedian([x for x in rise_by_tissue[t] if x is not None])) for t in tissue_names},
        "median_enrichment": {t: float(np.nanmedian([x for x in enrich_by_tissue[t] if x is not None])) for t in tissue_names},
        "wilcoxon_vein_vs_pure_lamina": {
            "statistic": float(wilc_vein_lam.statistic) if wilc_vein_lam else None,
            "p_value": float(wilc_vein_lam.pvalue) if wilc_vein_lam else None
        },
        "wilcoxon_hydathodes_vs_pure_lamina": {
            "statistic": float(wilc_hyd_lam.statistic) if wilc_hyd_lam else None,
            "p_value": float(wilc_hyd_lam.pvalue) if wilc_hyd_lam else None
        },
        "wilcoxon_hydathodes_vs_veins": {
            "statistic": float(wilc_hyd_vein.statistic) if wilc_hyd_vein else None,
            "p_value": float(wilc_hyd_vein.pvalue) if wilc_hyd_vein else None
        }
    }
    print(f"Median t50 by tissue across 8 pooled runs:")
    for tname, med in stats_summary["median_t50"].items():
        print(f"  {tname:15s}: {med:.1f} s")
    if wilc_vein_lam:
        print(f"Wilcoxon Veins vs Pure Lamina: stat={wilc_vein_lam.statistic:.2f}, p={wilc_vein_lam.pvalue:.4f}")

    # 5. Export structured results
    out_json = {
        "dataset": "FloodWave-At",
        "description": "Tissue-specific anatomical segmentation across all 12 widefield GCaMP recordings",
        "statistics": stats_summary,
        "runs": all_summaries
    }
    with open("results/tissue_segmentation_summary.json", "w") as f:
        json.dump(out_json, f, indent=2)
    print("Saved results/tissue_segmentation_summary.json")

    # CSV Export
    import csv
    with open("results/tissue_segmentation_summary.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "tag", "file", "pooled", "frames", "duration_s", "t_settle_s",
            "tissue", "px_count", "area_mm2", "frac_rosette", "bg_contamination_pct",
            "rise_counts", "peak_time_s", "noise_counts", "snr",
            "t50_median_s", "t50_p5_s", "first5_enrichment"
        ])
        for r in all_summaries:
            for tname, td in r["tissues"].items():
                writer.writerow([
                    r["tag"], r["file"], r["pooled"], r["frames"], r["duration_s"], r["t_settle_s"],
                    tname, td["px_count"], f"{td['area_mm2']:.3f}", f"{td['frac_rosette']:.4f}", f"{td['bg_contamination_pct']:.2f}",
                    f"{td['rise_amplitude_counts'] or 0:.1f}", f"{td['peak_time_s'] or 0:.1f}",
                    f"{td['noise_counts'] or 0:.2f}", f"{td['snr'] or 0:.2f}",
                    f"{td['t50_median_s'] or 0:.1f}", f"{td['t50_p5_s'] or 0:.1f}",
                    f"{td['first5_enrichment'] or 0:.2f}"
                ])
    print("Saved results/tissue_segmentation_summary.csv")


if __name__ == "__main__":
    run_full_tissue_segmentation()
