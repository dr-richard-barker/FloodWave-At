#!/usr/bin/env python3
"""
Scientific Publication Visualizations for SLEAP Plant Pose Estimation & Kinematics:
  1. Figure 9: Botanical Pose Skeleton & Vascular Graph Geodesic Conduction (sleap_skeleton_and_graph.png)
  2. Figure 10: Flooding-Induced Biomechanical Kinematics & Hydraulic Strain (sleap_kinematics_and_strain.png)

Saves figures to results/figures/ and docs/assets/figures/.
"""

import os, sys, json, math
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

# CoSE & Botanical Colors
COLORS = {
    "meristem": "#8E44AD",       # Royal Purple
    "petiole": "#2980B9",        # Blue
    "midrib": "#00A86B",         # Jade Green
    "hydathode_apex": "#E67E22", # Dark Amber
    "hydathode_tooth": "#F39C12",# Bright Gold
    "edge": "#2C3E50",           # Charcoal
    "water_window": "#3FA9C7",   # CoSE Sky Blue
    "cose_navy": "#004053",
    "cose_teal": "#0F7F9F",
    "cose_light": "#F6F9FA"
}


def plot_figure9():
    """Figure 9: Botanical Pose Skeleton & Vascular Graph Geodesic Conduction."""
    print("Generating Figure 9: sleap_skeleton_and_graph.png ...")
    
    npz_data = np.load("results/sleap/expt08_pose_trajectories.npz")
    ref = npz_data["ref"]
    mask = npz_data["mask"]
    t50 = npz_data["t50"]
    node_names = [str(n) for n in npz_data["node_names"]]
    node_coords = npz_data["node_coords"]
    node_types = [str(t) for t in npz_data["node_types"]]
    edges = npz_data["edges"]
    
    with open("results/sleap/pose_kinematics_summary.json") as f:
        summary = json.load(f)
    nodes_info = {n["name"]: n for n in summary["nodes"]}
    cond_stats = summary["conduction_statistics"]
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 11), facecolor="#ffffff")
    
    # Panel A: Rosette Overlaid with SLEAP Pose Skeleton Graph
    ax_a = axes[0, 0]
    lo, hi = np.percentile(ref, [2, 99.5])
    ax_a.imshow(ref, cmap="gray", vmin=lo, vmax=hi, aspect='equal')
    ax_a.contour(mask, levels=[0.5], colors=['#BDC3C7'], linewidths=[1.0], alpha=0.7)
    
    # Draw edges
    name_to_coord = {name: coord for name, coord in zip(node_names, node_coords)}
    for src, dst in edges:
        p1 = name_to_coord[src]
        p2 = name_to_coord[dst]
        ax_a.plot([p1[0], p2[0]], [p1[1], p2[1]], color="#004053", lw=2.2, zorder=3, alpha=0.85)
        ax_a.plot([p1[0], p2[0]], [p1[1], p2[1]], color="#3FA9C7", lw=1.2, zorder=4)

    # Draw nodes by type
    type_markers = {
        "SAM_meristem": ("*", COLORS["meristem"], 14, "Meristem (SAM Base)"),
        "petiole_conduit": ("s", COLORS["petiole"], 7, "Petiole Conduit Node"),
        "vascular_midrib": ("D", COLORS["midrib"], 7, "Vascular Midrib Node"),
        "hydathode_apex": ("o", COLORS["hydathode_apex"], 8, "Distal Hydathode Apex"),
        "hydathode_tooth": ("o", COLORS["hydathode_tooth"], 6, "Marginal Tooth Hydathode")
    }
    
    plotted_types = set()
    for name, coord, ntype in zip(node_names, node_coords, node_types):
        m, c, sz, lbl = type_markers.get(ntype, ("o", "white", 6, ntype))
        label_to_use = lbl if ntype not in plotted_types else None
        plotted_types.add(ntype)
        ax_a.plot(coord[0], coord[1], marker=m, color=c, markersize=sz,
                  markeredgecolor="white", markeredgewidth=1.0, zorder=5, label=label_to_use)
                  
    # Scale bar (2 mm)
    scale_px = 2000 / PX_UM
    ax_a.plot([15, 15 + scale_px], [ref.shape[0] - 15, ref.shape[0] - 15], color="white", lw=2.5)
    ax_a.text(15, ref.shape[0] - 20, "2 mm", color="white", fontsize=8.5, fontweight="bold")
    
    ax_a.set_title("A | SLEAP Articulated Plant Rosette Pose Skeleton", fontsize=11, fontweight="bold", color="#004053")
    ax_a.set_xticks([]); ax_a.set_yticks([])
    ax_a.legend(loc="upper left", fontsize=7.5, frameon=True, facecolor="#F6F9FA", edgecolor="#004053")

    # Panel B: Vascular Geodesic Path Distance Map (d_graph)
    ax_b = axes[0, 1]
    # Reconstruct 2D geodesic distance grid from meristem
    cy_m = int(round(node_coords[0, 1]))
    cx_m = int(round(node_coords[0, 0]))
    pts = np.argwhere(mask)
    idx_map = np.full(mask.shape, -1, int)
    for i, (y, x) in enumerate(pts):
        idx_map[y, x] = i
    from scipy.sparse import csr_matrix
    from scipy.sparse.csgraph import dijkstra
    N = len(pts)
    rows, cols, data = [], [], []
    for i, (y, x) in enumerate(pts):
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dy == 0 and dx == 0: continue
                ny, nx = y + dy, x + dx
                if 0 <= ny < mask.shape[0] and 0 <= nx < mask.shape[1]:
                    j = idx_map[ny, nx]
                    if j >= 0:
                        rows.append(i); cols.append(j); data.append(math.hypot(dy, dx))
    graph = csr_matrix((data, (rows, cols)), shape=(N, N))
    meri_idx = idx_map[cy_m, cx_m]
    dists = dijkstra(graph, indices=[meri_idx])[0]
    
    geo_grid = np.full(mask.shape, np.nan)
    for (y, x), d in zip(pts, dists):
        geo_grid[y, x] = d * PX_UM / 1000.0 # mm
        
    im_b = ax_b.imshow(geo_grid, cmap="viridis", aspect='equal')
    cb_b = plt.colorbar(im_b, ax=ax_b, fraction=0.046, pad=0.04)
    cb_b.set_label("Vascular Geodesic Distance d_graph (mm)", fontsize=9, fontweight="bold", color="#004053")
    
    # Overplot skeleton paths
    for src, dst in edges:
        p1 = name_to_coord[src]; p2 = name_to_coord[dst]
        ax_b.plot([p1[0], p2[0]], [p1[1], p2[1]], color="white", lw=1.2, zorder=3, alpha=0.8)
        
    ax_b.plot(cx_m, cy_m, marker="*", color="#E74C3C", markersize=12, markeredgecolor="white", zorder=4)
    ax_b.set_title("B | Topological Geodesic Distance from Meristem Base", fontsize=11, fontweight="bold", color="#004053")
    ax_b.set_xticks([]); ax_b.set_yticks([])

    # Panel C: Geodesic vs Euclidean Distance Correlation with Activation Latency (t50)
    ax_c = axes[1, 0]
    valid_nodes = [n for n in summary["nodes"] if n["t50_s"] is not None and n["d_geo_um"] > 200]
    d_geo_mm = np.array([n["d_geo_um"] / 1000.0 for n in valid_nodes])
    d_euc_mm = np.array([n["d_euclid_um"] / 1000.0 for n in valid_nodes])
    t50_s = np.array([n["t50_s"] for n in valid_nodes])
    
    ax_c.scatter(d_euc_mm, t50_s, color="#E74C3C", marker="^", s=50, alpha=0.75,
                 label=f"Euclidean Distance (R² = {cond_stats['r_squared_euclid']:.3f})")
    ax_c.scatter(d_geo_mm, t50_s, color="#2980B9", marker="o", s=65, edgecolors="#004053", lw=1.2,
                 label=f"Vascular Geodesic Path (R² = {cond_stats['r_squared_geodesic']:.3f})")
                 
    # Fit regression line for geodesic
    if len(d_geo_mm) >= 4:
        p_fit = np.poly1d(np.polyfit(d_geo_mm, t50_s, 1))
        x_line = np.linspace(d_geo_mm.min(), d_geo_mm.max(), 50)
        ax_c.plot(x_line, p_fit(x_line), color="#004053", linestyle="--", lw=1.8,
                  label=f"Linear Conduction Fit (v = {cond_stats['vascular_conduction_velocity_um_s']:.1f} µm/s)")
                  
    ax_c.set_xlabel("Distance from Meristem Base (mm)", fontsize=10, fontweight="bold", color="#004053")
    ax_c.set_ylabel("Activation Half-Rise Time t₅₀ (s)", fontsize=10, fontweight="bold", color="#004053")
    ax_c.set_title("C | Conduction Latency: Topological Geodesics Outperform Euclidean Proximity",
                   fontsize=11, fontweight="bold", color="#004053")
    ax_c.legend(loc="upper left", fontsize=8.5, frameon=True)
    ax_c.grid(True, linestyle=":", alpha=0.5)

    # Panel D: Vascular Conduction Velocity and Tortuosity
    ax_d = axes[1, 1]
    tortuosity = [n["tortuosity"] for n in valid_nodes]
    leaf_groups = [n["name"].split("_")[0] for n in valid_nodes]
    
    # Grouped scatter of tortuosity by leaf
    unique_leaves = sorted(list(set(leaf_groups)))
    x_positions = {l: i for i, l in enumerate(unique_leaves)}
    
    for l_name in unique_leaves:
        pts_leaf = [n for n in valid_nodes if n["name"].startswith(l_name)]
        x_vals = [x_positions[l_name] + np.random.uniform(-0.12, 0.12) for _ in pts_leaf]
        y_vals = [n["tortuosity"] for n in pts_leaf]
        ax_d.scatter(x_vals, y_vals, s=70, color=COLORS["midrib"], alpha=0.8, edgecolors="#004053")
        
    ax_d.axhline(1.0, color="#C0392B", linestyle=":", lw=1.5, label="Direct Straight Line (1.0×)")
    ax_d.set_xticks([x_positions[l] for l in unique_leaves])
    ax_d.set_xticklabels([f"Leaf {l.replace('Leaf_', '')}" for l in unique_leaves], fontsize=9.5, fontweight="500")
    ax_d.set_ylabel("Vascular Tortuosity Index (d_graph / d_euclid)", fontsize=10, fontweight="bold", color="#004053")
    ax_d.set_title("D | Vascular Tortuosity Index: Anatomical Routing to Leaf Teeth",
                   fontsize=11, fontweight="bold", color="#004053")
    ax_d.grid(axis='y', linestyle=':', alpha=0.5)
    ax_d.legend(loc="upper left", fontsize=8.5, frameon=True)
    
    # Inset annotation
    ax_d.text(0.97, 0.95, f"Mean Tortuosity: {cond_stats['mean_tortuosity']:.2f}×\nMax Routing Delay: {cond_stats['max_tortuosity']:.2f}×\nVascular Velocity: {cond_stats['vascular_conduction_velocity_um_s']:.1f} µm/s",
              transform=ax_d.transAxes, fontsize=8.5, ha="right", va="top",
              bbox=dict(boxstyle="round,pad=0.3", facecolor="#F6F9FA", edgecolor="#004053"))

    fig.suptitle("Figure 9 | SLEAP Botanical Pose Estimation: Resolving Vascular Geodesic Conduction in Arabidopsis",
                 fontsize=13, fontweight="bold", color="#004053", y=0.985)
    fig.tight_layout(rect=[0, 0.02, 1, 0.96])
    
    out_p1 = os.path.join(RESULTS_FIGS, "sleap_skeleton_and_graph.png")
    out_p2 = os.path.join(DOCS_FIGS, "sleap_skeleton_and_graph.png")
    fig.savefig(out_p1, dpi=200, bbox_inches='tight')
    fig.savefig(out_p2, dpi=200, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved: {out_p1} & {out_p2}")


def plot_figure10():
    """Figure 10: Flooding-Induced Biomechanical Kinematics & Hydraulic Strain."""
    print("Generating Figure 10: sleap_kinematics_and_strain.png ...")
    
    npz_data = np.load("results/sleap/expt08_pose_trajectories.npz")
    trajectories = npz_data["trajectories"] # (700, N, 2)
    t = npz_data["t"]
    i_settle = int(npz_data["i_settle"])
    t_settle = float(t[i_settle])
    ref = npz_data["ref"]
    mask = npz_data["mask"]
    
    with open("results/sleap/pose_kinematics_summary.json") as f:
        summary = json.load(f)
    leaf_kin = summary["leaf_kinematics"]
    fluo_comp = summary["fluorescence_noise_comparison"]
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10.5), facecolor="#ffffff")
    
    # Panel A: Landmark Displacement Vectors (Quiver Plot on Image)
    ax_a = axes[0, 0]
    lo, hi = np.percentile(ref, [2, 99.5])
    ax_a.imshow(ref, cmap="gray", vmin=lo, vmax=hi, aspect='equal')
    ax_a.contour(mask, levels=[0.5], colors=['#7F8C8D'], linewidths=[0.8], alpha=0.6)
    
    # Initial vs Water Peak Displacement (at frame 30 ~ 36.4 s)
    f_peak = 30
    x0 = trajectories[0, :, 0]
    y0 = trajectories[0, :, 1]
    dx = (trajectories[f_peak, :, 0] - x0) * 8.0 # scale up for visibility
    dy = (trajectories[f_peak, :, 1] - y0) * 8.0
    
    ax_a.scatter(x0, y0, color="#E74C3C", s=30, zorder=3, label="Resting Position (0 s)")
    ax_a.quiver(x0, y0, dx, dy, color="#3FA9C7", angles='xy', scale_units='xy', scale=1,
                width=0.007, headwidth=4, headlength=5, zorder=4, label="Meniscus Displacement Vector (8× scaled)")
                
    ax_a.set_title("A | Landmark Displacement Field During Meniscus Influx Surge (36.4 s)",
                   fontsize=11, fontweight="bold", color="#004053")
    ax_a.set_xticks([]); ax_a.set_yticks([])
    ax_a.legend(loc="upper left", fontsize=8, frameon=True)

    # Panel B: Hydraulic Elongation Strain Time Series ε(t)
    ax_b = axes[0, 1]
    # Highlight water addition window: 14.6 to 48.5 s
    ax_b.axvspan(14.6, 48.5, color="#3FA9C7", alpha=0.20, label="Water Influx Window (14.6–48.5 s)")
    ax_b.axvline(36.4, color="#C0392B", linestyle=":", lw=1.5, label="Surge Peak (36.4 s)")
    ax_b.axvline(t_settle, color="#004053", linestyle="--", lw=1.5, label=f"Motion Settle ({t_settle:.1f} s)")
    
    leaf_palette = {
        "Leaf_L": "#2980B9",
        "Leaf_UL": "#27AE60",
        "Leaf_UR": "#E67E22",
        "Leaf_R": "#8E44AD",
        "Leaf_B": "#16A085"
    }
    
    for leaf_name, ldata in leaf_kin.items():
        col = leaf_palette.get(leaf_name, "#2C3E50")
        ax_b.plot(t, ldata["strain_pct"], color=col, lw=1.8, label=f"{leaf_name.replace('Leaf_', 'Leaf ')} (L₀={ldata['initial_length_um']:.0f} µm)")
        
    ax_b.axhline(0, color="#7F8C8D", linestyle="--", lw=1.0)
    ax_b.set_xlabel("Time from Recording Start (s)", fontsize=10, fontweight="bold", color="#004053")
    ax_b.set_ylabel("Branch Elongation Strain ε(t) (%)", fontsize=10, fontweight="bold", color="#004053")
    ax_b.set_title("B | Transient Hydraulic Strain: Mechanical Leaf Distension During Flood Influx",
                   fontsize=11, fontweight="bold", color="#004053")
    ax_b.set_xlim(0, 300)
    ax_b.legend(loc="upper right", fontsize=7.5, frameon=True)
    ax_b.grid(True, linestyle=":", alpha=0.5)

    # Panel C: Leaf Angular Deflection Time Series Δθ(t)
    ax_c = axes[1, 0]
    ax_c.axvspan(14.6, 48.5, color="#3FA9C7", alpha=0.20)
    ax_c.axvline(36.4, color="#C0392B", linestyle=":", lw=1.5)
    ax_c.axvline(t_settle, color="#004053", linestyle="--", lw=1.5)
    
    for leaf_name, ldata in leaf_kin.items():
        col = leaf_palette.get(leaf_name, "#2C3E50")
        ax_c.plot(t, ldata["deflection_deg"], color=col, lw=1.8, label=leaf_name.replace('Leaf_', 'Leaf '))
        
    ax_c.axhline(0, color="#7F8C8D", linestyle="--", lw=1.0)
    ax_c.set_xlabel("Time from Recording Start (s)", fontsize=10, fontweight="bold", color="#004053")
    ax_c.set_ylabel("Angular Deflection Δθ(t) (degrees)", fontsize=10, fontweight="bold", color="#004053")
    ax_c.set_title("C | Non-Rigid Leaf Kinematics: Buoyant Tilting & Hyponasty",
                   fontsize=11, fontweight="bold", color="#004053")
    ax_c.set_xlim(0, 300)
    ax_c.legend(loc="upper right", fontsize=8, frameon=True)
    ax_c.grid(True, linestyle=":", alpha=0.5)

    # Panel D: Motion-Compensated vs Static GCaMP Sampling
    ax_d = axes[1, 1]
    # Show comparison on Leaf_L_apex and Leaf_UR_apex
    # Load traces from summary if available
    noise_reductions = [v["noise_reduction_pct"] for v in fluo_comp.values()]
    mean_noise_red = np.mean(noise_reductions)
    
    # Plot histogram / bar of noise reduction across landmarks
    sample_nodes = ["Leaf_L_apex", "Leaf_UL_apex", "Leaf_UR_apex", "Leaf_R_apex", "meristem"]
    sample_nodes = [n for n in sample_nodes if n in fluo_comp]
    
    stat_noises = [fluo_comp[n]["noise_static"] for n in sample_nodes]
    dyn_noises = [fluo_comp[n]["noise_dynamic"] for n in sample_nodes]
    
    y_pos = np.arange(len(sample_nodes))
    b_h = 0.35
    ax_d.barh(y_pos - b_h/2, stat_noises, height=b_h, color="#E74C3C", label="Static Circular Sampling (No Tracking)")
    ax_d.barh(y_pos + b_h/2, dyn_noises, height=b_h, color="#27AE60", label="SLEAP Motion-Compensated Sampling")
    
    ax_d.set_yticks(y_pos)
    ax_d.set_yticklabels([s.replace('_', ' ') for s in sample_nodes], fontsize=9)
    ax_d.set_xlabel("Baseline Temporal Noise (counts)", fontsize=10, fontweight="bold", color="#004053")
    ax_d.set_title(f"D | Physiological Signal Fidelity: {mean_noise_red:.1f}% Mean Motion Jitter Reduction",
                   fontsize=11, fontweight="bold", color="#004053")
    ax_d.legend(loc="lower right", fontsize=8.5, frameon=True)
    ax_d.grid(axis='x', linestyle=":", alpha=0.5)

    fig.suptitle("Figure 10 | SLEAP Biomechanical Kinematics: Hydraulic Strain, Angular Tilting, and Motion Compensation",
                 fontsize=13, fontweight="bold", color="#004053", y=0.985)
    fig.tight_layout(rect=[0, 0.02, 1, 0.96])
    
    out_p1 = os.path.join(RESULTS_FIGS, "sleap_kinematics_and_strain.png")
    out_p2 = os.path.join(DOCS_FIGS, "sleap_kinematics_and_strain.png")
    fig.savefig(out_p1, dpi=200, bbox_inches='tight')
    fig.savefig(out_p2, dpi=200, bbox_inches='tight')
    plt.close(fig)
    print(f"Saved: {out_p1} & {out_p2}")


if __name__ == "__main__":
    plot_figure9()
    plot_figure10()
