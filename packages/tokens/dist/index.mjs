/**
 * @vibe-ui/tokens
 * Typed OKLCH design tokens, physics curves, and contrast utilities.
 */
export const VISUAL_CHEMISTRIES = {
    MINIMALIST_SAAS: {
        id: 'MINIMALIST_SAAS',
        name: 'Minimalist SaaS',
        tagline: 'High-signal B2B productivity with subtle borders and monochrome restraint',
        colors: {
            canvas: 'oklch(0.985 0.002 264)',
            surface: 'oklch(1 0 0)',
            border: 'oklch(0.90 0.008 264)',
            primaryAccent: 'oklch(0.55 0.22 260)',
            onPrimaryAccent: 'oklch(0.99 0 0)',
            textPrimary: 'oklch(0.14 0.005 264)',
            textMuted: 'oklch(0.48 0.015 264)',
            ring: 'oklch(0.55 0.22 260)',
        },
        darkColors: {
            canvas: 'oklch(0.14 0.005 264)',
            surface: 'oklch(0.18 0.008 264)',
            border: 'oklch(0.28 0.01 264)',
            primaryAccent: 'oklch(0.65 0.22 260)',
            onPrimaryAccent: 'oklch(0.99 0 0)',
            textPrimary: 'oklch(0.98 0.002 264)',
            textMuted: 'oklch(0.65 0.015 264)',
            ring: 'oklch(0.65 0.22 260)',
        },
        typography: {
            display: 'Vazirmatn, Inter, system-ui, sans-serif',
            body: 'Vazirmatn, Inter, system-ui, sans-serif',
            mono: 'JetBrains Mono, Menlo, monospace',
        },
        physics: {
            springStiffness: 280,
            dampingRatio: 0.85,
            lerpAlpha: '1 - Math.exp(-14 * dt)',
        },
    },
    LUXURY_GLASS_2: {
        id: 'LUXURY_GLASS_2',
        name: 'Luxury Glassmorphism 2.0',
        tagline: 'Deep dark substrates with specular highlights and gold accents',
        colors: {
            canvas: 'oklch(0.97 0.01 85)',
            surface: 'oklch(1 0 0 / 0.85)',
            border: 'oklch(0.75 0.12 85 / 0.4)',
            primaryAccent: 'oklch(0.65 0.18 85)',
            onPrimaryAccent: 'oklch(0.12 0.02 85)',
            textPrimary: 'oklch(0.16 0.02 85)',
            textMuted: 'oklch(0.45 0.03 85)',
            ring: 'oklch(0.65 0.18 85)',
        },
        darkColors: {
            canvas: 'oklch(0.12 0.015 280)',
            surface: 'oklch(0.18 0.02 280 / 0.75)',
            border: 'oklch(0.75 0.15 85 / 0.35)',
            primaryAccent: 'oklch(0.78 0.16 85)',
            onPrimaryAccent: 'oklch(0.12 0.02 85)',
            textPrimary: 'oklch(0.98 0.005 85)',
            textMuted: 'oklch(0.70 0.03 85)',
            ring: 'oklch(0.78 0.16 85)',
        },
        typography: {
            display: 'Cinzel, Playfair Display, Vazirmatn, serif',
            body: 'Vazirmatn, Plus Jakarta Sans, sans-serif',
            mono: 'JetBrains Mono, monospace',
        },
        physics: {
            springStiffness: 180,
            dampingRatio: 0.92,
            lerpAlpha: '1 - Math.exp(-8 * dt)',
        },
    },
    NEOBRUTALISM: {
        id: 'NEOBRUTALISM',
        name: 'Neobrutalism',
        tagline: 'High-contrast saturated flat cards with hard 3px black offset shadows',
        colors: {
            canvas: 'oklch(0.96 0.01 95)',
            surface: 'oklch(0.99 0.002 95)',
            border: 'oklch(0.15 0.01 95)',
            primaryAccent: 'oklch(0.82 0.20 135)',
            onPrimaryAccent: 'oklch(0.10 0.01 95)',
            textPrimary: 'oklch(0.12 0.01 95)',
            textMuted: 'oklch(0.35 0.02 95)',
            ring: 'oklch(0.15 0.01 95)',
        },
        darkColors: {
            canvas: 'oklch(0.15 0.01 95)',
            surface: 'oklch(0.20 0.015 95)',
            border: 'oklch(0.95 0.01 95)',
            primaryAccent: 'oklch(0.82 0.20 135)',
            onPrimaryAccent: 'oklch(0.10 0.01 95)',
            textPrimary: 'oklch(0.96 0.01 95)',
            textMuted: 'oklch(0.70 0.02 95)',
            ring: 'oklch(0.82 0.20 135)',
        },
        typography: {
            display: 'Space Grotesk, Syne, Vazirmatn, sans-serif',
            body: 'Vazirmatn, Space Grotesk, sans-serif',
            mono: 'Space Mono, monospace',
        },
        physics: {
            springStiffness: 450,
            dampingRatio: 0.7,
            lerpAlpha: '1 - Math.exp(-22 * dt)',
        },
    },
    SWISS_EDITORIAL: {
        id: 'SWISS_EDITORIAL',
        name: 'Swiss Editorial',
        tagline: 'Asymmetric typography-first layout inspired by International Typographic Style',
        colors: {
            canvas: 'oklch(0.97 0.005 80)',
            surface: 'oklch(0.93 0.008 80)',
            border: 'oklch(0.20 0.005 80)',
            primaryAccent: 'oklch(0.58 0.24 28)',
            onPrimaryAccent: 'oklch(0.99 0 0)',
            textPrimary: 'oklch(0.15 0.005 80)',
            textMuted: 'oklch(0.42 0.01 80)',
            ring: 'oklch(0.58 0.24 28)',
        },
        darkColors: {
            canvas: 'oklch(0.13 0.005 80)',
            surface: 'oklch(0.17 0.008 80)',
            border: 'oklch(0.35 0.005 80)',
            primaryAccent: 'oklch(0.68 0.22 28)',
            onPrimaryAccent: 'oklch(0.12 0.005 80)',
            textPrimary: 'oklch(0.95 0.005 80)',
            textMuted: 'oklch(0.65 0.01 80)',
            ring: 'oklch(0.68 0.22 28)',
        },
        typography: {
            display: 'Helvetica Neue, Arial, Vazirmatn, sans-serif',
            body: 'Newsreader, Georgia, Vazirmatn, serif',
            mono: 'Courier New, monospace',
        },
        physics: {
            springStiffness: 300,
            dampingRatio: 0.9,
            lerpAlpha: '1 - Math.exp(-12 * dt)',
        },
    },
    STRIPE_CRISP_LIGHT: {
        id: 'STRIPE_CRISP_LIGHT',
        name: 'Stripe Crisp Light',
        tagline: 'Ultra-clean developer-first documentation layout with refined micro-borders',
        colors: {
            canvas: 'oklch(0.985 0.002 247.8)',
            surface: 'oklch(1 0 0)',
            border: 'oklch(0.90 0.008 247.8)',
            primaryAccent: 'oklch(0.55 0.22 265)',
            onPrimaryAccent: 'oklch(0.99 0 0)',
            textPrimary: 'oklch(0.20 0.02 265)',
            textMuted: 'oklch(0.50 0.02 265)',
            ring: 'oklch(0.55 0.22 265)',
        },
        darkColors: {
            canvas: 'oklch(0.13 0.005 265)',
            surface: 'oklch(0.17 0.008 265)',
            border: 'oklch(0.26 0.01 265)',
            primaryAccent: 'oklch(0.65 0.22 265)',
            onPrimaryAccent: 'oklch(0.99 0 0)',
            textPrimary: 'oklch(0.98 0 0)',
            textMuted: 'oklch(0.65 0.01 265)',
            ring: 'oklch(0.65 0.22 265)',
        },
        typography: {
            display: 'Vazirmatn, Inter, system-ui, sans-serif',
            body: 'Vazirmatn, Inter, system-ui, sans-serif',
            mono: 'Fira Code, monospace',
        },
        physics: {
            springStiffness: 320,
            dampingRatio: 0.88,
            lerpAlpha: '1 - Math.exp(-16 * dt)',
        },
    },
};
/** Easing curves adhering to Vibe UI motion standards */
export const MOTION_CURVES = {
    naturalSpring: 'cubic-bezier(0.16, 1, 0.3, 1)',
    responsiveSnap: 'cubic-bezier(0.25, 1, 0.5, 1)',
    crispEnter: 'cubic-bezier(0, 0, 0.2, 1)',
    crispExit: 'cubic-bezier(0.4, 0, 1, 1)',
};
/** Relative luminance formula conforming to WCAG 2.2 */
export function getRelativeLuminance(r, g, b) {
    const transform = (c) => {
        const s = c / 255;
        return s <= 0.04045 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
    };
    return 0.2126 * transform(r) + 0.7152 * transform(g) + 0.0722 * transform(b);
}
/** Contrast ratio between two luminance values */
export function getContrastRatio(lumA, lumB) {
    const l1 = Math.max(lumA, lumB);
    const l2 = Math.min(lumA, lumB);
    return (l1 + 0.05) / (l2 + 0.05);
}
