#!/usr/bin/env python3
"""
update_app_with_water_windows.py · Integrate water addition window metrics into docs/app.js.
"""

import json

with open('results/water_addition_windows.json') as f:
    water_windows = {r['tag']: r for r in json.load(f)}

with open('docs/app.js') as f:
    app_js = f.read()

# Add fields to each entry in RUNS_DATA
for tag, w in water_windows.items():
    target = f"tag: '{tag}',"
    injection = (
        f"tag: '{tag}',\n"
        f"    water_onset_s: {w['water_onset_s']},\n"
        f"    water_window_str: '{w['water_window_start_s']}–{w['water_window_end_s']} s',\n"
        f"    surge_peak_s: {w['surge_peak_s']},\n"
        f"    surge_peak_px: {w['surge_peak_step_px']},"
    )
    if injection not in app_js:
        app_js = app_js.replace(target, injection, 1)

# Update updateRunInspector in app.js
old_inspector = """    setTxt('mFrames', `${r.frames} (${r.duration_s.toFixed(0)} s)`);
    setTxt('mSettle', `${r.t_settle_s.toFixed(1)} s`);"""

new_inspector = """    setTxt('mFrames', `${r.frames} (${r.duration_s.toFixed(0)} s)`);
    setTxt('mSettle', `${r.t_settle_s.toFixed(1)} s`);
    setTxt('mWaterWindow', r.water_window_str);
    setTxt('mSurgePeak', `${r.surge_peak_s.toFixed(1)} s (${r.surge_peak_px.toFixed(1)} px)`);"""

if old_inspector in app_js:
    app_js = app_js.replace(old_inspector, new_inspector, 1)

# Update telemetry phase messages
old_telemetry = """    let phaseText = 'Water pouring & mesh motion';
    let activeChapterIdx = 0;
    if (realSec >= 650) {
      phaseText = 'Whole-plant peak plateau (~696 s)';
      activeChapterIdx = 4;
    } else if (realSec >= 440) {
      phaseText = 'Median pixel half-rise (t50 = 470 s)';
      activeChapterIdx = 3;
    } else if (realSec >= 240) {
      phaseText = 'Earliest 5% pixels (veins & margin)';
      activeChapterIdx = 2;
    } else if (realSec >= 48.4) {
      phaseText = 'Post-settle slow rise (veins lead)';
      activeChapterIdx = 1;
    }"""

new_telemetry = """    let phaseText = 'Pre-flood dry baseline (0–14.6 s)';
    let activeChapterIdx = 0;
    if (realSec >= 650) {
      phaseText = 'Whole-plant peak plateau (~696 s)';
      activeChapterIdx = 4;
    } else if (realSec >= 440) {
      phaseText = 'Median pixel half-rise (t50 = 470 s)';
      activeChapterIdx = 3;
    } else if (realSec >= 240) {
      phaseText = 'Earliest 5% pixels (veins & margin)';
      activeChapterIdx = 2;
    } else if (realSec >= 48.5) {
      phaseText = 'Post-settle slow rise (veins lead)';
      activeChapterIdx = 1;
    } else if (realSec >= 14.6) {
      phaseText = 'Water influx & meniscus surge (peak 36.4 s)';
      activeChapterIdx = 0;
    }"""

if old_telemetry in app_js:
    app_js = app_js.replace(old_telemetry, new_telemetry, 1)

# In master summary table, add Water Window column
old_table_header_data = """        <td class="num">${r.frames}</td>
        <td class="num">${r.t_settle_s.toFixed(1)}</td>"""

new_table_header_data = """        <td class="num">${r.frames}</td>
        <td class="num" style="color:var(--accent-amber);font-weight:600">${r.water_window_str}</td>
        <td class="num">${r.t_settle_s.toFixed(1)}</td>"""

if old_table_header_data in app_js:
    app_js = app_js.replace(old_table_header_data, new_table_header_data)

with open('docs/app.js', 'w') as f:
    f.write(app_js)

print("Updated docs/app.js successfully!")
