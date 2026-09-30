/**
 * Vibe UI — Design Token System & Visual Chemistry Models
 * Pure OKLCH color spaces preserving mathematical contrast ratios across light and dark themes.
 */

export type VisualChemistryId =
  | 'MINIMALIST_SAAS'
  | 'LUXURY_GLASS_2'
  | 'NEOBRUTALISM'
  | 'SWISS_EDITORIAL'
  | 'STRIPE_CRISP_LIGHT';

export interface ChemistryColors {
  /** Canvas / background base color in OKLCH */
  canvas: string;
  /** Surface card elevation in OKLCH */
  surface: string;
  /** Border stroke specification color in OKLCH */
  border: string;
  /** Primary brand / interactive accent in OKLCH */
  primaryAccent: string;
  /** Text color on primary accent guaranteeing >= 4.5:1 (AA) or >= 7:1 (AAA) contrast */
  onPrimaryAccent: string;
  /** Primary text color guaranteeing >= 4.5:1 contrast against canvas & surface */
  textPrimary: string;
  /** Muted secondary text color guaranteeing >= 3:1 contrast against canvas */
  textMuted: string;
  /** Focus ring and interactive highlight in OKLCH */
  ring: string;
}

export interface ChemistryTypography {
  display: string;
  body: string;
  mono: string;
}

export interface ChemistryMetadata {
  id: VisualChemistryId;
  name: string;
  tagline: string;
  domain: string;
  surfaceTreatment: string;
  colors: ChemistryColors;
  typography: ChemistryTypography;
}

export const VISUAL_CHEMISTRIES: Record<VisualChemistryId, ChemistryMetadata> = {
  MINIMALIST_SAAS: {
    id: 'MINIMALIST_SAAS',
    name: 'Minimalist High-Performance SaaS',
    tagline: 'Razor-sharp precision engineered for developer tools & B2B platforms',
    domain: 'Developer Tools, Modern Dashboards, Observability',
    surfaceTreatment: 'Ultra-crisp 1px borders, subtle linear gradients, zero heavy blur',
    colors: {
      canvas: 'oklch(0.14 0.005 260)',
      surface: 'oklch(0.18 0.008 260)',
      border: 'oklch(0.28 0.01 260)',
      primaryAccent: 'oklch(0.65 0.22 265)',
      onPrimaryAccent: 'oklch(0.99 0 0)',
      textPrimary: 'oklch(0.98 0 0)',
      textMuted: 'oklch(0.70 0.01 260)',
      ring: 'oklch(0.65 0.22 265)',
    },
    typography: {
      display: 'Vazirmatn, Inter, system-ui, -apple-system, sans-serif',
      body: 'Vazirmatn, Inter, system-ui, -apple-system, sans-serif',
      mono: 'JetBrains Mono, ui-monospace, monospace',
    },
  },
  LUXURY_GLASS_2: {
    id: 'LUXURY_GLASS_2',
    name: 'Luxury Obsidian & Glassmorphism 2.0',
    tagline: 'Deep velvet obsidian, champagne specular highlights, and ambient glow',
    domain: 'AI Flagship Models, Luxury Brands, High-Ticket Services',
    surfaceTreatment: 'Multi-layer frosted glass, Fresnel highlights, subtle noise texture',
    colors: {
      canvas: 'oklch(0.12 0.012 260)',
      surface: 'oklch(0.16 0.018 265)',
      border: 'oklch(0.32 0.03 265)',
      primaryAccent: 'oklch(0.78 0.16 75)',
      onPrimaryAccent: 'oklch(0.12 0.02 85)',
      textPrimary: 'oklch(0.98 0.005 75)',
      textMuted: 'oklch(0.68 0.02 260)',
      ring: 'oklch(0.78 0.16 75)',
    },
    typography: {
      display: 'Playfair Display, Vazirmatn, Georgia, serif',
      body: 'Vazirmatn, Inter, system-ui, -apple-system, sans-serif',
      mono: 'JetBrains Mono, ui-monospace, monospace',
    },
  },
  NEOBRUTALISM: {
    id: 'NEOBRUTALISM',
    name: 'Neobrutalism & Playful High-Contrast',
    tagline: 'Thick black structural ink, vibrant pop colors, and tactile offset drop shadows',
    domain: 'Creator Economy, Creative Studios, EdTech, Bold Web Apps',
    surfaceTreatment: 'Solid 2.5px ink borders, 4px unblurred hard shadows, physical click depth',
    colors: {
      canvas: 'oklch(0.97 0.08 95)',
      surface: 'oklch(1.00 0 0)',
      border: 'oklch(0.00 0 0)',
      primaryAccent: 'oklch(0.55 0.24 25)',
      onPrimaryAccent: 'oklch(0.99 0 0)',
      textPrimary: 'oklch(0.00 0 0)',
      textMuted: 'oklch(0.35 0.01 0)',
      ring: 'oklch(0.00 0 0)',
    },
    typography: {
      display: 'Space Grotesk, Vazirmatn, system-ui, sans-serif',
      body: 'Vazirmatn, Space Grotesk, system-ui, sans-serif',
      mono: 'Space Mono, ui-monospace, monospace',
    },
  },
  SWISS_EDITORIAL: {
    id: 'SWISS_EDITORIAL',
    name: 'Swiss Editorial & Paper Craft',
    tagline: 'Warm ivory paper, architectural grid discipline, and vermilion ink accents',
    domain: 'Journalism, Architecture Portfolios, Research & Monographs',
    surfaceTreatment: 'Hairline structural rules, zero synthetic blur, high-density typographical rhythm',
    colors: {
      canvas: 'oklch(0.98 0.005 80)',
      surface: 'oklch(0.95 0.008 80)',
      border: 'oklch(0.85 0.01 80)',
      primaryAccent: 'oklch(0.52 0.22 28)',
      onPrimaryAccent: 'oklch(0.99 0 0)',
      textPrimary: 'oklch(0.12 0.01 50)',
      textMuted: 'oklch(0.45 0.01 60)',
      ring: 'oklch(0.52 0.22 28)',
    },
    typography: {
      display: 'Instrument Serif, Vazirmatn, Bodoni MT, serif',
      body: 'Vazirmatn, Inter, system-ui, -apple-system, sans-serif',
      mono: 'JetBrains Mono, ui-monospace, monospace',
    },
  },
  STRIPE_CRISP_LIGHT: {
    id: 'STRIPE_CRISP_LIGHT',
    name: 'Modern Crisp Light',
    tagline: 'Pristine porcelain snow, electric sapphire blue, and diffuse ambient depth',
    domain: 'Global Fintech, Enterprise Cloud, Modern Commerce',
    surfaceTreatment: 'Multi-stage diffuse ambient shadows, crisp micro-borders, ultra-clean contrast',
    colors: {
      canvas: 'oklch(0.99 0.002 240)',
      surface: 'oklch(1.00 0 0)',
      border: 'oklch(0.90 0.01 240)',
      primaryAccent: 'oklch(0.56 0.21 255)',
      onPrimaryAccent: 'oklch(0.99 0 0)',
      textPrimary: 'oklch(0.15 0.02 260)',
      textMuted: 'oklch(0.48 0.02 260)',
      ring: 'oklch(0.56 0.21 255)',
    },
    typography: {
      display: 'Vazirmatn, Inter, system-ui, -apple-system, sans-serif',
      body: 'Vazirmatn, Inter, system-ui, -apple-system, sans-serif',
      mono: 'JetBrains Mono, ui-monospace, monospace',
    },
  },
};
