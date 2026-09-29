/**
 * @vibe-ui/tokens/tailwind
 * Configurable OKLCH Tailwind CSS preset plugin for Vibe UI supporting all Visual Chemistries.
 */
import { VISUAL_CHEMISTRIES, MOTION_CURVES } from './index';
export function createVibeUiPlugin(options = {}) {
    const chemId = options.chemistry || 'MINIMALIST_SAAS';
    const chem = VISUAL_CHEMISTRIES[chemId] || VISUAL_CHEMISTRIES.MINIMALIST_SAAS;
    return function ({ addBase, addUtilities }) {
        const rootVariables = {
            '--vibe-canvas': chem.colors.canvas,
            '--vibe-surface': chem.colors.surface,
            '--vibe-border': chem.colors.border,
            '--vibe-primary': chem.colors.primaryAccent,
            '--vibe-text-primary': chem.colors.textPrimary,
            '--vibe-text-muted': chem.colors.textMuted,
            '--vibe-ring': chem.colors.ring,
        };
        if (addBase) {
            addBase({
                ':root': rootVariables,
                '[dir="rtl"]': {
                    'letter-spacing': 'normal !important',
                },
            });
        }
        if (addUtilities) {
            addUtilities({
                '.vibe-spring': {
                    'transition-timing-function': MOTION_CURVES.naturalSpring,
                },
                '.ease-vibe-spring': {
                    'transition-timing-function': MOTION_CURVES.naturalSpring,
                },
                '.vibe-snap': {
                    'transition-timing-function': MOTION_CURVES.responsiveSnap,
                },
                '.ease-vibe-snap': {
                    'transition-timing-function': MOTION_CURVES.responsiveSnap,
                },
                '.ease-vibe-glide': {
                    'transition-timing-function': 'cubic-bezier(0.25, 1, 0.5, 1)',
                },
                '.vibe-glass': {
                    'backdrop-filter': 'blur(12px)',
                    '-webkit-backdrop-filter': 'blur(12px)',
                },
            });
        }
    };
}
// Dual-mode handler: functions as direct plugin or configurable plugin factory
export function vibeUiTailwindPlugin(arg) {
    if (arg && (arg.addBase || arg.addUtilities)) {
        return createVibeUiPlugin({})(arg);
    }
    return createVibeUiPlugin(arg || {});
}
export default vibeUiTailwindPlugin;
