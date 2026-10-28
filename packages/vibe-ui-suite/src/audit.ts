/**
 * Vibe UI Pure TypeScript Audit & Verification Engine
 * Audits HTML and React TSX/JSX files for WCAG contrast, mobile overflow risks,
 * raw unicode emojis, missing accessibility semantics, and bidirectional RTL isolation.
 * Zero external runtime dependencies.
 */

export interface AuditFinding {
  severity: 'FAIL' | 'WARN' | 'INFO';
  category: 'contrast' | 'accessibility' | 'responsive' | 'anti-slop' | 'bidi-rtl';
  message: string;
  line?: number;
  snippet?: string;
}

export interface AuditResult {
  filePath: string;
  pass: boolean;
  score: number; // 0 - 100
  counts: {
    fail: number;
    warn: number;
    info: number;
  };
  findings: AuditFinding[];
}

// Standard WCAG relative luminance calculation
export function hexToRgb(hex: string): { r: number; g: number; b: number } | null {
  const clean = hex.replace('#', '').trim();
  if (clean.length === 3) {
    return {
      r: parseInt(clean[0] + clean[0], 16),
      g: parseInt(clean[1] + clean[1], 16),
      b: parseInt(clean[2] + clean[2], 16),
    };
  }
  if (clean.length === 6) {
    return {
      r: parseInt(clean.substring(0, 2), 16),
      g: parseInt(clean.substring(2, 4), 16),
      b: parseInt(clean.substring(4, 6), 16),
    };
  }
  return null;
}

export function relativeLuminance(r: number, g: number, b: number): number {
  const rs = r / 255;
  const gs = g / 255;
  const bs = b / 255;

  const R = rs <= 0.03928 ? rs / 12.92 : Math.pow((rs + 0.055) / 1.055, 2.4);
  const G = gs <= 0.03928 ? gs / 12.92 : Math.pow((gs + 0.055) / 1.055, 2.4);
  const B = bs <= 0.03928 ? bs / 12.92 : Math.pow((bs + 0.055) / 1.055, 2.4);

  return 0.2126 * R + 0.7152 * G + 0.0722 * B;
}

export function contrastRatio(lum1: number, lum2: number): number {
  const lighter = Math.max(lum1, lum2);
  const darker = Math.min(lum1, lum2);
  return (lighter + 0.05) / (darker + 0.05);
}

// Regex for raw Unicode emoji symbols (Anti-slop rule: require accessible SVG or text)
const EMOJI_REGEX = /[\u{1F300}-\u{1F9FF}\u{1FA70}-\u{1FAFF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/u;

export function auditCode(content: string, filePath = '<inline-code>'): AuditResult {
  const findings: AuditFinding[] = [];
  const lines = content.split(/\r?\n/);

  // 1. Accessibility Checks: Clickable div without role="button" or tabIndex
  lines.forEach((line, idx) => {
    const lineNum = idx + 1;

    // Check 1: Non-semantic clickable elements
    if (
      (/<div[^>]*\sonClick/i.test(line) || /<span[^>]*\sonClick/i.test(line)) &&
      !/role=["']button["']/i.test(line)
    ) {
      findings.push({
        severity: 'FAIL',
        category: 'accessibility',
        message: 'Non-semantic clickable element (<div/span onClick>) without role="button". Use a native <button> or add role="button" and tabIndex={0}.',
        line: lineNum,
        snippet: line.trim(),
      });
    }

    // Check 2: Missing image alt attributes
    if (/<img\s/i.test(line) && !/\salt=/i.test(line)) {
      findings.push({
        severity: 'FAIL',
        category: 'accessibility',
        message: 'Image tag <img> is missing an accessible alt attribute.',
        line: lineNum,
        snippet: line.trim(),
      });
    }

    // Check 3: Raw Unicode Emoji (Anti-Slop rule)
    if (EMOJI_REGEX.test(line)) {
      // Exclude comments if possible
      if (!line.trim().startsWith('//') && !line.trim().startsWith('/*') && !line.trim().startsWith('*')) {
        findings.push({
          severity: 'WARN',
          category: 'anti-slop',
          message: 'Raw Unicode emoji detected. In professional UI, use accessible inline SVGs or wrap emojis with <span role="img" aria-label="...">.',
          line: lineNum,
          snippet: line.trim().slice(0, 80),
        });
      }
    }

    // Check 4: Risky hardcoded fixed widths causing horizontal mobile overflow
    if (/\b(?:w-\[?[0-9]{3,4}px\]?|min-w-\[?[5-9][0-9]{2}px\]?)\b/.test(line) && !/\b(?:sm:|md:|lg:|xl:)\b/.test(line)) {
      // If it has fixed width > 400px without responsive breakpoint
      const match = line.match(/\b(?:w-\[?([0-9]{3,4})px\]?|min-w-\[?([0-9]{3,4})px\]?)\b/);
      if (match) {
        const pxVal = parseInt(match[1] || match[2], 10);
        if (pxVal >= 420) {
          findings.push({
            severity: 'WARN',
            category: 'responsive',
            message: `Hardcoded wide width (${pxVal}px) without responsive mobile breakpoint (e.g., max-w-full or md: prefix). High risk of mobile horizontal overflow.`,
            line: lineNum,
            snippet: line.trim(),
          });
        }
      }
    }

    // Check 5: Form inputs without associated labels or aria-label
    if (/<input\s/i.test(line) && !/type=["']hidden["']/i.test(line)) {
      if (!/aria-label=/i.test(line) && !/id=/i.test(line) && !/aria-labelledby=/i.test(line)) {
        findings.push({
          severity: 'WARN',
          category: 'accessibility',
          message: '<input> element lacks explicit aria-label or id for label binding.',
          line: lineNum,
          snippet: line.trim(),
        });
      }
    }

    // Check 6: Bidirectional text without <bdi> isolation when mixed with variables/metrics
    if (/[\u0600-\u06FF]/.test(line) && (/\$[0-9]/.test(line) || /%[0-9]/.test(line) || /[0-9]+(?:\.[0-9]+)?\s*(?:ms|fps|gb|mb|px|rem|%)/i.test(line))) {
      if (!/<bdi>|<bdo>/i.test(line) && !/dir=["'](?:ltr|rtl)["']/i.test(line)) {
        findings.push({
          severity: 'WARN',
          category: 'bidi-rtl',
          message: 'Mixed RTL Persian text and LTR technical metrics/currencies detected without <bdi> isolation. May cause punctuation and number inversion.',
          line: lineNum,
          snippet: line.trim().slice(0, 80),
        });
      }
    }


    // Check 7: Mathematical WCAG AA Contrast Evaluation on declared color pairs
    const fgMatch = line.match(/(?:^|[;\s{])color\s*:\s*(#[0-9a-fA-F]{3,6})/i);
    const bgMatch = line.match(/(?:^|[;\s{])background(?:-color)?\s*:\s*(#[0-9a-fA-F]{3,6})/i);
    if (fgMatch && bgMatch) {
      const fgRgb = hexToRgb(fgMatch[1]);
      const bgRgb = hexToRgb(bgMatch[1]);
      if (fgRgb && bgRgb) {
        const fgLum = relativeLuminance(fgRgb.r, fgRgb.g, fgRgb.b);
        const bgLum = relativeLuminance(bgRgb.r, bgRgb.g, bgRgb.b);
        const cr = contrastRatio(fgLum, bgLum);
        if (cr < 4.5) {
          findings.push({
            severity: 'FAIL',
            category: 'contrast',
            message: `WCAG AA Contrast violation: ${cr.toFixed(2)}:1 is below the required 4.5:1 minimum (${fgMatch[1]} on ${bgMatch[1]}).`,
            line: lineNum,
            snippet: line.trim(),
          });
        }
      }
    }  });

  // 7. General Responsive Layout & Navigation Check
  if (/<nav\b/i.test(content)) {
    const hasHiddenMdFlex = /hidden\s+md:flex/i.test(content) || /md:flex\s+hidden/i.test(content);
    const hasMobileCounterpart = /md:hidden/i.test(content) || /hamburger/i.test(content) || /mobile/i.test(content) || /drawer/i.test(content);
    if (hasHiddenMdFlex && !hasMobileCounterpart) {
      findings.push({
        severity: 'FAIL',
        category: 'responsive',
        message: 'Desktop navigation (<nav class="hidden md:flex">) detected without a mobile navigation counterpart (0 md:hidden menu or hamburger). Navigation vanishes on screens <768px.',
      });
    }
  }

  // Calculate score and pass/fail
  const failCount = findings.filter(f => f.severity === 'FAIL').length;
  const warnCount = findings.filter(f => f.severity === 'WARN').length;
  const infoCount = findings.filter(f => f.severity === 'INFO').length;

  const score = Math.max(0, 100 - (failCount * 25) - (warnCount * 5));
  const pass = failCount === 0;

  return {
    filePath,
    pass,
    score,
    counts: {
      fail: failCount,
      warn: warnCount,
      info: infoCount,
    },
    findings,
  };
}
