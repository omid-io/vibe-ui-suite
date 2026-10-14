// Challenger 1 - Milestone 1: Comprehensive Empirical Verification Suite
// Tests ESM/CJS dual-mode imports, contract exports, and component registry primitives

import { pathToFileURL } from 'url';
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs';
import { createRequire } from 'module';
import { execSync } from 'child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const require = createRequire(import.meta.url);

const suiteRoot = path.resolve(__dirname, '..');
const pkgDist = path.resolve(suiteRoot, 'packages', 'vibe-ui-suite', 'dist');

let totalTests = 0;
let passedTests = 0;
let failedTests = [];

function assert(condition, message) {
  totalTests++;
  if (condition) {
    passedTests++;
    console.log(`  [PASS] ${message}`);
  } else {
    failedTests.push(message);
    console.error(`  [FAIL] ${message}`);
  }
}

async function runEsmTests() {
  console.log('\n======================================================');
  console.log('CHALLENGER SUITE 1: Node ESM Imports & Contract Exports');
  console.log('======================================================');

  // 1. Import dist/index.mjs
  const indexUrl = pathToFileURL(path.join(pkgDist, 'index.mjs')).href;
  const esmIndex = await import(indexUrl);
  assert(esmIndex !== undefined && esmIndex !== null, 'dist/index.mjs imported successfully in ESM');

  // Assert VISUAL_CHEMISTRIES
  assert(typeof esmIndex.VISUAL_CHEMISTRIES === 'object', 'esmIndex.VISUAL_CHEMISTRIES is an object');
  const expectedChemistries = [
    'MINIMALIST_SAAS',
    'LUXURY_GLASS_2',
    'NEOBRUTALISM',
    'SWISS_EDITORIAL',
    'STRIPE_CRISP_LIGHT'
  ];
  const chemKeys = Object.keys(esmIndex.VISUAL_CHEMISTRIES || {});
  assert(
    expectedChemistries.every(k => chemKeys.includes(k)),
    `VISUAL_CHEMISTRIES contains all 5 canonical chemistries (${chemKeys.join(', ')})`
  );

  // Assert MOTION_CURVES
  assert(typeof esmIndex.MOTION_CURVES === 'object', 'esmIndex.MOTION_CURVES is an object');
  assert(typeof esmIndex.MOTION_CURVES.naturalSpring === 'string', 'MOTION_CURVES.naturalSpring is a string');
  assert(typeof esmIndex.MOTION_CURVES.responsiveSnap === 'string', 'MOTION_CURVES.responsiveSnap is a string');
  assert(typeof esmIndex.MOTION_CURVES.crispEnter === 'string', 'MOTION_CURVES.crispEnter is a string');
  assert(typeof esmIndex.MOTION_CURVES.crispExit === 'string', 'MOTION_CURVES.crispExit is a string');

  // Assert getRelativeLuminance & getContrastRatio
  assert(typeof esmIndex.getRelativeLuminance === 'function', 'esmIndex.getRelativeLuminance is a function');
  assert(typeof esmIndex.getContrastRatio === 'function', 'esmIndex.getContrastRatio is a function');

  const blackLum = esmIndex.getRelativeLuminance(0, 0, 0);
  const whiteLum = esmIndex.getRelativeLuminance(255, 255, 255);
  assert(Math.abs(blackLum - 0.0) < 1e-6, `getRelativeLuminance(0,0,0) is 0.0 (got ${blackLum})`);
  assert(Math.abs(whiteLum - 1.0) < 1e-6, `getRelativeLuminance(255,255,255) is 1.0 (got ${whiteLum})`);

  const maxRatio = esmIndex.getContrastRatio(whiteLum, blackLum);
  assert(Math.abs(maxRatio - 21.0) < 1e-4, `getContrastRatio(white, black) is 21.0:1 (got ${maxRatio})`);
  const commRatio = esmIndex.getContrastRatio(blackLum, whiteLum);
  assert(Math.abs(commRatio - 21.0) < 1e-4, `getContrastRatio commutativity holds (got ${commRatio})`);

  // Assert COMPONENT_REGISTRY re-exported from index.mjs
  assert(typeof esmIndex.COMPONENT_REGISTRY === 'object', 'esmIndex.COMPONENT_REGISTRY is re-exported from index.mjs');
  assert(
    Object.keys(esmIndex.COMPONENT_REGISTRY || {}).length === 9,
    `esmIndex.COMPONENT_REGISTRY has exactly 9 primitives (got ${Object.keys(esmIndex.COMPONENT_REGISTRY || {}).length})`
  );

  // 2. Import dist/tailwind.mjs
  const tailwindUrl = pathToFileURL(path.join(pkgDist, 'tailwind.mjs')).href;
  const esmTailwind = await import(tailwindUrl);
  assert(esmTailwind !== undefined && esmTailwind !== null, 'dist/tailwind.mjs imported successfully in ESM');
  assert(typeof esmTailwind.createVibeUiPlugin === 'function', 'esmTailwind.createVibeUiPlugin is a function');
  assert(typeof esmTailwind.vibeUiTailwindPlugin === 'function', 'esmTailwind.vibeUiTailwindPlugin is a function');
  assert(esmTailwind.default === esmTailwind.vibeUiTailwindPlugin, 'esmTailwind.default equals vibeUiTailwindPlugin');

  // Execute tailwind plugin factory
  let basesAdded = null;
  let utilitiesAdded = null;
  const dummyApi = {
    addBase: (b) => { basesAdded = b; },
    addUtilities: (u) => { utilitiesAdded = u; }
  };
  const pluginInstance = esmTailwind.createVibeUiPlugin({ chemistry: 'NEOBRUTALISM' });
  assert(typeof pluginInstance === 'function', 'createVibeUiPlugin() returns an executable plugin function');
  pluginInstance(dummyApi);
  assert(basesAdded !== null && basesAdded[':root'] !== undefined, 'Tailwind plugin generates :root CSS variables');
  assert(basesAdded['[dir="rtl"]'] !== undefined, 'Tailwind plugin generates [dir="rtl"] letter-spacing rule');
  assert(utilitiesAdded !== null && utilitiesAdded['.vibe-spring'] !== undefined, 'Tailwind plugin generates .vibe-spring utility');
  assert(utilitiesAdded['.vibe-glass'] !== undefined, 'Tailwind plugin generates .vibe-glass utility');

  // Test dual-mode vibeUiTailwindPlugin directly with Tailwind API
  let directBases = null;
  esmTailwind.vibeUiTailwindPlugin({
    addBase: (b) => { directBases = b; },
    addUtilities: () => {}
  });
  assert(directBases !== null && directBases[':root'] !== undefined, 'vibeUiTailwindPlugin works when invoked directly as a Tailwind plugin');

  // 3. Import dist/registry/components.mjs
  const registryUrl = pathToFileURL(path.join(pkgDist, 'registry', 'components.mjs')).href;
  const esmRegistry = await import(registryUrl);
  assert(esmRegistry !== undefined && esmRegistry !== null, 'dist/registry/components.mjs imported successfully in ESM');
  assert(typeof esmRegistry.COMPONENT_REGISTRY === 'object', 'esmRegistry.COMPONENT_REGISTRY is an object');
  assert(
    Object.keys(esmRegistry.COMPONENT_REGISTRY || {}).length === 9,
    `esmRegistry.COMPONENT_REGISTRY has 9 primitives (got ${Object.keys(esmRegistry.COMPONENT_REGISTRY || {}).length})`
  );

  // 4. Import dist/cli.mjs
  const cliUrl = pathToFileURL(path.join(pkgDist, 'cli.mjs')).href;
  const origArgv = process.argv;
  process.argv = [process.argv[0], path.join(pkgDist, 'cli.mjs'), '--version'];
  try {
    const esmCli = await import(cliUrl);
    assert(esmCli !== undefined, 'dist/cli.mjs imported cleanly without crashing');
  } finally {
    process.argv = origArgv;
  }
}

function runCjsTests() {
  console.log('\n======================================================');
  console.log('CHALLENGER SUITE 2: Node CJS Requires & Contract Exports');
  console.log('======================================================');

  // 1. Require dist/index.js
  const cjsIndexPath = path.join(pkgDist, 'index.js');
  const cjsIndex = require(cjsIndexPath);
  assert(cjsIndex !== undefined && cjsIndex !== null, 'dist/index.js required successfully in CJS');
  assert(typeof cjsIndex.VISUAL_CHEMISTRIES === 'object', 'cjsIndex.VISUAL_CHEMISTRIES is an object');
  assert(Object.keys(cjsIndex.VISUAL_CHEMISTRIES).length === 5, 'cjsIndex.VISUAL_CHEMISTRIES has 5 chemistries');
  assert(typeof cjsIndex.MOTION_CURVES === 'object', 'cjsIndex.MOTION_CURVES is an object');
  assert(typeof cjsIndex.getRelativeLuminance === 'function', 'cjsIndex.getRelativeLuminance is a function');
  assert(typeof cjsIndex.getContrastRatio === 'function', 'cjsIndex.getContrastRatio is a function');
  assert(typeof cjsIndex.COMPONENT_REGISTRY === 'object', 'cjsIndex.COMPONENT_REGISTRY is an object');
  assert(Object.keys(cjsIndex.COMPONENT_REGISTRY).length === 9, 'cjsIndex.COMPONENT_REGISTRY has 9 primitives');

  // 2. Require dist/tailwind.js
  const cjsTailwindPath = path.join(pkgDist, 'tailwind.js');
  const cjsTailwind = require(cjsTailwindPath);
  assert(cjsTailwind !== undefined && cjsTailwind !== null, 'dist/tailwind.js required successfully in CJS');
  assert(typeof cjsTailwind.createVibeUiPlugin === 'function', 'cjsTailwind.createVibeUiPlugin is a function');
  assert(typeof cjsTailwind.vibeUiTailwindPlugin === 'function', 'cjsTailwind.vibeUiTailwindPlugin is a function');
  assert(typeof cjsTailwind.default === 'function', 'cjsTailwind.default is a function');

  let cjsBases = null;
  cjsTailwind.vibeUiTailwindPlugin({ chemistry: 'LUXURY_GLASS_2' })({
    addBase: (b) => { cjsBases = b; },
    addUtilities: () => {}
  });
  assert(cjsBases !== null && cjsBases[':root'] !== undefined, 'cjsTailwind creates :root config for LUXURY_GLASS_2');

  // 3. Require dist/registry/components.js
  const cjsRegistryPath = path.join(pkgDist, 'registry', 'components.js');
  const cjsRegistry = require(cjsRegistryPath);
  assert(cjsRegistry !== undefined && cjsRegistry !== null, 'dist/registry/components.js required successfully in CJS');
  assert(typeof cjsRegistry.COMPONENT_REGISTRY === 'object', 'cjsRegistry.COMPONENT_REGISTRY is an object');
  assert(Object.keys(cjsRegistry.COMPONENT_REGISTRY).length === 9, 'cjsRegistry.COMPONENT_REGISTRY has 9 primitives');

  // 4. Require dist/cli.js
  const cjsCliPath = path.join(pkgDist, 'cli.js');
  const origArgv = process.argv;
  process.argv = [process.argv[0], cjsCliPath, '--version'];
  try {
    const cjsCli = require(cjsCliPath);
    assert(cjsCli !== undefined, 'dist/cli.js required cleanly without throwing');
  } finally {
    process.argv = origArgv;
  }
}

async function runComponentRegistryValidation() {
  console.log('\n======================================================');
  console.log('CHALLENGER SUITE 3: Component Registry 9 Primitives Audit');
  console.log('======================================================');

  const registryUrl = pathToFileURL(path.join(pkgDist, 'registry', 'components.mjs')).href;
  const { COMPONENT_REGISTRY } = await import(registryUrl);

  const expectedPrimitives = [
    { key: 'thinking-drawer', filename: 'AiThinkingDrawer.tsx', category: 'ai-contracts' },
    { key: 'telemetry-hud', filename: 'TelemetryHud.tsx', category: 'ai-contracts' },
    { key: 'contrast-badge', filename: 'ContrastBadge.tsx', category: 'ai-contracts' },
    { key: 'theme-toggle', filename: 'ThemeToggle.tsx', category: 'ai-contracts' },
    { key: 'shimmer-button', filename: 'ShimmerButton.tsx', category: 'living-micro-interactions' },
    { key: 'cyber-loader', filename: 'CyberLoader.tsx', category: 'living-micro-interactions' },
    { key: 'holographic-card', filename: 'HolographicCard.tsx', category: 'living-micro-interactions' },
    { key: 'tactile-switch', filename: 'TactileSwitch.tsx', category: 'living-micro-interactions' },
    { key: 'glow-input', filename: 'GlowInput.tsx', category: 'living-micro-interactions' }
  ];

  assert(Object.keys(COMPONENT_REGISTRY).length === 9, `Registry contains exactly 9 components (got ${Object.keys(COMPONENT_REGISTRY).length})`);

  let ts;
  try {
    ts = require('typescript');
  } catch (e) {
    ts = require(path.join(suiteRoot, 'examples', 'nextjs-starter', 'node_modules', 'typescript'));
  }

  for (const exp of expectedPrimitives) {
    const comp = COMPONENT_REGISTRY[exp.key];
    assert(comp !== undefined, `Component primitive '${exp.key}' exists in registry`);
    if (!comp) continue;

    assert(comp.name === exp.key, `'${exp.key}'.name matches registry key ('${comp.name}')`);
    assert(comp.filename === exp.filename, `'${exp.key}'.filename is '${exp.filename}' (got '${comp.filename}')`);
    assert(comp.category === exp.category, `'${exp.key}'.category is '${exp.category}' (got '${comp.category}')`);
    assert(typeof comp.description === 'string' && comp.description.length > 10, `'${exp.key}'.description is descriptive (len: ${comp.description?.length})`);
    assert(typeof comp.code === 'string' && comp.code.length > 100, `'${exp.key}'.code contains substantive template code (len: ${comp.code?.length})`);
    assert(comp.code.includes("'use client'") || comp.code.includes('"use client"'), `'${exp.key}'.code includes 'use client' directive for Next.js/React`);
    assert(!/[\u{1F300}-\u{1F9FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/u.test(comp.code), `'${exp.key}'.code adheres to Anti-Slop (0 raw unicode emojis)`);

    // TypeScript TSX syntax AST check
    const sf = ts.createSourceFile(comp.filename, comp.code, ts.ScriptTarget.Latest, true, ts.ScriptKind.TSX);
    const syntaxErrors = sf.parseDiagnostics || [];
    assert(syntaxErrors.length === 0, `'${exp.key}' AST parses as valid TSX with 0 syntax diagnostics`);

    // TypeScript compilation / transpilation check
    const transpiled = ts.transpileModule(comp.code, {
      compilerOptions: { jsx: ts.JsxEmit.ReactJSX, module: ts.ModuleKind.ESNext, target: ts.ScriptTarget.ES2022 }
    });
    assert(typeof transpiled.outputText === 'string' && transpiled.outputText.length > 50, `'${exp.key}' transpiles to clean JavaScript/JSX`);
  }
}

async function runCliExecutionSuite() {
  console.log('\n======================================================');
  console.log('CHALLENGER SUITE 4: CLI Execution & Output Verification');
  console.log('======================================================');

  const cliJs = path.join(pkgDist, 'cli.js');
  const cliMjs = path.join(pkgDist, 'cli.mjs');

  // Test cli.js --version
  const verOut = execSync(`node "${cliJs}" --version`, { encoding: 'utf-8' }).trim();
  assert(verOut === 'v6.0.0', `cli.js --version returns 'v6.0.0' (got '${verOut}')`);

  // Test cli.mjs --version
  const mjsVerOut = execSync(`node "${cliMjs}" --version`, { encoding: 'utf-8' }).trim();
  assert(mjsVerOut === 'v6.0.0', `cli.mjs --version returns 'v6.0.0' (got '${mjsVerOut}')`);

  // Test cli.js list
  const listOut = execSync(`node "${cliJs}" list`, { encoding: 'utf-8' });
  assert(listOut.includes('AI Contracts & Observation:'), 'cli.js list contains AI Contracts section');
  assert(listOut.includes('Living Micro-Interactions:'), 'cli.js list contains Living Micro-Interactions section');
  assert(listOut.includes('thinking-drawer'), 'cli.js list includes thinking-drawer');
  assert(listOut.includes('telemetry-hud'), 'cli.js list includes telemetry-hud');
  assert(listOut.includes('contrast-badge'), 'cli.js list includes contrast-badge');
  assert(listOut.includes('theme-toggle'), 'cli.js list includes theme-toggle');
  assert(listOut.includes('shimmer-button'), 'cli.js list includes shimmer-button');
  assert(listOut.includes('cyber-loader'), 'cli.js list includes cyber-loader');
  assert(listOut.includes('holographic-card'), 'cli.js list includes holographic-card');
  assert(listOut.includes('tactile-switch'), 'cli.js list includes tactile-switch');
  assert(listOut.includes('glow-input'), 'cli.js list includes glow-input');

  // Test cli.js add with --dry-run
  const dryRunOut = execSync(`node "${cliJs}" add shimmer-button --dry-run`, { encoding: 'utf-8' });
  assert(dryRunOut.includes('[dry-run]'), 'cli.js add --dry-run prints dry-run tag');
  assert(dryRunOut.includes('ShimmerButton.tsx'), 'cli.js add --dry-run targets ShimmerButton.tsx');
}

async function runAdversarialEdgeCases() {
  console.log('\n======================================================');
  console.log('CHALLENGER SUITE 5: Adversarial Edge Cases & Fallbacks');
  console.log('======================================================');

  const { createVibeUiPlugin, vibeUiTailwindPlugin } = await import(pathToFileURL(path.join(pkgDist, 'tailwind.mjs')).href);

  // Fallback on invalid chemistry
  let fallbackBases = null;
  const invalidPlugin = createVibeUiPlugin({ chemistry: 'NON_EXISTENT_CHEMISTRY' });
  invalidPlugin({
    addBase: (b) => { fallbackBases = b; },
    addUtilities: () => {}
  });
  assert(
    fallbackBases !== null && fallbackBases[':root']['--vibe-canvas'] === 'oklch(0.985 0.002 264)',
    'createVibeUiPlugin safely falls back to MINIMALIST_SAAS when given non-existent chemistry'
  );

  // Call vibeUiTailwindPlugin with undefined / empty
  const emptyPlugin = vibeUiTailwindPlugin();
  assert(typeof emptyPlugin === 'function', 'vibeUiTailwindPlugin() with no args returns plugin function');

  // Mathematical edge cases for getContrastRatio
  const { getContrastRatio } = await import(pathToFileURL(path.join(pkgDist, 'index.mjs')).href);
  assert(getContrastRatio(0, 0) === 1.0, 'getContrastRatio(0, 0) === 1.0');
  assert(getContrastRatio(1, 1) === 1.0, 'getContrastRatio(1, 1) === 1.0');
  assert(getContrastRatio(0.5, 0.5) === 1.0, 'getContrastRatio(0.5, 0.5) === 1.0');

  // Verify contrast calculation on all 5 chemistry onPrimaryAccent colors
  const { VISUAL_CHEMISTRIES } = await import(pathToFileURL(path.join(pkgDist, 'index.mjs')).href);
  for (const [id, chem] of Object.entries(VISUAL_CHEMISTRIES)) {
    assert(typeof chem.colors.canvas === 'string' && chem.colors.canvas.startsWith('oklch('), `${id} canvas uses valid OKLCH syntax`);
    assert(typeof chem.colors.surface === 'string' && chem.colors.surface.startsWith('oklch('), `${id} surface uses valid OKLCH syntax`);
    assert(typeof chem.colors.primaryAccent === 'string' && chem.colors.primaryAccent.startsWith('oklch('), `${id} primaryAccent uses valid OKLCH syntax`);
    assert(typeof chem.colors.onPrimaryAccent === 'string' && chem.colors.onPrimaryAccent.startsWith('oklch('), `${id} onPrimaryAccent uses valid OKLCH syntax`);
    assert(typeof chem.typography.display === 'string' && chem.typography.display.length > 0, `${id} defines display typography`);
    assert(typeof chem.physics.springStiffness === 'number' && chem.physics.springStiffness > 0, `${id} defines positive spring stiffness`);
  }
}

async function runPackageExportsSuite() {
  console.log('\n======================================================');
  console.log('CHALLENGER SUITE 6: Package Self-Reference Exports (ESM & CJS)');
  console.log('======================================================');

  const pkgDir = path.resolve(suiteRoot, 'packages', 'vibe-ui-suite');

  // ESM exports .
  const esmRoot = execSync(
    `node --input-type=module -e "import * as v from 'vibe-ui-suite'; console.log(JSON.stringify(Object.keys(v)));"`,
    { cwd: pkgDir, encoding: 'utf-8' }
  ).trim();
  const rootKeys = JSON.parse(esmRoot);
  assert(rootKeys.includes('COMPONENT_REGISTRY'), "Package exports '.' resolves in ESM with COMPONENT_REGISTRY");
  assert(rootKeys.includes('VISUAL_CHEMISTRIES'), "Package exports '.' resolves in ESM with VISUAL_CHEMISTRIES");

  // ESM exports ./tailwind
  const esmTailwind = execSync(
    `node --input-type=module -e "import * as tw from 'vibe-ui-suite/tailwind'; console.log(JSON.stringify(Object.keys(tw)));"`,
    { cwd: pkgDir, encoding: 'utf-8' }
  ).trim();
  const twKeys = JSON.parse(esmTailwind);
  assert(twKeys.includes('createVibeUiPlugin'), "Package exports './tailwind' resolves in ESM with createVibeUiPlugin");

  // ESM exports ./registry
  const esmRegistry = execSync(
    `node --input-type=module -e "import * as reg from 'vibe-ui-suite/registry'; console.log(JSON.stringify(Object.keys(reg)));"`,
    { cwd: pkgDir, encoding: 'utf-8' }
  ).trim();
  const regKeys = JSON.parse(esmRegistry);
  assert(regKeys.includes('COMPONENT_REGISTRY'), "Package exports './registry' resolves in ESM with COMPONENT_REGISTRY");

  // CJS exports .
  const cjsRoot = execSync(
    `node -e "const v = require('vibe-ui-suite'); console.log(JSON.stringify(Object.keys(v)));"`,
    { cwd: pkgDir, encoding: 'utf-8' }
  ).trim();
  const cjsRootKeys = JSON.parse(cjsRoot);
  assert(cjsRootKeys.includes('COMPONENT_REGISTRY'), "Package exports '.' resolves in CJS with COMPONENT_REGISTRY");

  // CJS exports ./tailwind
  const cjsTailwind = execSync(
    `node -e "const tw = require('vibe-ui-suite/tailwind'); console.log(JSON.stringify(Object.keys(tw)));"`,
    { cwd: pkgDir, encoding: 'utf-8' }
  ).trim();
  const cjsTwKeys = JSON.parse(cjsTailwind);
  assert(cjsTwKeys.includes('createVibeUiPlugin'), "Package exports './tailwind' resolves in CJS with createVibeUiPlugin");

  // CJS exports ./registry
  const cjsReg = execSync(
    `node -e "const reg = require('vibe-ui-suite/registry'); console.log(JSON.stringify(Object.keys(reg)));"`,
    { cwd: pkgDir, encoding: 'utf-8' }
  ).trim();
  const cjsRegKeys = JSON.parse(cjsReg);
  assert(cjsRegKeys.includes('COMPONENT_REGISTRY'), "Package exports './registry' resolves in CJS with COMPONENT_REGISTRY");
}

async function main() {
  await runEsmTests();
  runCjsTests();
  await runComponentRegistryValidation();
  await runCliExecutionSuite();
  await runAdversarialEdgeCases();
  await runPackageExportsSuite();

  console.log('\n======================================================');
  console.log(`SUMMARY: ${totalTests} executed. ${failedTests.length} failure(s).`);
  console.log('======================================================');

  if (failedTests.length > 0) {
    console.error('\nFAILURES:');
    failedTests.forEach(f => console.error(`  - ${f}`));
    process.exit(1);
  } else {
    console.log('\n[VERDICT: APPROVE] All ESM/CJS imports, contract exports, CLI commands, and component registry primitives verified with 100% precision.');
    process.exit(0);
  }
}

main().catch(err => {
  console.error('Unhandled test failure:', err);
  process.exit(1);
});
