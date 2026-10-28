"""Render a short MP4 of one run for the deck: registered fluorescence (left) and
signal change since motion settled, in counts above local background (right).

Uses the same binning, registration and background model as flood_wave.py, and
that run's saved plant mask and settle frame (results/runs/<tag>/<tag>_maps.npz).
The burned-in clock is true time from the start of recording (ZEN TimeStamps).

usage: make_clip.py <run.czi> <maps.npz> <qc.json> <out.mp4> <still.png> [still_seconds]
"""
import json, os, re, subprocess, sys
import numpy as np
import czifile
from scipy import ndimage as ndi
from skimage.registration import phase_cross_correlation
from skimage.morphology import disk
from PIL import Image, ImageDraw, ImageFont
import matplotlib; matplotlib.use('Agg')
from matplotlib.colors import LinearSegmentedColormap

czi, mapsf, qcf, out_mp4, out_png = sys.argv[1:6]
still_s = float(sys.argv[6]) if len(sys.argv) > 6 else 600.0
tag = 'expt%02d' % int(re.match(r'Flooding expt (\d+)', os.path.basename(czi)).group(1))
z = np.load(mapsf); m = z['mask']; i_settle = int(z['i_settle'])

with czifile.CziFile(czi) as c:
    ts = next(np.asarray(x.data(), float) for x in c.attachments() if x.attachment_entry.name == 'TimeStamps')
    sbs = sorted(c.filtered_subblock_directory, key=lambda s: s.start[s.axes.index('T')])
    S = np.stack([np.squeeze(sb.data_segment().data()).astype(np.float32).reshape(260, 2, 346, 2).mean((1, 3)) for sb in sbs])
t = ts - ts[0]; T = len(S)

def hp(im):
    return ndi.gaussian_filter(im, 1.5) - ndi.gaussian_filter(im, 15)
ref = hp(np.median(S[int(T * 0.8):], 0))
for i in range(T):
    sh = phase_cross_correlation(ref, hp(S[i]), upsample_factor=10, normalization=None)[0]
    if np.hypot(*sh) > 0.05:
        S[i] = ndi.shift(S[i], sh, order=1, mode='nearest')
S = ndi.gaussian_filter(S, (0, 1, 1))

excl = np.zeros(m.shape, bool)
for x0, y0, x1, y1 in json.load(open(qcf)).get(tag, {}).get('exclude_boxes', []):
    excl[y0 // 2:y1 // 2, x0 // 2:x1 // 2] = True
bg = ~ndi.binary_dilation(m, disk(4)) & ~ndi.binary_dilation(excl, disk(4))
w = ndi.gaussian_filter(bg.astype(np.float32), 12)
Fc = np.stack([f - ndi.gaussian_filter(f * bg, 12) / np.maximum(w, 1e-3) for f in S])
Fc = ndi.uniform_filter1d(Fc, 5, axis=0)
dF = Fc - Fc[i_settle:i_settle + 5].mean(0)

AMBER = LinearSegmentedColormap.from_list('amber', ['#3a1f05', '#c97a12', '#f2b94b', '#fff1c9'])
glo, ghi = np.percentile(S[int(T * 0.8):], [1, 99.7])
vmax = float(np.percentile(dF[i_settle:][:, m], 99))
UP = 2; W, H = 346 * UP, 260 * UP; PAD, TOP, BOT = 24, 92, 80
CW, CH = 2 * W + 3 * PAD, H + TOP + BOT
CW += CW % 2; CH += CH % 2
f_big = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 30)
f_med = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 22)
BG, INK, MUTE = (18, 24, 29), (244, 242, 236), (191, 200, 204)

def frame(i):
    g = np.clip((S[i] - glo) / (ghi - glo), 0, 1)
    left = (np.stack([g] * 3, -1) * 255).astype(np.uint8)
    base = (np.stack([g] * 3, -1) * 0.35 * 255).astype(np.uint8)
    right = base.copy()
    if i >= i_settle:
        col = (AMBER(np.clip(dF[i] / vmax, 0, 1))[..., :3] * 255).astype(np.uint8)
        right[m] = col[m]
    canvas = Image.new('RGB', (CW, CH), BG)
    for k, arr in enumerate((left, right)):
        canvas.paste(Image.fromarray(arr).resize((W, H), Image.NEAREST), (PAD + k * (W + PAD), TOP))
    d = ImageDraw.Draw(canvas)
    mm, ss = divmod(t[i], 60)
    d.text((PAD, 18), f'expt 8  ·  {int(mm):02d}:{ss:04.1f} from start of recording', font=f_big, fill=INK)
    d.text((PAD, 58), 'registered fluorescence (GFP channel)', font=f_med, fill=MUTE)
    d.text((2 * PAD + W, 58), 'signal change since motion settled (counts above local background)' if i >= i_settle
           else f'water arriving, sample moving: map starts at {t[i_settle]:.0f} s', font=f_med, fill=MUTE)
    sx = PAD + 10; sy = TOP + H - 18
    d.line([(sx, sy), (sx + int(2000 / 40.985 * UP), sy)], fill=INK, width=4); d.text((sx, sy - 30), '2 mm', font=f_med, fill=INK)
    bx, by, bw = 2 * PAD + W, TOP + H + 22, 360
    bar = (AMBER(np.linspace(0, 1, bw))[:, :3] * 255).astype(np.uint8)[None].repeat(14, 0)
    canvas.paste(Image.fromarray(bar), (bx, by))
    d.text((bx, by + 20), '0', font=f_med, fill=MUTE); d.text((bx + bw - 60, by + 20), f'+{vmax:.0f}', font=f_med, fill=MUTE)
    d.text((PAD, TOP + H + 22), 'raw file, read only · 1 frame = 1.21 s · played at 30 fps', font=f_med, fill=MUTE)
    return canvas

proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{CW}x{CH}', '-r', '30', '-i', '-',
                         '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '24', '-preset', 'slow', '-movflags', '+faststart', out_mp4],
                        stdin=subprocess.PIPE)
for i in range(T):
    proc.stdin.write(frame(i).tobytes())
proc.stdin.close(); proc.wait()
frame(int(np.searchsorted(t, still_s))).save(out_png)
info = dict(tag=tag, frames=T, size=[CW, CH], fps=30, clip_seconds=T / 30, frame_interval_s=float(np.median(np.diff(t))),
            run_seconds=float(t[-1]), settle_s=float(t[i_settle]), dF_scale_counts=vmax,
            still_s=float(t[int(np.searchsorted(t, still_s))]), mp4_bytes=os.path.getsize(out_mp4))
json.dump(info, open(os.path.splitext(out_mp4)[0] + '.json', 'w'), indent=1)
print(json.dumps(info))
