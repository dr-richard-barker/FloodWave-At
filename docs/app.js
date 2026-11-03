/**
 * FloodWave-At · Interactive Scientific Showcase Controller
 * Data sourced directly from results/summary_all_runs.csv, results/pooled_summary.json,
 * metadata/file_table.csv, and results/clips/expt08_clip.json.
 */

const RUNS_DATA = [
  {
    expt: 1,
    tag: 'expt01',
    label: 'no label',
    file: 'Flooding expt 1  10012020.czi',
    zen: 'Experiment-454.czi',
    startCST: '11:19:58',
    stopCST: '11:29:05',
    frames: 451,
    duration_s: 545.8,
    size_MB: 325.1,
    t_settle_s: 111.5,
    max_reg_shift_px: 160.6,
    plant_area_mm2: 43.14,
    frac_valid: 0.986,
    plant_level_at_settle: 57.7,
    plant_rise_counts: 77.1,
    plant_trace_tpeak_s: 485.1,
    t50_p5_s: 194.1,
    t50_median_s: 328.7,
    margin_t50_s: 283.8,
    inner_t50_s: 289.8,
    vein_t50_s: 343.2,
    lamina_t50_s: 337.1,
    enrich_margin: 1.484,
    enrich_inner: 0.706,
    enrich_vein: 1.839,
    enrich_lamina: 0.744,
    bg_residual_max: 0.60,
    pooled: true,
    qc_status: 'Pooled (QC Pass)',
    qc_note: 'Field of view jumps ~3 mm at ~96 s as water arrives; rigid registration aligns post-settle frames cleanly.'
  },
  {
    expt: 2,
    tag: 'expt02',
    label: 'no label',
    file: 'Flooding expt 2  10012020.czi',
    zen: 'Experiment-455.czi',
    startCST: '11:39:09',
    stopCST: '11:49:14',
    frames: 499,
    duration_s: 603.9,
    size_MB: 359.7,
    t_settle_s: 36.4,
    max_reg_shift_px: 31.4,
    plant_area_mm2: 28.50,
    frac_valid: 0.984,
    plant_level_at_settle: 26.2,
    plant_rise_counts: 100.3,
    plant_trace_tpeak_s: 576.0,
    t50_p5_s: 88.5,
    t50_median_s: 479.1,
    margin_t50_s: 497.2,
    inner_t50_s: 499.7,
    vein_t50_s: 465.7,
    lamina_t50_s: 474.2,
    enrich_margin: 1.092,
    enrich_inner: 0.677,
    enrich_vein: 1.876,
    enrich_lamina: 0.813,
    bg_residual_max: 3.42,
    pooled: false,
    qc_status: 'Excluded (Motion)',
    qc_note: 'Single floating leaf drifts and rotates continuously across the frame (18 late motion steps > 0.5 px; max post-settle step 17.2 px).'
  },
  {
    expt: 3,
    tag: 'expt03',
    label: 'no label',
    file: 'Flooding expt 3  10012020.czi',
    zen: 'Experiment-456.czi',
    startCST: '11:53:38',
    stopCST: '12:02:20',
    frames: 430,
    duration_s: 520.0,
    size_MB: 310.0,
    t_settle_s: 34.0,
    max_reg_shift_px: 10.7,
    plant_area_mm2: 50.18,
    frac_valid: 0.948,
    plant_level_at_settle: 21.2,
    plant_rise_counts: 51.2,
    plant_trace_tpeak_s: 515.2,
    t50_p5_s: 61.9,
    t50_median_s: 127.3,
    margin_t50_s: 110.3,
    inner_t50_s: 114.0,
    vein_t50_s: 128.5,
    lamina_t50_s: 160.0,
    enrich_margin: 1.345,
    enrich_inner: 0.978,
    enrich_vein: 0.253,
    enrich_lamina: 1.048,
    bg_residual_max: 1.42,
    pooled: false,
    qc_status: 'Excluded (Mask)',
    qc_note: 'Bright out-of-focus objects beneath the support mesh are interleaved with rosette leaves, contaminating the automated Otsu mask.'
  },
  {
    expt: 4,
    tag: 'expt04',
    label: 'no label',
    file: 'Flooding expt 4  10012020.czi',
    zen: 'Experiment-457.czi',
    startCST: '12:09:36',
    stopCST: '12:13:37',
    frames: 198,
    duration_s: 238.9,
    size_MB: 142.9,
    t_settle_s: 40.0,
    max_reg_shift_px: 6.8,
    plant_area_mm2: 54.19,
    frac_valid: 0.481,
    plant_level_at_settle: 45.7,
    plant_rise_counts: 8.0,
    plant_trace_tpeak_s: 197.7,
    t50_p5_s: 47.3,
    t50_median_s: 58.2,
    margin_t50_s: 63.0,
    inner_t50_s: 60.6,
    vein_t50_s: 57.0,
    lamina_t50_s: 58.2,
    enrich_margin: 1.150,
    enrich_inner: 1.265,
    enrich_vein: 1.241,
    enrich_lamina: 0.813,
    bg_residual_max: 0.56,
    pooled: false,
    qc_status: 'Excluded (Mask / Out of Focus)',
    qc_note: 'Rosette is severely out of focus and the recording was stopped after 3.98 min (only 48% of pixels pass SNR >= 5).'
  },
  {
    expt: 5,
    tag: 'expt05',
    label: 'NormalWater',
    file: 'Flooding expt 5 NormalWater 10012020.czi',
    zen: 'Experiment-459.czi',
    startCST: '12:24:26',
    stopCST: '12:33:05',
    frames: 428,
    duration_s: 517.7,
    size_MB: 308.5,
    t_settle_s: 124.9,
    max_reg_shift_px: 31.1,
    plant_area_mm2: 37.21,
    frac_valid: 0.969,
    plant_level_at_settle: 50.7,
    plant_rise_counts: 48.1,
    plant_trace_tpeak_s: 510.4,
    t50_p5_s: 158.8,
    t50_median_s: 266.7,
    margin_t50_s: 270.4,
    inner_t50_s: 261.9,
    vein_t50_s: 291.0,
    lamina_t50_s: 260.7,
    enrich_margin: 1.457,
    enrich_inner: 0.840,
    enrich_vein: 0.689,
    enrich_lamina: 0.996,
    bg_residual_max: 1.61,
    pooled: true,
    qc_status: 'Pooled (QC Pass)',
    qc_note: 'Measured in the 2020 ROI workbook (StDev only). Outer margin enrichment (1.46x) clearly exceeds inner control band (0.84x).'
  },
  {
    expt: 6,
    tag: 'expt06',
    label: 'NormalWater YoungLeaf',
    file: 'Flooding expt 6 NormalWater YoungLeaf 10012020.czi',
    zen: 'Experiment-460.czi',
    startCST: '12:38:50',
    stopCST: '12:48:28',
    frames: 476,
    duration_s: 576.0,
    size_MB: 343.1,
    t_settle_s: 67.9,
    max_reg_shift_px: 21.5,
    plant_area_mm2: 30.41,
    frac_valid: 0.940,
    plant_level_at_settle: 71.1,
    plant_rise_counts: 25.6,
    plant_trace_tpeak_s: 351.5,
    t50_p5_s: 109.1,
    t50_median_s: 248.5,
    margin_t50_s: 271.5,
    inner_t50_s: 281.2,
    vein_t50_s: 236.3,
    lamina_t50_s: 220.6,
    enrich_margin: 0.622,
    enrich_inner: 0.792,
    enrich_vein: 2.147,
    enrich_lamina: 1.019,
    bg_residual_max: 0.69,
    pooled: true,
    qc_status: 'Pooled (QC Pass)',
    qc_note: 'Centered on young rosette leaves. Veins strongly lead earliest-5% activation (2.15x); only pooled run where margin < inner band.'
  },
  {
    expt: 7,
    tag: 'expt07',
    label: 'NormalWater YoungLeaf',
    file: 'Flooding expt 7 NormalWater YoungLeaf 10012020.czi',
    zen: 'Experiment-461.czi',
    startCST: '12:54:05',
    stopCST: '13:06:14',
    frames: 601,
    duration_s: 727.5,
    size_MB: 433.1,
    t_settle_s: 72.7,
    max_reg_shift_px: 18.1,
    plant_area_mm2: 52.64,
    frac_valid: 0.990,
    plant_level_at_settle: 69.9,
    plant_rise_counts: 66.4,
    plant_trace_tpeak_s: 543.0,
    t50_p5_s: 95.8,
    t50_median_s: 317.6,
    margin_t50_s: 387.9,
    inner_t50_s: 377.0,
    vein_t50_s: 335.8,
    lamina_t50_s: 299.4,
    enrich_margin: 1.290,
    enrich_inner: 1.018,
    enrich_vein: 0.742,
    enrich_lamina: 0.985,
    bg_residual_max: 2.06,
    pooled: true,
    qc_status: 'Pooled (QC Pass)',
    qc_note: '99.0% valid pixels; steady minutes-scale rise peaking at 543 s with outer margin leading inner band (1.29x vs 1.02x).'
  },
  {
    expt: 8,
    tag: 'expt08',
    label: 'NormalWater small plant representative',
    file: 'Flooding expt 8 NormalWater small plant representative 10012020.czi',
    zen: 'Experiment-463.czi',
    startCST: '13:25:38',
    stopCST: '13:39:48',
    frames: 700,
    duration_s: 847.5,
    size_MB: 504.4,
    t_settle_s: 48.5,
    max_reg_shift_px: 7.7,
    plant_area_mm2: 20.85,
    frac_valid: 0.995,
    plant_level_at_settle: 29.8,
    plant_rise_counts: 141.5,
    plant_trace_tpeak_s: 695.8,
    t50_p5_s: 260.6,
    t50_median_s: 470.3,
    margin_t50_s: 452.1,
    inner_t50_s: 446.1,
    vein_t50_s: 435.2,
    lamina_t50_s: 492.1,
    enrich_margin: 1.798,
    enrich_inner: 1.343,
    enrich_vein: 1.992,
    enrich_lamina: 0.356,
    bg_residual_max: 0.98,
    pooled: true,
    qc_status: 'Pooled · Representative Run',
    qc_note: 'Featured in the 2020 deck and all five 2020 videos. Veins (1.99x) and outer margin (1.80x) strongly lead lamina (0.36x); peaks at 696 s.'
  },
  {
    expt: 9,
    tag: 'expt09',
    label: 'NormalWater small plant',
    file: 'Flooding expt 9 NormalWater small plant 10012020.czi',
    zen: 'Experiment-464.czi',
    startCST: '13:44:29',
    stopCST: '14:07:32',
    frames: 1140,
    duration_s: 1381.7,
    size_MB: 821.5,
    t_settle_s: 75.2,
    max_reg_shift_px: 18.6,
    plant_area_mm2: 33.05,
    frac_valid: 0.944,
    plant_level_at_settle: 18.8,
    plant_rise_counts: 105.5,
    plant_trace_tpeak_s: 722.9,
    t50_p5_s: 173.3,
    t50_median_s: 459.6,
    margin_t50_s: 428.1,
    inner_t50_s: 429.3,
    vein_t50_s: 462.1,
    lamina_t50_s: 473.0,
    enrich_margin: 2.383,
    enrich_inner: 1.546,
    enrich_vein: 0.933,
    enrich_lamina: 0.586,
    bg_residual_max: 1.65,
    pooled: true,
    qc_status: 'Pooled (QC Pass)',
    qc_note: 'Longest recording (23.0 min, 1140 frames). Highest outer-margin enrichment in the dataset (2.38x vs 1.55x inner band).'
  },
  {
    expt: 10,
    tag: 'expt10',
    label: 'NormalWater Medium plant',
    file: 'Flooding expt 10 NormalWater Medium plant 10012020.czi',
    zen: 'Experiment-466.czi',
    startCST: '14:36:16',
    stopCST: '14:56:47',
    frames: 1015,
    duration_s: 1229.4,
    size_MB: 731.5,
    t_settle_s: 20.6,
    max_reg_shift_px: 6.0,
    plant_area_mm2: 26.92,
    frac_valid: 0.991,
    plant_level_at_settle: 1.8,
    plant_rise_counts: 108.3,
    plant_trace_tpeak_s: 837.7,
    t50_p5_s: 31.5,
    t50_median_s: 252.1,
    margin_t50_s: 263.0,
    inner_t50_s: 297.0,
    vein_t50_s: 331.5,
    lamina_t50_s: 153.3,
    enrich_margin: 1.278,
    enrich_inner: 0.860,
    enrich_vein: 0.373,
    enrich_lamina: 1.115,
    bg_residual_max: 6.40,
    pooled: false,
    qc_status: 'Excluded (Step at Settle)',
    qc_note: 'Plant jumps +21.0 counts within 6 s right after settling (t50_p5 = 31.5 s); simultaneous across the field and likely optical.'
  },
  {
    expt: 11,
    tag: 'expt11',
    label: 'NormalWater small plant',
    file: 'Flooding expt 11 NormalWater small plant 10012020.czi',
    zen: 'Experiment-465.czi',
    startCST: '14:12:35',
    stopCST: '14:31:03',
    frames: 914,
    duration_s: 1106.9,
    size_MB: 658.6,
    t_settle_s: 83.7,
    max_reg_shift_px: 8.7,
    plant_area_mm2: 19.04,
    frac_valid: 0.964,
    plant_level_at_settle: 40.8,
    plant_rise_counts: 61.6,
    plant_trace_tpeak_s: 917.7,
    t50_p5_s: 173.4,
    t50_median_s: 520.0,
    margin_t50_s: 541.8,
    inner_t50_s: 525.5,
    vein_t50_s: 586.7,
    lamina_t50_s: 489.7,
    enrich_margin: 0.782,
    enrich_inner: 0.574,
    enrich_vein: 0.240,
    enrich_lamina: 1.415,
    bg_residual_max: 2.78,
    pooled: true,
    qc_status: 'Pooled (QC Pass)',
    qc_note: 'Acquired before expt 10 (ZEN #465). Bright debris clump at upper left excluded via qc.json; margin (0.78x) > inner band (0.57x).'
  },
  {
    expt: 12,
    tag: 'expt12',
    label: 'NormalWater YoungLeaf',
    file: 'Flooding expt 12 NormalWater YoungLeaf 10012020.czi',
    zen: 'Experiment-462.czi',
    startCST: '13:12:55',
    stopCST: '13:19:29',
    frames: 324,
    duration_s: 391.6,
    size_MB: 233.6,
    t_settle_s: 61.8,
    max_reg_shift_px: 7.4,
    plant_area_mm2: 54.94,
    frac_valid: 0.735,
    plant_level_at_settle: 27.1,
    plant_rise_counts: 31.2,
    plant_trace_tpeak_s: 391.6,
    t50_p5_s: 77.6,
    t50_median_s: 194.0,
    margin_t50_s: 184.3,
    inner_t50_s: 198.8,
    vein_t50_s: 254.6,
    lamina_t50_s: 178.2,
    enrich_margin: 1.343,
    enrich_inner: 1.042,
    enrich_vein: 0.579,
    enrich_lamina: 1.045,
    bg_residual_max: 0.98,
    pooled: true,
    qc_status: 'Pooled (QC Pass)',
    qc_note: 'Acquired before expt 8 (ZEN #462). Still rising when stopped at 391.6 s; outer margin (1.34x) leads inner control band (1.04x).'
  }
];

const PATHWAY_STAGES = {
  root: {
    badge: 'Stage 1 · 0 – 90 s · Root Zone Submergence',
    title: 'Hydrostatic Surge, Aquaporin Gating & Root Hypoxia Onset',
    summary:
      'When water is poured through the funnel onto the root system, matric tension vanishes and water rapidly enters root cortical and endodermal cells via plasma-membrane aquaporins (PIP2;1). This sudden increase in root water potential generates a positive hydrostatic pressure surge (root pressure) in the xylem while mitochondrial O₂ consumption begins drawing down rhizosphere oxygen.',
    channels: ['PIP2;1 (Aquaporin)', 'MSL / MCA1/2 (Mechanosensors)', 'OSCA1 / PIEZO', 'CAX2 (Vacuolar Ca²⁺/H⁺)', 'ERF-VII / PCO (O₂ sensing)'],
    evidence:
      'In FloodWave-At, water pouring causes a physical disturbance visible in consecutive-frame difference traces between 34 and 96 s (motion settles at a median of 73.9 s across pooled runs; 48.5 s in expt 8).',
    refs: 'Peláez-Vico et al. (2023) Plant Physiol. 193:2215; Bakshi et al. (2023) New Phytol. 240:1830; Tournaire-Roux et al. (2003) Nature 425:393.'
  },
  vascular: {
    badge: 'Stage 2 · 1 – 5 min · Hypocotyl & Petiole Vasculature',
    title: 'Acropetal Hydraulic Wave & RBOHD / GLR3.3 / GLR3.6 Relay',
    summary:
      'Because xylem tracheary elements act as rigid hydraulic conduits, positive root pressure transmits an immediate axial hydraulic wave into the shoot petioles. Simultaneously, mechanosensitive Ca²⁺ influx and NADPH oxidase RBOHD form a self-amplifying apoplastic ROS (H₂O₂) and cytosolic Ca²⁺ loop that propagates acropetally through phloem sieve elements and xylem contact cells via Glutamate Receptor-Like channels GLR3.3 and GLR3.6 and tonoplast TPC1.',
    channels: ['GLR3.3 & GLR3.6 (Ca²⁺ channels)', 'RBOHD (NADPH oxidase)', 'TPC1 (Vacuolar channel)', 'PIP2;1 (H₂O₂/H₂O transport)', 'AHA1 (H⁺-ATPase)'],
    evidence:
      'In expt 8, the earliest 5% of pixels to reach half-rise (t50 ≤ 260.6 s) trace the rosette center, petioles, and primary leaf veins (1.99× enrichment over area expectation).',
    refs: 'Toyota et al. (2018) Science 361:1112; Choi et al. (2014) PNAS 111:6497; Evans et al. (2016) Plant Physiol. 171:1771; Fichman & Mittler (2021) Plant J. 107:7.'
  },
  veins: {
    badge: 'Stage 3 · 4 – 10 min · Foliar Vein Network & Lamina',
    title: 'Vascular-to-Mesophyll Spread Across the Rosette',
    summary:
      'Within the leaf blade, primary and secondary veins distribute both the hydraulic pressure wave and vascular Ca²⁺/ROS signals outward toward the serrated leaf periphery. Lateral spread from bundle-sheath cells into the interveinal mesophyll lamina occurs much more slowly than axial vascular conduction, creating a pronounced temporal lag between veins/margins and the interior lamina.',
    channels: ['GLR3.3 / GLR3.6 (Vein network)', 'CML38 (Hypoxia Ca²⁺ sensor)', 'CPKs / CIPKs', 'Plasmodesmata (PDLP1/5)'],
    evidence:
      'Across all 8 QC-passing FloodWave-At runs, median pixel half-rise (t50) occurs at 323.1 s (~5.4 min) and whole-plant peak occurs at 526.7 s (~8.8 min)—matching the ~10 min waterlogging Ca²⁺ wave reported by Peláez-Vico et al. (2023). Interior lamina lags in expt 8 (0.36× early enrichment).',
    refs: 'Peláez-Vico et al. (2023) Plant Physiol. 193:2215; Johns et al. (2021) Plant Physiol. 185:694; Lokdarshi et al. (2016) Plant Physiol. 170:1046.'
  },
  hydathode: {
    badge: 'Stage 4 · 4 – 12 min · Marginal Epithemal Hydathodes',
    title: 'Convergence at Vascular Termini, Guttation & Solute Scavenging',
    summary:
      'At the serrated leaf margin, vascular bundles terminate in blind-ending xylem vessels that irrigate a specialized parenchyma—the epithem—beneath constitutively open epidermal water pores (hydathodes). Driven by root flooding pressure, xylem exudate converges on these marginal termini (the classic pathway of guttation). Epithem cells actively scavenge ions, nutrients, and auxin from the arriving xylem stream, making leaf margins anatomical and physiological hotspots during root submergence.',
    channels: ['Epithem Vascular Termini', 'Constitutive Water Pores', 'Ion Scavengers (NRT2.1, PHT1;4)', 'Auxin & Ca²⁺ Signaling Hubs'],
    evidence:
      'In 7 of 8 QC-passing runs (sign test p = 0.070), the outer 80 µm leaf margin is enriched among the earliest 5% of activating pixels (median 1.40×) compared with the adjacent 80–160 µm inner control band (0.93×); in expt 8, the outer margin reaches 1.80×.',
    refs: 'Cerutti et al. (2019) Annu. Rev. Phytopathol. 57:91; Routaboul et al. (2024) Plant J. 120:857; Kim et al. (2021) Plant Cell 33:511.'
  }
};

const LITERATURE_DATA = [
  {
    theme: 'flooding',
    themeLabel: 'Flooding & Systemic Waves',
    title: 'Rapid systemic responses of Arabidopsis to waterlogging stress',
    authors: 'Peláez-Vico, M. Á., Tukuli, A., Singh, P., Mendoza-Cózatl, D. G., Joshi, T. & Mittler, R. (2023)',
    journal: 'Plant Physiology 193, 2215–2231',
    doi: 'https://doi.org/10.1093/plphys/kiad433',
    relevance:
      'Key benchmark for FloodWave-At: proves that abrupt root waterlogging in Arabidopsis triggers a rapid hydraulic wave plus systemic foliar Ca²⁺ (~10 min) and ROS (~20 min) waves dependent on RBOHD, GLR3.3/GLR3.6, and PIP2;1—matching our 2026 re-analysis timescale (median t50 = 5.4 min, peak = 8.8 min).'
  },
  {
    theme: 'flooding',
    themeLabel: 'Flooding & Ca²⁺ Homeostasis',
    title: 'The vacuolar Ca²⁺ transporter CATION EXCHANGER 2 regulates cytosolic calcium homeostasis, hypoxic signaling, and response to flooding in Arabidopsis thaliana',
    authors: 'Bakshi, A., Choi, W.-G., Kim, S.-H. & Gilroy, S. (2023)',
    journal: 'New Phytologist 240, 1830–1847',
    doi: 'https://doi.org/10.1111/nph.19274',
    relevance:
      'From the Gilroy lab: demonstrates that vacuolar Ca²⁺ transport via CAX2 shapes cytosolic Ca²⁺ signatures and root-to-shoot signaling during hypoxia and flooding stress.'
  },
  {
    theme: 'calcium',
    themeLabel: 'Vascular Ca²⁺ & Glutamate Waves',
    title: 'Glutamate triggers long-distance, calcium-based plant defense signaling',
    authors: 'Toyota, M., Spencer, D., Sawai-Toyota, S., Wang, J., Zhang, T., Koo, A. J., Howe, G. A. & Gilroy, S. (2018)',
    journal: 'Science 361, 1112–1115',
    doi: 'https://doi.org/10.1126/science.aat7744',
    relevance:
      'Establishes that apoplastic glutamate gates vascular GLR3.3 and GLR3.6 channels to drive systemic GCaMP3 fluorescence waves along leaf veins that visibly terminate at marginal hydathode teeth.'
  },
  {
    theme: 'calcium',
    themeLabel: 'Root-to-Shoot Ca²⁺ Waves',
    title: 'Salt stress-induced Ca²⁺ waves are associated with rapid, long-distance root-to-shoot signaling in plants',
    authors: 'Choi, W.-G., Toyota, M., Kim, S.-H., Hilleary, R. & Gilroy, S. (2014)',
    journal: 'PNAS 111, 6497–6502',
    doi: 'https://doi.org/10.1073/pnas.1319955111',
    relevance:
      'Foundational discovery of TPC1-dependent root-to-shoot Ca²⁺ waves (~400 µm/s) in Arabidopsis using ratiometric Yellow Cameleon imaging.'
  },
  {
    theme: 'hydathode',
    themeLabel: 'Hydathode Physiology & Scavenging',
    title: 'Arabidopsis hydathodes are sites of auxin accumulation and nutrient scavenging',
    authors: 'Routaboul, J.-M., Bellenot, C., Olympio, A. et al. & Noël, L. D. (2024)',
    journal: 'The Plant Journal 120, 857–871',
    doi: 'https://doi.org/10.1111/tpj.17014',
    relevance:
      'Demonstrates that Arabidopsis epithemal hydathodes are not passive water pores, but metabolically active vascular termini expressing >1,400 enriched genes for ion reabsorption and auxin signaling during guttation.'
  },
  {
    theme: 'hydathode',
    themeLabel: 'Hydathode Anatomy & Guttation',
    title: 'Mangroves in the leaves: anatomy, physiology, and immunity of epithemal hydathodes',
    authors: 'Cerutti, A., Jauneau, A., Laufs, P., Leonhardt, N., Schattat, M. H., Berthomé, R., Routaboul, J.-M. & Noël, L. D. (2019)',
    journal: 'Annual Review of Phytopathology 57, 91–116',
    doi: 'https://doi.org/10.1146/annurev-phyto-082718-100228',
    relevance:
      'Comprehensive anatomical synthesis showing how primary and secondary veins fan out into blind-ending xylem vessels inside the marginal epithem beneath constitutively open water pores.'
  },
  {
    theme: 'hydathode',
    themeLabel: 'Single-Cell Leaf & Hydathode Atlas',
    title: 'Single-cell RNA sequencing of Arabidopsis leaves reveals distinct vascular and hydathode transcriptomes',
    authors: 'Kim, J.-Y., Symeonidi, E., Pang, T. Y. et al. & Frommer, W. B. (2021)',
    journal: 'The Plant Cell 33, 511–530',
    doi: 'https://doi.org/10.1093/plcell/koaa060',
    relevance:
      'Resolves single-cell transcriptomic clusters for vascular parenchyma, bundle sheath, and epithemal hydathode cells in Arabidopsis rosette leaves.'
  },
  {
    theme: 'calcium',
    themeLabel: 'Coupled Hydraulic, ROS & Ca²⁺ Waves',
    title: 'Integration of electric, calcium, reactive oxygen species and hydraulic signals during rapid systemic signaling in plants',
    authors: 'Fichman, Y. & Mittler, R. (2021)',
    journal: 'The Plant Journal 107, 7–20',
    doi: 'https://doi.org/10.1111/tpj.15360',
    relevance:
      'Explains how vascular hydraulic pressure waves, RBOHD-mediated ROS waves, membrane depolarization, and Ca²⁺ transients operate as an integrated circuit across the plant.'
  },
  {
    theme: 'calcium',
    themeLabel: 'Long-Range Signaling Review',
    title: 'The fast and the furious: rapid long-range signaling in plants',
    authors: 'Johns, S., Hagihara, T., Toyota, M. & Gilroy, S. (2021)',
    journal: 'Plant Physiology 185, 694–706',
    doi: 'https://doi.org/10.1093/plphys/kiaa098',
    relevance:
      'Synthesizes the biophysical coupling of turgor/hydraulic shifts, mechanosensitive channels, GLRs, and ROS-assisted TPC1/RBOHD relays.'
  },
  {
    theme: 'imaging',
    themeLabel: 'Multiparametric Hypoxia Biosensing',
    title: 'Multiparametric real-time sensing of cytosolic physiology links hypoxia responses to mitochondrial electron transport',
    authors: 'Wagner, S., Steinbeck, J., Fuchs, P. et al. & Schwarzländer, M. (2019)',
    journal: 'New Phytologist 224, 1668–1684',
    doi: 'https://doi.org/10.1111/nph.16093',
    relevance:
      'Highlights how hypoxia simultaneously shifts cytosolic Ca²⁺, pH, ATP, and NAD(P)H redox poise—underscoring why single-wavelength intensity sensors require careful pH and optical controls.'
  },
  {
    theme: 'flooding',
    themeLabel: 'Flooding Stress Acclimation',
    title: 'Signal dynamics and interactions during flooding stress',
    authors: 'Sasidharan, R., Hartman, S., Liu, Z., Martopawiro, S., Sajeev, N., van Veen, H., Yeung, E. & Voesenek, L. A. C. J. (2018)',
    journal: 'Plant Physiology 176, 1106–1117',
    doi: 'https://doi.org/10.1104/pp.17.01232',
    relevance:
      'Details the temporal sequence of early ethylene trapping, nitric oxide depletion, ERF-VII stabilization, ROS, and cytosolic Ca²⁺ signals during submergence.'
  },
  {
    theme: 'imaging',
    themeLabel: 'Spaceflight & Hypoxia Transcriptomics',
    title: 'Meta-analysis of the space flight and microgravity response of the Arabidopsis plant transcriptome',
    authors: 'Barker, R., Kruse, C. P. S., Johnson, C. et al. & Gilroy, S. (2023)',
    journal: 'npj Microgravity 9, 21',
    doi: 'https://doi.org/10.1038/s41526-023-00247-6',
    relevance:
      'Contextualizes how root-zone water films, hypoxia, oxidative stress, and Ca²⁺ signaling intersect in Gilroy and Barker lab experimental frameworks.'
  }
];

document.addEventListener('DOMContentLoaded', () => {
  initVideoController();
  initSciencePathway();
  initForensicTabs();
  initRunExplorer();
  initLiteratureLibrary();
  initLightboxDialog();
  initCitationCopy();
});

/* ==========================================================================
   1. Video Showcase & Telemetry Controller (expt08_clip.mp4)
   ========================================================================== */
function initVideoController() {
  const video = document.getElementById('expt08Video');
  if (!video) return;

  const elRealTime = document.getElementById('telRealTime');
  const elRawFrame = document.getElementById('telRawFrame');
  const elClock2020 = document.getElementById('telClock2020');
  const elPhase = document.getElementById('telPhase');
  const chapterBtns = document.querySelectorAll('.chapter-btn');

  const FRAME_INTERVAL_S = 1.2120693;
  const CLIP_FPS = 30.0;

  function formatMMSS(sec) {
    const s = Math.max(0, Math.round(sec));
    const m = Math.floor(s / 60);
    const rem = s % 60;
    return `${String(m).padStart(2, '0')}:${String(rem).padStart(2, '0')}`;
  }

  function updateTelemetry() {
    const clipTime = video.currentTime || 0;
    const rawFrame = Math.min(699, Math.round(clipTime * CLIP_FPS));
    const realSec = rawFrame * FRAME_INTERVAL_S;

    if (elRealTime) elRealTime.textContent = `${realSec.toFixed(1)} s (${formatMMSS(realSec)})`;
    if (elRawFrame) elRawFrame.textContent = `${rawFrame} / 699`;

    if (elClock2020) {
      if (rawFrame < 40) {
        elClock2020.textContent = `Dropped (-${(48.5 - realSec).toFixed(0)} s)`;
      } else {
        const fakeSec = rawFrame - 40;
        elClock2020.textContent = `${formatMMSS(fakeSec)} (1 fps stamp)`;
      }
    }

    let phaseText = 'Water pouring & mesh motion';
    let activeChapterIdx = 0;
    if (realSec >= 650) {
      phaseText = 'Whole-plant peak plateau (~696 s)';
      activeChapterIdx = 4;
    } else if (realSec >= 440) {
      phaseText = 'Median pixel half-rise (t50 = 470 s)';
      activeChapterIdx = 3;
    } else if (realSec >= 240) {
      phaseText = 'Earliest 5% pixels (veins & margin)';
      activeChapterIdx = 2;
    } else if (realSec >= 48.4) {
      phaseText = 'Post-settle slow rise (veins lead)';
      activeChapterIdx = 1;
    }
    if (elPhase) elPhase.textContent = phaseText;

    chapterBtns.forEach((btn, idx) => {
      btn.classList.toggle('active', idx === activeChapterIdx);
    });
  }

  video.addEventListener('timeupdate', updateTelemetry);
  video.addEventListener('seeked', updateTelemetry);

  chapterBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      const targetRealSec = parseFloat(btn.dataset.realSec || '0');
      const targetClipSec = (targetRealSec / FRAME_INTERVAL_S) / CLIP_FPS;
      video.currentTime = Math.min(video.duration || 23.3, Math.max(0, targetClipSec));
      updateTelemetry();
      video.play().catch(() => {});
    });
  });

  updateTelemetry();
}

/* ==========================================================================
   2. Interactive Science Pathway (Root -> Vasculature -> Veins -> Hydathode)
   ========================================================================== */
function initSciencePathway() {
  const stageButtons = document.querySelectorAll('[data-stage-target]');
  const svgGroups = document.querySelectorAll('[data-svg-stage]');
  const elBadge = document.getElementById('pathwayBadge');
  const elTitle = document.getElementById('pathwayTitle');
  const elSummary = document.getElementById('pathwaySummary');
  const elChannels = document.getElementById('pathwayChannels');
  const elEvidence = document.getElementById('pathwayEvidence');
  const elRefs = document.getElementById('pathwayRefs');

  if (!elTitle) return;

  function selectStage(stageKey) {
    const data = PATHWAY_STAGES[stageKey];
    if (!data) return;

    stageButtons.forEach((btn) => {
      btn.classList.toggle('active', btn.dataset.stageTarget === stageKey);
    });

    svgGroups.forEach((grp) => {
      const isMatch = grp.dataset.svgStage === stageKey;
      grp.style.opacity = isMatch ? '1' : '0.62';
      const strokeBox = grp.querySelector('.stage-highlight-ring');
      if (strokeBox) {
        strokeBox.setAttribute('stroke-width', isMatch ? '3.5' : '1.5');
        strokeBox.setAttribute('stroke', isMatch ? '#e8a33d' : '#8a8984');
      }
    });

    elBadge.textContent = data.badge;
    elTitle.textContent = data.title;
    elSummary.textContent = data.summary;
    elChannels.innerHTML = data.channels.map((c) => `<span class="mol-tag">${c}</span>`).join('');
    elEvidence.textContent = data.evidence;
    elRefs.textContent = `Key references: ${data.refs}`;
  }

  stageButtons.forEach((btn) => {
    btn.addEventListener('click', () => selectStage(btn.dataset.stageTarget));
  });

  svgGroups.forEach((grp) => {
    grp.addEventListener('click', () => selectStage(grp.dataset.svgStage));
  });

  selectStage('root');
}

/* ==========================================================================
   3. Forensic Audit Tabs
   ========================================================================== */
function initForensicTabs() {
  const tabBtns = document.querySelectorAll('[data-forensic-tab]');
  const panels = document.querySelectorAll('[data-forensic-panel]');

  tabBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      const target = btn.dataset.forensicTab;
      tabBtns.forEach((b) => b.classList.toggle('active', b === btn));
      panels.forEach((p) => p.classList.toggle('active', p.dataset.forensicPanel === target));
    });
  });
}

/* ==========================================================================
   4. Interactive 12-Run Explorer
   ========================================================================== */
function initRunExplorer() {
  const stripEl = document.getElementById('runSelectorStrip');
  const filterBtns = document.querySelectorAll('[data-run-filter]');
  const tableBody = document.getElementById('allRunsTableBody');

  if (!stripEl) return;

  let currentFilter = 'all';
  let selectedTag = 'expt08';

  function renderStrip() {
    const filtered = RUNS_DATA.filter((r) => {
      if (currentFilter === 'pooled') return r.pooled;
      if (currentFilter === 'excluded') return !r.pooled;
      return true;
    });

    if (!filtered.some((r) => r.tag === selectedTag) && filtered.length > 0) {
      selectedTag = filtered[0].tag;
    }

    stripEl.innerHTML = filtered
      .map(
        (r) => `
      <button type="button" class="run-pill-btn ${r.tag === selectedTag ? 'active' : ''} ${!r.pooled ? 'excluded-run' : ''}" data-select-run="${r.tag}">
        <div class="run-pill-top">
          <span>Expt ${r.expt}</span>
          <span class="${r.pooled ? 'badge-pass' : 'badge-excl'}">${r.pooled ? 'Pooled' : 'Excl'}</span>
        </div>
        <div class="run-pill-sub">${r.label}</div>
      </button>
    `
      )
      .join('');

    stripEl.querySelectorAll('[data-select-run]').forEach((btn) => {
      btn.addEventListener('click', () => {
        selectedTag = btn.dataset.selectRun;
        renderStrip();
        renderRunDetail(selectedTag);
      });
    });

    renderRunDetail(selectedTag);
  }

  function renderRunDetail(tag) {
    const r = RUNS_DATA.find((item) => item.tag === tag) || RUNS_DATA[7];

    const setTxt = (id, val) => {
      const el = document.getElementById(id);
      if (el) el.textContent = val;
    };

    setTxt('inspTitle', `Experiment ${r.expt} (${r.tag}) · ${r.label}`);
    setTxt('inspSubtitle', `File: ${r.file} · Original ZEN counter: ${r.zen} · Acquired ${r.startCST}–${r.stopCST} CST (${r.size_MB} MB)`);

    const statusBadge = document.getElementById('inspStatusBadge');
    if (statusBadge) {
      statusBadge.textContent = r.qc_status;
      statusBadge.className = r.pooled ? 'badge-pass' : 'badge-excl';
      statusBadge.style.fontSize = '0.82rem';
      statusBadge.style.padding = '0.35rem 0.75rem';
    }

    setTxt('inspNote', r.qc_note);
    setTxt('mFrames', `${r.frames} (${r.duration_s.toFixed(0)} s)`);
    setTxt('mSettle', `${r.t_settle_s.toFixed(1)} s`);
    setTxt('mT50P5', `${r.t50_p5_s.toFixed(1)} s`);
    setTxt('mT50Med', `${r.t50_median_s.toFixed(1)} s`);
    setTxt('mPeak', `${r.plant_trace_tpeak_s.toFixed(1)} s`);
    setTxt('mRise', `+${r.plant_rise_counts.toFixed(1)} cts`);
    setTxt('mEnrichMargin', `${r.enrich_margin.toFixed(2)}×`);
    setTxt('mEnrichInner', `${r.enrich_inner.toFixed(2)}×`);
    setTxt('mEnrichVein', `${r.enrich_vein.toFixed(2)}×`);
    setTxt('mEnrichLamina', `${r.enrich_lamina.toFixed(2)}×`);

    const imgAct = document.getElementById('inspImgActivation');
    const imgFrames = document.getElementById('inspImgFrames');
    const imgQC = document.getElementById('inspImgQC');

    if (imgAct) {
      imgAct.src = `assets/runs/${r.tag}_activation.png`;
      imgAct.alt = `${r.tag} 6-panel activation diagnostic: regions, t50 map, rise map, regional traces, t50 histograms, registration shift`;
    }
    if (imgFrames) {
      imgFrames.src = `assets/previews/${r.tag}_frames.png`;
      imgFrames.alt = `${r.tag} time-lapse frame montage (0, 1/4, 1/2, 3/4, end, max projection)`;
    }
    if (imgQC) {
      imgQC.src = `assets/previews/${r.tag}_qc_traces.png`;
      imgQC.alt = `${r.tag} whole-field mean, 99th percentile and consecutive-frame difference QC trace`;
    }
  }

  if (tableBody) {
    tableBody.innerHTML = RUNS_DATA.map(
      (r) => `
      <tr class="${r.pooled ? '' : 'excluded-row'}" style="cursor:pointer" data-row-run="${r.tag}">
        <td class="mono"><strong>${r.tag}</strong></td>
        <td>${r.label}</td>
        <td class="mono">${r.zen.replace('Experiment-', '#').replace('.czi', '')}</td>
        <td><span class="${r.pooled ? 'badge-pass' : 'badge-excl'}">${r.pooled ? 'Pooled' : 'Excluded'}</span></td>
        <td class="num">${r.frames}</td>
        <td class="num">${r.t_settle_s.toFixed(1)}</td>
        <td class="num"><strong>${r.t50_median_s.toFixed(1)}</strong></td>
        <td class="num">${r.plant_trace_tpeak_s.toFixed(1)}</td>
        <td class="num">+${r.plant_rise_counts.toFixed(1)}</td>
        <td class="num" style="color:#ff9b73;font-weight:600">${r.enrich_margin.toFixed(2)}×</td>
        <td class="num">${r.enrich_inner.toFixed(2)}×</td>
        <td class="num" style="color:#6eb2ff;font-weight:600">${r.enrich_vein.toFixed(2)}×</td>
        <td class="num">${r.enrich_lamina.toFixed(2)}×</td>
      </tr>
    `
    ).join('');

    tableBody.querySelectorAll('[data-row-run]').forEach((row) => {
      row.addEventListener('click', () => {
        selectedTag = row.dataset.rowRun;
        currentFilter = 'all';
        filterBtns.forEach((b) => b.classList.toggle('active', b.dataset.runFilter === 'all'));
        renderStrip();
        document.getElementById('runDetailInspector')?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      });
    });
  }

  filterBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      currentFilter = btn.dataset.runFilter;
      filterBtns.forEach((b) => b.classList.toggle('active', b === btn));
      renderStrip();
    });
  });

  renderStrip();
}

/* ==========================================================================
   5. Curated Literature Review Library
   ========================================================================== */
function initLiteratureLibrary() {
  const grid = document.getElementById('litGrid');
  const filterBtns = document.querySelectorAll('[data-lit-filter]');
  if (!grid) return;

  function renderLit(filterKey) {
    const items = LITERATURE_DATA.filter((item) => filterKey === 'all' || item.theme === filterKey);
    grid.innerHTML = items
      .map(
        (item) => `
      <article class="lit-card">
        <div>
          <span class="lit-theme-tag">${item.themeLabel}</span>
          <h3 class="lit-title">${item.title}</h3>
          <p class="lit-authors">${item.authors} · <em>${item.journal}</em></p>
          <p class="lit-relevance">${item.relevance}</p>
        </div>
        <div class="lit-footer">
          <span>Verified DOI</span>
          <a href="${item.doi}" target="_blank" rel="noopener noreferrer">${item.doi.replace('https://doi.org/', 'doi:')} ↗</a>
        </div>
      </article>
    `
      )
      .join('');
  }

  filterBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      filterBtns.forEach((b) => b.classList.toggle('active', b === btn));
      renderLit(btn.dataset.litFilter);
    });
  });

  renderLit('all');
}

/* ==========================================================================
   6. Lightbox Modal Dialog (Compliant with modern-web-guidance light-dismiss-a-dialog)
   ========================================================================== */
function initLightboxDialog() {
  const dialog = document.getElementById('figLightbox');
  const dialogImg = document.getElementById('lightboxImg');
  const dialogTitle = document.getElementById('lightboxTitle');
  const dialogCaption = document.getElementById('lightboxCaption');

  if (!dialog) return;

  // Fallback for browsers without <dialog closedby="any"> support
  if (!('closedBy' in HTMLDialogElement.prototype)) {
    dialog.addEventListener('click', (event) => {
      if (event.target !== dialog) return;
      const rect = dialog.getBoundingClientRect();
      const isDialogContent =
        rect.top <= event.clientY &&
        event.clientY <= rect.top + rect.height &&
        rect.left <= event.clientX &&
        event.clientX <= rect.left + rect.width;
      if (isDialogContent) return;
      dialog.close();
    });
  }

  document.addEventListener('click', (e) => {
    const img = e.target.closest('.zoomable-fig');
    if (!img) return;
    dialogImg.src = img.src;
    dialogImg.alt = img.alt || 'High-resolution scientific figure';
    dialogTitle.textContent = img.dataset.title || 'Figure Inspector';
    dialogCaption.textContent = img.alt || '';
    dialog.showModal();
  });
}

/* ==========================================================================
   7. Citation Copy Helper
   ========================================================================== */
function initCitationCopy() {
  const copyBtn = document.getElementById('copyBibtexBtn');
  const bibtexPre = document.getElementById('bibtexBlock');
  if (!copyBtn || !bibtexPre) return;

  copyBtn.addEventListener('click', () => {
    navigator.clipboard.writeText(bibtexPre.textContent.trim()).then(() => {
      const orig = copyBtn.textContent;
      copyBtn.textContent = 'Copied BibTeX!';
      setTimeout(() => {
        copyBtn.textContent = orig;
      }, 2000);
    });
  });
}
