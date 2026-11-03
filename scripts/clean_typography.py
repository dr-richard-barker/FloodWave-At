#!/usr/bin/env python3
"""
clean_typography.py · Comprehensive cleaning of all raw LaTeX artifacts, \text{...},
and stray $ wrappers across docs/index.html, docs/manuscript.html,
manuscript/FloodWave_NatureCommunications_Perspective.md, and README.md.
"""

import re

def clean_html(content):
    # Chemical and biological symbols
    content = content.replace(r'$\text{Ca}^{2+}$', 'Ca<sup>2+</sup>')
    content = content.replace(r'\text{Ca}^{2+}', 'Ca<sup>2+</sup>')
    content = content.replace(r'$\text{LaCl}_3$', 'LaCl<sub>3</sub>')
    content = content.replace(r'\text{LaCl}_3', 'LaCl<sub>3</sub>')
    content = content.replace(r'$\text{LaCl}_3$ blocks the wave', 'LaCl<sub>3</sub> blocks the wave')
    content = content.replace(r'no $\text{LaCl}_3$ recordings', 'no LaCl<sub>3</sub> recordings')
    content = content.replace(r'Systemic $\text{Ca}^{2+}$ Waves', 'Systemic Ca<sup>2+</sup> Waves')
    content = content.replace(r'vascular $\text{Ca}^{2+}$ signals', 'vascular Ca<sup>2+</sup> signals')
    content = content.replace(r'waterlogging $\text{Ca}^{2+}$ wave', 'waterlogging Ca<sup>2+</sup> wave')
    content = content.replace(r'foliar $\text{Ca}^{2+}$ wave', 'foliar Ca<sup>2+</sup> wave')
    content = content.replace(r'cytosolic $\text{Ca}^{2+}$ concentration', 'cytosolic Ca<sup>2+</sup> concentration')
    content = content.replace(r'calcium ($\text{Ca}^{2+}$) signaling', 'calcium (Ca<sup>2+</sup>) signaling')

    # Delta F and t50
    content = content.replace(r'$\Delta F / F_0$', '&Delta;<em>F</em> / <em>F</em><sub>0</sub>')
    content = content.replace(r'($\Delta F$, 0–248 counts)', '(&Delta;<em>F</em>, 0–248 counts)')
    content = content.replace(r'$\Delta F$', '&Delta;<em>F</em>')
    content = content.replace(r'Rise Time ($t_{50}$)', 'Rise Time (<em>t</em><sub>50</sub>)')
    content = content.replace(r'half-rise time ($t_{50}$)', 'half-rise time (<em>t</em><sub>50</sub>)')
    content = content.replace(r'Pixel $t_{50}$ Map', 'Pixel <em>t</em><sub>50</sub> Map')
    content = content.replace(r'Pixel $t_{50}$ Rank Maps', 'Pixel <em>t</em><sub>50</sub> Rank Maps')
    content = content.replace(r'its $t_{50}$ rank', 'its <em>t</em><sub>50</sub> rank')
    content = content.replace(r'$t_{50} =$', '<em>t</em><sub>50</sub> =')
    content = content.replace(r'peak $=$', 'peak =')
    content = content.replace(r'$t_{50}$', '<em>t</em><sub>50</sub>')

    # Specific t50 comparisons and counts
    content = content.replace(r'($t_{50} \le 260.6\text{ s}$', '(<em>t</em><sub>50</sub> &le; 260.6 s')
    content = content.replace(r'$t_{50} \le 260.6 s$', '<em>t</em><sub>50</sub> &le; 260.6 s')
    content = content.replace(r'($t_{50} \le 261\text{ s}$)?', '(<em>t</em><sub>50</sub> &le; 261 s)?')
    content = content.replace(r'median $t_{50} = 435.2\text{ s}$; rise $+217.2\text{ counts}$', 'median <em>t</em><sub>50</sub> = 435.2 s; rise +217.2 counts')
    content = content.replace(r'median $t_{50} = 452.1\text{ s}$; rise $+115.4\text{ counts}$', 'median <em>t</em><sub>50</sub> = 452.1 s; rise +115.4 counts')
    content = content.replace(r'median $t_{50} = 446.1\text{ s}$; rise $+95.0\text{ counts}$', 'median <em>t</em><sub>50</sub> = 446.1 s; rise +95.0 counts')
    content = content.replace(r'median $t_{50} = 446.1 s$; rise $+153.2 counts$', 'median <em>t</em><sub>50</sub> = 446.1 s; rise +153.2 counts')
    content = content.replace(r'median $t_{50} = 492.1\text{ s}$; rise $+98.3\text{ counts}$', 'median <em>t</em><sub>50</sub> = 492.1 s; rise +98.3 counts')
    content = content.replace(r'median $t_{50} = 492.1 s$; rise $+171.1 counts$', 'median <em>t</em><sub>50</sub> = 492.1 s; rise +171.1 counts')
    content = content.replace(r'median $t_{50} = 323\text{ s}$, median peak $= 527\text{ s}$, median rise $= +64.0\text{ counts}$', 'median <em>t</em><sub>50</sub> = 323 s, median peak = 527 s, median rise = +64.0 counts')
    content = content.replace(r'median $t_{50} = 323 s$, median peak $= 527 s$, median rise $+64 counts$', 'median <em>t</em><sub>50</sub> = 323 s, median peak = 527 s, median rise +64 counts')
    content = content.replace(r'held-out background residual $\le 2.8\text{ counts}$', 'held-out background residual &le; 2.8 counts')
    content = content.replace(r'$\le 0.98$ counts', '&le; 0.98 counts')
    content = content.replace(r'($+21\text{ counts}$)', '(+21 counts)')
    content = content.replace(r'($+21.0\text{ counts}$)', '(+21.0 counts)')

    # Sigmas, SNR, and constants
    content = content.replace(r'($\sigma = 1.5, 15\text{ px}$)', '(&sigma; = 1.5, 15 px)')
    content = content.replace(r'($\sigma = 12\text{ px}$)', '(&sigma; = 12 px)')
    content = content.replace(r'$\text{SNR} \ge 5$', 'SNR &ge; 5')
    content = content.replace(r'($t_{50} \le P_5$)', '(<em>t</em><sub>50</sub> &le; <em>P</em><sub>5</sub>)')
    content = content.replace(r'$\text{p}K_a \approx 7.0\text{–}7.5$', 'p<em>K</em><sub>a</sub> &asymp; 7.0–7.5')
    content = content.replace(r'fraction $p$', 'fraction <em>p</em>')

    # Water potentials, ions, and chemical formulas in manuscript.html
    content = content.replace(r'($\Delta \Psi_w$)', '(&Delta;&Psi;<sub>w</sub>)')
    content = content.replace(r'($O_2^{\bullet-}$)', '(O<sub>2</sub><sup>&bull;&minus;</sup>)')
    content = content.replace(r'$O_2^{\bullet-}$', 'O<sub>2</sub><sup>&bull;&minus;</sup>')
    content = content.replace(r'$H_2O_2$', 'H<sub>2</sub>O<sub>2</sub>')
    content = content.replace(r'$NO_3^-$', 'NO<sub>3</sub><sup>&minus;</sup>')
    content = content.replace(r'$PO_4^{3-}$', 'PO<sub>4</sub><sup>3&minus;</sup>')
    content = content.replace(r'$K^+$', 'K<sup>+</sup>')

    # Total variance formula and parameters
    content = content.replace(
        r'$\sigma_{\text{ROI}}^2(t) = p\sigma_{\text{leaf}}^2 + (1-p)\sigma_{\text{bg}}^2 + p(1-p)(\mu_{\text{leaf}} - \mu_{\text{bg}})^2$',
        '<em>&sigma;</em><sup>2</sup><sub>ROI</sub>(<em>t</em>) = <em>p&sigma;</em><sup>2</sup><sub>leaf</sub> + (1 &minus; <em>p</em>)<em>&sigma;</em><sup>2</sup><sub>bg</sub> + <em>p</em>(1 &minus; <em>p</em>)(<em>&mu;</em><sub>leaf</sub> &minus; <em>&mu;</em><sub>bg</sub>)<sup>2</sup>'
    )
    content = content.replace(
        r'$\sigma_{\text{ROI}}^2(t) = p\,\sigma_{\text{leaf}}^2(t) + (1 - p)\,\sigma_{\text{bg}}^2(t) + p(1 - p)[\mu_{\text{leaf}}(t) - \mu_{\text{bg}}(t)]^2$',
        '<em>&sigma;</em><sup>2</sup><sub>ROI</sub>(<em>t</em>) = <em>p</em><em>&sigma;</em><sup>2</sup><sub>leaf</sub>(<em>t</em>) + (1 &minus; <em>p</em>)<em>&sigma;</em><sup>2</sup><sub>bg</sub>(<em>t</em>) + <em>p</em>(1 &minus; <em>p</em>)[<em>&mu;</em><sub>leaf</sub>(<em>t</em>) &minus; <em>&mu;</em><sub>bg</sub>(<em>t</em>)]<sup>2</sup>'
    )
    content = content.replace(
        r'$p(1-p)[\mu_{\text{leaf}}(t) - \mu_{\text{bg}}(t)]^2$',
        '<em>p</em>(1 &minus; <em>p</em>)[<em>&mu;</em><sub>leaf</sub>(<em>t</em>) &minus; <em>&mu;</em><sub>bg</sub>(<em>t</em>)]<sup>2</sup>'
    )
    content = content.replace(r'$\mu_{leaf}(t)$', '<em>&mu;</em><sub>leaf</sub>(<em>t</em>)')
    content = content.replace(r'$\mu_{bg}(t)$', '<em>&mu;</em><sub>bg</sub>(<em>t</em>)')
    content = content.replace(r'$(1 - p)$', '(1 &minus; <em>p</em>)')
    content = content.replace(r'$\sigma_{ROI}^2(t)$', '<em>&sigma;</em><sup>2</sup><sub>ROI</sub>(<em>t</em>)')
    content = content.replace(r'($p \approx 0.5–0.8$', '(<em>p</em> &asymp; 0.5–0.8')
    content = content.replace(r'where $p = 0.75$', 'where <em>p</em> = 0.75')
    content = content.replace(r'where $p = 0.76$', 'where <em>p</em> = 0.76')
    content = content.replace(r'$\sigma_{leaf}^2(t)$', '<em>&sigma;</em><sup>2</sup><sub>leaf</sub>(<em>t</em>)')
    content = content.replace(r'$StDev = \sigma_{ROI}(t)$', 'StDev = <em>&sigma;</em><sub>ROI</sub>(<em>t</em>)')
    content = content.replace(r'($p \approx 0.75$)', '(<em>p</em> &asymp; 0.75)')
    content = content.replace(r'$\mu_{\text{leaf}} - \mu_{\text{bg}}$', '<em>&mu;</em><sub>leaf</sub> &minus; <em>&mu;</em><sub>bg</sub>')

    # Remove any residual \text{...} wrappers
    content = re.sub(r'\\text\{([^}]+)\}', r'\1', content)

    return content

def clean_markdown(content):
    # Chemical species
    content = content.replace(r'$\text{Ca}^{2+}$', 'Ca²⁺')
    content = content.replace(r'\text{Ca}^{2+}', 'Ca²⁺')
    content = content.replace(r'$\text{LaCl}_3$', 'LaCl₃')
    content = content.replace(r'\text{LaCl}_3', 'LaCl₃')
    content = content.replace(r'Systemic $\text{Ca}^{2+}$ Waves', 'Systemic Ca²⁺ Waves')
    content = content.replace(r'vascular $\text{Ca}^{2+}$ signals', 'vascular Ca²⁺ signals')
    content = content.replace(r'coupled $\text{Ca}^{2+}$/ROS', 'coupled Ca²⁺/ROS')
    content = content.replace(r'Coupled $\text{Ca}^{2+}$/ROS', 'Coupled Ca²⁺/ROS')
    content = content.replace(r'Cytosolic $\text{Ca}^{2+}$', 'Cytosolic Ca²⁺')
    content = content.replace(r'cytosolic $\text{Ca}^{2+}$', 'cytosolic Ca²⁺')
    content = content.replace(r'Vacuolar $\text{Ca}^{2+}$', 'Vacuolar Ca²⁺')
    content = content.replace(r'vacuolar $\text{Ca}^{2+}$', 'vacuolar Ca²⁺')
    content = content.replace(r'waterlogging $\text{Ca}^{2+}$', 'waterlogging Ca²⁺')
    content = content.replace(r'foliar $\text{Ca}^{2+}$', 'foliar Ca²⁺')
    content = content.replace(r'root-to-hydathode $\text{Ca}^{2+}$', 'root-to-hydathode Ca²⁺')
    content = content.replace(r'$\text{Ca}^{2+}$-insensitive', 'Ca²⁺-insensitive')
    content = content.replace(r'calcium ($\text{Ca}^{2+}$)', 'calcium (Ca²⁺)')
    content = content.replace(r'$\text{Ca}^{2+}$ wave', 'Ca²⁺ wave')
    content = content.replace(r'$\text{Ca}^{2+}$ waves', 'Ca²⁺ waves')

    # Citation superscripts: $^{1,2}$ -> <sup>1,2</sup>
    content = re.sub(r'\$\^\{([^}]+)\}\$', r'<sup>\1</sup>', content)

    # Brackets and chemical species
    content = content.replace(r'$[Ca^{2+}]_{cyt}$', '[Ca²⁺]<sub>cyt</sub>')
    content = content.replace(r'$[Ca^{2+}]_{\text{cyt}}$', '[Ca²⁺]<sub>cyt</sub>')
    content = content.replace(r'$H^+/Ca²⁺$', 'H⁺/Ca²⁺')
    content = content.replace(r'$O_2$', 'O₂')
    content = content.replace(r'$z$-focus', '*z*-focus')
    content = content.replace(r'$z$', '*z*')

    # Delta F and t50
    content = content.replace(r'$\Delta F / F_0$', 'Δ*F* / *F*₀')
    content = content.replace(r'$\Delta F$', 'Δ*F*')
    content = content.replace(r'$t_{50}$', '*t*₅₀')
    content = content.replace(r'$t_{50} = 323\text{ s}$', '*t*₅₀ = 323 s')
    content = content.replace(r'median peak $= 527\text{ s}$', 'median peak = 527 s')
    content = content.replace(r'($\sim 10\text{ min}$)', '(~10 min)')
    content = content.replace(r'($\sim 10\text{--}15\text{ min}$)', '(~10–15 min)')
    content = content.replace(r'$80\ \mu\text{m}$', '80 µm')
    content = content.replace(r'$1.40\times$', '1.40×')
    content = content.replace(r'$0.93\times$', '0.93×')
    content = content.replace(r'$1.99\times$', '1.99×')
    content = content.replace(r'$100\text{–}150\text{ mM NaCl}$', '100–150 mM NaCl')
    content = content.replace(r'$\text{p}K_a \approx 7.0\text{–}7.5$', 'p*K*ₐ ≈ 7.0–7.5')
    content = content.replace(r'fraction $p$', 'fraction *p*')
    content = content.replace(r'$692 \times 520\text{ px}$', '692 × 520 px')
    content = content.replace(r'$2 \times 2$', '2 × 2')
    content = content.replace(r'$346 \times 260\text{ px}$', '346 × 260 px')
    content = content.replace(r'$10\times$', '10×')
    content = content.replace(r'$0\text{–}82\ \mu\text{m}$', '0–82 µm')
    content = content.replace(r'$d \le 2\text{ px}$', '*d* ≤ 2 px')
    content = content.replace(r'$82\text{–}164\ \mu\text{m}$', '82–164 µm')
    content = content.replace(r'$2 < d \le 4\text{ px}$', '2 < *d* ≤ 4 px')
    content = content.replace(r'$d > 4\text{ px}$', '*d* > 4 px')
    content = content.replace(r'($T$)', '(*T*)')
    content = content.replace(r'($\text{s}$)', '(s)')
    content = content.replace(r'($\text{counts}$)', '(counts)')
    content = content.replace(r'($\text{cts}$)', '(cts)')
    content = content.replace(r'($t_{50} \le P_5$)', '(*t*₅₀ ≤ *P*₅)')
    content = content.replace(r'$p(1-p)[\mu_{\text{leaf}}(t) - \mu_{\text{bg}}(t)]^2$', '*p*(1 − *p*)[*μ*<sub>leaf</sub>(*t*) − *μ*<sub>bg</sub>(*t*)]²')

    # Water potential, chemical formulas in markdown
    content = content.replace(r'($\Delta \Psi_w$)', '(ΔΨ<sub>w</sub>)')
    content = content.replace(r'($O_2^{\bullet-}$)', '(O₂•⁻)')
    content = content.replace(r'$O_2^{\bullet-}$', 'O₂•⁻')
    content = content.replace(r'$H_2O_2$', 'H₂O₂')
    content = content.replace(r'$NO_3^-$', 'NO₃⁻')
    content = content.replace(r'$PO_4^{3-}$', 'PO₄³⁻')
    content = content.replace(r'$K^+$', 'K⁺')
    content = content.replace(r'($40.99\ \mum px^{-1}$)', '(40.99 µm px⁻¹)')
    content = content.replace(r'$\le 0.98$ counts', '≤ 0.98 counts')
    content = content.replace(r'$\le 2.8$ counts', '≤ 2.8 counts')
    content = content.replace(r'($+21.0$ counts)', '(+21.0 counts)')
    content = content.replace(r'($+21$ counts)', '(+21 counts)')
    content = content.replace(r'($\Delta F$', '(Δ*F*')
    content = content.replace(r'$t_{50} \le 260.6$ s', '*t*₅₀ ≤ 260.6 s')
    content = content.replace(r'$t_{50} \le 261$ s', '*t*₅₀ ≤ 261 s')

    # Units and numbers in $...$
    content = re.sub(r'\$([0-9.,–-]+)\\\s*mum\s*s\^\{-1\}\$', r'\1 µm s⁻¹', content)
    content = re.sub(r'\$([0-9.,–-]+)\\\s*mum\s*px\^\{-1\}\$', r'\1 µm px⁻¹', content)
    content = re.sub(r'\$([0-9.,–-]+)\\\s*mum\$', r'\1 µm', content)
    content = re.sub(r'\$([0-9.,–-]+)\s*s\$', r'\1 s', content)
    content = re.sub(r'\$([0-9.,–-]+)\s*min\$', r'\1 min', content)
    content = re.sub(r'\$([0-9.,–-]+)\s*mm\$', r'\1 mm', content)
    content = re.sub(r'\$([0-9.,–-]+)\s*px\$', r'\1 px', content)
    content = re.sub(r'\$([0-9.,–-]+)\s*counts\$', r'\1 counts', content)
    content = re.sub(r'\$([0-9.,–-]+)\s*GB\$', r'\1 GB', content)
    content = re.sub(r'\$([0-9.,–-]+)\s*MB\$', r'\1 MB', content)
    content = re.sub(r'\$([0-9.,–-]+)\$', r'\1', content)

    # Remaining specific patterns
    content = content.replace(r'$\sim 400\ \mum s^{-1}$', '~400 µm s⁻¹')
    content = content.replace(r'($\sim 5–10 min$)', '(~5–10 min)')
    content = content.replace(r'**$\sim 10 min$**', '**~10 min**')
    content = content.replace(r'$PlanApo Z  0.5\times, NA  0.125$', 'PlanApo Z 0.5×, NA 0.125')
    content = content.replace(r'$\sim 0.5 mm$', '~0.5 mm')
    content = content.replace(r'$160 px \approx 3.3 mm$', '160 px ≈ 3.3 mm')
    content = content.replace(r'$\Delta F / F_0 > 100–300\%$', 'Δ*F* / *F*₀ > 100–300%')
    content = content.replace(r'$\le 1 count$', '≤ 1 count')
    content = content.replace(r'$= 527 s$', '= 527 s')

    # Variance equation in markdown blockquote
    content = content.replace(
        r'$$\sigma_{ROI}^2(t) = p\,\sigma_{leaf}^2(t) + (1 - p)\,\sigma_{bg}^2(t) + p(1 - p)\,\big[\mu_{leaf}(t) - \mu_{bg}(t)\big]^2$$',
        r'*σ*²<sub>ROI</sub>(*t*) = *p* *σ*²<sub>leaf</sub>(*t*) + (1 − *p*) *σ*²<sub>bg</sub>(*t*) + *p*(1 − *p*)[*μ*<sub>leaf</sub>(*t*) − *μ*<sub>bg</sub>(*t*)]²'
    )
    content = content.replace(r'$\mu_{leaf}(t)$', '*μ*<sub>leaf</sub>(*t*)')
    content = content.replace(r'$\mu_{bg}(t)$', '*μ*<sub>bg</sub>(*t*)')
    content = content.replace(r'$(1 - p)$', '(1 − *p*)')
    content = content.replace(r'$\sigma_{ROI}^2(t)$', '*σ*²<sub>ROI</sub>(*t*)')
    content = content.replace(r'($p \approx 0.5–0.8$', '(*p* ≈ 0.5–0.8')
    content = content.replace(r'where $p = 0.75$', 'where *p* = 0.75')
    content = content.replace(r'where $p = 0.76$', 'where *p* = 0.76')
    content = content.replace(r'$\sigma_{leaf}^2(t)$', '*σ*²<sub>leaf</sub>(*t*)')
    content = content.replace(r'$StDev = \sigma_{ROI}(t)$', 'StDev = *σ*<sub>ROI</sub>(*t*)')

    # Clean residual \text{...} wrappers in markdown
    content = re.sub(r'\\text\{([^}]+)\}', r'\1', content)

    return content

def main():
    files = [
        ('docs/index.html', clean_html),
        ('docs/manuscript.html', clean_html),
        ('manuscript/FloodWave_NatureCommunications_Perspective.md', clean_markdown),
        ('README.md', clean_markdown)
    ]
    
    for path, cleaner in files:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        cleaned = cleaner(content)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        print(f"Cleaned {path}")

if __name__ == '__main__':
    main()
