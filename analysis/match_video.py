import sys, numpy as np, czifile, av, cv2
czi, vid = sys.argv[1], sys.argv[2]
with czifile.CziFile(czi) as c:
    sbs = sorted(c.filtered_subblock_directory, key=lambda s: s.start[s.axes.index('T')])
    ts = next(np.asarray(x.data(), float) for x in c.attachments() if x.attachment_entry.name == 'TimeStamps')
    raw = np.stack([np.squeeze(sb.data_segment().data()).astype(np.float32) for sb in sbs])
c = av.open(vid); frames = [f.to_ndarray(format='gray').astype(np.float32) for f in c.decode(video=0)]
V = np.stack(frames); print('video', V.shape, 'czi', raw.shape)
# spatial mapping: template-match a downscaled video frame inside the raw frame at several scales
ref_raw = raw[350]; best = None
for s in np.arange(0.70, 1.31, 0.01):
    v = cv2.resize(V[300], None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
    if v.shape[0] > raw.shape[1] or v.shape[1] > raw.shape[2]: continue
    r = cv2.matchTemplate(cv2.normalize(ref_raw, None, 0, 1, cv2.NORM_MINMAX), cv2.normalize(v, None, 0, 1, cv2.NORM_MINMAX), cv2.TM_CCOEFF_NORMED)
    _, mv, _, loc = cv2.minMaxLoc(r)
    if best is None or mv > best[0]: best = (mv, s, loc)
mv, s, (x0, y0) = best; print(f'best scale video->raw {s:.2f}, offset x={x0} y={y0}, ncc={mv:.3f}')
h, w = (np.array(V.shape[1:]) * s).round().astype(int)
crop = raw[:, y0:y0+h, x0:x0+w]
cs = np.stack([cv2.resize(f, (V.shape[2], V.shape[1]), interpolation=cv2.INTER_AREA) for f in crop])
def z(a): a = a - a.mean((1, 2), keepdims=True); return a / (a.std((1, 2), keepdims=True) + 1e-6)
# temporal mapping: correlate frame-mean time courses and a few frames
vm, cm = V.mean((1, 2)), cs.mean((1, 2))
best_o = max(range(0, raw.shape[0] - V.shape[0] + 1), key=lambda o: np.corrcoef(vm, cm[o:o+V.shape[0]])[0, 1])
print('best frame offset (video frame 0 = raw frame):', best_o, 'corr', round(np.corrcoef(vm, cm[best_o:best_o+V.shape[0]])[0, 1], 4),
      '-> time', round(ts[best_o]-ts[0], 2), 's to', round(ts[best_o+V.shape[0]-1]-ts[0], 2), 's')
zv, zc = z(V[::60]), z(cs[best_o:best_o+V.shape[0]][::60])
print('per-frame spatial corr (every 60th):', np.round((zv*zc).mean((1, 2)), 3))
# intensity mapping raw -> 8 bit
sel = cs[best_o:best_o+V.shape[0]].ravel()[::997]; vv = V.ravel()[::997]
A = np.polyfit(sel, vv, 1); print('linear raw->8bit fit: gain %.4f offset %.1f (8-bit = gain*raw + offset)' % tuple(A), 'clip frac', round((vv>=254).mean(), 4), round((vv<=1).mean(), 4))
