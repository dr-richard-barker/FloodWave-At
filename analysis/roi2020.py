import sys, json, numpy as np, czifile, cv2
from PIL import Image
czi, slide_img, outjson = sys.argv[1:4]
with czifile.CziFile(czi) as c:
    sbs = sorted(c.filtered_subblock_directory, key=lambda s: s.start[s.axes.index('T')])
    ts = next(np.asarray(x.data(), float) for x in c.attachments() if x.attachment_entry.name == 'TimeStamps')
    raw = np.stack([np.squeeze(sb.data_segment().data()).astype(np.float32) for sb in sbs])
t = ts - ts[0]
ref = np.median(raw[436-5:436+5], 0)          # raw frame 436 = video frame 396 = the '06:36' slide frame
im = np.asarray(Image.open(slide_img).convert('RGB')).astype(np.float32)
g = im.mean(2)
best = None
for s in np.arange(0.55, 1.0, 0.005):
    gs = cv2.resize(g, None, fx=s, fy=s, interpolation=cv2.INTER_AREA)
    if gs.shape[0] > ref.shape[0] or gs.shape[1] > ref.shape[1]: continue
    r = cv2.matchTemplate(cv2.GaussianBlur(ref, (0, 0), 1.5), cv2.GaussianBlur(gs, (0, 0), 1.5), cv2.TM_CCOEFF_NORMED)
    _, mv, _, loc = cv2.minMaxLoc(r)
    if best is None or mv > best[0]: best = (mv, s, loc)
mv, s, (x0, y0) = best
print(f'slide image -> raw: scale {s:.3f}, offset ({x0},{y0}), NCC {mv:.3f}')
# ROI centres/radii read off the slide image (px in the 782x619 image), labels as in the 2020 legend order
rois = {1: (516, 227, 18), 2: (569, 178, 18), 3: (121, 468, 18), 4: (163, 525, 18), 5: (86, 514, 18), 6: (464, 333, 31), 7: (436, 119, 18)}
legend = {1: 'Hydrathode-1', 2: 'Hydrathode-2', 3: 'Lamina-1', 4: 'Lamina-2', 5: 'Lamina-3', 6: 'Mersitem-1', 7: 'Hydrathode-3'}
yy, xx = np.indices(ref.shape); res = {}
for k, (cx, cy, r) in rois.items():
    X, Y, R = x0 + cx * s, y0 + cy * s, r * s
    msk = (xx - X) ** 2 + (yy - Y) ** 2 <= R ** 2
    res[k] = dict(label=legend[k], x=float(X), y=float(Y), r=float(R), mean=raw[:, msk].mean(1).tolist(), sd=raw[:, msk].std(1).tolist())
json.dump(dict(scale=s, x0=x0, y0=y0, ncc=mv, t=t.tolist(), rois=res), open(outjson, 'w'))

# ---- background-subtracted ROI means (same additive local-background model as flood_wave.py, full resolution)
from scipy import ndimage as ndi
from skimage.filters import threshold_otsu
from skimage.morphology import remove_small_objects, binary_opening, disk
late = ndi.gaussian_filter(np.median(raw[int(len(raw) * 0.8):], 0), 2)
flat = late - ndi.gaussian_filter(late, 80)
m = flat > threshold_otsu(flat)
m = remove_small_objects(binary_opening(m, disk(2)), max_size=600)
m = ndi.binary_fill_holes(m)
lab, nlab = ndi.label(m)
if nlab > 1:
    sizes = ndi.sum(m, lab, range(1, nlab + 1)); m = np.isin(lab, 1 + np.where(sizes >= 0.05 * sizes.max())[0])
bgm = ~ndi.binary_dilation(m, disk(8))
w = ndi.gaussian_filter(bgm.astype(np.float32), 24)
dist = ndi.distance_transform_edt(m)
out = json.load(open(outjson))
masks = {}
for k, r in out['rois'].items():
    masks[k] = (xx - r['x']) ** 2 + (yy - r['y']) ** 2 <= r['r'] ** 2
    r['edge_dist_um_centre'] = float(dist[int(round(r['y'])), int(round(r['x']))] * 20.4925)
    r['frac_on_plant'] = float(m[masks[k]].mean())
sub = {k: [] for k in masks}
for f in raw:
    B = ndi.gaussian_filter(f * bgm, 24) / np.maximum(w, 1e-3)
    for k, mk in masks.items(): sub[k].append(float((f - B)[mk].mean()))
for k in masks: out['rois'][k]['mean_bgsub'] = sub[k]
json.dump(out, open(outjson, 'w'))
for k, r in out['rois'].items(): print(k, r['label'], 'centre-to-leaf-edge %.0f um' % r['edge_dist_um_centre'], 'on-plant %.2f' % r['frac_on_plant'])
