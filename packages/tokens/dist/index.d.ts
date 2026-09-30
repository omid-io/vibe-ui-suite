/**
 * @vibe-ui/tokens
 * Typed OKLCH design tokens, physics curves, and contrast utilities.
 */
export type VisualChemistryId = 'MINIMALIST_SAAS' | 'LUXURY_GLASS_2' | 'NEOBRUTALISM' | 'SWISS_EDITORIAL' | 'STRIPE_CRISP_LIGHT';
export interface ChemistryColors {
    canvas: string;
    surface: string;
    border: string;
    primaryAccent: string;
    /** Text color on primary accent guaranteeing >= 4.5:1 (AA) or >= 7:1 (AAA) contrast */
    onPrimaryAccent: string;
    textPrimary: string;
    textMuted: string;
    ring: string;
}
export interface ChemistryTypography {
    display: string;
    body: string;
    mono: string;
}
export interface ChemistryPhysics {
    springStiffness: number;
    dampingRatio: number;
    lerpAlpha: string;
}
export interface VisualChemistry {
    id: VisualChemistryId;
    name: string;
    tagline: string;
    colors: ChemistryColors;
    darkColors?: ChemistryColors;
    typography: ChemistryTypography;
    physics: ChemistryPhysics;
}
export declare const VISUAL_CHEMISTRIES: Record<VisualChemistryId, VisualChemistry>;
/** Easing curves adhering to Vibe UI motion standards */
export declare const MOTION_CURVES: {
    readonly naturalSpring: "cubic-bezier(0.16, 1, 0.3, 1)";
    readonly responsiveSnap: "cubic-bezier(0.25, 1, 0.5, 1)";
    readonly crispEnter: "cubic-bezier(0, 0, 0.2, 1)";
    readonly crispExit: "cubic-bezier(0.4, 0, 1, 1)";
};
/** Relative luminance formula conforming to WCAG 2.2 */
export declare function getRelativeLuminance(r: number, g: number, b: number): number;
/** Contrast ratio between two luminance values */
export declare function getContrastRatio(lumA: number, lumB: number): number;
