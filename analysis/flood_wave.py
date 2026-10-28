"""First-pass activation analysis of one Flood_DRB .czi run.

Reads one raw run read-only, bins 2x2 (41 um px), registers rigidly to a late
reference, removes an additive local background estimated from off-plant
pixels, and maps for every plant pixel the half-maximum rise time (t50) of
its signal after sample motion has settled. Leaf regions are split into an
outer margin band, a control band just inside it, veins and interior lamina.

Writes <outdir>/<tag>/: maps (.npz), a summary (.json) and figures.
"""
import argparse, json, os, re
import numpy as np
import czifile
from scipy import ndimage as ndi
from skimage.registration import phase_cross_correlation
from skimage.filters import threshold_otsu, sato
from skimage.morphology import remove_small_objects, binary_opening, disk

ap = argparse.ArgumentParser()
ap.add_argument('czi'); ap.add_argument('outdir')
ap.add_argument('--min-settle-s', type=float, default=20.0)
ap.add_argument('--snr', type=float, default=5.0, help='minimum rise / pixel noise for a valid t50')
ap.add_argument('--qc', default=None, help='qc.json with per-run exclude_boxes (raw px)')
a = ap.parse_args()

PX_UM = 20.4925 * 2
n = int(re.match(r'Flooding expt (\d+)', os.path.basename(a.czi)).group(1))
tag = f'expt{n:02d}'
out = os.path.join(a.outdir, tag); os.makedirs(out, exist_ok=True)

# ---- read + bin 2x2
with czifile.CziFile(a.czi) as c:
    ts = next(np.asarray(x.data(), float) for x in c.attachments() if x.attachment_entry.name == 'TimeStamps')
    sbs = sorted(c.filtered_subblock_directory, key=lambda s: s.start[s.axes.index('T')])
    T = len(sbs)
    S = np.empty((T, 260, 346), np.float32)
    for i, sb in enumerate(sbs):
        S[i] = np.squeeze(sb.data_segment().data()).astype(np.float32).reshape(260, 2, 346, 2).mean((1, 3))
t = ts - ts[0]

# ---- rigid registration to a late reference (high-passed, so background changes do not drive it)
def hp(im):
    return ndi.gaussian_filter(im, 1.5) - ndi.gaussian_filter(im, 15)
ref = hp(np.median(S[int(T * 0.8):], 0))
shifts = np.zeros((T, 2))
for i in range(T):
    shifts[i] = phase_cross_correlation(ref, hp(S[i]), upsample_factor=10, normalization=None)[0]
    if np.hypot(*shifts[i]) > 0.05:
        S[i] = ndi.shift(S[i], shifts[i], order=1, mode='nearest')
step = np.r_[0, np.hypot(*np.diff(shifts, axis=0).T)]

# settle time: 3 frames after the last early registration step > 0.5 px (first 150 s)
early = np.where((step > 0.5) & (t < 150))[0]
i_settle = int(max(np.searchsorted(t, a.min_settle_s), (early[-1] + 3) if early.size else 0))
t_settle = float(t[i_settle])
late_steps = np.where((step > 0.5) & (t >= 150))[0]

# ---- plant mask and regions from the late registered reference
S = ndi.gaussian_filter(S, (0, 1, 1))
ref_img = np.median(S[int(T * 0.8):], 0)
flat = ref_img - ndi.gaussian_filter(ref_img, 40)
excl = np.zeros(ref_img.shape, bool)              # curated off-plant objects (qc.json), raw px -> binned
if a.qc:
    for x0, y0, x1, y1 in json.load(open(a.qc)).get(tag, {}).get('exclude_boxes', []):
        excl[y0 // 2:y1 // 2, x0 // 2:x1 // 2] = True
flat = np.where(excl, np.median(flat), flat)
m = flat > threshold_otsu(np.minimum(flat, np.percentile(flat, 99)))  # clip so saturated debris cannot set the threshold
m = remove_small_objects(binary_opening(m, disk(1)), max_size=150)
m = ndi.binary_fill_holes(m)
lab, nlab = ndi.label(m)                 # drop detached objects < 5% of the largest (debris in mesh holes)
if nlab > 1:
    sizes = ndi.sum(m, lab, range(1, nlab + 1))
    m = np.isin(lab, 1 + np.where(sizes >= 0.05 * sizes.max())[0])
dist = ndi.distance_transform_edt(m)
margin = m & (dist <= 2)                 # outer ~80 um
inner = m & (dist > 2) & (dist <= 4)     # control band, 80-160 um in
core = m & (dist > 4)
ridge = sato(ref_img, sigmas=[1, 2], black_ridges=False)
vein = core & (ridge > np.percentile(ridge[core], 80)) if core.any() else core
lamina = core & ~vein
bg = ~ndi.binary_dilation(m, disk(4)) & ~ndi.binary_dilation(excl, disk(4))

# ---- additive local background (normalised convolution of off-plant pixels), held-out check
yy, xx = np.indices(m.shape)
checker = ((yy // 20) + (xx // 20)) % 2 == 0
train, test = bg & checker, bg & ~checker
def bgfield(frame, msk, s=12):
    w = ndi.gaussian_filter(msk.astype(np.float32), s)
    return ndi.gaussian_filter(frame * msk, s) / np.maximum(w, 1e-3)
leak = np.zeros(T)
for i in range(T):
    f = S[i]
    leak[i] = (f - bgfield(f, train))[test].mean()
    S[i] = f - bgfield(f, bg)              # S now holds background-subtracted signal
Fc = ndi.uniform_filter1d(S, 5, axis=0); del S

# ---- per-pixel rise after settling: t50, peak time, rise amplitude (counts)
post = Fc[i_settle:]
y0 = Fc[i_settle:i_settle + 5].mean(0)
pk_i = post.argmax(0)
rise = post.max(0) - y0
noise = np.median(np.abs(np.diff(Fc[i_settle:], axis=0)), 0) / 0.6745 / np.sqrt(2) * np.sqrt(5)
noise = ndi.gaussian_filter(noise, 2)
valid = m & (rise > a.snr * noise)
half = post >= (y0 + 0.5 * rise)[None]
t50 = np.where(valid, t[i_settle + half.argmax(0)], np.nan)
tpk = np.where(valid, t[i_settle + pk_i], np.nan)
amp = np.where(m, rise, np.nan)

regions = dict(margin=margin, inner=inner, vein=vein, lamina=lamina)
traces = {k: (Fc[:, r].mean(1) - Fc[i_settle:i_settle + 5, r].mean()) if r.any() else np.full(T, np.nan)
          for k, r in dict(plant=m, **regions).items()}
level = float(np.median(Fc[i_settle:i_settle + 5][:, m])) if m.any() else np.nan
traces['background residual'] = (leak - leak[i_settle:i_settle + 5].mean())

S_ = dict(tag=tag, file=os.path.basename(a.czi), frames=T, duration_s=float(t[-1]), t_settle_s=t_settle,
          max_reg_shift_px=float(np.hypot(*shifts.T).max()), late_motion_steps=int(late_steps.size),
          plant_px=int(m.sum()), plant_area_mm2=float(m.sum() * (PX_UM / 1000) ** 2),
          frac_valid=float(valid.sum() / max(m.sum(), 1)), plant_level_at_settle_counts=level,
          bg_residual_max_abs_counts=float(np.abs(traces['background residual'][i_settle:]).max()),
          plant_rise_counts=float(np.nanmax(traces['plant'][i_settle:])),
          plant_trace_tpeak_s=float(t[i_settle + np.nanargmax(traces['plant'][i_settle:])]))
for k, r in regions.items():
    v = r & valid
    S_[f'{k}_px'] = int(r.sum()); S_[f'{k}_frac_valid'] = float(v.sum() / max(r.sum(), 1))
    S_[f'{k}_t50_median_s'] = float(np.median(t50[v])) if v.sum() >= 10 else None
    S_[f'{k}_rise_median_counts'] = float(np.median(rise[r])) if r.any() else None
first = np.zeros_like(m)
if valid.sum() >= 50:
    q = np.percentile(t50[valid], 5)
    first = valid & (t50 <= q)
    S_['t50_p5_s'] = float(q); S_['t50_median_s'] = float(np.median(t50[valid]))
    for k, r in regions.items():
        area = (r & valid).sum() / valid.sum(); share = (first & r).sum() / first.sum()
        S_[f'first5_share_{k}'] = float(share); S_[f'first5_enrich_{k}'] = float(share / area) if area else None

np.savez_compressed(os.path.join(out, f'{tag}_maps.npz'), t50=t50.astype(np.float32), tpk=tpk.astype(np.float32),
                    rise=amp.astype(np.float32), ref=ref_img, mask=m, margin=margin, inner=inner, vein=vein,
                    lamina=lamina, t=t, shifts=shifts, i_settle=i_settle,
                    **{f'trace_{k.replace(" ", "_")}': v for k, v in traces.items()})
json.dump(S_, open(os.path.join(out, f'{tag}_summary.json'), 'w'), indent=1)

# ---- figures
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
lo, hi = np.percentile(ref_img, [1, 99.7])
fig, ax = plt.subplots(2, 3, figsize=(15, 8.4))
ax[0, 0].imshow(ref_img, cmap='gray', vmin=lo, vmax=hi)
ov = np.zeros(m.shape + (4,)); ov[margin] = (1, .25, .25, .8); ov[inner] = (1, .8, .2, .6); ov[vein] = (.3, .8, 1, .6); ov[lamina] = (.4, 1, .4, .2)
ax[0, 0].imshow(ov); ax[0, 0].set_title('regions: margin (red), inner band (amber), vein (blue), lamina (green)', fontsize=9)
ax[0, 0].plot([10, 10 + 2000 / PX_UM], [250, 250], 'w-', lw=3); ax[0, 0].text(10, 244, '2 mm', color='w', fontsize=8)
if valid.any():
    vmin, vmax = np.percentile(t50[valid], [2, 98])
    ax[0, 1].imshow(ref_img, cmap='gray', vmin=lo, vmax=hi)
    im = ax[0, 1].imshow(t50, cmap='turbo', vmin=vmin, vmax=vmax); plt.colorbar(im, ax=ax[0, 1], fraction=.04)
    ax[0, 1].contour(first, [0.5], colors='w', linewidths=.8)
ax[0, 1].set_title('t50: half-max rise time (s from recording start); white = earliest 5%', fontsize=9)
ax[0, 2].imshow(ref_img, cmap='gray', vmin=lo, vmax=hi)
im = ax[0, 2].imshow(np.where(m, rise, np.nan), cmap='magma', vmin=0, vmax=np.nanpercentile(amp, 99)); plt.colorbar(im, ax=ax[0, 2], fraction=.04)
ax[0, 2].set_title('rise after settling (background-subtracted counts)', fontsize=9)
for x in ax[0]: x.axis('off')
for k, col in dict(plant='k', margin='C3', inner='C1', vein='C0', lamina='C2').items():
    ax[1, 0].plot(t, traces[k], color=col, lw=1, label=k)
ax[1, 0].plot(t, traces['background residual'], color='0.6', lw=1, label='held-out background residual')
ax[1, 0].axvline(t_settle, color='k', ls=':', lw=1); ax[1, 0].set_xlabel('time from recording start (s)'); ax[1, 0].set_ylabel('signal change from t_settle (counts)')
ax[1, 0].legend(fontsize=7)
if valid.any():
    bins = np.linspace(vmin, vmax, 40)
    for k, col in dict(margin='C3', inner='C1', vein='C0', lamina='C2').items():
        v = regions[k] & valid
        if v.sum() >= 10: ax[1, 1].hist(t50[v], bins, histtype='step', color=col, density=True, label=f'{k} (n={v.sum()})')
    ax[1, 1].legend(fontsize=7)
ax[1, 1].set_xlabel('t50 (s)'); ax[1, 1].set_title('t50 by region', fontsize=9)
ax[1, 2].plot(t, np.hypot(*shifts.T), 'k', lw=1); ax[1, 2].axvline(t_settle, color='k', ls=':', lw=1)
ax[1, 2].set_xlabel('time (s)'); ax[1, 2].set_ylabel('registration shift (41 um px)'); ax[1, 2].set_title('motion; dotted = t_settle', fontsize=9)
fig.suptitle(f"{S_['file']}", fontsize=10)
fig.tight_layout(); fig.savefig(os.path.join(out, f'{tag}_activation.png'), dpi=80); plt.close(fig)
print(json.dumps(S_))
