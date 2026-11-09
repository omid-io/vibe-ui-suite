const fs = require('fs');
const path = require('path');

let ts;
try {
  ts = require('typescript');
} catch (e) {
  try {
    ts = require('../../examples/nextjs-starter/node_modules/typescript');
  } catch (e2) {
    console.error('Error: typescript is required to build packages/vibe-ui-suite.');
    process.exit(1);
  }
}

const distDir = path.join(__dirname, 'dist');
if (!fs.existsSync(distDir)) {
  fs.mkdirSync(distDir, { recursive: true });
}

const files = [
  path.join(__dirname, 'src', 'index.ts'),
  path.join(__dirname, 'src', 'tailwind.ts'),
  path.join(__dirname, 'src', 'registry', 'components.ts'),
  path.join(__dirname, 'src', 'audit.ts'),
  path.join(__dirname, 'src', 'mcp.ts'),
  path.join(__dirname, 'src', 'cli.ts')
];

const localTypesDir = path.resolve(__dirname, 'node_modules/@types');
const fallbackTypesDir = path.resolve(__dirname, '../../examples/nextjs-starter/node_modules/@types');
const detectedTypeRoots = [localTypesDir, fallbackTypesDir].filter(d => fs.existsSync(d));

// Compile CommonJS and .d.ts
const cjsOptions = {
  target: ts.ScriptTarget.ES2022,
  module: ts.ModuleKind.CommonJS,
  declaration: true,
  outDir: distDir,
  strict: true,
  esModuleInterop: true,
  moduleResolution: ts.ModuleResolutionKind.Node10,
  typeRoots: detectedTypeRoots.length > 0 ? detectedTypeRoots : undefined,
  types: ['node'],
  skipLibCheck: true,
};

const cjsProgram = ts.createProgram(files, cjsOptions);
const cjsDiagnostics = ts.getPreEmitDiagnostics(cjsProgram);
if (cjsDiagnostics.length > 0) {
  const formatHost = {
    getCanonicalFileName: (f) => f,
    getCurrentDirectory: ts.sys.getCurrentDirectory,
    getNewLine: () => ts.sys.newLine,
  };
  const message = ts.formatDiagnosticsWithColorAndContext(cjsDiagnostics, formatHost);
  console.error(message);
  process.exit(1);
}
cjsProgram.emit();

// Rewrite relative import/export specifiers for ESM (.mjs)
function rewriteRelativeImports(code) {
  return code.replace(
    /(from\s*|import\s*\(\s*|import\s+)(['"])(\.{1,2}\/[^'"]+?)\2(\s*\))?/g,
    (match, prefix, quote, specifier, closeParen) => {
      let resolved = specifier;
      if (resolved.endsWith('.js')) {
        resolved = resolved.slice(0, -3) + '.mjs';
      } else if (
        !resolved.endsWith('.mjs') &&
        !resolved.endsWith('.json') &&
        !resolved.endsWith('.css') &&
        !resolved.endsWith('.node')
      ) {
        resolved = resolved + '.mjs';
      }
      return `${prefix}${quote}${resolved}${quote}${closeParen || ''}`;
    }
  );
}

// Compile ESM (.mjs)
const esmOptions = {
  target: ts.ScriptTarget.ES2022,
  module: ts.ModuleKind.ESNext,
  declaration: false,
  outDir: distDir,
  strict: true,
  esModuleInterop: true,
  moduleResolution: ts.ModuleResolutionKind.Node10,
  typeRoots: detectedTypeRoots.length > 0 ? detectedTypeRoots : undefined,
  types: ['node'],
  skipLibCheck: true,
};

const esmProgram = ts.createProgram(files, esmOptions);
const esmDiagnostics = ts.getPreEmitDiagnostics(esmProgram);
if (esmDiagnostics.length > 0) {
  const formatHost = {
    getCanonicalFileName: (f) => f,
    getCurrentDirectory: ts.sys.getCurrentDirectory,
    getNewLine: () => ts.sys.newLine,
  };
  const message = ts.formatDiagnosticsWithColorAndContext(esmDiagnostics, formatHost);
  console.error(message);
  process.exit(1);
}

esmProgram.emit(undefined, (fileName, data) => {
  if (fileName.endsWith('.js')) {
    const mjsName = fileName.replace(/\.js$/, '.mjs');
    const fixedData = rewriteRelativeImports(data);
    fs.writeFileSync(mjsName, fixedData);
  } else {
    fs.writeFileSync(fileName, data);
  }
});

// Prepend shebang to dist/cli.js and dist/cli.mjs if not present
['cli.js', 'cli.mjs'].forEach((file) => {
  const cliFilePath = path.join(distDir, file);
  if (fs.existsSync(cliFilePath)) {
    let cliContent = fs.readFileSync(cliFilePath, 'utf-8');
    if (!cliContent.startsWith('#!/usr/bin/env node')) {
      cliContent = '#!/usr/bin/env node\n' + cliContent;
      fs.writeFileSync(cliFilePath, cliContent, 'utf-8');
    }
    try {
      fs.chmodSync(cliFilePath, 0o755);
    } catch (e) {}
  }
});

// Copy Tailwind v4 theme CSS to dist
const v4CssSrc = path.join(__dirname, 'v4.css');
if (fs.existsSync(v4CssSrc)) {
  fs.copyFileSync(v4CssSrc, path.join(distDir, 'v4.css'));
}

// Copy canonical skills directory into package root and .agents/skills
const rootSkillsDir = path.resolve(__dirname, '../../skills');
const pkgSkillsDir = path.join(__dirname, 'skills');
const agentsSkillsDir = path.resolve(__dirname, '../../.agents/skills');
if (fs.existsSync(rootSkillsDir)) {
  [pkgSkillsDir, agentsSkillsDir].forEach((dest) => {
    if (fs.existsSync(dest)) {
      fs.rmSync(dest, { recursive: true, force: true });
    }
    fs.cpSync(rootSkillsDir, dest, { recursive: true });
  });
  console.log(`📦 Synced ${fs.readdirSync(pkgSkillsDir).length} canonical skills into packages/vibe-ui-suite/skills and .agents/skills`);
}

// Copy canonical agents directory into package root
const rootAgentsDir = path.resolve(__dirname, '../../agents');
const pkgAgentsDir = path.join(__dirname, 'agents');
if (fs.existsSync(rootAgentsDir)) {
  if (fs.existsSync(pkgAgentsDir)) {
    fs.rmSync(pkgAgentsDir, { recursive: true, force: true });
  }
  fs.cpSync(rootAgentsDir, pkgAgentsDir, { recursive: true });
  console.log(`🤖 Synced ${fs.readdirSync(pkgAgentsDir).length} canonical agents into packages/vibe-ui-suite/agents`);
}

// Copy python execution engine into package root
const rootVibeCore = path.resolve(__dirname, '../../vibe_core');
const pkgVibeCore = path.join(__dirname, 'vibe_core');
if (fs.existsSync(rootVibeCore)) {
  if (fs.existsSync(pkgVibeCore)) {
    fs.rmSync(pkgVibeCore, { recursive: true, force: true });
  }
  fs.cpSync(rootVibeCore, pkgVibeCore, { recursive: true });
  console.log('🐍 Synced vibe_core into packages/vibe-ui-suite/vibe_core');
}

const rootSchemas = path.resolve(__dirname, '../../schemas');
const pkgSchemas = path.join(__dirname, 'schemas');
if (fs.existsSync(rootSchemas)) {
  if (fs.existsSync(pkgSchemas)) {
    fs.rmSync(pkgSchemas, { recursive: true, force: true });
  }
  fs.cpSync(rootSchemas, pkgSchemas, { recursive: true });
  console.log('📐 Synced schemas into packages/vibe-ui-suite/schemas');
}

const rootDataCatalog = path.resolve(__dirname, '../../data/catalog');
const pkgDataCatalog = path.join(__dirname, 'data', 'catalog');
const rootDataTaxonomy = path.resolve(__dirname, '../../data/taxonomy.json');
const pkgDataTaxonomy = path.join(__dirname, 'data', 'taxonomy.json');

if (fs.existsSync(rootDataCatalog)) {
  if (fs.existsSync(pkgDataCatalog)) {
    fs.rmSync(pkgDataCatalog, { recursive: true, force: true });
  }
  fs.mkdirSync(path.dirname(pkgDataCatalog), { recursive: true });
  fs.cpSync(rootDataCatalog, pkgDataCatalog, { recursive: true });
  console.log('📊 Synced data/catalog into packages/vibe-ui-suite/data/catalog');
}

if (fs.existsSync(rootDataTaxonomy)) {
  fs.mkdirSync(path.dirname(pkgDataTaxonomy), { recursive: true });
  fs.copyFileSync(rootDataTaxonomy, pkgDataTaxonomy);
  console.log('📑 Synced data/taxonomy.json into packages/vibe-ui-suite/data/taxonomy.json');
}

const rootDomainBlueprints = path.resolve(__dirname, '../../data/domain_blueprints.json');
const pkgDomainBlueprints = path.join(__dirname, 'data', 'domain_blueprints.json');
if (fs.existsSync(rootDomainBlueprints)) {
  fs.mkdirSync(path.dirname(pkgDomainBlueprints), { recursive: true });
  fs.copyFileSync(rootDomainBlueprints, pkgDomainBlueprints);
  console.log('🏛️ Synced data/domain_blueprints.json into packages/vibe-ui-suite/data/domain_blueprints.json');
}

const rootCuratedWebp = path.resolve(__dirname, '../../assets/curated_webp');
const pkgCuratedWebp = path.join(__dirname, 'assets', 'curated_webp');
if (fs.existsSync(rootCuratedWebp)) {
  if (fs.existsSync(pkgCuratedWebp)) {
    fs.rmSync(pkgCuratedWebp, { recursive: true, force: true });
  }
  fs.mkdirSync(path.dirname(pkgCuratedWebp), { recursive: true });
  fs.cpSync(rootCuratedWebp, pkgCuratedWebp, { recursive: true });
  console.log('🖼️ Synced assets/curated_webp into packages/vibe-ui-suite/assets/curated_webp');
}

const rootScreenshotAudit = path.resolve(__dirname, '../../scripts/screenshot_audit.py');
const pkgScreenshotAudit = path.join(__dirname, 'scripts', 'screenshot_audit.py');
if (fs.existsSync(rootScreenshotAudit)) {
  fs.mkdirSync(path.dirname(pkgScreenshotAudit), { recursive: true });
  fs.copyFileSync(rootScreenshotAudit, pkgScreenshotAudit);
  console.log('📸 Synced scripts/screenshot_audit.py into packages/vibe-ui-suite/scripts/screenshot_audit.py');
}

const rootVibeCli = path.resolve(__dirname, '../../vibe_cli.py');
const pkgVibeCli = path.join(__dirname, 'vibe_cli.py');
if (fs.existsSync(rootVibeCli)) {
  fs.copyFileSync(rootVibeCli, pkgVibeCli);
  console.log('🚀 Synced vibe_cli.py into packages/vibe-ui-suite/vibe_cli.py');
}

console.log('✅ vibe-ui-suite build complete: CLI, ESM, CJS, v4.css, skills, and .d.ts generated in dist/');
