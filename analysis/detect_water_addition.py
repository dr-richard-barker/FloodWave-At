#!/usr/bin/env python3
"""
detect_water_addition.py · Detect and predict the water-addition window across all 12 FloodWave-At runs.

In each experiment, time-lapse recording was started first with the plant sitting in air
on the dry support mesh. Flood water was subsequently administered to the root compartment
over an estimated 10-30 s.

This script analyzes the frame-by-frame registration shifts and motion steps from
results/runs/expt*/expt*_maps.npz to detect:
1. Quiescent dry baseline noise level and duration: [0, t_onset]
2. Water addition onset: t_onset (first frame with step > 3*sigma above baseline)
3. Peak fluid surge / hydrodynamic disturbance: t_surge_peak (maximum early step in px)
4. Fluid settling point: t_settle (where motion drops below 0.5 px)
5. Predicted water addition window / bin: [t_onset, t_settle]
"""

import os
import glob
import json
import csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def analyze_water_addition():
    results = []
    
    # Process all 12 experiments in order
    for expt_num in range(1, 13):
        tag = f'expt{expt_num:02d}'
        npz_path = f'results/runs/{tag}/{tag}_maps.npz'
        if not os.path.exists(npz_path):
            print(f'Warning: {npz_path} not found')
            continue
            
        data = np.load(npz_path)
        t = data['t']
        shifts = data['shifts']
        step = np.r_[0, np.hypot(*np.diff(shifts, axis=0).T)]
        i_settle = int(data['i_settle'])
        t_settle = float(t[i_settle])
        
        # Estimate quiescent noise in early frames (first 8 frames, ~10s)
        base_steps = step[1:min(9, len(step))]
        noise_median = float(np.median(base_steps))
        noise_std = float(np.std(base_steps))
        threshold = max(0.20, noise_median + 3.0 * max(noise_std, 0.05))
        
        # Look for motion onset in first 120 s
        early_mask = t < 120
        elevated = np.where((step > threshold) & early_mask)[0]
        
        if len(elevated) > 0:
            first_f = int(elevated[0])
            t_onset = float(t[first_f])
            
            # Peak early disturbance
            peak_f = int(np.argmax(step * early_mask))
            t_peak = float(t[peak_f])
            peak_mag = float(step[peak_f])
            
            last_elevated_f = int(elevated[-1])
            t_last_elevated = float(t[last_elevated_f])
        else:
            first_f = 0
            t_onset = 0.0
            peak_f = 0
            t_peak = 0.0
            peak_mag = 0.0
            t_last_elevated = t_settle
            
        # Water addition window is from onset until settling
        # (or end of elevated motion if settling happened earlier)
        t_end = min(t_settle, max(t_last_elevated + 2.5, t_onset + 10.0))
        duration = t_end - t_onset
        
        row = {
            'expt': expt_num,
            'tag': tag,
            'frames': len(t),
            'duration_s': round(float(t[-1]), 1),
            'quiescent_baseline_s': round(t_onset, 1),
            'quiescent_noise_px': round(noise_median, 3),
            'water_onset_frame': first_f,
            'water_onset_s': round(t_onset, 1),
            'surge_peak_frame': peak_f,
            'surge_peak_s': round(t_peak, 1),
            'surge_peak_step_px': round(peak_mag, 2),
            'settle_frame': i_settle,
            'settle_s': round(t_settle, 1),
            'water_window_start_s': round(t_onset, 1),
            'water_window_end_s': round(t_settle, 1),
            'water_window_duration_s': round(t_settle - t_onset, 1)
        }
        results.append(row)
        print(f"[{tag}] Pre-flood: 0-{row['water_onset_s']}s | Water Added: {row['water_window_start_s']}-{row['water_window_end_s']}s (peak {row['surge_peak_s']}s, {row['surge_peak_step_px']}px) | Settled: {row['settle_s']}s")

    # Save to JSON
    json_path = 'results/water_addition_windows.json'
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Saved {json_path}")
    
    # Save to CSV
    csv_path = 'results/water_addition_windows.csv'
    fieldnames = list(results[0].keys())
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    print(f"Saved {csv_path}")

    # Generate multi-run timeline figure
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=150)
    
    # Dark CoSE slate/teal background styling
    fig.patch.set_facecolor('#0C1A1F')
    ax.set_facecolor('#122730')
    
    y_pos = np.arange(len(results))
    labels = [r['tag'] for r in results]
    
    for i, r in enumerate(results):
        y = i
        t_onset = r['water_window_start_s']
        t_settle = r['water_window_end_s']
        t_peak = r['surge_peak_s']
        peak_px = r['surge_peak_step_px']
        
        # 1. Pre-flood baseline (gray bar)
        ax.barh(y, t_onset, left=0, height=0.55, color='#4A646E', alpha=0.85, label='Pre-Flood Dry Baseline' if i == 0 else "")
        
        # 2. Water addition & fluid surge window (cyan/amber bar)
        ax.barh(y, t_settle - t_onset, left=t_onset, height=0.55, color='#0F7F9F', edgecolor='#3FA9C7', lw=1.2,
                label='Predicted Water Addition & Surge Window' if i == 0 else "")
        
        # 3. Post-settle period (up to 140s for display)
        post_dur = max(0, 140 - t_settle)
        ax.barh(y, post_dur, left=t_settle, height=0.55, color='#17323C', edgecolor='#23404A', alpha=0.9,
                label='Post-Settle Signal Analysis (> t_settle)' if i == 0 else "")
        
        # Mark peak disturbance
        ax.scatter([t_peak], [y], color='#FBBF24', s=45, zorder=5, edgecolors='#061318', lw=1,
                   label='Peak Fluid Disturbance' if i == 0 else "")
        
        # Annotate text
        annot = f"Water: {t_onset:.0f}–{t_settle:.0f}s (peak {t_peak:.0f}s, {peak_px:.1f}px)"
        ax.text(142, y, annot, va='center', ha='left', color='#E3ECEF', fontsize=8.5, fontfamily='monospace')

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels, color='#E3ECEF', fontsize=10, fontfamily='monospace')
    ax.invert_yaxis()  # expt01 on top
    ax.set_xlabel('Time from Recording Start (seconds)', color='#E3ECEF', fontsize=11, fontweight='medium')
    ax.set_xlim(0, 240)
    ax.tick_params(colors='#B7C8CE', which='both')
    
    for spine in ax.spines.values():
        spine.set_color('#23404A')
        
    ax.grid(axis='x', color='#23404A', linestyle='--', alpha=0.6)
    
    # Highlight expt08 representative run
    ax.get_yticklabels()[7].set_color('#FBBF24')
    ax.get_yticklabels()[7].set_fontweight('bold')
    
    ax.set_title('Predicted Water Addition Windows Across All 12 FloodWave-At Time Series\n'
                 'Resolved from Pre-Flood Quiescent Baselines, Hydrodynamic Onset, and Registration Settling',
                 color='#DCEBF0', fontsize=12, fontweight='bold', pad=15)
                 
    ax.legend(loc='lower right', facecolor='#122730', edgecolor='#23404A', labelcolor='#E3ECEF', fontsize=9)
    plt.tight_layout()
    
    out_fig = 'results/figures/water_addition_timeline.png'
    fig.savefig(out_fig, dpi=150, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Saved {out_fig}")
    
    # Also copy to docs/assets/figures/
    docs_fig = 'docs/assets/figures/water_addition_timeline.png'
    os.makedirs(os.path.dirname(docs_fig), exist_ok=True)
    import shutil
    shutil.copyfile(out_fig, docs_fig)
    print(f"Copied to {docs_fig}")

if __name__ == '__main__':
    analyze_water_addition()
