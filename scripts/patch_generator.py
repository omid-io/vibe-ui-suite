import re

with open("vibe_core/generator.py", "r", encoding="utf-8") as f:
    content = f.read()

# Pattern for _render_domain_widget up to generate_react_tsx
pattern = r'(    def _render_domain_widget\(self, domain_id: str, is_rtl: bool, style_cfg: Dict\[str, str\], blueprint: Dict\[str, Any\]\) -> str:.*?)(?=    def generate_react_tsx\()'

replacement = '''    def _render_domain_widget(self, domain_id: str, is_rtl: bool, style_cfg: Dict[str, str], blueprint: Dict[str, Any]) -> str:
        """
        Renders rich, functional signature widget JSX tailored to the exact domain via canonical registry.
        Features real causal reactive calculations connecting simulatedValue and splitPos to business metrics.
        Guarantees zero generic fallbacks across all 24 canonical domains.
        """
        return render_domain_widget(domain_id, is_rtl, style_cfg, blueprint)

'''

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
assert new_content != content, "Regex substitution failed"

# Also update tab touch target from min-h-[36px] to min-h-[44px]
new_content = new_content.replace('min-h-[36px]', 'min-h-[44px]')

with open("vibe_core/generator.py", "w", encoding="utf-8") as f:
    f.write(new_content)

print("Successfully patched vibe_core/generator.py!")
