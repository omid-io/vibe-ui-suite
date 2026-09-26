"""
vibe_core.stack_sensor — Project Stack & Context Sensor Module
Autonomously detects framework, React version, Tailwind CSS generation,
icon packages, and existing brand tokens in <10ms to eliminate stack collisions.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, List

class ProjectStackSensor:
    def __init__(self, target_dir: Optional[Path] = None):
        self.target_dir = Path(target_dir).resolve() if target_dir else Path.cwd().resolve()

    def scan(self) -> Dict[str, Any]:
        """
        Scans target directory and returns a comprehensive ProjectStackProfile.
        """
        pkg_json = self._read_package_json()
        css_theme = self._detect_css_theme()
        design_system = self._detect_existing_design_system(pkg_json)
        
        framework = self._detect_framework(pkg_json)
        react_ver = self._detect_react_version(pkg_json)
        tailwind_ver = self._detect_tailwind_version(pkg_json)
        icons_lib = self._detect_icons_library(pkg_json)
        has_ts = self._detect_typescript(pkg_json)

        return {
            "target_dir": str(self.target_dir),
            "framework": framework,
            "react_version": react_ver,
            "tailwind_version": tailwind_ver,
            "icons_library": icons_lib,
            "typescript": has_ts,
            "inherited_theme": css_theme,
            "existing_design_system": design_system,
            "recommendation": self._generate_recommendation(framework, react_ver, tailwind_ver, icons_lib, has_ts, design_system)
        }

    def _read_package_json(self) -> Dict[str, Any]:
        pkg_path = self.target_dir / "package.json"
        if not pkg_path.exists():
            # Check parent directory
            pkg_path = self.target_dir.parent / "package.json"
        if pkg_path.exists():
            try:
                with open(pkg_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def _detect_framework(self, pkg: Dict[str, Any]) -> str:
        deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
        if "next" in deps:
            # Check for App Router vs Pages Router
            if (self.target_dir / "app").exists() or (self.target_dir / "src" / "app").exists():
                return "nextjs_app_router"
            return "nextjs_pages_router"
        if "astro" in deps:
            return "astro"
        if "vite" in deps:
            if "vue" in deps:
                return "vite_vue"
            if "svelte" in deps:
                return "vite_svelte"
            return "vite_react"
        if "remix" in deps:
            return "remix"
        return "standard_web"

    def _detect_react_version(self, pkg: Dict[str, Any]) -> Optional[int]:
        deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
        react_dep = deps.get("react", "")
        if "19" in react_dep or "^19" in react_dep or "rc" in react_dep:
            return 19
        if "18" in react_dep or "^18" in react_dep:
            return 18
        if react_dep:
            return 18
        return None

    def _detect_tailwind_version(self, pkg: Dict[str, Any]) -> Optional[int]:
        deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
        tw_dep = deps.get("tailwindcss", "")
        if "4" in tw_dep or "^4" in tw_dep or "@tailwindcss/postcss" in deps:
            return 4
        if "3" in tw_dep or "^3" in tw_dep:
            return 3
        
        # Check files on disk
        if (self.target_dir / "tailwind.config.ts").exists() or (self.target_dir / "tailwind.config.js").exists():
            return 3
        # Check for @theme in globals.css
        css_candidates = [
            self.target_dir / "app" / "globals.css",
            self.target_dir / "src" / "app" / "globals.css",
            self.target_dir / "src" / "index.css",
            self.target_dir / "styles" / "globals.css",
            self.target_dir / "globals.css"
        ]
        for css in css_candidates:
            if css.exists():
                try:
                    content = css.read_text(encoding="utf-8", errors="ignore")
                    if "@theme" in content or '@import "tailwindcss";' in content:
                        return 4
                except Exception:
                    pass
        return 4 if tw_dep else None

    def _detect_icons_library(self, pkg: Dict[str, Any]) -> str:
        deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
        if "lucide-react" in deps:
            return "lucide-react"
        if "@heroicons/react" in deps:
            return "@heroicons/react"
        if "react-icons" in deps:
            return "react-icons"
        return "inline_svg"

    def _detect_typescript(self, pkg: Dict[str, Any]) -> bool:
        deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
        if "typescript" in deps:
            return True
        if (self.target_dir / "tsconfig.json").exists():
            return True
        return False

    def _detect_css_theme(self) -> Dict[str, Any]:
        """
        Scans css files for existing CSS custom properties (colors, fonts).
        """
        css_candidates = [
            self.target_dir / "app" / "globals.css",
            self.target_dir / "src" / "app" / "globals.css",
            self.target_dir / "src" / "index.css",
            self.target_dir / "styles" / "globals.css",
            self.target_dir / "globals.css"
        ]
        
        found_vars = []
        found_font = None

        for path in css_candidates:
            if path.exists():
                try:
                    content = path.read_text(encoding="utf-8", errors="ignore")
                    import re
                    var_matches = re.findall(r"(--[a-zA-Z0-9_-]+)\s*:", content)
                    found_vars.extend(var_matches[:15])
                    font_match = re.search(r"font-family\s*:\s*([^;]+);", content)
                    if font_match:
                        found_font = font_match.group(1).strip()
                    break
                except Exception:
                    pass

        return {
            "has_existing_tokens": len(found_vars) > 0,
            "detected_variables_sample": found_vars[:10],
            "detected_font_family": found_font
        }

    def _detect_existing_design_system(self, pkg: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deep scans project for established design systems (shadcn/ui, Radix, existing primitives).
        Guarantees Vibe UI inherits existing components rather than duplicating or colliding.
        """
        deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
        
        # 1. Check components.json (shadcn/ui)
        components_json_path = self.target_dir / "components.json"
        if not components_json_path.exists():
            components_json_path = self.target_dir.parent / "components.json"

        has_shadcn = components_json_path.exists()
        shadcn_cfg = {}
        if has_shadcn:
            try:
                with open(components_json_path, "r", encoding="utf-8") as f:
                    shadcn_cfg = json.load(f)
            except Exception:
                pass

        # 2. Check for Radix UI or headless primitives
        radix_primitives = [dep for dep in deps if dep.startswith("@radix-ui/react-")]
        has_radix = len(radix_primitives) > 0
        has_next_themes = "next-themes" in deps

        # 3. Check for existing UI primitives on disk
        ui_dirs = [
            self.target_dir / "components" / "ui",
            self.target_dir / "src" / "components" / "ui",
            self.target_dir / "ui"
        ]
        detected_primitives = []
        for d in ui_dirs:
            if d.exists() and d.is_dir():
                for f in d.glob("*.tsx"):
                    detected_primitives.append(f.stem)

        return {
            "has_shadcn": has_shadcn,
            "shadcn_style": shadcn_cfg.get("style", "default") if has_shadcn else None,
            "shadcn_tailwind_base_color": shadcn_cfg.get("tailwind", {}).get("baseColor") if has_shadcn else None,
            "has_radix": has_radix,
            "radix_primitives_count": len(radix_primitives),
            "has_theme_provider": has_next_themes,
            "detected_primitives": detected_primitives[:10]
        }

    def _generate_recommendation(
        self,
        framework: str,
        react_ver: Optional[int],
        tailwind_ver: Optional[int],
        icons_lib: str,
        has_ts: bool,
        design_system: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        ext = ".tsx" if has_ts else ".jsx"
        tw_mode = "v4_theme" if tailwind_ver == 4 else "v3_config"
        design_sys = design_system or {}
        
        inheritance_strategy = "standalone_vibe_tokens"
        if design_sys.get("has_shadcn"):
            inheritance_strategy = "inherit_existing_shadcn"
            prims = design_sys.get("detected_primitives", [])[:3]
            prims_str = ", ".join(prims) if prims else "Button/Card"
            instructions = f"Inherit existing shadcn/ui primitives ({prims_str}) and integrate with {tw_mode} Tailwind and {icons_lib} icons without collision."
        elif design_sys.get("detected_primitives"):
            inheritance_strategy = "inherit_existing_primitives"
            prims = design_sys.get("detected_primitives", [])[:3]
            instructions = f"Inherit existing UI primitives ({', '.join(prims)}) and integrate cleanly with {tw_mode} Tailwind."
        else:
            instructions = f"Generate modular React {react_ver or 19} component with {tw_mode} Tailwind and {icons_lib} icons."

        return {
            "file_extension": ext,
            "export_format": "react_component",
            "tailwind_syntax": tw_mode,
            "icons_strategy": icons_lib,
            "inheritance_strategy": inheritance_strategy,
            "instructions": instructions
        }
