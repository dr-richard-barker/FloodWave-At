"""Figures for the 'Flood Wave, revisited' deck and results/ (reads flood_wave.py outputs)."""
import json, os, sys, glob, re
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

AW, ROIJ, OUT, QCJ = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
os.makedirs(OUT, exist_ok=True)
INK, INK2, PAPER, DARK = '#1a1a19', '#52514e', '#f4f2ec', '#12181d'
C = dict(margin='#eb6834', vein='#2a78d6', lamina='#1baf7a', inner='#8a8984', plant=INK)
AMBER = LinearSegmentedColormap.from_list('amber', ['#fff1c9', '#f2b94b', '#c97a12', '#6b3a05'])
plt.rcParams.update({'font.size': 17, 'axes.edgecolor': INK2, 'axes.labelcolor': INK, 'xtick.color': INK2,
                     'ytick.color': INK2, 'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.grid': True, 'grid.color': '#dedcd5', 'grid.linewidth': 0.8, 'lines.linewidth': 2})

S = sorted((json.load(open(f)) for f in glob.glob(os.path.join(AW, 'expt*', 'expt*_summary.json'))), key=lambda s: s['tag'])
assert len(S) == 12, f'expected 12 run summaries, found {len(S)}'
# motion QC: any frame-to-frame registration step > 2 binned px (82 um) after t_settle flags the run
for s in S:
    zq = np.load(os.path.join(AW, s['tag'], f"{s['tag']}_maps.npz"))
    st = np.r_[0, np.hypot(*np.diff(zq['shifts'], axis=0).T)][int(zq['i_settle']):]
    s['max_post_settle_step_px'] = float(st.max()); s['motion_flag'] = bool(st.max() > 2.0)
    # earliest responders coincide with the settle step: their order is not a propagation order
    s['step_flag'] = bool(s.get('t50_p5_s') is not None and s['t50_p5_s'] - s['t_settle_s'] < 15)
    # fastest ~6 s rise in the 60 s after settling: plant mean vs held-out background (counts)
    i0 = int(zq['i_settle']); tq = zq['t']; i1 = int(np.searchsorted(tq, tq[i0] + 60))
    pl, bgr = zq['trace_plant'][i0:i1 + 5], zq['trace_background_residual'][i0:i1 + 5]
    s['fast6s_plant_counts'] = float((pl[5:] - pl[:-5]).max()); s['fast6s_background_counts'] = float((bgr[5:] - bgr[:-5]).max())
QC = json.load(open(QCJ))
for s in S:
    s['mask_ok'] = QC[s['tag']]['mask_ok']; s['qc_note'] = QC[s['tag']]['note']
    s['pooled'] = s['mask_ok'] and not s['motion_flag'] and not s['step_flag']
label = lambda f: (re.sub(r'^Flooding expt \d+\s*', '', f).replace('10012020.czi', '').strip() or 'no label')

def load(tag):
    return np.load(os.path.join(AW, tag, f'{tag}_maps.npz'))

def gray(ref):
    lo, hi = np.percentile(ref, [1, 99.7]); return np.clip((ref - lo) / (hi - lo), 0, 1)

# ---- A: expt 8 regions + t50 map (dark panel)
z = load('expt08'); s8 = next(s for s in S if s['tag'] == 'expt08')
fig, ax = plt.subplots(1, 2, figsize=(16, 6.4), facecolor=DARK)
ov = np.zeros(z['mask'].shape + (4,))
for k, col in (('margin', C['margin']), ('vein', C['vein']), ('lamina', C['lamina'])):
    ov[z[k]] = matplotlib.colors.to_rgba(col, 0.75 if k != 'lamina' else 0.35)
ov[z['inner']] = matplotlib.colors.to_rgba('#bdbbb4', 0.55)
ax[0].imshow(gray(z['ref']), cmap='gray'); ax[0].imshow(ov)
t50 = z['t50']; v = np.isfinite(t50); lo, hi = np.percentile(t50[v], [2, 98])
ax[1].imshow(gray(z['ref']), cmap='gray')
im = ax[1].imshow(np.where(v, t50, np.nan), cmap=AMBER, vmin=lo, vmax=hi)
first = v & (t50 <= np.percentile(t50[v], 5)); ax[1].contour(first, [0.5], colors='#ffffff', linewidths=1.2)
for a in ax:
    a.axis('off'); a.plot([12, 12 + 2000 / 40.985], [248, 248], color='#f4f2ec', lw=4); a.text(12, 241, '2 mm', color='#f4f2ec', fontsize=15)
cb = fig.colorbar(im, ax=ax[1], fraction=0.035, pad=0.02); cb.set_label('t50, s from recording start', color='#f4f2ec')
cb.ax.yaxis.set_tick_params(color='#f4f2ec'); plt.setp(cb.ax.get_yticklabels(), color='#f4f2ec')
fig.tight_layout(); fig.savefig(os.path.join(OUT, 'expt08_regions_t50.png'), dpi=100, facecolor=DARK); plt.close(fig)

# ---- B: expt 8 region traces (light)
fig, ax = plt.subplots(figsize=(16, 6.6), facecolor=PAPER); ax.set_facecolor(PAPER)
t = z['t']; i0 = int(z['i_settle'])
for k in ('plant', 'vein', 'lamina', 'margin'):
    ax.plot(t[i0:], z[f'trace_{k}'][i0:], color=C[k], lw=2.4 if k == 'plant' else 2, label={'plant': 'whole plant'}.get(k, k))
ax.plot(t[i0:], z['trace_inner'][i0:], color=C['inner'], lw=2, ls='--', label='inner band (control)')
ax.plot(t[i0:], z['trace_background_residual'][i0:], color='#b9b7af', lw=1.5, label='held-out background')
ax.set_xlabel('seconds from start of recording'); ax.set_ylabel('signal change (counts above local background)')
ax.set_xlim(0, t[-1]); ax.legend(frameon=False, fontsize=15, loc='upper left', ncol=2)
fig.tight_layout(); fig.savefig(os.path.join(OUT, 'expt08_traces.png'), dpi=100, facecolor=PAPER); plt.close(fig)

# ---- C: 2020 ROI reproduction (light)
d = json.load(open(ROIJ)); tt = np.array(d['t'])
cls = lambda lab: 'margin' if lab.startswith('Hydr') else ('lamina' if lab.startswith('Lam') else 'vein')
clsname = {'margin': '“hydathode” ROIs (2020 label)', 'lamina': '“lamina” ROIs', 'vein': '“meristem” ROI'}
sm = lambda x: np.convolve(np.asarray(x), np.ones(5) / 5, 'valid')
ts_ = tt[2:-2]
fig, ax = plt.subplots(1, 2, figsize=(16, 6.4), facecolor=PAPER, sharex=True)
seen = set()
for k, r in sorted(d['rois'].items()):
    c = cls(r['label']); lab = clsname[c] if c not in seen else None; seen.add(c)
    ax[0].plot(ts_[38:], sm(r['sd'])[38:], color=C[c], lw=1.8, label=lab)
    y = sm(r['mean_bgsub']); ax[1].plot(ts_[38:], y[38:] - y[38:43].mean(), color=C[c], lw=1.8)
ax[0].set_title('What the 2020 chart plotted: SD inside each ROI', fontsize=17, loc='left', color=INK)
ax[1].set_title('Mean inside each ROI, background-subtracted', fontsize=17, loc='left', color=INK)
ax[0].set_ylabel('raw counts (SD)'); ax[1].set_ylabel('change from 48.5 s (counts)')
for a in ax: a.set_facecolor(PAPER); a.set_xlabel('seconds from start of recording')
fig.legend(*ax[0].get_legend_handles_labels(), frameon=False, fontsize=15, loc='lower center', ncol=3)
fig.tight_layout(rect=(0, 0.08, 1, 1)); fig.savefig(os.path.join(OUT, 'roi2020_reproduction.png'), dpi=100, facecolor=PAPER); plt.close(fig)

# ---- D: all runs, relative order maps (percentile of t50 within each run), dark small multiples
order = sorted(S, key=lambda s: int(s['tag'][4:]))
fig, axs = plt.subplots(3, 4, figsize=(16, 9.6), facecolor=DARK)
for a, s in zip(axs.flat, order):
    zz = load(s['tag']); t5 = zz['t50']; vv = np.isfinite(t5)
    a.imshow(gray(zz['ref']), cmap='gray')
    if vv.sum() > 50:
        pr = np.full(t5.shape, np.nan); r = t5[vv].argsort().argsort(); pr[vv] = r / max(r.max(), 1)
        a.imshow(pr, cmap=AMBER, vmin=0, vmax=1)
    short = {'no label': 'unlabelled', 'NormalWater': 'NormalWater', 'NormalWater YoungLeaf': 'NW · young leaf',
             'NormalWater small plant representative': 'NW · small (rep.)', 'NormalWater small plant': 'NW · small',
             'NormalWater Medium plant': 'NW · medium'}[label(s['file'])]
    flag = 'pooled' if s['pooled'] else ('excluded: motion' if s['motion_flag'] else 'excluded: mask QC' if not s['mask_ok'] else 'excluded: step at settle')
    a.set_title(f"expt {int(s['tag'][4:])} · {short}\n{flag}", color='#f4f2ec' if s['pooled'] else '#e8a33d', fontsize=13, loc='left')
    a.axis('off')
fig.subplots_adjust(left=0.01, right=0.99, top=0.93, bottom=0.08, wspace=0.04, hspace=0.30)
cax = fig.add_axes([0.30, 0.03, 0.40, 0.018]); sm_ = plt.cm.ScalarMappable(cmap=AMBER); sm_.set_array([0, 1])
cb = fig.colorbar(sm_, cax=cax, orientation='horizontal'); cb.set_ticks([0, 1]); cb.set_ticklabels(['first to half-max', 'last'])
plt.setp(cb.ax.get_xticklabels(), color='#f4f2ec'); cb.outline.set_edgecolor('#f4f2ec')
fig.savefig(os.path.join(OUT, 'all_runs_order_maps.png'), dpi=100, facecolor=DARK); plt.close(fig)

# ---- E: earliest-5% enrichment by region, all runs (light dot plot, log2 axis)
fig, ax = plt.subplots(figsize=(16, 7.4), facecolor=PAPER); ax.set_facecolor(PAPER)
ys = np.arange(len(order))[::-1]
for k, mk, off in (('margin', 'o', -0.18), ('inner', 'o', -0.06), ('vein', 'o', 0.06), ('lamina', 'o', 0.18)):
    xs = [np.log2(s.get(f'first5_enrich_{k}') or np.nan) for s in order]
    ax.scatter(xs, ys + off, s=90, color=C[k], edgecolor=PAPER, linewidth=1.5, zorder=3,
               label={'inner': 'inner band (control)'}.get(k, k), marker=mk if k != 'inner' else 'D')
ax.axvline(0, color=INK2, lw=1.2)
why = lambda s: '' if s['pooled'] else ' · ' + ('motion' if s['motion_flag'] else 'mask' if not s['mask_ok'] else 'step')
ax.set_yticks(ys); ax.set_yticklabels([f"expt {int(s['tag'][4:])}{why(s)}" for s in order])
for tl, s in zip(ax.get_yticklabels(), order):
    tl.set_color(INK if s['pooled'] else '#9a9890')
ax.set_xticks([-3, -2, -1, 0, 1, 2]); ax.set_xticklabels(['⅛×', '¼×', '½×', '1×', '2×', '4×'])
ax.set_xlabel('share of the earliest 5% of pixels ÷ share of area (1× = no enrichment)')
ax.legend(frameon=False, ncol=4, loc='upper center', bbox_to_anchor=(0.5, 1.09), fontsize=15)
fig.tight_layout(); fig.savefig(os.path.join(OUT, 'enrichment_all_runs.png'), dpi=100, facecolor=PAPER); plt.close(fig)

# ---- table for results/
import csv
keys = ['tag', 'file', 'frames', 'duration_s', 't_settle_s', 'max_reg_shift_px', 'late_motion_steps', 'plant_area_mm2', 'frac_valid',
        'plant_level_at_settle_counts', 'plant_rise_counts', 'plant_trace_tpeak_s', 't50_p5_s', 't50_median_s',
        'margin_t50_median_s', 'inner_t50_median_s', 'vein_t50_median_s', 'lamina_t50_median_s',
        'first5_enrich_margin', 'first5_enrich_inner', 'first5_enrich_vein', 'first5_enrich_lamina', 'bg_residual_max_abs_counts',
        'max_post_settle_step_px', 'motion_flag', 'step_flag', 'mask_ok', 'pooled', 'fast6s_plant_counts',
        'fast6s_background_counts', 'qc_note']
with open(os.path.join(OUT, 'summary_all_runs.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['label'] + keys)
    for s in order: w.writerow([label(s['file'])] + [s.get(k) if not isinstance(s.get(k), float) else round(s[k], 3) for k in keys])

# ---- pooled summary over QC-passing runs
from scipy.stats import binomtest
P = [s for s in order if s['pooled']]
pooled = dict(runs=[s['tag'] for s in P], n=len(P),
              excluded={s['tag']: ('motion' if s['motion_flag'] else 'mask' if not s['mask_ok'] else 'step at settle') for s in order if not s['pooled']})
for k in ('margin', 'inner', 'vein', 'lamina'):
    v = [s[f'first5_enrich_{k}'] for s in P if s.get(f'first5_enrich_{k}') is not None]
    pooled[f'enrich_{k}_median'] = float(np.median(v)) if v else None
    pooled[f'enrich_{k}_range'] = [float(min(v)), float(max(v))] if v else None
diff = [s['first5_enrich_margin'] - s['first5_enrich_inner'] for s in P]
k_up = int(sum(d > 0 for d in diff)); pooled['margin_gt_inner_runs'] = f'{k_up} of {len(diff)}'
pooled['margin_gt_inner_sign_test_p_two_sided'] = float(binomtest(k_up, len(diff), 0.5).pvalue) if diff else None
for k in ('t_settle_s', 't50_median_s', 'plant_trace_tpeak_s', 'plant_rise_counts', 'plant_level_at_settle_counts'):
    v = [s[k] for s in P]; pooled[f'{k}_median'] = float(np.median(v)); pooled[f'{k}_range'] = [float(min(v)), float(max(v))]
json.dump(pooled, open(os.path.join(OUT, 'pooled_summary.json'), 'w'), indent=1)
print(json.dumps(pooled, indent=1))
print('ok')
