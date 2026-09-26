const fs = require('fs');
const path = require('path');

const srcDistDir = path.resolve(__dirname, '../tokens/dist');
const targetDistDir = path.resolve(__dirname, 'dist');

if (!fs.existsSync(srcDistDir)) {
  console.error('Error: ../tokens/dist does not exist. Please build @omid-io/tokens first.');
  process.exit(1);
}

// Copy recursively from tokens/dist to vibe-ui-suite/dist
fs.cpSync(srcDistDir, targetDistDir, { recursive: true });

// Ensure executable permission on dist/cli.js
const cliPath = path.join(targetDistDir, 'cli.js');
if (fs.existsSync(cliPath)) {
  try {
    fs.chmodSync(cliPath, 0o755);
  } catch (e) {}
}

console.log('✅ vibe-ui-suite build complete: synchronized dist/ from tokens package.');
