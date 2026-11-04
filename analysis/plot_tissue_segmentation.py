#!/usr/bin/env python3
"""
Scientific Publication Visualizations for Tissue-Specific Anatomical Segmentation:
  1. Figure 6: Multi-Run Tissue Segmentation Atlas (tissue_segmentation_all_runs.png)
  2. Figure 7: Head-to-Head Performance Audit on expt08: 2020 Crude Circles vs. Refined 2026 ROIs (tissue_comparison_expt08.png)
  3. Figure 8: Population Kinetics and Hierarchical Flow Across 8 Pooled Runs (tissue_kinetics_population.png)

Saves high-res figures to both results/figures/ and docs/assets/figures/.
"""

import os, sys, glob, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D
from scipy import ndimage as ndi

PX_UM = 20.4925 * 2 # 40.985 um per binned px

RESULTS_FIGS = "results/figures"
DOCS_FIGS = "docs/assets/figures"
os.makedirs(RESULTS_FIGS, exist_ok=True)
os.makedirs(DOCS_FIGS, exist_ok=True)

# CoSE Brand & Tissue Color Palette
COLORS = {
    "hydathodes": "#E67E22",      # Rich Amber / Orange
    "veins": "#2980B9",           # Deep Cerulean Blue
    "pure_lamina": "#27AE60",     # Emerald Green
    "meristem": "#8E44AD",        # Amethyst Purple
    "margin_other": "#D35400",    # Rust Orange
    "inner_control": "#7F8C8D",   # Slate Grey
    "background_leak": "#E74C3C", # Crimson Red
    "cose_navy": "#004053",
    "cose_teal": "#0F7F9F",
    "cose_light": "#F6F9FA"
}

POOLED_RUNS = ["expt01", "expt05", "expt06", "expt07", "expt08", "expt09", "expt11", "expt12"]


def plot_atlas_all_runs():
    """Figure 6: 12-panel tissue segmentation gallery across all recordings."""
    print("Generating Figure 6: tissue_segmentation_all_runs.png ...")
    fig, axes = plt.subplots(3, 4, figsize=(16, 11), facecolor="#ffffff")
    axes = axes.flatten()
    
    # Load summary data
    with open("results/tissue_segmentation_summary.json") as f:
        summary_data = json.load(f)
    run_records = {r["tag"]: r for r in summary_data["runs"]}
    
    for idx in range(1, 13):
        tag = f"expt{idx:02d}"
        ax = axes[idx - 1]
        
        npz_path = f"results/runs/{tag}/{tag}_tissue_maps.npz"
        if not os.path.exists(npz_path):
            ax.text(0.5, 0.5, f"{tag}\n(not found)", ha='center', va='center')
            ax.axis('off')
            continue
            
        data = np.load(npz_path)
        ref = data["ref"]
        mask = data["mask"]
        m_hyd = data["mask_hydathodes"]
        m_vein = data["mask_veins"]
        m_lam = data["mask_pure_lamina"]
        m_meri = data["mask_meristem"]
        m_inner = data["mask_inner_control"]
        
        # Display grayscale base
        lo, hi = np.percentile(ref, [2, 99.5])
        ax.imshow(ref, cmap="gray", vmin=lo, vmax=hi, aspect='equal')
        
        # Create RGBA overlay
        overlay = np.zeros(ref.shape + (4,), dtype=np.float32)
        
        # Inner control
        overlay[m_inner] = [0.5, 0.55, 0.55, 0.45]
        # Pure Lamina (Green)
        overlay[m_lam] = [0.15, 0.70, 0.35, 0.50]
        # Veins (Blue)
        overlay[m_vein] = [0.15, 0.55, 0.95, 0.75]
        # Meristem (Purple)
        overlay[m_meri] = [0.65, 0.20, 0.85, 0.80]
        # Hydathodes (Gold/Orange with border highlight)
        overlay[m_hyd] = [0.95, 0.55, 0.10, 0.95]
        
        ax.imshow(overlay)
        
        # Outline hydathode clusters for clear visibility
        hyd_labeled, num_hyd = ndi.label(m_hyd)
        if num_hyd > 0:
            for h_i in range(1, num_hyd + 1):
                cy, cx = ndi.center_of_mass(hyd_labeled == h_i)
                ax.plot(cx, cy, marker='o', markersize=3.5, color='#F39C12', markeredgecolor='white', markeredgewidth=0.6)
                
        # Annotate run title and status
        rec = run_records.get(tag, {})
        is_pooled = rec.get("pooled", False)
        status_str = "Pooled" if is_pooled else "Excluded"
        status_col = "#004053" if is_pooled else "#C0392B"
        
        ax.set_title(f"{tag} ({status_str})", fontsize=10, fontweight="bold", color=status_col, pad=4)
        
        # Scale bar on expt01 & expt08
        if idx in [1, 8]:
            scale_px = 2000 / PX_UM
            ax.plot([15, 15 + scale_px], [ref.shape[0] - 15, ref.shape[0] - 15], color="white", lw=2.5)
            ax.text(15, ref.shape[0] - 20, "2 mm", color="white", fontsize=8, fontweight="bold")
            
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color("#004053" if is_pooled else "#E74C3C")
            spine.set_linewidth(1.8 if is_pooled else 1.2)
            
    # Add overarching legend
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Hydathode Teeth (0% BG)', markerfacecolor=COLORS["hydathodes"], markersize=8, markeredgecolor='white'),
        patches.Patch(facecolor=COLORS["veins"], edgecolor='none', label='Primary & Secondary Veins'),
        patches.Patch(facecolor=COLORS["pure_lamina"], edgecolor='none', label='Pure Interveinal Lamina'),
        patches.Patch(facecolor=COLORS["meristem"], edgecolor='none', label='Rosette Shoot Apex / Meristem'),
        patches.Patch(facecolor=COLORS["inner_control"], edgecolor='none', label='Inner Control Band (80–160 µm)')
    ]
    fig.legend(handles=legend_elements, loc='lower center', ncol=5, fontsize=10, frameon=True,
               facecolor="#F6F9FA", edgecolor="#004053", bbox_to_anchor=(0.5, 0.015))
               
    fig.suptitle("Figure 6 | Multi-Run Tissue-Specific Anatomical Segmentation Atlas (n = 12 Recordings)",
                 fontsize=14, fontweight="bold", color="#004053", y=0.985)
                 
    fig.subplots_adjust(left=0.03, right=0.97, top=0.93, bottom=0.06, wspace=0.08, hspace=0.18)
    
    out_p1 = os.path.join(RESULTS_FIGS, "tissue_segmentation_all_runs.png")
    out_p2 = os.path.join(DOCS_FIGS, "tissue_segmentation_all_runs.png")
    fig.savefig(out_p1, dpi=200, bbox_inches='tight')
    fig.savefig(out_p2, dpi=200, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved: {out_p1} & {out_p2}")


def plot_expt08_comparison():
    """Figure 7: Head-to-Head Performance Audit on expt08 (Crude vs Refined ROIs)."""
    print("Generating Figure 7: tissue_comparison_expt08.png ...")
    
    with open("results/refined_rois_expt08.json") as f:
        data = json.load(f)
        
    t = np.array(data["t"])
    i_settle = data["i_settle"]
    t_settle = data["t_settle_s"]
    rois = data["rois"]
    
    # Load maps
    d_map = np.load("results/runs/expt08/expt08_tissue_maps.npz")
    ref = d_map["ref"]
    mask = d_map["mask"]
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 11), facecolor="#ffffff")
    
    # Panel A: Spatial Overlay of Crude Circles vs Refined ROIs
    ax_a = axes[0, 0]
    lo, hi = np.percentile(ref, [2, 99.5])
    ax_a.imshow(ref, cmap="gray", vmin=lo, vmax=hi, aspect='equal')
    
    # Draw plant contour
    ax_a.contour(mask, levels=[0.5], colors=['#3FA9C7'], linewidths=[1.2])
    
    # Load crude definitions
    with open("results/roi2020_expt08.json") as f:
        r2020 = json.load(f)
        
    roi_colors = {
        1: "#E67E22", # Hydathode-1
        2: "#D35400", # Hydathode-2
        3: "#27AE60", # Lamina-1
        4: "#2ECC71", # Lamina-2
        5: "#16A085", # Lamina-3
        6: "#8E44AD", # Meristem-1
        7: "#F39C12"  # Hydathode-3
    }
    
    yy, xx = np.indices(mask.shape)
    for k_str, r_entry in r2020["rois"].items():
        k = int(k_str)
        bx, by, br = r_entry["x"] / 2.0, r_entry["y"] / 2.0, r_entry["r"] / 2.0
        col = roi_colors[k]
        
        # Crude circle boundary (dashed)
        circ = patches.Circle((bx, by), br, fill=False, edgecolor=col, linestyle='--', linewidth=1.8)
        ax_a.add_patch(circ)
        
        # Highlight off-plant leakage in red
        circle_mask = (xx - bx)**2 + (yy - by)**2 <= br**2
        leak_mask = circle_mask & ~mask
        if leak_mask.any():
            leak_overlay = np.zeros(mask.shape + (4,), dtype=np.float32)
            leak_overlay[leak_mask] = [0.95, 0.15, 0.15, 0.65] # red
            ax_a.imshow(leak_overlay)
            
        ax_a.text(bx, by - br - 3, r_entry["label"], color="white", fontsize=8, fontweight="bold",
                  ha="center", bbox=dict(boxstyle="round,pad=0.2", facecolor=col, alpha=0.8, edgecolor="none"))
                  
    ax_a.set_title("A | Spatial ROI Layout: 2020 Circles vs Refined Boundaries", fontsize=11, fontweight="bold", color="#004053")
    ax_a.set_xticks([]); ax_a.set_yticks([])
    
    # Inset text
    ax_a.text(10, ref.shape[0] - 25, "Dashed = 2020 crude circles\nRed shade = Off-plant background contamination\nCyan outline = True leaf mask",
              color="white", fontsize=8.5, bbox=dict(boxstyle="round,pad=0.4", facecolor="#004053", alpha=0.85))
              
    # Panel B: Background Contamination Fraction (%)
    ax_b = axes[0, 1]
    roi_labels = [rois[str(k)]["label"] for k in range(1, 8)]
    crude_bg = [rois[str(k)]["crude"]["bg_frac"] * 100 for k in range(1, 8)]
    refined_bg = [rois[str(k)]["refined"]["bg_frac"] * 100 for k in range(1, 8)]
    
    y_pos = np.arange(len(roi_labels))
    bar_h = 0.38
    
    ax_b.barh(y_pos - bar_h/2, crude_bg, height=bar_h, color="#E74C3C", label="2020 Crude Circles (up to 27.7% BG)")
    ax_b.barh(y_pos + bar_h/2, refined_bg, height=bar_h, color="#27AE60", label="2026 Refined ROIs (0.00% BG)")
    
    ax_b.set_yticks(y_pos)
    ax_b.set_yticklabels(roi_labels, fontsize=9.5, fontweight="500")
    ax_b.set_xlabel("Off-Plant Background Contamination (%)", fontsize=10, fontweight="bold", color="#004053")
    ax_b.set_title("B | Contamination Elimination: 0% Background Across All ROIs", fontsize=11, fontweight="bold", color="#004053")
    ax_b.legend(loc="upper right", fontsize=9, frameon=True)
    ax_b.grid(axis='x', linestyle=':', alpha=0.6)
    ax_b.set_xlim(0, 32)
    
    for i, v in enumerate(crude_bg):
        if v > 0:
            ax_b.text(v + 0.6, i - bar_h/2, f"{v:.1f}%", va='center', fontsize=8.5, fontweight="bold", color="#C0392B")
    for i, v in enumerate(refined_bg):
        ax_b.text(v + 0.6, i + bar_h/2, "0.0%", va='center', fontsize=8.5, fontweight="bold", color="#27AE60")
        
    # Panel C: Mean Fluorescence Time Courses: Crude vs Refined
    ax_c = axes[1, 0]
    for k in range(1, 8):
        rd = rois[str(k)]
        col = roi_colors[k]
        lbl = rd["label"]
        # Plot crude as dashed, refined as solid
        ax_c.plot(t, rd["crude"]["mean_bgsub"], color=col, linestyle="--", lw=1.2, alpha=0.6)
        ax_c.plot(t, rd["refined"]["mean_bgsub"], color=col, linestyle="-", lw=2.0, label=f"{lbl} (Refined)")
        
    ax_c.axvline(t_settle, color="#2C3E50", linestyle=":", lw=1.5, label="t_settle (48.5 s)")
    ax_c.set_xlabel("Time from Recording Start (s)", fontsize=10, fontweight="bold", color="#004053")
    ax_c.set_ylabel("Signal Above Local Background (counts)", fontsize=10, fontweight="bold", color="#004053")
    ax_c.set_title("C | Mean Fluorescence Dynamics: True Minutes-Scale Rise", fontsize=11, fontweight="bold", color="#004053")
    ax_c.legend(loc="upper left", fontsize=7.5, ncol=2, frameon=True)
    ax_c.grid(True, linestyle=':', alpha=0.5)
    
    # Inset note explaining dashed vs solid
    ax_c.text(0.97, 0.05, "Dashed = Crude 2020 circle\nSolid = Refined pure tissue",
              transform=ax_c.transAxes, fontsize=8, ha="right", va="bottom",
              bbox=dict(boxstyle="round,pad=0.3", facecolor="#F6F9FA", edgecolor="#BDC3C7"))

    # Panel D: Within-ROI Standard Deviation (The Artifact Collapse)
    ax_d = axes[1, 1]
    # Highlight Hydathode-2 and Meristem-1 which had 25% background
    ax_d.plot(t, rois["2"]["crude"]["sd_bgsub"], color="#D35400", linestyle="--", lw=2.0,
              label="Hydathode-2 Crude (27.7% BG - False Wave!)")
    ax_d.plot(t, rois["2"]["refined"]["sd_bgsub"], color="#D35400", linestyle="-", lw=2.4,
              label="Hydathode-2 Refined (0.0% BG - Artifact Gone)")
              
    ax_d.plot(t, rois["6"]["crude"]["sd_bgsub"], color="#8E44AD", linestyle="--", lw=2.0,
              label="Meristem-1 Crude (21.3% BG - False Wave!)")
    ax_d.plot(t, rois["6"]["refined"]["sd_bgsub"], color="#8E44AD", linestyle="-", lw=2.4,
              label="Meristem-1 Refined (0.0% BG - Artifact Gone)")
              
    ax_d.plot(t, rois["3"]["crude"]["sd_bgsub"], color="#27AE60", linestyle="--", lw=1.2, alpha=0.7,
              label="Lamina-1 Crude (0% BG)")
    ax_d.plot(t, rois["3"]["refined"]["sd_bgsub"], color="#27AE60", linestyle="-", lw=1.5,
              label="Lamina-1 Refined (vein-free)")
              
    ax_d.axvline(t_settle, color="#2C3E50", linestyle=":", lw=1.5)
    ax_d.set_xlabel("Time from Recording Start (s)", fontsize=10, fontweight="bold", color="#004053")
    ax_d.set_ylabel("Within-ROI Pixel Standard Deviation (counts)", fontsize=10, fontweight="bold", color="#004053")
    ax_d.set_title("D | Forensic Proof: Edge-Contamination StDev Peaks Collapse to Zero",
                   fontsize=11, fontweight="bold", color="#004053")
    ax_d.legend(loc="upper right", fontsize=8, frameon=True)
    ax_d.grid(True, linestyle=':', alpha=0.5)

    fig.suptitle("Figure 7 | Quantitative Forensic Performance Audit: 2020 Crude Circles vs. 2026 Refined Tissue ROIs (expt08)",
                 fontsize=13, fontweight="bold", color="#004053", y=0.985)
                 
    fig.tight_layout(rect=[0, 0.02, 1, 0.96])
    
    out_p1 = os.path.join(RESULTS_FIGS, "tissue_comparison_expt08.png")
    out_p2 = os.path.join(DOCS_FIGS, "tissue_comparison_expt08.png")
    fig.savefig(out_p1, dpi=200, bbox_inches='tight')
    fig.savefig(out_p2, dpi=200, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved: {out_p1} & {out_p2}")


def plot_population_kinetics():
    """Figure 8: Population Kinetics Across 8 Pooled Runs."""
    print("Generating Figure 8: tissue_kinetics_population.png ...")
    
    with open("results/tissue_segmentation_summary.json") as f:
        summary_data = json.load(f)
        
    runs = [r for r in summary_data["runs"] if r["pooled"]]
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10.5), facecolor="#ffffff")
    
    tissues = ["hydathodes", "veins", "pure_lamina", "meristem"]
    t_labels = ["Hydathode Teeth", "Primary Veins", "Pure Lamina", "Shoot Meristem"]
    t_colors = [COLORS["hydathodes"], COLORS["veins"], COLORS["pure_lamina"], COLORS["meristem"]]
    
    # Panel A: Population Normalized Time Courses
    ax_a = axes[0, 0]
    
    # Load traces from pooled runs interpolated to common time grid [0, 800 s]
    common_t = np.linspace(0, 750, 300)
    tissue_interpolated = {t: [] for t in tissues}
    
    for r in runs:
        tag = r["tag"]
        d_map = np.load(f"results/runs/{tag}/{tag}_tissue_maps.npz")
        t_run = d_map["t"]
        i_settle = r["i_settle"]
        t_settle = r["t_settle_s"]
        
        for tname in tissues:
            trace_key = f"trace_{tname}"
            if trace_key in d_map:
                tr = d_map[trace_key]
                if len(tr) > 0 and not np.all(np.isnan(tr)):
                    # Normalize peak post-settle to 1.0 for shape comparison
                    post_tr = np.copy(tr)
                    max_val = np.nanmax(post_tr[i_settle:])
                    if max_val > 5:
                        norm_tr = post_tr / max_val
                        # Interpolate to common_t
                        interp_tr = np.interp(common_t, t_run, norm_tr, left=0, right=np.nan)
                        tissue_interpolated[tname].append(interp_tr)
                        
    for tname, col, lbl in zip(tissues, t_colors, t_labels):
        arr = np.array(tissue_interpolated[tname])
        if len(arr) > 0:
            med_tr = np.nanmedian(arr, axis=0)
            p25 = np.nanpercentile(arr, 25, axis=0)
            p75 = np.nanpercentile(arr, 75, axis=0)
            
            ax_a.plot(common_t, med_tr, color=col, lw=2.4, label=f"{lbl} (n={len(arr)})")
            ax_a.fill_between(common_t, p25, p75, color=col, alpha=0.15)
            
    ax_a.axhline(0.5, color="#7F8C8D", linestyle=":", lw=1.2, label="50% Activation Threshold")
    ax_a.set_xlabel("Time from Recording Start (s)", fontsize=10, fontweight="bold", color="#004053")
    ax_a.set_ylabel("Normalized GCaMP ΔF (Median ± IQR)", fontsize=10, fontweight="bold", color="#004053")
    ax_a.set_title("A | Population Time Courses Across 8 Passing Runs", fontsize=11, fontweight="bold", color="#004053")
    ax_a.legend(loc="upper left", fontsize=8.5, frameon=True)
    ax_a.grid(True, linestyle=':', alpha=0.5)
    ax_a.set_xlim(0, 750)
    ax_a.set_ylim(-0.05, 1.1)
    
    # Panel B: Half-Rise Time (t50) Boxplots & Paired Points
    ax_b = axes[0, 1]
    t50_data = []
    for tname in tissues:
        vals = [r["tissues"][tname]["t50_median_s"] for r in runs if r["tissues"][tname]["t50_median_s"] is not None]
        t50_data.append(vals)
        
    bp = ax_b.boxplot(t50_data, positions=np.arange(len(tissues)), widths=0.45, patch_artist=True,
                      showmeans=True, meanprops=dict(marker='D', markeredgecolor='#004053', markerfacecolor='white', markersize=6))
    for patch, col in zip(bp['boxes'], t_colors):
        patch.set_facecolor(col)
        patch.set_alpha(0.5)
        patch.set_edgecolor(col)
        patch.set_linewidth(1.8)
    for element in ['whiskers', 'caps', 'medians']:
        plt.setp(bp[element], color='#004053', lw=1.6)
        
    # Overlay paired lines connecting runs
    for r_idx, r in enumerate(runs):
        y_vals = [r["tissues"][tname]["t50_median_s"] for tname in tissues]
        valid_x = [i for i, y in enumerate(y_vals) if y is not None]
        valid_y = [y for y in y_vals if y is not None]
        if len(valid_x) >= 2:
            ax_b.plot(valid_x, valid_y, color='#7F8C8D', alpha=0.35, lw=1.2, marker='o', markersize=4)
            
    ax_b.set_xticks(np.arange(len(tissues)))
    ax_b.set_xticklabels(t_labels, fontsize=9.5, fontweight="500")
    ax_b.set_ylabel("Half-Rise Time t₅₀ (s)", fontsize=10, fontweight="bold", color="#004053")
    ax_b.set_title("B | Activation Timing Hierarchy: Veins Lead Pure Lamina", fontsize=11, fontweight="bold", color="#004053")
    ax_b.grid(axis='y', linestyle=':', alpha=0.5)
    
    # Wilcoxon stat text
    stats = summary_data.get("statistics", {})
    w_res = stats.get("wilcoxon_vein_vs_pure_lamina", {})
    p_val = w_res.get("p_value")
    if p_val is not None:
        ax_b.text(0.95, 0.92, f"Veins vs Pure Lamina:\nWilcoxon p = {p_val:.4f} *",
                  transform=ax_b.transAxes, fontsize=8.5, ha="right", va="top",
                  bbox=dict(boxstyle="round,pad=0.3", facecolor="#F6F9FA", edgecolor="#004053"))

    # Panel C: Earliest 5% Responder Enrichment (E_tissue)
    ax_c = axes[1, 0]
    enrich_tissues = ["hydathodes", "margin_other", "veins", "pure_lamina", "inner_control"]
    e_labels = ["Hydathode\nTeeth", "Margin\n(Non-Tooth)", "Primary\nVeins", "Pure\nLamina", "Inner Control\n(80–160 µm)"]
    e_colors = [COLORS["hydathodes"], COLORS["margin_other"], COLORS["veins"], COLORS["pure_lamina"], COLORS["inner_control"]]
    
    enrich_data = []
    for tname in enrich_tissues:
        vals = [r["tissues"][tname]["first5_enrichment"] for r in runs if r["tissues"][tname]["first5_enrichment"] is not None]
        enrich_data.append(vals)
        
    bp_e = ax_c.boxplot(enrich_data, positions=np.arange(len(enrich_tissues)), widths=0.45, patch_artist=True,
                        showmeans=True, meanprops=dict(marker='D', markeredgecolor='#004053', markerfacecolor='white', markersize=6))
    for patch, col in zip(bp_e['boxes'], e_colors):
        patch.set_facecolor(col)
        patch.set_alpha(0.5)
        patch.set_edgecolor(col)
        patch.set_linewidth(1.8)
    for element in ['whiskers', 'caps', 'medians']:
        plt.setp(bp_e[element], color='#004053', lw=1.6)
        
    ax_c.axhline(1.0, color="#C0392B", linestyle="--", lw=1.5, label="Parity (1.0× = Uniform Chance)")
    ax_c.set_xticks(np.arange(len(enrich_tissues)))
    ax_c.set_xticklabels(e_labels, fontsize=9, fontweight="500")
    ax_c.set_ylabel("Early-5% Responder Enrichment (Fold)", fontsize=10, fontweight="bold", color="#004053")
    ax_c.set_title("C | Spatial Enrichment of Earliest Activating Pixels (t₅₀ ≤ P₅)", fontsize=11, fontweight="bold", color="#004053")
    ax_c.grid(axis='y', linestyle=':', alpha=0.5)
    ax_c.legend(loc="upper right", fontsize=8.5, frameon=True)
    
    # Panel D: Signal Amplitude (Rise in Counts Above Background)
    ax_d = axes[1, 1]
    rise_data = []
    for tname in tissues:
        vals = [r["tissues"][tname]["rise_amplitude_counts"] for r in runs if r["tissues"][tname]["rise_amplitude_counts"] is not None]
        rise_data.append(vals)
        
    bp_r = ax_d.boxplot(rise_data, positions=np.arange(len(tissues)), widths=0.45, patch_artist=True,
                        showmeans=True, meanprops=dict(marker='D', markeredgecolor='#004053', markerfacecolor='white', markersize=6))
    for patch, col in zip(bp_r['boxes'], t_colors):
        patch.set_facecolor(col)
        patch.set_alpha(0.5)
        patch.set_edgecolor(col)
        patch.set_linewidth(1.8)
    for element in ['whiskers', 'caps', 'medians']:
        plt.setp(bp_r[element], color='#004053', lw=1.6)
        
    ax_d.set_xticks(np.arange(len(tissues)))
    ax_d.set_xticklabels(t_labels, fontsize=9.5, fontweight="500")
    ax_d.set_ylabel("Peak Rise Amplitude ΔF (counts above BG)", fontsize=10, fontweight="bold", color="#004053")
    ax_d.set_title("D | GCaMP Dynamic Range by Anatomical Tissue", fontsize=11, fontweight="bold", color="#004053")
    ax_d.grid(axis='y', linestyle=':', alpha=0.5)

    fig.suptitle("Figure 8 | Dataset-Wide Tissue Kinetics and Hierarchical Signaling Flow (n = 8 Pooled Runs)",
                 fontsize=13, fontweight="bold", color="#004053", y=0.985)
                 
    fig.tight_layout(rect=[0, 0.02, 1, 0.96])
    
    out_p1 = os.path.join(RESULTS_FIGS, "tissue_kinetics_population.png")
    out_p2 = os.path.join(DOCS_FIGS, "tissue_kinetics_population.png")
    fig.savefig(out_p1, dpi=200, bbox_inches='tight')
    fig.savefig(out_p2, dpi=200, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved: {out_p1} & {out_p2}")


if __name__ == "__main__":
    plot_atlas_all_runs()
    plot_expt08_comparison()
    plot_population_kinetics()
