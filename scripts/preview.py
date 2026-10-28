import sys, os, re, json, czifile, numpy as np
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
outdir = sys.argv[1]; srcs = sys.argv[2:]
qc = {}
for src in srcs:
    base = os.path.basename(src)
    m = re.match(r'Flooding expt (\d+)', base); n = int(m.group(1))
    tag = f'expt{n:02d}'
    with czifile.CziFile(src) as c:
        ts = None
        for a in c.attachments():
            if a.attachment_entry.name == 'TimeStamps': ts = np.asarray(a.data(), float)
        sbs = sorted(c.filtered_subblock_directory, key=lambda s: s.start[s.axes.index('T')])
        T = len(sbs)
        pick = sorted(set([0, T//4, T//2, 3*T//4, T-1]))
        mx = None; mean = np.zeros(T); p99 = np.zeros(T); sat = np.zeros(T); dif = np.zeros(T); frames = {}
        prev = None
        for i, sb in enumerate(sbs):
            a = np.squeeze(sb.data_segment().data()).astype(np.float32)
            mx = a if mx is None else np.maximum(mx, a)
            mean[i] = a.mean(); p99[i] = np.percentile(a, 99); sat[i] = (a >= 4095).mean()
            if prev is not None: dif[i] = np.abs(a - prev).mean()
            prev = a
            if i in pick: frames[i] = a
            if i == 0: amin, amax = a.min(), a.max()
            else: amin, amax = min(amin, a.min()), max(amax, a.max())
    t = ts - ts[0] if ts is not None else np.arange(T)*1.218
    lo, hi = np.percentile(np.stack(list(frames.values())), [0.5, 99.8])
    fig, axs = plt.subplots(2, 3, figsize=(15, 7.6))
    for ax, i in zip(axs.flat[:5], pick):
        ax.imshow(frames[i], cmap='gray', vmin=lo, vmax=hi); ax.set_title(f'frame {i}  t={t[i]:.0f} s', fontsize=10); ax.axis('off')
    ax = axs.flat[5]; ax.imshow(mx, cmap='gray', vmin=lo, vmax=np.percentile(mx, 99.8)); ax.set_title('max over time', fontsize=10); ax.axis('off')
    # scale bar 2 mm at 20.49 um/px
    px = 2000/20.4925; axs.flat[0].plot([20, 20+px], [500, 500], 'w-', lw=3); axs.flat[0].text(20, 485, '2 mm', color='w', fontsize=9)
    fig.suptitle(f'{base}  |  EGFP channel (ex 450-490 / em 500-550), {T} frames, display {lo:.0f}-{hi:.0f} counts (same for 5 frames)', fontsize=10)
    fig.tight_layout(); fig.savefig(os.path.join(outdir, f'{tag}_frames.png'), dpi=80); plt.close(fig)
    fig, axs = plt.subplots(3, 1, figsize=(10, 6.5), sharex=True)
    axs[0].plot(t, mean, lw=0.8); axs[0].set_ylabel('whole-field mean')
    axs[1].plot(t, p99, lw=0.8, color='C1'); axs[1].set_ylabel('whole-field p99')
    axs[2].plot(t, dif, lw=0.8, color='C2'); axs[2].set_ylabel('mean |frame diff|'); axs[2].set_xlabel('time from first frame (s)')
    fig.suptitle(f'{base}: QC traces (whole field, no ROI, not a result)', fontsize=10)
    fig.tight_layout(); fig.savefig(os.path.join(outdir, f'{tag}_qc_traces.png'), dpi=80); plt.close(fig)
    qc[tag] = dict(file=base, frames=T, min=float(amin), max=float(amax), sat_frac_max=float(sat.max()),
                   mean_first10=float(mean[:10].mean()), mean_last10=float(mean[-10:].mean()),
                   diff_median=float(np.median(dif[1:])), diff_max=float(dif.max()), diff_argmax_s=float(t[int(dif.argmax())]),
                   duration_s=float(t[-1]))
    print(json.dumps(qc[tag]), flush=True)
json.dump(qc, open(os.path.join(outdir, '..', 'metadata', 'qc_stats.json'), 'w'), indent=1)
