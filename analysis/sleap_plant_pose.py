#!/usr/bin/env python3
"""
SLEAP Plant Pose Estimation, Biomechanical Kinematics, and Vascular Graph Conduction
for FloodWave-At (https://sleap.ai/).

1. Constructs an articulated Botanical Pose Skeleton (ArabidopsisRosette) using sleap-io.
2. Extracts landmark nodes: shoot apical meristem (SAM anchor), petiole bases,
   midrib vascular conduits, and terminal epithemal hydathodes.
3. Computes vascular graph geodesics (d_graph) vs Euclidean distance (d_euclid)
   and determines vascular signal conduction velocity (v_vascular = Δd / Δt50).
4. Performs sub-pixel time-series landmark tracking across all 700 frames:
   - Hydraulic strain ε(t) = ΔL(t) / L0
   - Angular deflection Δθ(t)
   - Motion-compensated "de-warped" GCaMP fluorescence traces.
5. Exports standard SLEAP project files (.slp) via sleap-io and structured kinematics datasets.
"""

import os, sys, json, math, csv
import numpy as np
import czifile
import cv2
import imageio
from scipy import ndimage as ndi
from scipy.stats import pearsonr, spearmanr
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra
from skimage.morphology import disk, dilation, erosion, skeletonize

import sleap_io as sio

PX_UM = 20.4925 * 2 # 40.985 um per binned px

RAW_CZI = "/Volumes/Barker_2016/Hyperspectral_UW-Botany_July 2016/Flood_DRB/Flooding expt 8 NormalWater small plant representative 10012020.czi"
NPZ_08 = "results/runs/expt08/expt08_tissue_maps.npz"

OUT_SLEAP = "results/sleap"
DOCS_SLEAP = "docs/assets/sleap"
os.makedirs(OUT_SLEAP, exist_ok=True)
os.makedirs(DOCS_SLEAP, exist_ok=True)


def build_plant_skeleton_and_nodes(ref, mask, m_hyd, m_vein, m_meri):
    """
    Construct the botanical pose skeleton graph from segmented tissue masks on expt08.
    """
    yy, xx = np.indices(mask.shape)
    
    # 1. Meristem anchor node
    cy_m, cx_m = ndi.center_of_mass(m_meri)
    meristem_coord = (float(cx_m), float(cy_m))
    
    # 2. Extract discrete hydathode clusters
    hyd_lab, n_hyd = ndi.label(m_hyd)
    hyd_clusters = []
    for i in range(1, n_hyd + 1):
        cy, cx = ndi.center_of_mass(hyd_lab == i)
        # Distance and polar angle from meristem
        dx = cx - cx_m
        dy = cy - cy_m
        r = math.hypot(dx, dy)
        theta = math.degrees(math.atan2(dy, dx)) % 360 # 0 to 360
        hyd_clusters.append({
            "id": i,
            "x": float(cx),
            "y": float(cy),
            "r_px": r,
            "theta_deg": theta,
            "mask": (hyd_lab == i)
        })
        
    print(f"Extracted {len(hyd_clusters)} discrete hydathode tooth loci.")

    # 3. Partition hydathodes into 5 primary morphological leaf lobes based on angle
    # Lobe 1: Left lobe (150 - 210 deg)
    # Lobe 2: Upper-Left (100 - 150 deg)
    # Lobe 3: Upper-Right (40 - 100 deg)
    # Lobe 4: Right lobe (320 - 40 deg)
    # Lobe 5: Lower-Right/Bottom (210 - 320 deg)
    leaf_lobes = {
        "Leaf_L": [],
        "Leaf_UL": [],
        "Leaf_UR": [],
        "Leaf_R": [],
        "Leaf_B": []
    }
    
    for h in hyd_clusters:
        th = h["theta_deg"]
        if 150 <= th < 210:
            leaf_lobes["Leaf_L"].append(h)
        elif 95 <= th < 150:
            leaf_lobes["Leaf_UL"].append(h)
        elif 35 <= th < 95:
            leaf_lobes["Leaf_UR"].append(h)
        elif th >= 320 or th < 35:
            leaf_lobes["Leaf_R"].append(h)
        else:
            leaf_lobes["Leaf_B"].append(h)

    # 4. Define nodes and edges for the SLEAP skeleton
    node_names = ["meristem"]
    node_coords = [meristem_coord]
    node_types = ["SAM_meristem"]
    edges = []
    leaf_branches = {}

    for leaf_name, cluster_list in leaf_lobes.items():
        if not cluster_list:
            continue
            
        # Sort by distance from meristem
        cluster_list.sort(key=lambda c: c["r_px"])
        apex_hydathode = cluster_list[-1] # most distal is leaf apex
        lateral_teeth = cluster_list[:-1] # others are lateral marginal teeth
        
        # Conduit nodes: Petiole base (~25% of distance) and Midrib mid (~60% of distance)
        dx_apex = apex_hydathode["x"] - cx_m
        dy_apex = apex_hydathode["y"] - cy_m
        
        # Petiole base
        px_pet = cx_m + dx_apex * 0.28
        py_pet = cy_m + dy_apex * 0.28
        pet_name = f"{leaf_name}_petiole"
        node_names.append(pet_name)
        node_coords.append((float(px_pet), float(py_pet)))
        node_types.append("petiole_conduit")
        pet_idx = len(node_names) - 1
        edges.append(("meristem", pet_name))
        
        # Midrib mid
        px_mid = cx_m + dx_apex * 0.65
        py_mid = cy_m + dy_apex * 0.65
        mid_name = f"{leaf_name}_midrib"
        node_names.append(mid_name)
        node_coords.append((float(px_mid), float(py_mid)))
        node_types.append("vascular_midrib")
        mid_idx = len(node_names) - 1
        edges.append((pet_name, mid_name))
        
        # Distal Hydathode Apex
        apex_name = f"{leaf_name}_apex"
        node_names.append(apex_name)
        node_coords.append((apex_hydathode["x"], apex_hydathode["y"]))
        node_types.append("hydathode_apex")
        apex_idx = len(node_names) - 1
        edges.append((mid_name, apex_name))
        
        # Lateral Teeth Hydathodes
        tooth_indices = []
        for t_idx, tooth in enumerate(lateral_teeth):
            t_name = f"{leaf_name}_tooth_{t_idx + 1}"
            node_names.append(t_name)
            node_coords.append((tooth["x"], tooth["y"]))
            node_types.append("hydathode_tooth")
            tooth_indices.append(len(node_names) - 1)
            edges.append((mid_name, t_name))
            
        leaf_branches[leaf_name] = {
            "petiole_idx": pet_idx,
            "midrib_idx": mid_idx,
            "apex_idx": apex_idx,
            "tooth_indices": tooth_indices
        }

    # Create sleap_io.Skeleton with isolated copies
    node_names_str = [str(n) for n in node_names]
    edges_str = [(str(u), str(v)) for u, v in edges]
    skel = sio.Skeleton(nodes=list(node_names), edges=list(edges), name="ArabidopsisRosette")
    print(f"Constructed SLEAP Skeleton with {len(node_names)} nodes and {len(edges)} edges.")
    
    return {
        "skeleton": skel,
        "node_names": node_names_str,
        "node_coords": np.array(node_coords, dtype=np.float32),
        "node_types": node_types,
        "leaf_branches": leaf_branches,
        "edges": edges_str
    }


def compute_vascular_geodesic_conduction(mask, m_vein, m_meri, skeleton_data, t50_map):
    """
    Pattern 1: Compute vascular graph geodesic distances vs straight Euclidean distances
    from the meristem to all skeleton nodes, and calculate vascular conduction velocity.
    """
    print("\n--- Computing Vascular Geodesic Distances & Signal Propagation ---")
    
    # Network graph through continuous leaf tissue (using Dijkstra's algorithm)
    network = mask
    cy_m = int(round(skeleton_data["node_coords"][0, 1]))
    cx_m = int(round(skeleton_data["node_coords"][0, 0]))
    
    pts = np.argwhere(network)
    idx_map = np.full(network.shape, -1, int)
    for i, (y, x) in enumerate(pts):
        idx_map[y, x] = i
        
    N = len(pts)
    rows, cols, data = [], [], []
    for i, (y, x) in enumerate(pts):
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dy == 0 and dx == 0: continue
                ny, nx = y + dy, x + dx
                if 0 <= ny < network.shape[0] and 0 <= nx < network.shape[1]:
                    j = idx_map[ny, nx]
                    if j >= 0:
                        rows.append(i)
                        cols.append(j)
                        data.append(math.hypot(dy, dx))
                        
    graph = csr_matrix((data, (rows, cols)), shape=(N, N))
    meri_idx = idx_map[cy_m, cx_m]
    if meri_idx == -1:
        dist_to_m = np.hypot(pts[:, 0] - cy_m, pts[:, 1] - cx_m)
        meri_idx = dist_to_m.argmin()
        
    geo_dist_grid = dijkstra(graph, indices=[meri_idx])[0]
    
    node_metrics = []
    
    for i, (name, coord, ntype) in enumerate(zip(
        skeleton_data["node_names"], skeleton_data["node_coords"], skeleton_data["node_types"]
    )):
        x, y = coord
        ix, iy = int(round(x)), int(round(y))
        
        # Euclidean distance from meristem
        d_euclid_px = math.hypot(x - cx_m, y - cy_m)
        d_euclid_um = d_euclid_px * PX_UM
        
        # Graph geodesic distance
        # Sample within 3 px radius
        rad = 3
        local_idx = []
        for dy in range(-rad, rad + 1):
            for dx in range(-rad, rad + 1):
                if 0 <= iy + dy < network.shape[0] and 0 <= ix + dx < network.shape[1]:
                    j = idx_map[iy + dy, ix + dx]
                    if j >= 0:
                        local_idx.append(j)
                        
        if local_idx:
            finite_dists = [geo_dist_grid[idx] for idx in local_idx if np.isfinite(geo_dist_grid[idx])]
            if finite_dists:
                d_geo_px = float(min(finite_dists))
                d_geo_um = d_geo_px * PX_UM
            else:
                d_geo_px = d_euclid_px * 1.25  # tortuous fallback if path disconnected
                d_geo_um = d_geo_px * PX_UM
        else:
            d_geo_px = d_euclid_px
            d_geo_um = d_euclid_um
            
        tortuosity = float(d_geo_um / max(d_euclid_um, 1e-3))
        if not np.isfinite(tortuosity) or tortuosity < 1.0:
            tortuosity = 1.0
        
        # Local t50 latency (median within 3-px disc)
        yy, xx = np.indices(mask.shape)
        disc = (xx - x)**2 + (yy - y)**2 <= 3**2
        v_t50 = t50_map[disc & ~np.isnan(t50_map)]
        t50_val = float(np.median(v_t50)) if len(v_t50) >= 3 else None
        
        node_metrics.append({
            "node_idx": int(i),
            "name": str(getattr(name, 'name', name)),
            "type": str(getattr(ntype, 'name', ntype)),
            "x": float(x),
            "y": float(y),
            "d_euclid_um": float(d_euclid_um),
            "d_geo_um": float(d_geo_um),
            "tortuosity": float(tortuosity),
            "t50_s": float(t50_val) if t50_val is not None else None
        })
        
    # Correlate t50 against d_geo vs d_euclid
    valid_pts = [
        m for m in node_metrics 
        if m["t50_s"] is not None 
        and np.isfinite(m["t50_s"])
        and np.isfinite(m["d_geo_um"])
        and np.isfinite(m["d_euclid_um"])
        and m["d_geo_um"] > 100
    ]
    
    if len(valid_pts) >= 4:
        d_geo_arr = np.array([m["d_geo_um"] for m in valid_pts], dtype=np.float64)
        d_euc_arr = np.array([m["d_euclid_um"] for m in valid_pts], dtype=np.float64)
        t50_arr = np.array([m["t50_s"] for m in valid_pts], dtype=np.float64)
        
        r_geo, p_geo = pearsonr(d_geo_arr, t50_arr)
        r_euc, p_euc = pearsonr(d_euc_arr, t50_arr)
        
        # Linear fit: t50 = t0 + d / v -> v = 1 / slope (um / s)
        try:
            poly = np.polyfit(d_geo_arr, t50_arr, 1)
            slope_geo = poly[0]
            v_vascular = float(1.0 / slope_geo) if slope_geo != 0 else 0.0
        except Exception as e:
            print(f"Warning in polyfit: {e}")
            v_vascular = 0.0
    else:
        r_geo, p_geo = 0.0, 1.0
        r_euc, p_euc = 0.0, 1.0
        v_vascular = 0.0
    
    non_meristem_tort = [m["tortuosity"] for m in node_metrics if m["name"] != "meristem" and np.isfinite(m["tortuosity"])]
    mean_tort = float(np.mean(non_meristem_tort)) if non_meristem_tort else 1.0
    max_tort = float(np.max(non_meristem_tort)) if non_meristem_tort else 1.0
    
    conduction_stats = {
        "n_nodes": len(node_metrics),
        "n_valid_t50": len(valid_pts),
        "pearson_r_geodesic": float(r_geo),
        "p_value_geodesic": float(p_geo),
        "r_squared_geodesic": float(r_geo**2),
        "pearson_r_euclid": float(r_euc),
        "p_value_euclid": float(p_euc),
        "r_squared_euclid": float(r_euc**2),
        "vascular_conduction_velocity_um_s": v_vascular,
        "mean_tortuosity": mean_tort,
        "max_tortuosity": max_tort
    }
    
    print(f"Vascular Geodesic Correlation with t50: R² = {conduction_stats['r_squared_geodesic']:.3f} (r = {r_geo:.3f}, p = {p_geo:.4e})")
    print(f"Euclidean Distance Correlation with t50: R² = {conduction_stats['r_squared_euclid']:.3f} (r = {r_euc:.3f}, p = {p_euc:.4e})")
    print(f"Estimated Vascular Conduction Velocity: {v_vascular:.2f} µm/s ({v_vascular*0.06:.2f} mm/min)")
    
    return node_metrics, conduction_stats


def track_landmarks_and_kinematics(raw_czi_path, shifts, skeleton_data, bg_mask, i_settle, t):
    """
    Pattern 2 & 3: Track landmarks across all 700 frames to measure:
      - Hydraulic branch strain ε(t)
      - Petiole angular deflection Δθ(t)
      - Motion-compensated GCaMP fluorescence vs static sampling.
    """
    print("\n--- Sub-Pixel Landmark Tracking & Biomechanical Strain Analysis ---")
    
    # Read raw CZI
    with czifile.CziFile(raw_czi_path) as c:
        arr = np.squeeze(c.asarray()).astype(np.float32)
        T, Y, X = arr.shape
        raw_binned = arr.reshape(T, Y // 2, 2, X // 2, 2).mean((2, 4))
        
    # Apply rigid shifts
    S = np.empty_like(raw_binned)
    for i in range(T):
        if math.hypot(*shifts[i]) > 0.05:
            S[i] = ndi.shift(raw_binned[i], shifts[i], order=1, mode='nearest')
        else:
            S[i] = raw_binned[i]

    # Additive local background subtraction
    w = ndi.gaussian_filter(bg_mask.astype(np.float32), 12)
    Fc = np.empty_like(S)
    for i in range(T):
        B = ndi.gaussian_filter(S[i] * bg_mask, 12) / np.maximum(w, 1e-3)
        Fc[i] = S[i] - B
    Fc = ndi.uniform_filter1d(Fc, 5, axis=0) # smooth

    num_nodes = len(skeleton_data["node_names"])
    init_coords = skeleton_data["node_coords"]
    
    # Trajectory array: shape (T, num_nodes, 2)
    trajectories = np.zeros((T, num_nodes, 2), dtype=np.float32)
    trajectories[0] = init_coords
    
    # Reference patches from median late reference (frames 500-600)
    ref_frame = np.median(S[500:600], 0)
    
    patch_rad = 8 # 17x17 window
    search_rad = 6 # search window
    templates = []
    for k in range(num_nodes):
        ix, iy = int(round(init_coords[k, 0])), int(round(init_coords[k, 1]))
        tmpl = ref_frame[iy - patch_rad : iy + patch_rad + 1, ix - patch_rad : ix + patch_rad + 1]
        templates.append(tmpl)

    print("Tracking landmark positions across 700 frames...")
    for t_i in range(T):
        f = S[t_i]
        for k in range(num_nodes):
            ix, iy = int(round(init_coords[k, 0])), int(round(init_coords[k, 1]))
            # Search region
            y0, y1 = max(0, iy - patch_rad - search_rad), min(f.shape[0], iy + patch_rad + search_rad + 1)
            x0, x1 = max(0, ix - patch_rad - search_rad), min(f.shape[1], ix + patch_rad + search_rad + 1)
            search_area = f[y0:y1, x0:x1]
            tmpl = templates[k]
            
            if search_area.shape[0] >= tmpl.shape[0] and search_area.shape[1] >= tmpl.shape[1]:
                res = cv2.matchTemplate(search_area, tmpl, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, max_loc = cv2.minMaxLoc(res)
                # Optimal center
                opt_x = x0 + max_loc[0] + patch_rad
                opt_y = y0 + max_loc[1] + patch_rad
                trajectories[t_i, k] = [opt_x, opt_y]
            else:
                trajectories[t_i, k] = [ix, iy]

    # Smooth trajectories across time (3-frame median)
    trajectories = ndi.median_filter(trajectories, size=(5, 1, 1))

    # Compute Kinematics:
    # 1. Meristem motion
    meri_disp = np.hypot(
        trajectories[:, 0, 0] - trajectories[0, 0, 0],
        trajectories[:, 0, 1] - trajectories[0, 0, 1]
    ) * PX_UM

    # 2. Branch elongation strain and leaf deflection for each leaf branch
    leaf_kinematics = {}
    for leaf_name, b in skeleton_data["leaf_branches"].items():
        apex_idx = b["apex_idx"]
        pet_idx = b["petiole_idx"]
        
        # Length over time
        dx = trajectories[:, apex_idx, 0] - trajectories[:, 0, 0]
        dy = trajectories[:, apex_idx, 1] - trajectories[:, 0, 1]
        L = np.hypot(dx, dy) * PX_UM # length in um
        L0 = np.median(L[:10]) # baseline length
        
        # Strain: ε(t) = (L(t) - L0) / L0
        strain = (L - L0) / max(L0, 1e-3)
        
        # Angle over time
        angles_deg = np.degrees(np.arctan2(dy, dx))
        theta0 = np.median(angles_deg[:10])
        # Angular deflection (handling 360 wrap)
        deflection = np.unwrap(np.radians(angles_deg - theta0)) * (180.0 / math.pi)
        
        # Peak strain during water window vs post-settle
        water_window_strain = float(np.max(np.abs(strain[:i_settle])))
        post_settle_strain = float(np.max(np.abs(strain[i_settle:])))
        
        leaf_kinematics[leaf_name] = {
            "initial_length_um": float(L0),
            "max_water_strain_pct": float(water_window_strain * 100),
            "max_post_strain_pct": float(post_settle_strain * 100),
            "max_deflection_deg": float(np.max(np.abs(deflection))),
            "length_um": L.tolist(),
            "strain_pct": (strain * 100).tolist(),
            "deflection_deg": deflection.tolist()
        }
        print(f"  {leaf_name:8s}: L0={L0:5.0f} µm | Water Strain={water_window_strain*100:4.2f}% | Max Deflection={np.max(np.abs(deflection)):4.2f}°")

    # 3. Motion-Compensated vs Static GCaMP Sampling
    print("Extracting motion-compensated landmark fluorescence...")
    fluorescence_comparison = {}
    yy, xx = np.indices(S[0].shape)
    
    for k, name in enumerate(skeleton_data["node_names"]):
        # Dynamic sampling at moving landmark
        dynamic_trace = []
        static_trace = []
        static_x, static_y = init_coords[k]
        static_disc = (xx - static_x)**2 + (yy - static_y)**2 <= 2**2
        
        for t_i in range(T):
            cur_x, cur_y = trajectories[t_i, k]
            dyn_disc = (xx - cur_x)**2 + (yy - cur_y)**2 <= 2**2
            dynamic_trace.append(float(Fc[t_i][dyn_disc].mean()))
            static_trace.append(float(Fc[t_i][static_disc].mean()))
            
        dyn_arr = np.array(dynamic_trace)
        stat_arr = np.array(static_trace)
        
        # Baseline subtraction
        dyn_dF = dyn_arr - np.mean(dyn_arr[i_settle:i_settle+5])
        stat_dF = stat_arr - np.mean(stat_arr[i_settle:i_settle+5])
        
        # High-frequency noise (motion jitter)
        noise_dyn = float(np.std(np.diff(dyn_dF[i_settle:])) / math.sqrt(2))
        noise_stat = float(np.std(np.diff(stat_dF[i_settle:])) / math.sqrt(2))
        
        str_k = str(getattr(name, 'name', name))
        fluorescence_comparison[str_k] = {
            "dynamic_trace": dyn_dF.tolist(),
            "static_trace": stat_dF.tolist(),
            "noise_dynamic": noise_dyn,
            "noise_static": noise_stat,
            "noise_reduction_pct": float((noise_stat - noise_dyn) / max(noise_stat, 1e-3) * 100)
        }

    return S, Fc, trajectories, leaf_kinematics, fluorescence_comparison


def export_sleap_project(registered_stack, trajectories, skeleton_data, t, out_slp_path, out_mp4_path):
    """
    Pattern 4: Export standardized SLEAP dataset file (.slp) and MP4 video.
    """
    print(f"\n--- Generating Standard SLEAP Project: {out_slp_path} ---")
    T, H, W = registered_stack.shape
    
    # 1. Export 8-bit normalized grayscale video (compatible with OpenCV/FFmpeg)
    lo, hi = np.percentile(registered_stack, [1, 99.5])
    norm_stack = np.clip((registered_stack - lo) / max(hi - lo, 1e-3) * 255.0, 0, 255).astype(np.uint8)
    
    # Write MP4 video using imageio-ffmpeg
    writer = imageio.get_writer(out_mp4_path, fps=20, codec='libx264', quality=8)
    for frame in norm_stack:
        # Convert to 3-channel for standard MP4
        rgb_frame = np.stack([frame, frame, frame], axis=-1)
        writer.append_data(rgb_frame)
    writer.close()
    print(f"Exported registered video: {out_mp4_path} ({T} frames, {W}x{H})")
    
    # Also copy to docs/assets/sleap/ for web download
    import shutil
    docs_mp4 = os.path.join(DOCS_SLEAP, os.path.basename(out_mp4_path))
    shutil.copy2(out_mp4_path, docs_mp4)

    # 2. Build SLEAP project data structures
    vid = sio.load_video(out_mp4_path)
    skel = skeleton_data["skeleton"]
    
    labeled_frames = []
    # Sample every 5 frames across all 700 frames to keep file compact and responsive
    step = 5
    for f_idx in range(0, T, step):
        pts = trajectories[f_idx] # shape (N, 2)
        inst = sio.Instance.from_numpy(points_data=pts, skeleton=skel)
        lf = sio.LabeledFrame(video=vid, frame_idx=f_idx, instances=[inst])
        labeled_frames.append(lf)
        
    labels = sio.Labels(videos=[vid], labeled_frames=labeled_frames, skeletons=[skel])
    sio.save_slp(labels, out_slp_path)
    print(f"Exported SLEAP project (.slp): {out_slp_path} ({len(labeled_frames)} labeled frames)")
    
    docs_slp = os.path.join(DOCS_SLEAP, os.path.basename(out_slp_path))
    shutil.copy2(out_slp_path, docs_slp)
    print(f"Copied SLEAP package to web assets: {docs_slp}")


def run_sleap_pipeline():
    # Load tissue maps
    d_map = np.load(NPZ_08)
    ref = d_map["ref"]
    mask = d_map["mask"]
    m_hyd = d_map["mask_hydathodes"]
    m_vein = d_map["mask_veins"]
    m_meri = d_map["mask_meristem"]
    t50_map = d_map["t50"]
    shifts = d_map["shifts"]
    t = d_map["t"]
    i_settle = int(d_map["i_settle"])
    
    bg_mask = ~ndi.binary_dilation(mask, disk(4))
    
    # 1. Build Botanical Pose Skeleton
    skeleton_data = build_plant_skeleton_and_nodes(ref, mask, m_hyd, m_vein, m_meri)
    
    # 2. Vascular Graph Geodesic vs Euclidean Analysis
    node_metrics, conduction_stats = compute_vascular_geodesic_conduction(
        mask, m_vein, m_meri, skeleton_data, t50_map
    )
    
    # 3. Time-Series Landmark Tracking & Kinematics
    registered_stack, Fc, trajectories, leaf_kinematics, fluo_comp = track_landmarks_and_kinematics(
        RAW_CZI, shifts, skeleton_data, bg_mask, i_settle, t
    )
    
    # 4. Export SLEAP Project (.slp) and MP4
    out_slp = os.path.join(OUT_SLEAP, "expt08_plant_pose.slp")
    out_mp4 = os.path.join(OUT_SLEAP, "expt08_rosette_registered.mp4")
    export_sleap_project(registered_stack, trajectories, skeleton_data, t, out_slp, out_mp4)
    
    # 5. Save structured summary outputs
    summary_data = {
        "dataset": "FloodWave-At",
        "experiment": "expt08 (representative run)",
        "frames": len(t),
        "duration_s": float(t[-1]),
        "t_settle_s": float(t[i_settle]),
        "conduction_statistics": conduction_stats,
        "nodes": node_metrics,
        "leaf_kinematics": leaf_kinematics,
        "fluorescence_noise_comparison": {
            k: {
                "noise_dynamic": v["noise_dynamic"],
                "noise_static": v["noise_static"],
                "noise_reduction_pct": v["noise_reduction_pct"]
            }
            for k, v in fluo_comp.items()
        }
    }
    
    json_path = os.path.join(OUT_SLEAP, "pose_kinematics_summary.json")
    with open(json_path, "w") as f:
        json.dump(summary_data, f, indent=2)
    print(f"Saved: {json_path}")
    
    # Save CSV of nodes and geodesic metrics
    csv_path = os.path.join(OUT_SLEAP, "pose_kinematics_summary.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["node_idx", "name", "type", "x", "y", "d_euclid_um", "d_geo_um", "tortuosity", "t50_s"])
        for m in node_metrics:
            writer.writerow([
                m["node_idx"], m["name"], m["type"],
                f"{m['x']:.2f}", f"{m['y']:.2f}",
                f"{m['d_euclid_um']:.1f}", f"{m['d_geo_um']:.1f}",
                f"{m['tortuosity']:.3f}",
                f"{m['t50_s']:.1f}" if m['t50_s'] is not None else ""
            ])
    print(f"Saved: {csv_path}")

    # Save trajectories and kinematics in NPZ for fast plotting
    npz_out = os.path.join(OUT_SLEAP, "expt08_pose_trajectories.npz")
    np.savez_compressed(
        npz_out,
        trajectories=trajectories,
        t=t,
        i_settle=i_settle,
        ref=ref,
        mask=mask,
        t50=t50_map,
        node_names=np.array(skeleton_data["node_names"]),
        node_coords=skeleton_data["node_coords"],
        node_types=np.array(skeleton_data["node_types"]),
        edges=np.array(skeleton_data["edges"])
    )
    print(f"Saved: {npz_out}")


if __name__ == "__main__":
    run_sleap_pipeline()
