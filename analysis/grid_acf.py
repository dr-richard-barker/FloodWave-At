import sys, czifile, numpy as np
from scipy.ndimage import gaussian_filter
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
PX = 20.4925
src, y0, y1, x0, x1, out = sys.argv[1], *map(int, sys.argv[2:6]), sys.argv[6]
with czifile.CziFile(src) as c:
    sbs = sorted(c.filtered_subblock_directory, key=lambda s: s.start[s.axes.index('T')])
    a = np.squeeze(sbs[len(sbs)//2].data_segment().data()).astype(float)
p = a[y0:y1, x0:x1]; p = p - gaussian_filter(p, 25); p = gaussian_filter(p, 1.5)
def first_peak(prof):
    prof = prof - prof.mean(); ac = np.correlate(prof, prof, 'full')[len(prof)-1:]; ac /= ac[0]
    for k in range(8, len(ac)-1):
        if ac[k] > ac[k-1] and ac[k] >= ac[k+1] and ac[k] > 0.1: return k, ac[k]
    return None, None
kx, vx = first_peak(p.mean(0)); ky, vy = first_peak(p.mean(1))
print(src.split('/')[-1][:38], 'x-period', kx, 'px', None if kx is None else round(kx*PX), 'um', '| y-period', ky, 'px', None if ky is None else round(ky*PX), 'um')
fig, ax = plt.subplots(1, 2, figsize=(10, 4)); ax[0].imshow(a, cmap='gray', vmin=np.percentile(a, 1), vmax=np.percentile(a, 99.5)); ax[0].add_patch(plt.Rectangle((x0, y0), x1-x0, y1-y0, fill=False, ec='r')); ax[1].imshow(p, cmap='gray'); fig.savefig(out, dpi=70)
