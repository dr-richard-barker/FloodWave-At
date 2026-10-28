import sys, glob, os, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
AW = sys.argv[1]; out = sys.argv[2]
fs = sorted(glob.glob(os.path.join(AW, 'expt*', 'expt*_maps.npz')))
fig, axs = plt.subplots(3, 4, figsize=(24, 13.5))
for a, f in zip(axs.flat, fs):
    z = np.load(f); r = z['ref']; lo, hi = np.percentile(r, [1, 99.7])
    a.imshow(r, cmap='gray', vmin=lo, vmax=hi)                       # binned coords (346 x 260)
    a.contour(z['mask'].astype(float), [0.5], colors='r', linewidths=0.9)
    a.set_xticks(np.arange(0, 346, 50)); a.set_xticklabels(np.arange(0, 346, 50) * 2)   # labels in raw px
    a.set_yticks(np.arange(0, 260, 50)); a.set_yticklabels(np.arange(0, 260, 50) * 2)
    a.grid(color='y', lw=0.4, alpha=0.6); a.set_title(os.path.basename(f)[:6], fontsize=12); a.tick_params(labelsize=8)
fig.tight_layout(); fig.savefig(out, dpi=55)
