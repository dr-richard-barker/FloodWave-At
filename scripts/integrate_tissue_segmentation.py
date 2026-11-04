#!/usr/bin/env python3
"""
Integrate Tissue-Specific Anatomical Segmentation into:
  1. docs/app.js (RUNS_DATA enrichment, tissue metrics in inspector)
  2. docs/index.html (Tissue showcase panel, Figures 6, 7, 8, Table 4 audit)
  3. docs/manuscript.html (Narrative subsection, Figures 6, 7, 8, Table 4)
  4. manuscript/FloodWave_NatureCommunications_Perspective.md (Markdown narrative, Figures 6, 7, 8, Table 4)
"""

import json, os, re

def update_app_js():
    with open("results/tissue_segmentation_summary.json") as f:
        tissue_summary = json.load(f)
        
    tissue_by_tag = {r["tag"]: r["tissues"] for r in tissue_summary["runs"]}
    
    with open("docs/app.js", "r", encoding="utf-8") as f:
        content = f.read()
        
    # Enrich RUNS_DATA objects with tissue metrics
    for tag, td in tissue_by_tag.items():
        hyd = td.get("hydathodes", {})
        vein = td.get("veins", {})
        lam = td.get("pure_lamina", {})
        meri = td.get("meristem", {})
        
        # Build insertion string
        t_props = f"""    hydathode_t50_s: {hyd.get('t50_median_s') if hyd.get('t50_median_s') is not None else 'null'},
    pure_lamina_t50_s: {lam.get('t50_median_s') if lam.get('t50_median_s') is not None else 'null'},
    meristem_t50_s: {meri.get('t50_median_s') if meri.get('t50_median_s') is not None else 'null'},
    hydathode_enrich: {hyd.get('first5_enrichment') if hyd.get('first5_enrichment') is not None else 'null'},
    hydathode_rise: {hyd.get('rise_amplitude_counts') if hyd.get('rise_amplitude_counts') is not None else 'null'},
    vein_rise: {vein.get('rise_amplitude_counts') if vein.get('rise_amplitude_counts') is not None else 'null'},
    pure_lamina_rise: {lam.get('rise_amplitude_counts') if lam.get('rise_amplitude_counts') is not None else 'null'},"""
        
        # Look for tag marker and insert before 'label:'
        pattern = rf"(tag:\s*'{tag}',\s*\n\s*water_onset_s:[^\n]+,\s*\n\s*water_window_str:[^\n]+,\s*\n\s*surge_peak_s:[^\n]+,\s*\n\s*surge_peak_px:[^\n]+,\s*\n)"
        m = re.search(pattern, content)
        if m and "hydathode_t50_s" not in content[m.end():m.end()+400]:
            content = content[:m.end()] + t_props + "\n" + content[m.end():]

    # Update updateRunInspector to populate tissue metric cards if they exist
    old_insp = "setTxt('mSurgePeak', `${r.surge_peak_s.toFixed(1)} s (${r.surge_peak_px.toFixed(1)} px)`);"
    new_insp = """setTxt('mSurgePeak', `${r.surge_peak_s.toFixed(1)} s (${r.surge_peak_px.toFixed(1)} px)`);
    setTxt('mHydT50', r.hydathode_t50_s ? `${r.hydathode_t50_s.toFixed(1)} s` : 'N/A');
    setTxt('mLamT50', r.pure_lamina_t50_s ? `${r.pure_lamina_t50_s.toFixed(1)} s` : 'N/A');
    setTxt('mMeriT50', r.meristem_t50_s ? `${r.meristem_t50_s.toFixed(1)} s` : 'N/A');
    setTxt('mHydEnrich', r.hydathode_enrich ? `${r.hydathode_enrich.toFixed(2)}×` : 'N/A');"""

    if old_insp in content and "mHydT50" not in content:
        content = content.replace(old_insp, new_insp)

    with open("docs/app.js", "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated docs/app.js")


def update_index_html():
    with open("docs/index.html", "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add tissue metrics to run-metrics-strip
    old_metrics = """          <div class="run-metric-box"><span>Lamina Enrich</span><strong id="mEnrichLamina" style="color:#5ce6b5">0.36×</strong></div>
        </div>"""
        
    new_metrics = """          <div class="run-metric-box"><span>Lamina Enrich</span><strong id="mEnrichLamina" style="color:#5ce6b5">0.36×</strong></div>
          <div class="run-metric-box"><span>Hydathode t50</span><strong id="mHydT50" style="color:#E67E22">426.1 s</strong></div>
          <div class="run-metric-box"><span>Pure Lamina t50</span><strong id="mLamT50" style="color:#27AE60">503.0 s</strong></div>
          <div class="run-metric-box"><span>Meristem t50</span><strong id="mMeriT50" style="color:#8E44AD">206.7 s</strong></div>
          <div class="run-metric-box"><span>Hydathode 5% Enrich</span><strong id="mHydEnrich" style="color:#E67E22">0.94×</strong></div>
        </div>"""

    if old_metrics in content and "mHydT50" not in content:
        content = content.replace(old_metrics, new_metrics)
        print("Added tissue metrics to docs/index.html")

    # 2. Add Tissue-Specific Anatomical Segmentation section
    tissue_section_html = """
      <!-- Tissue-Specific Anatomical Segmentation Section -->
      <div style="background:var(--bg-slate-card);border:1px solid var(--border-slate);border-radius:var(--radius-lg);padding:1.5rem;margin-bottom:2.25rem">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:1rem;margin-bottom:1.25rem">
          <div>
            <p class="eyebrow" style="margin-bottom:0.35rem">Quantitative Tissue Refinement</p>
            <h3 style="font-family:var(--font-serif);font-size:1.45rem;margin:0 0 0.4rem 0;color:var(--text-on-slate)">
              From Crude Circular ROIs to Pure Anatomical Compartments (0.00% Background Contamination)
            </h3>
            <p style="font-size:0.92rem;color:var(--text-on-slate-muted);max-width:88ch;margin:0">
              In the 2020 analysis, plant regions were measured using crude hand-drawn circles (245–422 µm radius). Because circular stamps do not conform to leaf boundaries, <code>Hydrathode-2</code> suffered <strong>27.7%</strong> and <code>Mersitem-1</code> suffered <strong>21.3%</strong> off-plant background contamination, creating spurious contrast artifacts that masqueraded as early "calcium waves". We developed an automated segmentation system partitioning rosettes into pure tissues: <strong>Hydathode Teeth</strong> (curvature peaks at vein termini), <strong>Primary Veins</strong> (multiscale Sato ridge filter), <strong>Pure Lamina</strong> (mesophyll &gt;120 µm inside edge and &gt;80 µm from veins), and <strong>Shoot Meristem</strong> (0.00% background contamination).
            </p>
          </div>
        </div>

        <!-- 2-Column Visual Comparison -->
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;margin-bottom:1.75rem">
          <div class="run-visual-card">
            <h4>
              <span>Figure 7 | Performance Audit on Representative Run (<code>expt08</code>)</span>
              <span class="mono" style="font-size:0.72rem;color:var(--text-on-slate-muted)">Click to zoom</span>
            </h4>
            <img src="assets/figures/tissue_comparison_expt08.png" alt="Forensic audit comparing 2020 crude circular ROIs vs 2026 refined tissue ROIs on expt08" class="zoomable-fig" data-title="Figure 7: 2020 Crude Circles vs 2026 Refined ROIs (expt08)" style="border-color:var(--border-slate)">
            <p style="font-size:0.8rem;color:var(--text-on-slate-muted);margin:0.5rem 0 0 0">
              Eliminating the 27.7% off-plant background contamination completely collapses the false <code>StDev</code> "wave" peaks while restoring true physiological amplitude (+58% in meristem, +26% in hydathode-2).
            </p>
          </div>

          <div class="run-visual-card">
            <h4>
              <span>Figure 8 | Population Kinetics Across 8 Pooled Runs</span>
              <span class="mono" style="font-size:0.72rem;color:var(--text-on-slate-muted)">Click to zoom</span>
            </h4>
            <img src="assets/figures/tissue_kinetics_population.png" alt="Dataset-wide population kinetics and hierarchical signaling flow across 8 pooled runs" class="zoomable-fig" data-title="Figure 8: Population Kinetics Across 8 Pooled Runs" style="border-color:var(--border-slate)">
            <p style="font-size:0.8rem;color:var(--text-on-slate-muted);margin:0.5rem 0 0 0">
              Across passing runs, discrete hydathode teeth show a <strong>1.39×</strong> median enrichment of early responders (up to 4.52×), while pure mesophyll lamina lags vascular conduits.
            </p>
          </div>
        </div>

        <!-- Multi-Run Gallery Banner -->
        <div class="run-visual-card">
          <h4>
            <span>Figure 6 | Multi-Run Tissue-Specific Anatomical Segmentation Atlas (All 12 Runs)</span>
            <span class="mono" style="font-size:0.72rem;color:var(--text-on-slate-muted)">Click to zoom</span>
          </h4>
          <img src="assets/figures/tissue_segmentation_all_runs.png" alt="12-run gallery showing refined tissue segmentation overlays" class="zoomable-fig" data-title="Figure 6: Multi-Run Tissue Segmentation Atlas (All 12 Runs)" style="border-color:var(--border-slate);width:100%">
        </div>
      </div>
"""

    if "<!-- Tissue-Specific Anatomical Segmentation Section -->" not in content:
        # Insert before Master Table
        marker = "<!-- Master Table of All 12 Runs -->"
        if marker in content:
            content = content.replace(marker, tissue_section_html + "\n      " + marker)
            print("Inserted Tissue Section into docs/index.html")

    with open("docs/index.html", "w", encoding="utf-8") as f:
        f.write(content)


def update_manuscript_html():
    with open("docs/manuscript.html", "r", encoding="utf-8") as f:
        content = f.read()

    section_text = """
      <!-- Refined Tissue-Specific Segmentation Subsection -->
      <h3 id="sec-tissue-segmentation">From Crude Circles to Anatomical Tissues: A Refined Segmentation System</h3>
      <p>
        A central limitation of the initial 2020 exploratory analysis was the reliance on crude circular regions of interest (radius 245 µm; meristem circle 422 µm) hand-drawn onto a single video frame. Circular geometries do not conform to irregular leaf margins, serrations, or vascular anatomy. Consequently, measuring circles positioned near the rosette boundary introduced severe <strong>off-plant background contamination</strong>: <code>Hydrathode-2</code> encompassed <strong>27.7%</strong> off-plant background pixels (only 72.3% on plant), while <code>Mersitem-1</code> straddled petiole bases and empty voids with <strong>21.3%</strong> background pixels (Fig. 7; Table 4).
      </p>
      <p>
        By the law of total variance (Box 2), any uniform brightening of the leaf relative to the dark background creates a massive, spurious spike in within-ROI pixel standard deviation (&sigma;<sub>ROI</sub>) strictly proportional to the boundary contrast term <em>p</em>(1 &minus; <em>p</em>)[<em>&mu;</em><sub>leaf</sub> &minus; <em>&mu;</em><sub>bg</sub>]<sup>2</sup>. This mathematical artifact explains why <code>Hydrathode-2</code> and <code>Mersitem-1</code> produced steep, early "waves" in the 2020 workbook that vanished when mean fluorescence was plotted instead (Fig. 7d). Furthermore, circular lamina ROIs directly intersected major primary and secondary veins, conflating high-amplitude vascular calcium transients with slower interveinal mesophyll responses.
      </p>
      <p>
        To overcome these limitations and determine whether tissue-specific kinetics genuinely exist, we developed an automated, reproducible anatomical segmentation pipeline applied across all twelve recordings (<code>analysis/tissue_segmentation.py</code>; Fig. 6):
      </p>
      <ol>
        <li><strong>Hydathode Epithems / Marginal Teeth (<code>hydathodes</code>):</strong> Morphological boundary curvature peaks along leaf serrations and the distal apex that connect to terminal branches of the vascular network. Clipped strictly to plant tissue (<em>r</em> &approx; 40–80 µm, 0.00% background contamination).</li>
        <li><strong>Primary &amp; Secondary Vasculature (<code>veins</code>):</strong> Multiscale Sato ridge filter (&gt; 80th percentile on the rosette core) isolating xylem and phloem bundles along petioles and leaf veins.</li>
        <li><strong>Pure Interveinal Lamina (<code>pure_lamina</code>):</strong> Mesophyll ground tissue located &gt; 120 µm inward from leaf margins and &gt; 80 µm away from any vascular bundle. This guarantees <strong>zero edge contrast artifacts and zero vascular spillover</strong>.</li>
        <li><strong>Rosette Shoot Apex / Meristem (<code>meristem</code>):</strong> The central confluence of the rosette where petiole bases converge, strictly masked to tissue (0.00% background void).</li>
        <li><strong>Spatial Negative Controls:</strong> Non-hydathode leaf margin (<code>margin_other</code>) and an 80–160 µm concentric inner control band (<code>inner_control</code>).</li>
      </ol>

      <figure class="manuscript-figure">
        <img src="assets/figures/tissue_comparison_expt08.png" alt="Figure 7: Forensic Performance Audit: 2020 Crude Circles vs 2026 Refined Tissue ROIs on Representative Run expt08" data-title="Figure 7: Forensic Performance Audit on expt08" class="zoomable-fig">
        <figcaption>
          <strong>Figure 7 | Quantitative forensic performance audit: 2020 crude circular ROIs versus 2026 refined tissue ROIs on the representative recording (<code>expt08</code>).</strong> <strong>A:</strong> Spatial layout showing the seven 2020 circular ROIs (dashed colored rings) with off-plant background leakage highlighted in red, compared with the refined tissue masks. <strong>B:</strong> Off-plant background contamination percentage: crude circles suffered up to 27.7% contamination (<code>Hydrathode-2</code>: 27.7%, <code>Mersitem-1</code>: 21.3%), whereas all refined ROIs achieve <strong>0.00% contamination</strong>. <strong>C:</strong> Background-subtracted mean fluorescence time courses (counts above local background). <strong>D:</strong> Within-ROI pixel standard deviation over time: the steep peaks in <code>Hydrathode-2</code> and <code>Mersitem-1</code> present in crude circles completely collapse in the refined 0%-background ROIs, proving they were boundary-contrast artifacts.
        </figcaption>
      </figure>

      <div class="table-scroll" style="margin:1.75rem 0">
        <table class="data-table">
          <caption><strong>Table 4 | Direct forensic audit of the seven 2020 ROIs versus 2026 refined pure-tissue ROIs on representative recording <code>expt08</code> (<code>results/refined_rois_expt08.json</code>).</strong></caption>
          <thead>
            <tr>
              <th>ROI Label</th>
              <th>Anatomical Target</th>
              <th>2020 Crude Pixels</th>
              <th>2020 BG Contamination</th>
              <th>2020 Rise (counts)</th>
              <th>2020 SNR</th>
              <th>2026 Refined Pixels</th>
              <th>2026 BG Contamination</th>
              <th>2026 Rise (counts)</th>
              <th>2026 SNR</th>
              <th>2026 <em>t</em><sub>50</sub> (s)</th>
              <th>Forensic Finding</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><code>Hydrathode-1</code></td>
              <td>Marginal tooth epithem</td>
              <td>110</td>
              <td>2.7%</td>
              <td>225.7</td>
              <td>569.0</td>
              <td>25</td>
              <td><strong>0.00%</strong></td>
              <td>218.0</td>
              <td>257.9</td>
              <td>417.0</td>
              <td>Refined to discrete tooth apex; true rise matches vascular fan</td>
            </tr>
            <tr>
              <td><code>Hydrathode-2</code></td>
              <td>Marginal tooth tip</td>
              <td>112</td>
              <td><span class="badge badge-warning">27.7%</span></td>
              <td>108.4</td>
              <td>124.8</td>
              <td>35</td>
              <td><strong>0.00%</strong></td>
              <td>136.6</td>
              <td>173.0</td>
              <td>339.4</td>
              <td>27.7% BG depressed amplitude; refined ROI restores +26% signal</td>
            </tr>
            <tr>
              <td><code>Lamina-1</code></td>
              <td>Blade mesophyll</td>
              <td>112</td>
              <td>0.0%</td>
              <td>220.7</td>
              <td>361.8</td>
              <td>102</td>
              <td><strong>0.00%</strong></td>
              <td>216.6</td>
              <td>343.9</td>
              <td>507.9</td>
              <td>Overlapped secondary vein; refined mesophyll rises at 8.5 min</td>
            </tr>
            <tr>
              <td><code>Lamina-2</code></td>
              <td>Blade/petiole nexus</td>
              <td>111</td>
              <td>0.0%</td>
              <td>199.2</td>
              <td>533.2</td>
              <td>78</td>
              <td><strong>0.00%</strong></td>
              <td>198.5</td>
              <td>502.2</td>
              <td>527.3</td>
              <td>Overlapped primary midrib; pure lamina lags vein by ~90 s</td>
            </tr>
            <tr>
              <td><code>Lamina-3</code></td>
              <td>Distal blade mesophyll</td>
              <td>114</td>
              <td>0.0%</td>
              <td>155.0</td>
              <td>97.3</td>
              <td>108</td>
              <td><strong>0.00%</strong></td>
              <td>153.6</td>
              <td>95.1</td>
              <td>560.0</td>
              <td>Pure interveinal mesophyll; latest activating sector (9.3 min)</td>
            </tr>
            <tr>
              <td><code>Mersitem-1</code></td>
              <td>Rosette shoot apex</td>
              <td>334</td>
              <td><span class="badge badge-warning">21.3%</span></td>
              <td>71.5</td>
              <td>105.7</td>
              <td>263</td>
              <td><strong>0.00%</strong></td>
              <td>113.0</td>
              <td>123.4</td>
              <td>258.2</td>
              <td>21.3% void depressed amplitude; refined ROI restores +58% signal</td>
            </tr>
            <tr>
              <td><code>Hydrathode-3</code></td>
              <td>Internal lamina/vein</td>
              <td>111</td>
              <td>0.0%</td>
              <td>145.3</td>
              <td>287.4</td>
              <td>111</td>
              <td><strong>0.00%</strong></td>
              <td>145.3</td>
              <td>287.4</td>
              <td>301.8</td>
              <td>Sits 569 µm inside plant; actually internal vascular termination</td>
            </tr>
          </tbody>
        </table>
      </div>

      <figure class="manuscript-figure">
        <img src="assets/figures/tissue_segmentation_all_runs.png" alt="Figure 6: Multi-Run Tissue-Specific Anatomical Segmentation Atlas Across All 12 Recordings" data-title="Figure 6: Multi-Run Tissue Segmentation Atlas" class="zoomable-fig">
        <figcaption>
          <strong>Figure 6 | Multi-run tissue-specific anatomical segmentation atlas across all twelve recordings (<code>analysis/tissue_segmentation.py</code>).</strong> Grayscale reference images with transparent multi-color overlays defining the five pure anatomical compartments: hydathode teeth (orange/gold markers, 0% background), primary and secondary veins (cyan/blue), pure interveinal lamina (green), rosette shoot apex / meristem (purple), and concentric inner control band (grey). Scale bars, 2 mm. Border color denotes QC status (teal = pooled, red = excluded).
        </figcaption>
      </figure>

      <figure class="manuscript-figure">
        <img src="assets/figures/tissue_kinetics_population.png" alt="Figure 8: Dataset-Wide Tissue Kinetics and Hierarchical Signaling Flow Across 8 Pooled Runs" data-title="Figure 8: Population Kinetics Across 8 Pooled Runs" class="zoomable-fig">
        <figcaption>
          <strong>Figure 8 | Dataset-wide tissue kinetics and hierarchical signaling flow across the eight pooled recordings.</strong> <strong>A:</strong> Population-normalized background-subtracted time courses (median &plusmn; interquartile range) for hydathodes (orange), veins (blue), pure lamina (green), and shoot meristem (purple). <strong>B:</strong> Half-rise time (<em>t</em><sub>50</sub>) boxplots with paired individual-run lines. <strong>C:</strong> Spatial enrichment of the earliest 5% of activating pixels (<em>t</em><sub>50</sub> &le; <em>P</em><sub>5</sub>): hydathode teeth exhibit a median enrichment of <strong>1.39&times;</strong> (up to 4.52&times;), exceeding non-hydathode margin and lamina. <strong>D:</strong> Dynamic range by tissue: primary veins sustain the highest peak amplitude (&Delta;<em>F</em> median 99.9 counts).
        </figcaption>
      </figure>
"""

    if "From Crude Circles to Anatomical Tissues" not in content:
        # Insert right after Figure 4 / Table 3 in Section 4
        marker = "<!-- Section 5 -->"
        if marker in content:
            content = content.replace(marker, section_text + "\n\n      " + marker)
            print("Inserted Tissue Section into docs/manuscript.html")

    with open("docs/manuscript.html", "w", encoding="utf-8") as f:
        f.write(content)


def update_markdown_manuscript():
    with open("manuscript/FloodWave_NatureCommunications_Perspective.md", "r", encoding="utf-8") as f:
        content = f.read()

    section_md = """### From Crude Circles to Anatomical Tissues: A Refined Segmentation System
A central limitation of the initial 2020 exploratory analysis was its reliance on crude circular regions of interest (radius 245 µm; meristem circle 422 µm) hand-drawn onto a single video frame. Circular geometries do not conform to irregular leaf margins, serrations, or vascular anatomy. Consequently, measuring circles positioned near the rosette boundary introduced severe **off-plant background contamination**: `Hydrathode-2` encompassed **27.7%** off-plant background pixels (only 72.3% on plant), while `Mersitem-1` straddled petiole bases and empty voids with **21.3%** background pixels (Fig. 7; Table 4).

By the law of total variance (Box 2), any uniform brightening of the leaf relative to the dark background creates a massive, spurious spike in within-ROI pixel standard deviation (*σ*<sub>ROI</sub>) strictly proportional to the boundary contrast term *p*(1 − *p*)[*μ*<sub>leaf</sub> − *μ*<sub>bg</sub>]². This mathematical artifact explains why `Hydrathode-2` and `Mersitem-1` produced steep, early "waves" in the 2020 workbook that vanished when mean fluorescence was plotted instead (Fig. 7d). Furthermore, circular lamina ROIs directly intersected major primary and secondary veins, conflating high-amplitude vascular calcium transients with slower interveinal mesophyll responses.

To overcome these limitations and determine whether tissue-specific kinetics genuinely exist, we developed an automated, reproducible anatomical segmentation pipeline applied across all twelve recordings (`analysis/tissue_segmentation.py`; Fig. 6):

1. **Hydathode Epithems / Marginal Teeth (`hydathodes`):** Morphological boundary curvature peaks along leaf serrations and the distal apex that connect to terminal branches of the vascular network. Clipped strictly to plant tissue (*r* ≈ 40–80 µm, 0.00% background contamination).
2. **Primary & Secondary Vasculature (`veins`):** Multiscale Sato ridge filter (> 80th percentile on the rosette core) isolating xylem and phloem bundles along petioles and leaf veins.
3. **Pure Interveinal Lamina (`pure_lamina`):** Mesophyll ground tissue located > 120 µm inward from leaf margins and > 80 µm away from any vascular bundle. This guarantees **zero edge contrast artifacts and zero vascular spillover**.
4. **Rosette Shoot Apex / Meristem (`meristem`):** The central confluence of the rosette where petiole bases converge, strictly masked to tissue (0.00% background void).
5. **Spatial Negative Controls:** Non-hydathode leaf margin (`margin_other`) and an 80–160 µm concentric inner control band (`inner_control`).

![Figure 7: Forensic Performance Audit: 2020 Crude Circles vs 2026 Refined Tissue ROIs on Representative Run expt08](../docs/assets/figures/tissue_comparison_expt08.png)
**Figure 7 | Quantitative forensic performance audit: 2020 crude circular ROIs versus 2026 refined tissue ROIs on the representative recording (`expt08`).** **A:** Spatial layout showing the seven 2020 circular ROIs (dashed colored rings) with off-plant background leakage highlighted in red, compared with the refined tissue masks. **B:** Off-plant background contamination percentage: crude circles suffered up to 27.7% contamination (`Hydrathode-2`: 27.7%, `Mersitem-1`: 21.3%), whereas all refined ROIs achieve **0.00% contamination**. **C:** Background-subtracted mean fluorescence time courses (counts above local background). **D:** Within-ROI pixel standard deviation over time: the steep peaks in `Hydrathode-2` and `Mersitem-1` present in crude circles completely collapse in the refined 0%-background ROIs, proving they were boundary-contrast artifacts.

| ROI Label | Anatomical Target | 2020 Crude Pixels | 2020 BG Contam | 2020 Rise (counts) | 2020 SNR | 2026 Refined Pixels | 2026 BG Contam | 2026 Rise (counts) | 2026 SNR | 2026 *t*₅₀ (s) | Forensic Finding |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| `Hydrathode-1` | Marginal tooth epithem | 110 | 2.7% | 225.7 | 569.0 | 25 | **0.00%** | 218.0 | 257.9 | 417.0 | Refined to tooth apex; true rise matches vascular fan |
| `Hydrathode-2` | Marginal tooth tip | 112 | **27.7%** | 108.4 | 124.8 | 35 | **0.00%** | 136.6 | 173.0 | 339.4 | 27.7% BG depressed amplitude; refined ROI restores +26% signal |
| `Lamina-1` | Blade mesophyll | 112 | 0.0% | 220.7 | 361.8 | 102 | **0.00%** | 216.6 | 343.9 | 507.9 | Overlapped secondary vein; pure mesophyll rises at 8.5 min |
| `Lamina-2` | Blade/petiole nexus | 111 | 0.0% | 199.2 | 533.2 | 78 | **0.00%** | 198.5 | 502.2 | 527.3 | Overlapped primary midrib; pure lamina lags vein by ~90 s |
| `Lamina-3` | Distal blade mesophyll | 114 | 0.0% | 155.0 | 97.3 | 108 | **0.00%** | 153.6 | 95.1 | 560.0 | Pure interveinal mesophyll; latest activating sector (9.3 min) |
| `Mersitem-1` | Rosette shoot apex | 334 | **21.3%** | 71.5 | 105.7 | 263 | **0.00%** | 113.0 | 123.4 | 258.2 | 21.3% void depressed amplitude; refined ROI restores +58% signal |
| `Hydrathode-3` | Internal lamina/vein | 111 | 0.0% | 145.3 | 287.4 | 111 | **0.00%** | 145.3 | 287.4 | 301.8 | Sits 569 µm inside plant; actually internal vascular termination |

**Table 4 | Direct forensic audit of the seven 2020 ROIs versus 2026 refined pure-tissue ROIs on representative recording `expt08` (`results/refined_rois_expt08.json`).**

![Figure 6: Multi-Run Tissue-Specific Anatomical Segmentation Atlas Across All 12 Recordings](../docs/assets/figures/tissue_segmentation_all_runs.png)
**Figure 6 | Multi-run tissue-specific anatomical segmentation atlas across all twelve recordings (`analysis/tissue_segmentation.py`).** Grayscale reference images with transparent multi-color overlays defining the five pure anatomical compartments: hydathode teeth (orange/gold markers, 0% background), primary and secondary veins (cyan/blue), pure interveinal lamina (green), rosette shoot apex / meristem (purple), and concentric inner control band (grey). Scale bars, 2 mm. Border color denotes QC status (teal = pooled, red = excluded).

![Figure 8: Dataset-Wide Tissue Kinetics and Hierarchical Signaling Flow Across 8 Pooled Runs](../docs/assets/figures/tissue_kinetics_population.png)
**Figure 8 | Dataset-wide tissue kinetics and hierarchical signaling flow across the eight pooled recordings.** **A:** Population-normalized background-subtracted time courses (median ± interquartile range) for hydathodes (orange), veins (blue), pure lamina (green), and shoot meristem (purple). **B:** Half-rise time (*t*₅₀) boxplots with paired individual-run lines. **C:** Spatial enrichment of the earliest 5% of activating pixels (*t*₅₀ ≤ *P*₅): hydathode teeth exhibit a median enrichment of **1.39×** (up to 4.52×), exceeding non-hydathode margin and lamina. **D:** Dynamic range by tissue: primary veins sustain the highest peak amplitude (Δ*F* median 99.9 counts).

---
"""

    if "From Crude Circles to Anatomical Tissues" not in content:
        marker = "## Optical Confounds and FAIR Standards for Whole-Plant Biosensor Imaging"
        if marker in content:
            content = content.replace(marker, section_md + "\n\n" + marker)
            print("Inserted Tissue Section into markdown manuscript")

    with open("manuscript/FloodWave_NatureCommunications_Perspective.md", "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    update_app_js()
    update_index_html()
    update_manuscript_html()
    update_markdown_manuscript()
