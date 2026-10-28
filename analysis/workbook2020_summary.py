"""Summarise the 2020 Fiji ROI workbook (legacy/2020_roi_workbook/) for INVENTORY.md §5c.

Per tab: rows holding data, which measurement columns it has, and for the expt 8
tab the first-frame StDev, the frame of each ROI's maximum mean, and the largest
rise of any ROI mean over 10 frames.

usage: workbook2020_summary.py <workbook.xlsx> <out.json>
"""
import json, sys
import numpy as np
import pandas as pd

wb, out = sys.argv[1:3]
tabs = pd.read_excel(wb, sheet_name=None, header=0)
summary = {}
for name, df in tabs.items():
    cols = [str(c) for c in df.columns]
    num = df.apply(pd.to_numeric, errors='coerce')
    kinds = sorted({k for c in cols for k in ('Mean', 'StDev', 'StdDev', 'Mode', 'Min', 'Max', 'Area') if c.startswith(k) or f' {k}' in c or c.split('.')[0] == k})
    meas = [c for c in cols if any(c.startswith(k) for k in ('Mean', 'StDev', 'StdDev'))]
    rows = int(num[meas].notna().any(axis=1).sum()) if meas else 0
    entry = dict(rows_with_data=rows, measurement_kinds=kinds, n_columns=len(cols))
    files = [str(v) for c in cols if c.lower() in ('file', 'label') for v in df[c].dropna().unique()[:3]]
    if files: entry['file_or_label_values'] = files
    tcol = [c for c in cols if 'Time (min)' in c]
    if tcol:
        last = pd.to_numeric(df[tcol[0]], errors='coerce').dropna()
        if len(last): entry['last_time_min_as_labelled'] = float(last.iloc[-1])
    mean_cols = [c for c in cols if c.startswith('Mean')]
    if mean_cols:
        m = num[mean_cols].dropna(how='all').to_numpy()
        sd = num[[c for c in cols if c.startswith('StDev')]].to_numpy()
        rise10 = np.nanmax(m[10:] - m[:-10], axis=0)
        entry['roi_first_frame_stdev'] = [round(float(v), 3) for v in sd[0]]
        entry['roi_mean_frame_of_max'] = [int(np.nanargmax(m[:, j]) + 1) for j in range(m.shape[1])]
        entry['roi_mean_max_10frame_rise'] = [round(float(v), 1) for v in rise10]
    summary[name] = entry
json.dump(summary, open(out, 'w'), indent=1)
print(json.dumps({k: (v['rows_with_data'], v['measurement_kinds']) for k, v in summary.items()}))
