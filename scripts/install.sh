#!/usr/bin/env bash
set -eo pipefail

# ==============================================================================
# Safe Non-Destructive Installer for Vibe UI & vibe-ui-agent Skills Suite
# ==============================================================================
# Usage:
#   ./install.sh                     # Installs to default ~/.gemini/config/skills
#   ./install.sh --agent claude      # Installs to .claude/skills
#   ./install.sh --agent cursor      # Installs to .cursor/skills
#   ./install.sh --target /my/path   # Installs to custom path
#   ./install.sh --version <tag>     # Installs specific tagged version
#   ./install.sh --force             # Overwrite without backup
# ==============================================================================

AGENT="antigravity"
TARGET_DIR=""
VERSION="v3.0.0-alpha.1"
BACKUP=true
FORCE=false
TEMP_DIR=""

trap '[ -n "$TEMP_DIR" ] && rm -rf "$TEMP_DIR"' EXIT

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --agent) AGENT="$2"; shift ;;
        --target) TARGET_DIR="$2"; shift ;;
        --version) VERSION="$2"; shift ;;
        --force) FORCE=true; BACKUP=false ;;
        --no-backup) BACKUP=false ;;
        -h|--help)
            echo "Usage: ./install.sh [--agent <antigravity|claude|cursor|windsurf>] [--target <dir>] [--version <tag>] [--force] [--no-backup]"
            exit 0
            ;;
        *)
            if [[ "$1" == --* ]]; then
                echo "❌ Error: Unknown option $1" >&2
                exit 1
            fi
            TARGET_DIR="$1"
            ;;
    esac
    shift
done

# Resolve default target if not explicitly provided
if [ -z "$TARGET_DIR" ]; then
    case "$AGENT" in
        antigravity|gemini) TARGET_DIR="$HOME/.gemini/config/skills" ;;
        claude)             TARGET_DIR="$(pwd)/.claude/skills" ;;
        cursor)             TARGET_DIR="$(pwd)/.cursor/skills" ;;
        windsurf)           TARGET_DIR="$(pwd)/.windsurf/skills" ;;
        *)                  TARGET_DIR="$HOME/.gemini/config/skills" ;;
    esac
fi

echo "✨ Installing Vibe UI & vibe-ui-agent Skills Suite..."
echo "🤖 Target Agent     : $AGENT"
echo "🎯 Target Directory : $TARGET_DIR"
echo "🛡️  Safe Backup Mode : $([ "$FORCE" = true ] && echo 'Disabled (--force)' || echo 'Enabled')"

mkdir -p "$TARGET_DIR"

TEMP_DIR=""
SOURCE_SKILLS=""

# Check if running inside cloned repo or local directory
if [ -n "${BASH_SOURCE[0]}" ] && [ -f "${BASH_SOURCE[0]}" ]; then
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    if [ -d "$SCRIPT_DIR/skills" ]; then
        SOURCE_SKILLS="$SCRIPT_DIR/skills"
    fi
fi

if [ -z "$SOURCE_SKILLS" ] && [ -d "./skills" ]; then
    SOURCE_SKILLS="$(pwd)/skills"
fi

# If skills folder not found locally, download from GitHub
if [ -z "$SOURCE_SKILLS" ] || [ ! -d "$SOURCE_SKILLS" ]; then
    echo "📦 Fetching skills suite (version: $VERSION) from GitHub repository..."
    TEMP_DIR=$(mktemp -d 2>/dev/null || mktemp -d -t 'vibe_ui')
    if [ -n "$VERSION" ] && [ "$VERSION" != "main" ]; then
        ARCHIVE_URL="https://github.com/omid-io/vibe-ui-suite/archive/refs/tags/${VERSION}.tar.gz"
    else
        ARCHIVE_URL="https://github.com/omid-io/vibe-ui-suite/archive/refs/heads/main.tar.gz"
    fi
    
    if command -v curl >/dev/null 2>&1; then
        curl -fsSL "$ARCHIVE_URL" | tar -xz -C "$TEMP_DIR"
    elif command -v wget >/dev/null 2>&1; then
        wget -qO- "$ARCHIVE_URL" | tar -xz -C "$TEMP_DIR"
    else
        echo "❌ Error: Neither curl nor wget found. Please install curl or wget."
        [ -n "$TEMP_DIR" ] && rm -rf "$TEMP_DIR"
        exit 1
    fi
    
    # Locate skills directory dynamically inside extracted tarball
    SOURCE_SKILLS=$(find "$TEMP_DIR" -type d -name "skills" | head -n 1)
fi

if [ ! -d "$SOURCE_SKILLS" ]; then
    echo "❌ Error: Could not find 'skills' directory in $SOURCE_SKILLS."
    [ -n "$TEMP_DIR" ] && rm -rf "$TEMP_DIR"
    exit 1
fi

count=0
for skill in "$SOURCE_SKILLS"/*; do
    if [ -d "$skill" ] && [ -f "$skill/SKILL.md" ]; then
        skill_name=$(basename "$skill")
        dest="$TARGET_DIR/$skill_name"
        
        # Safe non-destructive backup
        if [ -d "$dest" ] && [ "$FORCE" = false ] && [ "$BACKUP" = true ]; then
            if [ -d "${dest}.bak" ]; then
                mv "${dest}.bak" "${dest}.bak.$(date +%s)"
            fi
            mv "$dest" "${dest}.bak"
            echo "  [i] Backed up existing $skill_name -> ${dest}.bak"
        elif [ -d "$dest" ] && [ "$FORCE" = true ]; then
            rm -rf "$dest"
        fi

        echo "  [+] Installing skill: $skill_name -> $dest"
        cp -r "$skill" "$TARGET_DIR/"
        count=$((count + 1))
    fi
done

# Clean up temp files if created
if [ -n "$TEMP_DIR" ] && [ -d "$TEMP_DIR" ]; then
    rm -rf "$TEMP_DIR"
fi

echo ""
echo "🎉 Successfully installed all $count Vibe UI skills into $TARGET_DIR!"
echo "✨ Commanded by vibe-ui-agent with 70+ components, WCAG AA accessibility, and semantic RTL support."
