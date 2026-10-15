#!/usr/bin/env node

import * as fs from 'fs';
import * as path from 'path';
import * as readline from 'readline';
import { COMPONENT_REGISTRY } from './registry/components';
import { VISUAL_CHEMISTRIES } from './index';

const VERSION = '6.1.1';

interface CliOptions {
  force: boolean;
  dryRun: boolean;
  yes?: boolean;
  chemistry?: string;
  editor?: string;
}

function printBanner() {
  console.log(`
\x1b[35m  ▲ VIBE UI CLI v${VERSION}\x1b[0m
  \x1b[90mDeterministic UI contracts, 11 design paradigms & flagship components for AI coding assistants\x1b[0m
`);
}

function printHelp() {
  printBanner();
  console.log(`\x1b[1mUSAGE:\x1b[0m
  npx vibe-ui-suite <command> [options]
  vibe-ui <command> [options]

\x1b[1mCOMMANDS:\x1b[0m
  \x1b[32minit\x1b[0m               Initialize Vibe UI contracts, 11 paradigm tokens & AI rules in current project
  \x1b[32msync\x1b[0m               Synchronize existing AI contracts to canonical v${VERSION} master rules
  \x1b[32minstall-skills\x1b[0m     Install or update Vibe UI agent skills in .agents/skills/
  \x1b[32madd <component>\x1b[0m     Add an accessible, AI-native component template to your project
  \x1b[32mlist\x1b[0m               List all available component primitives in the registry

\x1b[1mOPTIONS:\x1b[0m
  -f, --force        Overwrite existing files (creates automated .bak backups)
  -y, --yes          Non-interactive mode (use defaults without prompting)
  --chemistry <1-5>  Select visual chemistry in non-interactive mode
  --editor <1-4>     Select target AI editor in non-interactive mode (1: Cursor, 2: Claude, 3: Windsurf, 4: All)
  --dry-run          Preview file operations without making actual modifications
  -v, --version      Show CLI version
  -h, --help         Show help menu

\x1b[1mEXAMPLES:\x1b[0m
  npx vibe-ui-suite init
  npx vibe-ui-suite init -y
  npx vibe-ui-suite sync
  npx vibe-ui-suite install-skills
  npx vibe-ui-suite add device-mockup
  npx vibe-ui-suite add before-after-lens
  npx vibe-ui-suite add specular-card
  npx vibe-ui-suite add thinking-drawer
  npx vibe-ui-suite add shimmer-button
  npx vibe-ui-suite add theme-toggle
  npx vibe-ui-suite add device-mockup --force
`);
}

function prompt(rl: readline.Interface, query: string): Promise<string> {
  return new Promise((resolve) => rl.question(query, resolve));
}

function safeWriteFile(filePath: string, content: string, options: CliOptions): { written: boolean; skipped: boolean; backup?: string } {
  const relPath = path.relative(process.cwd(), filePath);
  if (options.dryRun) {
    console.log(`  \x1b[34m[dry-run]\x1b[0m Would write: ${relPath}`);
    return { written: false, skipped: false };
  }
  if (fs.existsSync(filePath) && !options.force) {
    console.log(`  \x1b[33m[skip]\x1b[0m ${relPath} already exists. (Use --force to overwrite)`);
    return { written: false, skipped: true };
  }
  if (fs.existsSync(filePath) && options.force) {
    const backupPath = `${filePath}.bak`;
    fs.copyFileSync(filePath, backupPath);
    fs.writeFileSync(filePath, content, 'utf-8');
    console.log(`  \x1b[35m[backup]\x1b[0m Backed up existing file to ${path.relative(process.cwd(), backupPath)}`);
    return { written: true, skipped: false, backup: backupPath };
  }
  fs.writeFileSync(filePath, content, 'utf-8');
  return { written: true, skipped: false };
}

const CONTRACT_RULES = `# 👑 Vibe UI Master Design & Architecture Contract (v6.1.1)
# Generated via npx vibe-ui-suite init / sync

## 🏛️ The 5 Master Execution Gates & Autonomous Lazy-Prompt Protocol
When receiving UI design or redesign prompts (especially lazy prompts: "design this", "redesign this", "make it look good", "make it pop", "craft a modern UI"):

1. 📸 MANDATORY PRE-EDIT VISUAL AUDIT:
   - Before editing any code, capture an initial browser screenshot (screenshots/before.png).
   - Visually critique layout flaws, spacing balance, visual hierarchy, and focal points with multimodal vision.

2. 🎨 ARCHITECTURAL PARADIGM & TREND BENCHMARKING:
   - Benchmark against premier design sources: Dribbble, Figma Community, Mobbin, and Awwwards.
   - Autonomously select a modern paradigm (Bento Grid, Linear Minimal, Stripe Crisp Light, Swiss Editorial).
   - Light Mode is the primary default canvas (#ffffff/#f8fafc). Mandatory dual-theme support with accessible Dark Mode toggle.

3. 🧱 STRUCTURAL DOM & SPATIAL OVERHAUL:
   - ZERO COSMETIC-ONLY PATCH INVARIANT: Strictly forbidden to perform shallow skin-patches (altering only colors, borders, or emojis while leaving dead layouts untouched).
   - Overhaul structural spatial rhythm, 8pt spacing system, and asymmetric bento card hierarchies.
   - Inject tactile micro-interactions (shimmer buttons, cyber loaders, tactile switches, holographic cards) and authentic imagery.
   - CONTEXTUAL CREATIVE MEDIA: Background video is strictly contextual (for creative/cinematic requests only); never force video onto utility SaaS or dashboards. Intelligently evaluate whether curated video, lightweight SVG particles, or static photography deliver the cleanest UX.

4. 👁️ MULTI-VIEWPORT LIVING VISUAL VERIFICATION:
   - Capture post-edit full-page screenshots (screenshots/after.png, Desktop 1440px / Mobile 390px).
   - Multimodal self-critique: verify visual rhythm, zero horizontal overflow, and pristine typography hierarchy before handoff.

5. 🧼 SILENT TABLE-STAKES (INTERNAL WORKER BASELINES):
   - Low-level hygiene (OKLCH color math, WCAG AAA formulas, zero raw unicode emojis -> inline SVGs, <bdi> bidirectional text isolation) are silent worker requirements.
   - NEVER report these hygiene baselines as headline accomplishments or key deliverables in chat summaries.
   - Chat summaries MUST lead with architectural layout transformations, aesthetic paradigm chosen, and visual before/after evidence.
`;

function findSourceSkillsDir(): string | null {
  const candidates = [
    path.resolve(__dirname, '..', 'skills'),
    path.resolve(__dirname, 'skills'),
    path.resolve(__dirname, '..', '..', '..', 'skills'),
    path.resolve(process.cwd(), 'skills'),
  ];
  for (const c of candidates) {
    if (fs.existsSync(c) && fs.existsSync(path.join(c, 'ui-kit', 'SKILL.md'))) {
      return c;
    }
  }
  return null;
}

function installSkills(targetProjectDir: string, options: CliOptions): { installed: string[]; skipped: string[] } {
  const srcSkillsDir = findSourceSkillsDir();
  const installed: string[] = [];
  const skipped: string[] = [];

  if (!srcSkillsDir) {
    console.log('  \x1b[33m[warn]\x1b[0m Could not locate Vibe UI skills source directory to install.');
    return { installed, skipped };
  }

  const destSkillsDir = path.join(targetProjectDir, '.agents', 'skills');

  if (options.dryRun) {
    console.log(`  \x1b[34m[dry-run]\x1b[0m Would install Vibe UI skills to: ${path.relative(process.cwd(), destSkillsDir)}`);
    return { installed, skipped };
  }

  if (!fs.existsSync(destSkillsDir)) {
    fs.mkdirSync(destSkillsDir, { recursive: true });
  }

  const skillsList = fs.readdirSync(srcSkillsDir).filter((f) => {
    const full = path.join(srcSkillsDir, f);
    return fs.statSync(full).isDirectory() && fs.existsSync(path.join(full, 'SKILL.md'));
  });

  for (const skillName of skillsList) {
    const srcSkillPath = path.join(srcSkillsDir, skillName);
    const destSkillPath = path.join(destSkillsDir, skillName);

    if (fs.existsSync(destSkillPath) && !options.force) {
      skipped.push(skillName);
      continue;
    }

    if (fs.existsSync(destSkillPath) && options.force) {
      fs.rmSync(destSkillPath, { recursive: true, force: true });
    }

    fs.cpSync(srcSkillPath, destSkillPath, { recursive: true });
    installed.push(skillName);
  }

  return { installed, skipped };
}

async function handleInstallSkills(options: CliOptions) {
  printBanner();
  console.log('\x1b[36mInstalling Vibe UI Agent Skills into current project workspace (.agents/skills/)...\x1b[0m\n');
  const cwd = process.cwd();
  const res = installSkills(cwd, options);

  if (res.installed.length > 0) {
    console.log(`\n\x1b[32m✔ Successfully installed ${res.installed.length} skill(s) in .agents/skills/:\x1b[0m`);
    res.installed.forEach((s) => console.log(`  + .agents/skills/${s}`));
  }
  if (res.skipped.length > 0) {
    console.log(`\n\x1b[33mSkipped ${res.skipped.length} existing skill(s) (use --force to overwrite):\x1b[0m`);
    res.skipped.forEach((s) => console.log(`  - ${s}`));
  }
}

async function handleSync(options: CliOptions) {
  printBanner();
  console.log('\x1b[36mSynchronizing AI contracts to canonical v6.1.1 Master Architectural Standard...\x1b[0m\n');
  const cwd = process.cwd();
  const targetFiles = ['.cursorrules', '.windsurfrules', 'CLAUDE.md'];
  let updatedCount = 0;

  for (const filename of targetFiles) {
    const filePath = path.join(cwd, filename);
    if (fs.existsSync(filePath)) {
      const res = safeWriteFile(filePath, CONTRACT_RULES, { ...options, force: true });
      if (res.written) {
        console.log(`  \x1b[32m✔\x1b[0m Updated \x1b[1m${filename}\x1b[0m to v6.1.1 contract rules`);
        updatedCount++;
      }
    }
  }

  const destSkills = path.join(cwd, '.agents', 'skills');
  if (fs.existsSync(destSkills) || updatedCount > 0) {
    console.log('\n\x1b[36mSynchronizing Vibe UI workspace skills (.agents/skills/):\x1b[0m');
    const skillRes = installSkills(cwd, { ...options, force: true });
    if (skillRes.installed.length > 0) {
      console.log(`  \x1b[32m✔\x1b[0m Synchronized ${skillRes.installed.length} skills in .agents/skills/`);
    }
  }

  if (updatedCount === 0) {
    console.log('  \x1b[33mNo existing AI rule files found in current directory.\x1b[0m');
    console.log('  Run \x1b[32mnpx vibe-ui-suite init\x1b[0m to initialize contracts from scratch.');
  } else {
    console.log(`\n\x1b[32m✔ Successfully synchronized AI rule file(s) and workspace skills to v6.1.1!\x1b[0m`);
  }
}

async function handleInit(options: CliOptions) {
  printBanner();
  if (options.dryRun) {
    console.log('\x1b[34m[DRY-RUN MODE ACTIVATED: No files will be modified on disk]\x1b[0m\n');
  }

  const isInteractive = !options.yes && Boolean(process.stdin.isTTY);
  let chemChoice = options.chemistry || '1';
  let editorChoice = options.editor || '4';

  const chemMap: Record<string, keyof typeof VISUAL_CHEMISTRIES> = {
    '1': 'MINIMALIST_SAAS',
    '2': 'LUXURY_GLASS_2',
    '3': 'NEOBRUTALISM',
    '4': 'SWISS_EDITORIAL',
    '5': 'STRIPE_CRISP_LIGHT',
  };

  if (isInteractive) {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
    });

    try {
      console.log('\x1b[1mInitialize Vibe UI in current workspace:\x1b[0m\n');

      // 1. Select Visual Chemistry
      console.log('\x1b[36m1. Select Visual Chemistry:\x1b[0m');
      console.log('  [1] Minimalist SaaS (Monochrome restraint, high signal - Recommended)');
      console.log('  [2] Luxury Glass 2.0 (Specular Fresnel, deep dark, gold accents)');
      console.log('  [3] Neobrutalism (Hard 3px black offset shadows, bold high saturation)');
      console.log('  [4] Swiss Editorial (Asymmetric grid, typography-first, high contrast)');
      console.log('  [5] Stripe Crisp Light (Developer docs, precision micro-borders)');

      chemChoice = (await prompt(rl, 'Choice [1-5] (default: 1): ')).trim() || '1';

      // 2. Select AI Editor
      console.log('\n\x1b[36m2. Select AI Coding Environment:\x1b[0m');
      console.log('  [1] Cursor (.cursorrules - Recommended)');
      console.log('  [2] Claude Code (CLAUDE.md)');
      console.log('  [3] Windsurf (.windsurfrules)');
      console.log('  [4] All of the above');

      editorChoice = (await prompt(rl, 'Choice [1-4] (default: 1): ')).trim() || '1';
    } finally {
      rl.close();
    }
  } else {
    console.log('\x1b[36m  [auto]\x1b[0m Non-interactive mode activated. Using defaults.');
  }

  const selectedChemKey = chemMap[chemChoice] || 'MINIMALIST_SAAS';
  const selectedChem = VISUAL_CHEMISTRIES[selectedChemKey];
  const darkColors = selectedChem.darkColors || selectedChem.colors;

  console.log(`  \x1b[32m✔\x1b[0m Visual Chemistry: \x1b[1m${selectedChem.name}\x1b[0m (Dual Light & Dark Themes)`);

  // 3. Write contract rules safely
  const cwd = process.cwd();
  const createdFiles: string[] = [];

  if (editorChoice === '1' || editorChoice === '4') {
    const res = safeWriteFile(path.join(cwd, '.cursorrules'), CONTRACT_RULES, options);
    if (res.written) createdFiles.push('.cursorrules');
  }
  if (editorChoice === '2' || editorChoice === '4') {
    const claudePath = path.join(cwd, 'CLAUDE.md');
    if (options.dryRun) {
      console.log('  \x1b[34m[dry-run]\x1b[0m Would update CLAUDE.md');
    } else if (fs.existsSync(claudePath)) {
      fs.appendFileSync(claudePath, `\n\n${CONTRACT_RULES}`, 'utf-8');
      createdFiles.push('CLAUDE.md (appended)');
    } else {
      const res = safeWriteFile(claudePath, CONTRACT_RULES, options);
      if (res.written) createdFiles.push('CLAUDE.md');
    }
  }
  if (editorChoice === '3' || editorChoice === '4') {
    const res = safeWriteFile(path.join(cwd, '.windsurfrules'), CONTRACT_RULES, options);
    if (res.written) createdFiles.push('.windsurfrules');
  }

  // 4. Generate Dual-Theme CSS Tokens file safely
  const cssContent = `:root {
  /* Vibe UI Chemistry: ${selectedChem.name} (${selectedChem.id}) - Light Theme */
  --vibe-canvas: ${selectedChem.colors.canvas};
  --vibe-surface: ${selectedChem.colors.surface};
  --vibe-border: ${selectedChem.colors.border};
  --vibe-primary-accent: ${selectedChem.colors.primaryAccent};
  --vibe-on-primary: ${selectedChem.colors.onPrimaryAccent};
  --vibe-text-primary: ${selectedChem.colors.textPrimary};
  --vibe-text-muted: ${selectedChem.colors.textMuted};
  --vibe-ring: ${selectedChem.colors.ring};
}

.dark, [data-theme="dark"] {
  /* Vibe UI Chemistry: ${selectedChem.name} (${selectedChem.id}) - Dark Theme */
  --vibe-canvas: ${darkColors.canvas};
  --vibe-surface: ${darkColors.surface};
  --vibe-border: ${darkColors.border};
  --vibe-primary-accent: ${darkColors.primaryAccent};
  --vibe-on-primary: ${darkColors.onPrimaryAccent};
  --vibe-text-primary: ${darkColors.textPrimary};
  --vibe-text-muted: ${darkColors.textMuted};
  --vibe-ring: ${darkColors.ring};
}
`;
  const cssPath = path.join(cwd, 'vibe-tokens.css');
  const cssRes = safeWriteFile(cssPath, cssContent, options);
  if (cssRes.written) createdFiles.push('vibe-tokens.css');

  // 5. Install Vibe UI Workspace Skills into .agents/skills/
  console.log('\n\x1b[36mInstalling Vibe UI Agent Skills (.agents/skills/):\x1b[0m');
  const skillRes = installSkills(cwd, options);
  if (skillRes.installed.length > 0) {
    skillRes.installed.forEach((s) => {
      console.log(`  \x1b[32m✔\x1b[0m Installed skill: \x1b[1m${s}\x1b[0m`);
      createdFiles.push(`.agents/skills/${s}`);
    });
  }
  if (skillRes.skipped.length > 0) {
    skillRes.skipped.forEach((s) => console.log(`  \x1b[33m[skip]\x1b[0m Skill ${s} already installed (use --force to overwrite)`));
  }

  console.log('\n\x1b[32m✔ Initialized successfully!\x1b[0m');
  if (createdFiles.length > 0) {
    console.log('\x1b[90mGenerated/Updated files:\x1b[0m');
    createdFiles.forEach((f) => console.log(`  + ${f}`));
  }

  console.log(`
\x1b[1mNext Steps:\x1b[0m
1. Import \x1b[35mvibe-tokens.css\x1b[0m into your layout or globals.css
2. Run \x1b[32mnpx vibe-ui-suite add thinking-drawer\x1b[0m to add your first AI component
3. Run \x1b[32mnpx vibe-ui-suite add theme-toggle\x1b[0m to add accessible Dark/Light theme switch
`);
}

function handleAdd(componentName?: string, options: CliOptions = { force: false, dryRun: false }) {
  if (!componentName) {
    console.log('\x1b[33mError: Please specify a component to add.\x1b[0m\n');
    handleList();
    console.log('\nUsage: npx vibe-ui-suite add <component> [--force]');
    process.exit(1);
    return;
  }

  const comp = COMPONENT_REGISTRY[componentName.toLowerCase()];
  if (!comp) {
    console.log(`\x1b[31mError: Unknown component "${componentName}".\x1b[0m\n`);
    handleList();
    process.exit(1);
    return;
  }

  const cwd = process.cwd();
  const targetDir = path.join(cwd, 'components', 'vibe-ui');
  if (!options.dryRun) {
    fs.mkdirSync(targetDir, { recursive: true });
  }

  const targetFile = path.join(targetDir, comp.filename);
  const writeRes = safeWriteFile(targetFile, comp.code, options);

  if (writeRes.skipped) {
    console.log(`\n\x1b[33mWarning: Component already exists at components/vibe-ui/${comp.filename}\x1b[0m`);
    console.log(`To overwrite with automated .bak backup, re-run with:`);
    console.log(`  \x1b[32mnpx vibe-ui-suite add ${componentName} --force\x1b[0m\n`);
    return;
  }

  if (writeRes.written) {
    console.log(`\x1b[32m✔ Added component "${comp.name}"!\x1b[0m`);
    console.log(`  \x1b[90mLocation:\x1b[0m components/vibe-ui/${comp.filename}`);
    console.log(`  \x1b[90mDescription:\x1b[0m ${comp.description}\n`);
    console.log(`\x1b[1mUsage in your page or view:\x1b[0m`);
    console.log(`  import { ${comp.filename.replace('.tsx', '')} } from '@/components/vibe-ui/${comp.filename.replace('.tsx', '')}';\n`);
  }
}

function handleList() {
  console.log('\x1b[1mAvailable Vibe UI Components:\x1b[0m\n');

  console.log('  \x1b[1;36mAI Contracts & Observation:\x1b[0m');
  Object.values(COMPONENT_REGISTRY)
    .filter((comp) => comp.category === 'ai-contracts')
    .forEach((comp) => {
      console.log(`    \x1b[32m${comp.name.padEnd(20)}\x1b[0m \x1b[90m${comp.description}\x1b[0m`);
    });

  console.log('\n  \x1b[1;35mLiving Micro-Interactions:\x1b[0m');
  Object.values(COMPONENT_REGISTRY)
    .filter((comp) => comp.category === 'living-micro-interactions')
    .forEach((comp) => {
      console.log(`    \x1b[32m${comp.name.padEnd(20)}\x1b[0m \x1b[90m${comp.description}\x1b[0m`);
    });
  console.log('');
}

async function main() {
  const rawArgs = process.argv.slice(2);
  const force = rawArgs.includes('--force') || rawArgs.includes('-f');
  const dryRun = rawArgs.includes('--dry-run');
  const yes = rawArgs.includes('--yes') || rawArgs.includes('-y');

  let chemistry: string | undefined;
  let editor: string | undefined;
  for (let i = 0; i < rawArgs.length; i++) {
    if (rawArgs[i] === '--chemistry' && rawArgs[i + 1]) chemistry = rawArgs[i + 1];
    if (rawArgs[i] === '--editor' && rawArgs[i + 1]) editor = rawArgs[i + 1];
  }

  const filteredArgs = rawArgs.filter(
    (a: string) => !['--force', '-f', '--dry-run', '--yes', '-y', '--chemistry', '--editor'].includes(a) && a !== chemistry && a !== editor
  );
  const cmd = filteredArgs[0]?.toLowerCase();

  const options: CliOptions = { force, dryRun, yes, chemistry, editor };

  if (!cmd || cmd === '--help' || cmd === '-h') {
    printHelp();
    return;
  }

  if (cmd === '--version' || cmd === '-v') {
    console.log(`v${VERSION}`);
    return;
  }

  switch (cmd) {
    case 'init':
      await handleInit(options);
      break;
    case 'sync':
    case 'update':
      await handleSync(options);
      break;
    case 'install-skills':
    case 'skills':
      await handleInstallSkills(options);
      break;
    case 'add':
      handleAdd(filteredArgs[1], options);
      break;
    case 'list':
      printBanner();
      handleList();
      break;
    default:
      console.log(`\x1b[31mUnknown command "${cmd}".\x1b[0m`);
      printHelp();
      process.exit(1);
  }
}

main().catch((err) => {
  console.error('\x1b[31mFatal CLI error:\x1b[0m', err);
  process.exit(1);
});

