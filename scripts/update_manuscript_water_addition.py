#!/usr/bin/env python3
"""
Update manuscript/FloodWave_NatureCommunications_Perspective.md and docs/manuscript.html
with Section 4 narrative on experimental timing / water addition dynamics,
embed Figure 5 (water_addition_timeline.png), and update Table 3 with Water Addition Window (s).
"""
import re

def update_markdown_manuscript():
    md_path = "manuscript/FloodWave_NatureCommunications_Perspective.md"
    with open(md_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Narrative block to insert
    timing_narrative = """### Reconstructing Experimental Timing and Water Addition Dynamics
A critical ambiguity in unannotated historical time-lapse imaging is separating the initiation of the camera from the physical delivery of the experimental stimulus. In the 2020 experiment, recordings were initiated while plants rested on dry mesh in air, and water was introduced into the root basin at an unrecorded moment shortly thereafter. Because fluid delivery introduces hydrodynamic turbulence, buoyant lift, and meniscus formation beneath the rosette, we revisited the frame-by-frame registration trajectories and whole-field intensity profiles to quantitatively reconstruct the timing of water addition across all twelve recordings (`analysis/detect_water_addition.py`; Fig. 5; Table 3):

1. **Phase 1: Quiescent Pre-Flood Baseline (0 s to *t*<sub>onset</sub>; median 24.3 s, range 12.1–48.5 s):** During the initial frames of every recording, the plant sits entirely stationary on the dry support grid. Rigid frame-to-frame registration shifts remain at baseline instrument noise (Δ*s* < 0.15 px ≈ 6.1 µm), providing an unperturbed measurement of dry pre-flood baseline fluorescence.
2. **Phase 2: Fluid Influx and Meniscus Surge (*t*<sub>onset</sub> to *t*<sub>settle</sub>; median window [24.3 s, 73.9 s], median duration 38.6 s):** Fluid arrival produces a sharp mechanical onset (*t*<sub>onset</sub>), followed by a surge in frame-to-frame displacement peaking at a median of **35.2 s** (ranging up to 228.8 px in `expt01`, 9.4 px in `expt09`, and 1.41 px in the representative run `expt08`). During this ~10–60 s window, rising water contacts the sub-rosette grid, establishes fluid menisci around petioles, and causes transient buoyant tilting or lateral drift before fluid motion subsides (*t*<sub>settle</sub>; median 73.9 s, range 20.6–124.9 s).
3. **Phase 3: Post-Settle Signaling and Whole-Plant Wave (*t* > *t*<sub>settle</sub>):** Once hydrodynamic motion settles, the tissue stabilizes within the focal plane, and physiological whole-plant GCaMP fluorescence begins its gradual, minutes-scale systemic rise.

Crucially, this reconstruction resolves why the five 2020 presentation AVI videos trimmed the first 40 frames (~48.5 s in `expt08`): frames 0–11 (0–14.6 s) constituted the quiescent dry baseline, while frames 12–39 (14.6–48.5 s, peak surge at 36.4 s) encompassed the water addition and fluid turbulence. Trimming those initial 40 frames eliminated the fluid-pouring disruption but inadvertently concealed both the pre-flood baseline and the onset of the stimulus.

![Figure 5: Experimental Timeline of Water Addition, Hydrodynamic Meniscus Surge, and Post-Settle Signaling Across All 12 Widefield GCaMP Recordings](../docs/assets/figures/water_addition_timeline.png)
**Figure 5 | Experimental timeline of water addition, hydrodynamic meniscus surge, and post-settle signaling across all twelve widefield GCaMP recordings (`analysis/detect_water_addition.py`).** Horizontal bars delineate the three physical phases for each recording: quiescent dry baseline (light grey, registration step Δ*s* < 0.15 px; median 24.3 s), fluid influx and meniscus formation window (teal, median duration 38.6 s; diamond marker indicates peak hydrodynamic surge, median 35.2 s, with maximum step size in pixels), and post-settle physiological signaling analysis window (dark blue; > *t*<sub>settle</sub>, median 73.9 s). The representative run `expt08` shows water onset at 14.6 s, peak surge at 36.4 s (1.41 px), and settling at 48.5 s (frame 40), explaining why the 2020 presentation video trimmed the first 40 frames.

---
"""

    # Insert timing_narrative before "### Deconstructing the 2020" if not already present
    if "### Reconstructing Experimental Timing and Water Addition Dynamics" not in content:
        target = "### Deconstructing the 2020 \"Seconds-Scale Hydathode Wave\""
        if target in content:
            content = content.replace(target, timing_narrative + "\n" + target)
        else:
            print("Target for markdown narrative not found!")

    # Update Table 3 in markdown
    old_table_header = "| Run (`tag`) | Filename Label | ZEN # | Frames (*T*) | Duration (s) | Settle Time `t_settle` (s) | Median *t*₅₀ (s) | Peak Time (s) | Whole-Plant Rise (counts) | Earliest-5% Enrichment: Margin | Inner Band | Veins | Lamina | QC Status & Notes |\n| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |"
    
    new_table_header = "| Run (`tag`) | Filename Label | ZEN # | Frames (*T*) | Duration (s) | Water Window (s) | Settle Time `t_settle` (s) | Median *t*₅₀ (s) | Peak Time (s) | Whole-Plant Rise (counts) | Earliest-5% Enrichment: Margin | Inner Band | Veins | Lamina | QC Status & Notes |\n| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |"

    table_rows = [
        ("| `expt01` | *(no label)* | 454 | 451 | 545.8 | 111.5 |", "| `expt01` | *(no label)* | 454 | 451 | 545.8 | 48.5–111.5 | 111.5 |"),
        ("| `expt02` | *(no label)* | 455 | 499 | 603.9 | 36.4 |", "| `expt02` | *(no label)* | 455 | 499 | 603.9 | 30.3–36.4 | 36.4 |"),
        ("| `expt03` | *(no label)* | 456 | 430 | 520.0 | 34.0 |", "| `expt03` | *(no label)* | 456 | 430 | 520.0 | 26.7–34.0 | 34.0 |"),
        ("| `expt04` | *(no label)* | 457 | 198 | 238.9 | 40.0 |", "| `expt04` | *(no label)* | 457 | 198 | 238.9 | 26.7–40.0 | 40.0 |"),
        ("| `expt05` | `NormalWater` | 459 | 428 | 517.7 | 124.9 |", "| `expt05` | `NormalWater` | 459 | 428 | 517.7 | 21.8–124.9 | 124.9 |"),
        ("| `expt06` | `NW YoungLeaf` | 460 | 476 | 576.0 | 67.9 |", "| `expt06` | `NW YoungLeaf` | 460 | 476 | 576.0 | 25.5–67.9 | 67.9 |"),
        ("| `expt07` | `NW YoungLeaf` | 461 | 601 | 727.5 | 72.7 |", "| `expt07` | `NW YoungLeaf` | 461 | 601 | 727.5 | 21.8–72.7 | 72.7 |"),
        ("| `expt08` | `NW small (rep.)` | 463 | 700 | 847.5 | 48.5 |", "| `expt08` | `NW small (rep.)` | 463 | 700 | 847.5 | 14.6–48.5 | 48.5 |"),
        ("| `expt09` | `NW small plant` | 464 | 1140 | 1381.7 | 75.2 |", "| `expt09` | `NW small plant` | 464 | 1140 | 1381.7 | 17.0–75.2 | 75.2 |"),
        ("| `expt10` | `NW Medium plant` | 466 | 1015 | 1229.4 | 20.6 |", "| `expt10` | `NW Medium plant` | 466 | 1015 | 1229.4 | 12.1–20.6 | 20.6 |"),
        ("| `expt11` | `NW small plant` | 465 | 914 | 1106.9 | 83.7 |", "| `expt11` | `NW small plant` | 465 | 914 | 1106.9 | 26.7–83.7 | 83.7 |"),
        ("| `expt12` | `NW YoungLeaf` | 462 | 324 | 391.6 | 61.8 |", "| `expt12` | `NW YoungLeaf` | 462 | 324 | 391.6 | 24.3–61.8 | 61.8 |"),
        ("| **Pooled Median** | **8 QC-passing runs** | — | — | — | **73.9** |", "| **Pooled Median** | **8 QC-passing runs** | — | — | — | **24.3–73.9** | **73.9** |"),
    ]

    if old_table_header in content:
        content = content.replace(old_table_header, new_table_header)
        for old_row, new_row in table_rows:
            content = content.replace(old_row, new_row)
        print("Updated Table 3 in markdown")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(content)


def update_html_manuscript():
    html_path = "docs/manuscript.html"
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    timing_html = """      <h3>Reconstructing Experimental Timing and Water Addition Dynamics</h3>
      <p>
        A critical ambiguity in unannotated historical time-lapse imaging is separating the initiation of the camera from the physical delivery of the experimental stimulus. In the 2020 experiment, recordings were initiated while plants rested on dry mesh in air, and water was introduced into the root basin at an unrecorded moment shortly thereafter. Because fluid delivery introduces hydrodynamic turbulence, buoyant lift, and meniscus formation beneath the rosette, we revisited the frame-by-frame registration trajectories and whole-field intensity profiles to quantitatively reconstruct the timing of water addition across all twelve recordings (<code>analysis/detect_water_addition.py</code>; Fig. 5; Table 3):
      </p>
      <ol>
        <li><strong>Phase 1: Quiescent Pre-Flood Baseline (0 s to <em>t</em><sub>onset</sub>; median 24.3 s, range 12.1–48.5 s):</strong> During the initial frames of every recording, the plant sits entirely stationary on the dry support grid. Rigid frame-to-frame registration shifts remain at baseline instrument noise (&Delta;<em>s</em> &lt; 0.15 px &asymp; 6.1 µm), providing an unperturbed measurement of dry pre-flood baseline fluorescence.</li>
        <li><strong>Phase 2: Fluid Influx and Meniscus Surge (<em>t</em><sub>onset</sub> to <em>t</em><sub>settle</sub>; median window [24.3 s, 73.9 s], median duration 38.6 s):</strong> Fluid arrival produces a sharp mechanical onset (<em>t</em><sub>onset</sub>), followed by a surge in frame-to-frame displacement peaking at a median of <strong>35.2 s</strong> (ranging up to 228.8 px in <code>expt01</code>, 9.4 px in <code>expt09</code>, and 1.41 px in the representative run <code>expt08</code>). During this ~10–60 s window, rising water contacts the sub-rosette grid, establishes fluid menisci around petioles, and causes transient buoyant tilting or lateral drift before fluid motion subsides (<em>t</em><sub>settle</sub>; median 73.9 s, range 20.6–124.9 s).</li>
        <li><strong>Phase 3: Post-Settle Signaling and Whole-Plant Wave (<em>t</em> &gt; <em>t</em><sub>settle</sub>):</strong> Once hydrodynamic motion settles, the tissue stabilizes within the focal plane, and physiological whole-plant GCaMP fluorescence begins its gradual, minutes-scale systemic rise.</li>
      </ol>
      <p>
        Crucially, this reconstruction resolves why the five 2020 presentation AVI videos trimmed the first 40 frames (~48.5 s in <code>expt08</code>): frames 0–11 (0–14.6 s) constituted the quiescent dry baseline, while frames 12–39 (14.6–48.5 s, peak surge at 36.4 s) encompassed the water addition and fluid turbulence. Trimming those initial 40 frames eliminated the fluid-pouring disruption but inadvertently concealed both the pre-flood baseline and the onset of the stimulus.
      </p>

      <figure class="manuscript-figure">
        <img src="assets/figures/water_addition_timeline.png" alt="Figure 5: Experimental Timeline of Water Addition, Hydrodynamic Meniscus Surge, and Post-Settle Signaling Across All 12 Widefield GCaMP Recordings" data-title="Figure 5: Experimental Timeline of Water Addition Across All 12 Runs" class="zoomable-fig">
        <figcaption>
          <strong>Figure 5 | Experimental timeline of water addition, hydrodynamic meniscus surge, and post-settle signaling across all twelve widefield GCaMP recordings (<code>analysis/detect_water_addition.py</code>).</strong> Horizontal timeline bars delineate the three physical phases for each recording: quiescent dry baseline (light grey, registration step &Delta;<em>s</em> &lt; 0.15 px; median 24.3 s), fluid influx and meniscus formation window (teal, median duration 38.6 s; diamond marker indicates peak hydrodynamic surge, median 35.2 s, with maximum step size in pixels), and post-settle physiological signaling analysis window (dark blue; &gt; <em>t</em><sub>settle</sub>, median 73.9 s). The representative run <code>expt08</code> shows water onset at 14.6 s, peak surge at 36.4 s (1.41 px), and settling at 48.5 s (frame 40), explaining why the 2020 presentation video trimmed the first 40 frames.
        </figcaption>
      </figure>
"""

    if "<h3>Reconstructing Experimental Timing and Water Addition Dynamics</h3>" not in content:
        target = "<h3>Deconstructing the 2020 “Seconds-Scale Hydathode Wave”</h3>"
        if target in content:
            content = content.replace(target, timing_html + "\n      " + target)
            print("Inserted timing narrative into docs/manuscript.html")
        else:
            print("Target for html narrative not found!")

    # Table 3 HTML block
    table3_html = """      <div class="table-scroll" style="margin:1.75rem 0">
        <table class="data-table">
          <caption><strong>Table 3 | Complete quantitative summary of all twelve widefield GCaMP recordings (<code>results/summary_all_runs.csv</code>, <code>results/water_addition_windows.json</code>, and <code>results/pooled_summary.json</code>).</strong> &dagger;Signal still rising at manual stop of recording.</caption>
          <thead>
            <tr>
              <th>Run (<code>tag</code>)</th>
              <th>Filename Label</th>
              <th>ZEN #</th>
              <th>Frames (<em>T</em>)</th>
              <th>Duration (s)</th>
              <th>Water Window (s)</th>
              <th>Settle Time <em>t</em><sub>settle</sub> (s)</th>
              <th>Median <em>t</em><sub>50</sub> (s)</th>
              <th>Peak Time (s)</th>
              <th>Whole-Plant Rise (counts)</th>
              <th>Margin 5%</th>
              <th>Inner Band</th>
              <th>Veins</th>
              <th>Lamina</th>
              <th>QC Status &amp; Notes</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><code>expt01</code></td>
              <td><em>(no label)</em></td>
              <td>454</td>
              <td>451</td>
              <td>545.8</td>
              <td>48.5–111.5</td>
              <td>111.5</td>
              <td>328.7</td>
              <td>485.1</td>
              <td>77.1</td>
              <td><strong>1.48&times;</strong></td>
              <td>0.71&times;</td>
              <td><strong>1.84&times;</strong></td>
              <td>0.74&times;</td>
              <td><span class="badge badge-success">Pooled</span> (3 mm FOV jump at 96 s; analyzed post-settle)</td>
            </tr>
            <tr>
              <td><code>expt02</code></td>
              <td><em>(no label)</em></td>
              <td>455</td>
              <td>499</td>
              <td>603.9</td>
              <td>30.3–36.4</td>
              <td>36.4</td>
              <td>479.1</td>
              <td>576.0</td>
              <td>100.3</td>
              <td>1.09&times;</td>
              <td>0.68&times;</td>
              <td>1.88&times;</td>
              <td>0.81&times;</td>
              <td><span class="badge badge-warning">Excluded (motion)</span> detached leaf drifts/rotates</td>
            </tr>
            <tr>
              <td><code>expt03</code></td>
              <td><em>(no label)</em></td>
              <td>456</td>
              <td>430</td>
              <td>520.0</td>
              <td>26.7–34.0</td>
              <td>34.0</td>
              <td>127.3</td>
              <td>515.2</td>
              <td>51.2</td>
              <td>1.35&times;</td>
              <td>0.98&times;</td>
              <td>0.25&times;</td>
              <td>1.05&times;</td>
              <td><span class="badge badge-warning">Excluded (mask)</span> out-of-focus sub-mesh debris</td>
            </tr>
            <tr>
              <td><code>expt04</code></td>
              <td><em>(no label)</em></td>
              <td>457</td>
              <td>198</td>
              <td>238.9</td>
              <td>26.7–40.0</td>
              <td>40.0</td>
              <td>58.2</td>
              <td>197.7</td>
              <td>8.0</td>
              <td>1.15&times;</td>
              <td>1.27&times;</td>
              <td>1.24&times;</td>
              <td>0.81&times;</td>
              <td><span class="badge badge-warning">Excluded (mask/step)</span> badly out of focus; 4-min run</td>
            </tr>
            <tr>
              <td><code>expt05</code></td>
              <td><code>NormalWater</code></td>
              <td>459</td>
              <td>428</td>
              <td>517.7</td>
              <td>21.8–124.9</td>
              <td>124.9</td>
              <td>266.7</td>
              <td>510.4&dagger;</td>
              <td>48.1</td>
              <td><strong>1.46&times;</strong></td>
              <td>0.84&times;</td>
              <td>0.69&times;</td>
              <td>1.00&times;</td>
              <td><span class="badge badge-success">Pooled</span></td>
            </tr>
            <tr>
              <td><code>expt06</code></td>
              <td><code>NW YoungLeaf</code></td>
              <td>460</td>
              <td>476</td>
              <td>576.0</td>
              <td>25.5–67.9</td>
              <td>67.9</td>
              <td>248.5</td>
              <td>351.5</td>
              <td>25.6</td>
              <td>0.62&times;</td>
              <td>0.79&times;</td>
              <td><strong>2.15&times;</strong></td>
              <td>1.02&times;</td>
              <td><span class="badge badge-success">Pooled</span> (veins strongly lead)</td>
            </tr>
            <tr>
              <td><code>expt07</code></td>
              <td><code>NW YoungLeaf</code></td>
              <td>461</td>
              <td>601</td>
              <td>727.5</td>
              <td>21.8–72.7</td>
              <td>72.7</td>
              <td>317.6</td>
              <td>543.0</td>
              <td>66.4</td>
              <td><strong>1.29&times;</strong></td>
              <td>1.02&times;</td>
              <td>0.74&times;</td>
              <td>0.99&times;</td>
              <td><span class="badge badge-success">Pooled</span></td>
            </tr>
            <tr>
              <td><code>expt08</code></td>
              <td><code>NW small (rep.)</code></td>
              <td>463</td>
              <td>700</td>
              <td>847.5</td>
              <td>14.6–48.5</td>
              <td>48.5</td>
              <td>470.3</td>
              <td>695.8</td>
              <td>141.5</td>
              <td><strong>1.80&times;</strong></td>
              <td>1.34&times;</td>
              <td><strong>1.99&times;</strong></td>
              <td>0.36&times;</td>
              <td><span class="badge badge-success">Pooled</span> (2020 deck representative run)</td>
            </tr>
            <tr>
              <td><code>expt09</code></td>
              <td><code>NW small plant</code></td>
              <td>464</td>
              <td>1140</td>
              <td>1381.7</td>
              <td>17.0–75.2</td>
              <td>75.2</td>
              <td>459.6</td>
              <td>722.9</td>
              <td>105.5</td>
              <td><strong>2.38&times;</strong></td>
              <td>1.55&times;</td>
              <td>0.93&times;</td>
              <td>0.59&times;</td>
              <td><span class="badge badge-success">Pooled</span></td>
            </tr>
            <tr>
              <td><code>expt10</code></td>
              <td><code>NW Medium plant</code></td>
              <td>466</td>
              <td>1015</td>
              <td>1229.4</td>
              <td>12.1–20.6</td>
              <td>20.6</td>
              <td>252.1</td>
              <td>837.7</td>
              <td>108.3</td>
              <td>1.28&times;</td>
              <td>0.86&times;</td>
              <td>0.37&times;</td>
              <td>1.12&times;</td>
              <td><span class="badge badge-warning">Excluded (step)</span> 21-count simultaneous step in 6 s</td>
            </tr>
            <tr>
              <td><code>expt11</code></td>
              <td><code>NW small plant</code></td>
              <td>465</td>
              <td>914</td>
              <td>1106.9</td>
              <td>26.7–83.7</td>
              <td>83.7</td>
              <td>520.0</td>
              <td>917.7</td>
              <td>61.6</td>
              <td><strong>0.78&times;</strong></td>
              <td>0.57&times;</td>
              <td>0.24&times;</td>
              <td>1.42&times;</td>
              <td><span class="badge badge-success">Pooled</span> (margin &gt; inner band, lamina leads)</td>
            </tr>
            <tr>
              <td><code>expt12</code></td>
              <td><code>NW YoungLeaf</code></td>
              <td>462</td>
              <td>324</td>
              <td>391.6</td>
              <td>24.3–61.8</td>
              <td>61.8</td>
              <td>194.0</td>
              <td>391.6&dagger;</td>
              <td>31.2</td>
              <td><strong>1.34&times;</strong></td>
              <td>1.04&times;</td>
              <td>0.58&times;</td>
              <td>1.05&times;</td>
              <td><span class="badge badge-success">Pooled</span> (acquired before <code>expt08</code>)</td>
            </tr>
          </tbody>
          <tfoot>
            <tr style="font-weight:700;background:var(--bg-card)">
              <td>Pooled Median</td>
              <td>8 QC-passing runs</td>
              <td>—</td>
              <td>—</td>
              <td>—</td>
              <td>24.3–73.9</td>
              <td>73.9</td>
              <td>323.1</td>
              <td>526.7</td>
              <td>64.0</td>
              <td>1.40&times;</td>
              <td>0.93&times;</td>
              <td>0.84&times;</td>
              <td>0.99&times;</td>
              <td>Margin &gt; Inner Band in 7 of 8 runs (<em>p</em> = 0.070)</td>
            </tr>
          </tfoot>
        </table>
      </div>
"""

    if "Table 3 | Complete quantitative summary of all twelve widefield GCaMP recordings" not in content:
        # Insert after Table 2's closing </div>
        t2_marker = "All 12 <code>.czi</code> files on the drive are plain-water floods; no LaCl<sub>3</sub>-treated recordings exist in this dataset.</td>\n            </tr>\n          </tbody>\n        </table>\n      </div>"
        if t2_marker in content:
            content = content.replace(t2_marker, t2_marker + "\n\n" + table3_html)
            print("Inserted Table 3 into docs/manuscript.html")
        else:
            print("Table 2 marker not matched exactly, trying regex search")
            m = re.search(r'(</table>\s*</div>)(\s*<!-- Section 5 -->)', content)
            if m:
                content = content[:m.start(1) + len(m.group(1))] + "\n\n" + table3_html + content[m.end(1):]
                print("Inserted Table 3 via regex match")
            else:
                print("Could not find insertion point for Table 3 in docs/manuscript.html")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    update_markdown_manuscript()
    update_html_manuscript()
