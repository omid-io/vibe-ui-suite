"""
vibe_core/sections_compiler.py
==============================
Dynamic Multi-Archetype Layout & Section Compiler.
Evolves Vibe UI from a single monolithic template into an authentic, multi-archetype
layout synthesizer with 6 distinct architectural paradigms mapped across all 24 domains.
"""

from typing import Dict, List, Any


def get_domain_nav_links(domain_id: str, blueprint: Dict[str, Any]) -> List[Dict[str, str]]:
    """Returns domain-calibrated navigation links with guaranteed existing section IDs."""
    if domain_id == "devops_cloud_terminal":
        return [
            {"href": "#cluster", "label": "Cluster Health"},
            {"href": "#latency", "label": "P95/P99 Latency"},
            {"href": "#services", "label": "Services Mesh"},
            {"href": "#logs", "label": "Live Terminal"}
        ]
    elif domain_id in ["beauty_clinical_wellness", "healthcare_clinical_dental", "health_medical_clinic", "healthcare_hospital_medical"]:
        return [
            {"href": "#services", "label": "Treatments & Pricing"},
            {"href": "#portfolio", "label": "Clinical Results"},
            {"href": "#doctors", "label": "Specialists"},
            {"href": "#booking", "label": "Book Appointment"}
        ]

    from vibe_core.generator import DOMAIN_MACRO_ARCHETYPES
    arch = DOMAIN_MACRO_ARCHETYPES.get(domain_id, "classic_structured_saas")

    archetype_defaults = {
        "dense_telemetry_hud": [
            {"href": "#telemetry", "label": "Node Telemetry"},
            {"href": "#metrics", "label": "Throughput & SLAs"},
            {"href": "#terminal", "label": "Event Stream"}
        ],
        "editorial_asymmetric_spread": [
            {"href": "#curated", "label": "Curated Portfolio"},
            {"href": "#monograph", "label": "Editorial Thesis"},
            {"href": "#inquire", "label": "Private Inquiries"}
        ],
        "conversion_stepper_funnel": [
            {"href": "#pricing", "label": "Transparent Tiers"},
            {"href": "#calculator", "label": "Rate Calculator"},
            {"href": "#compliance", "label": "Institutional Trust"}
        ],
        "creative_canvas_showcase": [
            {"href": "#showcase", "label": "Featured Works"},
            {"href": "#disciplines", "label": "Design Disciplines"},
            {"href": "#contact", "label": "Start Project"}
        ],
        "split_laboratory_studio": [
            {"href": "#laboratory", "label": "Interactive Lab"},
            {"href": "#benchmarks", "label": "Performance Matrix"},
            {"href": "#deploy", "label": "SDK Quickstart"}
        ],
        "classic_structured_saas": [
            {"href": "#capabilities", "label": "Enterprise Features"},
            {"href": "#solutions", "label": "Architecture"},
            {"href": "#faq", "label": "FAQ & Support"}
        ]
    }
    return archetype_defaults.get(arch, archetype_defaults["classic_structured_saas"])


def compile_domain_sections(
    domain_id: str,
    blueprint: Dict[str, Any],
    style_cfg: Dict[str, str],
    card_border: str,
    card_shadow: str,
    is_rtl: bool = False
) -> str:
    """
    Synthesizes authentic, domain-specialized sections based on the 6 macro archetypes.
    Guarantees that each archetype produces radically different structural HTML layouts,
    eliminating homogenous template assembly and generic meta-marketing.
    """
    mock_data = blueprint.get("mock_data", {})
    if isinstance(mock_data.get("en"), dict):
        mock_data = mock_data.get("en", {})

    # Specialized canonical implementations for primary domains
    if domain_id == "devops_cloud_terminal":
        return _compile_devops_dedicated(domain_id, mock_data, style_cfg, card_border, card_shadow)
    elif domain_id in ["beauty_clinical_wellness", "healthcare_clinical_dental", "health_medical_clinic", "healthcare_hospital_medical"]:
        return _compile_healthcare_dedicated(domain_id, mock_data, style_cfg, card_border, card_shadow, is_rtl)

    from vibe_core.generator import DOMAIN_MACRO_ARCHETYPES
    archetype = DOMAIN_MACRO_ARCHETYPES.get(domain_id, "classic_structured_saas")

    if archetype == "dense_telemetry_hud":
        return _compile_dense_telemetry_hud(domain_id, mock_data, style_cfg, card_border, card_shadow)
    elif archetype == "editorial_asymmetric_spread":
        return _compile_editorial_spread(domain_id, mock_data, style_cfg, card_border, card_shadow)
    elif archetype == "conversion_stepper_funnel":
        return _compile_conversion_funnel(domain_id, mock_data, style_cfg, card_border, card_shadow)
    elif archetype == "creative_canvas_showcase":
        return _compile_creative_showcase(domain_id, mock_data, style_cfg, card_border, card_shadow)
    elif archetype == "split_laboratory_studio":
        return _compile_laboratory_studio(domain_id, mock_data, style_cfg, card_border, card_shadow)
    else:
        return _compile_structured_saas(domain_id, mock_data, style_cfg, card_border, card_shadow)


# ----------------------------------------------------------------------
# DEDICATED DOMAIN COMPILERS
# ----------------------------------------------------------------------
def _compile_devops_dedicated(
    domain_id: str,
    mock_data: Dict[str, Any],
    style_cfg: Dict[str, str],
    card_border: str,
    card_shadow: str
) -> str:
    return f"""
    <!-- DevOps Section 1: Cluster Health -->
    <section id="cluster" class="mt-12 pt-8 border-t border-[var(--border-subtle)]" aria-labelledby="cluster-heading">
      <div class="flex flex-wrap items-center justify-between gap-4 mb-6">
        <div>
          <h2 id="cluster-heading" class="text-2xl font-bold tracking-tight font-mono">Cluster Topology & Node Health</h2>
          <p class="text-xs text-[var(--text-muted)] mt-1">Real-time state synchronization across distributed kubernetes clusters.</p>
        </div>
        <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-[var(--surface-bg)] border border-[var(--border-subtle)] font-mono text-xs">
          <span class="size-2 rounded-full bg-emerald-500 animate-ping"></span>
          <span class="text-emerald-500 font-bold">K8S_MESH://ONLINE</span>
          <span class="text-[var(--text-muted)]">|</span>
          <span class="text-[var(--text-primary)]">UPTIME: 99.999%</span>
        </div>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 font-mono text-xs">
        <div class="p-4 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-2">
          <div class="flex justify-between text-[var(--text-muted)]"><span>Ingress Router</span><span class="text-emerald-500 font-bold">OPTIMAL</span></div>
          <div class="text-base font-bold text-[var(--text-primary)]"><bdi>0.82 ms (p50)</bdi></div>
          <div class="w-full bg-[var(--canvas-bg)] rounded-full h-1.5"><div class="bg-emerald-500 h-1.5 rounded-full" style="width: 98%"></div></div>
        </div>
        <div class="p-4 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-2">
          <div class="flex justify-between text-[var(--text-muted)]"><span>Payload Pipeline</span><span class="text-emerald-500 font-bold">SYNCED</span></div>
          <div class="text-base font-bold text-[var(--text-primary)]"><bdi>42,100 ops/s</bdi></div>
          <div class="w-full bg-[var(--canvas-bg)] rounded-full h-1.5"><div class="bg-emerald-500 h-1.5 rounded-full" style="width: 92%"></div></div>
        </div>
        <div class="p-4 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-2">
          <div class="flex justify-between text-[var(--text-muted)]"><span>Memory Allocation</span><span class="text-amber-500 font-bold">64.2%</span></div>
          <div class="text-base font-bold text-[var(--text-primary)]"><bdi>12.8 / 20.0 GB</bdi></div>
          <div class="w-full bg-[var(--canvas-bg)] rounded-full h-1.5"><div class="bg-amber-500 h-1.5 rounded-full" style="width: 64%"></div></div>
        </div>
        <div class="p-4 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-2">
          <div class="flex justify-between text-[var(--text-muted)]"><span>Consensus Engine</span><span class="text-emerald-500 font-bold">VERIFIED</span></div>
          <div class="text-base font-bold text-[var(--text-primary)]"><bdi>Zero Slashing</bdi></div>
          <div class="w-full bg-[var(--canvas-bg)] rounded-full h-1.5"><div class="bg-emerald-500 h-1.5 rounded-full" style="width: 100%"></div></div>
        </div>
      </div>
    </section>

    <!-- DevOps Section 2: P95/P99 Latency -->
    <section id="latency" class="mt-12 pt-8 border-t border-[var(--border-subtle)]" aria-labelledby="latency-heading">
      <div class="max-w-2xl mb-6">
        <h2 id="latency-heading" class="text-2xl font-bold tracking-tight font-mono">P95 / P99 Tail Latency Telemetry</h2>
        <p class="text-xs text-[var(--text-muted)] mt-1">Deterministic performance thresholds under peak synthetic concurrency load.</p>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 font-mono text-xs">
        <div class="p-5 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow}">
          <div class="text-zinc-500 uppercase tracking-wider mb-1">Tail Latency (p99)</div>
          <div class="text-2xl font-bold text-[var(--accent)] mb-2"><bdi>1.42 ms</bdi></div>
          <p class="text-[var(--text-muted)]">Guaranteed execution bounds under maximum concurrent traffic load.</p>
        </div>
        <div class="p-5 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow}">
          <div class="text-zinc-500 uppercase tracking-wider mb-1">Network Reliability</div>
          <div class="text-2xl font-bold text-emerald-500 mb-2"><bdi>99.999%</bdi></div>
          <p class="text-[var(--text-muted)]">Multi-region active redundancy with sub-second failover routing.</p>
        </div>
        <div class="p-5 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow}">
          <div class="text-zinc-500 uppercase tracking-wider mb-1">Zero Jitter Protocol</div>
          <div class="text-2xl font-bold text-[var(--text-primary)] mb-2"><bdi>&lt; 0.05 ms</bdi></div>
          <p class="text-[var(--text-muted)]">Kernel-bypass eBPF network filtering for deterministic scheduling.</p>
        </div>
      </div>
    </section>

    <!-- DevOps Section 3: Services Mesh -->
    <section id="services" class="mt-12 pt-8 border-t border-[var(--border-subtle)]" aria-labelledby="services-heading">
      <div class="max-w-2xl mb-6">
        <h2 id="services-heading" class="text-2xl font-bold tracking-tight font-mono">Microservices Mesh Routing</h2>
        <p class="text-xs text-[var(--text-muted)] mt-1">Service discovery, automatic mutual TLS, and circuit-breaking proxies.</p>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-6 font-mono text-xs">
        <div class="p-4 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow}">
          <div class="font-bold text-[var(--text-primary)] mb-1">auth-service-v3</div>
          <div class="text-emerald-500">HEALTHY (100% quorum)</div>
        </div>
        <div class="p-4 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow}">
          <div class="font-bold text-[var(--text-primary)] mb-1">billing-ledger-v1</div>
          <div class="text-emerald-500">HEALTHY (100% quorum)</div>
        </div>
        <div class="p-4 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow}">
          <div class="font-bold text-[var(--text-primary)] mb-1">stream-ingest-v2</div>
          <div class="text-emerald-500">HEALTHY (100% quorum)</div>
        </div>
      </div>
    </section>

    <!-- DevOps Section 4: Live Logs Console -->
    <section id="logs" class="mt-12 pt-8 border-t border-[var(--border-subtle)]" aria-labelledby="logs-heading">
      <div class="flex items-center justify-between mb-4">
        <h2 id="logs-heading" class="text-2xl font-bold tracking-tight font-mono">Live Cluster Terminal Logs</h2>
        <span class="px-2.5 py-1 text-xs font-mono rounded bg-emerald-500/10 text-emerald-500 border border-emerald-500/20">BUFFER: 10,000 LINES</span>
      </div>
      <div class="p-5 bg-black border border-emerald-900/50 rounded-[var(--radius-container)] font-mono text-xs text-emerald-400 space-y-1.5 overflow-x-auto shadow-2xl">
        <div class="text-zinc-500"># Initializing cluster observation pipeline... [SESSION: ESTABLISHED]</div>
        <div>[CLUSTER] Ingress gateway: handshake verified with remote peer (TLS 1.3)</div>
        <div>[CONSENSUS] State transition validated across 32 quorum nodes</div>
        <div>[METRICS] Latency: optimal delta recorded (&lt; 0.82 ms standard deviation)</div>
        <div class="text-emerald-300 font-bold animate-pulse">&gt; pipeline stream continuous --live [OK]</div>
      </div>
    </section>
"""


def _compile_healthcare_dedicated(
    domain_id: str,
    mock_data: Dict[str, Any],
    style_cfg: Dict[str, str],
    card_border: str,
    card_shadow: str,
    is_rtl: bool = False
) -> str:
    btn_text = "ثبت نوبت مشاوره تخصصی" if is_rtl else "Book Appointment"
    return f"""
    <!-- Healthcare Section 1: Services & Treatments -->
    <section id="services" class="mt-12 pt-8 border-t border-[var(--border-subtle)]" aria-labelledby="services-heading">
      <div class="max-w-2xl mb-8">
        <h2 id="services-heading" class="text-3xl font-bold tracking-tight">Clinical Treatments & Procedures</h2>
        <p class="text-sm text-[var(--text-muted)] mt-2">Certified medical standards with minimally invasive technology.</p>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-3">
          <h3 class="text-lg font-bold">Preventive Diagnostics</h3>
          <p class="text-xs text-[var(--text-muted)]">High-resolution 3D digital imaging and non-invasive diagnostic scanning.</p>
        </div>
        <div class="p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-3">
          <h3 class="text-lg font-bold">Specialized Therapeutics</h3>
          <p class="text-xs text-[var(--text-muted)]">Personalized clinical therapies overseen by accredited board specialists.</p>
        </div>
        <div class="p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-3">
          <h3 class="text-lg font-bold">Post-Care Rehabilitation</h3>
          <p class="text-xs text-[var(--text-muted)]">Dedicated follow-up monitoring with zero-latency telemedicine support.</p>
        </div>
      </div>
    </section>

    <!-- Healthcare Section 2: Clinical Results & Portfolio -->
    <section id="portfolio" class="mt-12 pt-8 border-t border-[var(--border-subtle)]" aria-labelledby="portfolio-heading">
      <div class="max-w-2xl mb-8">
        <h2 id="portfolio-heading" class="text-3xl font-bold tracking-tight">Verified Clinical Outcomes</h2>
        <p class="text-sm text-[var(--text-muted)] mt-2">Documented recovery rates and audited patient satisfaction metrics.</p>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <div class="p-5 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} text-center space-y-1">
          <div class="text-3xl font-extrabold text-[var(--accent)]"><bdi>99.4%</bdi></div>
          <div class="text-xs text-[var(--text-muted)]">Clinical Success Rate</div>
        </div>
        <div class="p-5 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} text-center space-y-1">
          <div class="text-3xl font-extrabold text-emerald-500"><bdi>15,000+</bdi></div>
          <div class="text-xs text-[var(--text-muted)]">Completed Procedures</div>
        </div>
        <div class="p-5 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} text-center space-y-1">
          <div class="text-3xl font-extrabold text-[var(--text-primary)]"><bdi>Zero</bdi></div>
          <div class="text-xs text-[var(--text-muted)]">Hospital Acquired Defect</div>
        </div>
      </div>
    </section>

    <!-- Healthcare Section 3: Medical Specialists -->
    <section id="doctors" class="mt-12 pt-8 border-t border-[var(--border-subtle)]" aria-labelledby="doctors-heading">
      <div class="max-w-2xl mb-8">
        <h2 id="doctors-heading" class="text-3xl font-bold tracking-tight">Medical Staff & Specialists</h2>
        <p class="text-sm text-[var(--text-muted)] mt-2">Board-certified clinical doctors and senior surgical faculty.</p>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
        <div class="p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-2">
          <h3 class="text-base font-bold">Dr. Elena Rostova, MD, PhD</h3>
          <p class="text-xs text-[var(--accent)] font-semibold">Chief of Clinical Research & Diagnostics</p>
          <p class="text-xs text-[var(--text-muted)]">Over 18 years of pioneering research in regenerative clinical therapies.</p>
        </div>
        <div class="p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-2">
          <h3 class="text-base font-bold">Dr. Marcus Vance, FACS</h3>
          <p class="text-xs text-[var(--accent)] font-semibold">Director of Advanced Surgical Care</p>
          <p class="text-xs text-[var(--text-muted)]">Specialized in robotic-assisted precision surgery and rehabilitation protocols.</p>
        </div>
      </div>
    </section>

    <!-- Healthcare Section 4: Booking & Quick Appointment Form -->
    <section id="booking" class="mt-12 pt-8 border-t border-[var(--border-subtle)]" aria-labelledby="booking-heading">
      <div class="max-w-xl mx-auto p-8 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow}">
        <h2 id="booking-heading" class="text-2xl font-bold text-center mb-2">Reserve an Appointment Slot</h2>
        <p class="text-xs text-[var(--text-muted)] text-center mb-6">Select your preferred consultation time with an accredited specialist.</p>
        <form id="quick-booking-form" class="space-y-4" onsubmit="event.preventDefault();">
          <div>
            <label for="booking-name" class="block text-xs font-semibold mb-1">Full Patient Name</label>
            <input type="text" id="booking-name" required placeholder="Jane Doe" class="w-full px-4 py-2.5 text-xs rounded-[var(--radius-button)] bg-[var(--canvas-bg)] border border-[var(--border-subtle)] focus:border-[var(--accent)] min-h-[44px] outline-none">
          </div>
          <div>
            <label for="booking-contact" class="block text-xs font-semibold mb-1">Phone or Email Address</label>
            <input type="text" id="booking-contact" required placeholder="+1 (555) 000-0000" class="w-full px-4 py-2.5 text-xs rounded-[var(--radius-button)] bg-[var(--canvas-bg)] border border-[var(--border-subtle)] focus:border-[var(--accent)] min-h-[44px] outline-none">
          </div>
          <button type="submit" id="submit-booking-btn" class="w-full py-3 text-xs font-bold rounded-[var(--radius-button)] bg-[var(--accent)] text-[var(--vibe-on-primary,#fff)] min-h-[44px] transition-opacity hover:opacity-90">{btn_text}</button>
        </form>
      </div>
    </section>
"""


# ----------------------------------------------------------------------
# 1. DENSE TELEMETRY HUD (DevOps, Crypto, Cybersecurity, Logistics)
# ----------------------------------------------------------------------
def _compile_dense_telemetry_hud(
    domain_id: str,
    mock_data: Dict[str, Any],
    style_cfg: Dict[str, str],
    card_border: str,
    card_shadow: str
) -> str:
    tag = "CRYPTO_NODE" if "crypto" in domain_id else ("SEC_AGENT" if "cyber" in domain_id else "K8S_MESH")
    title1 = "Orderbook & Market Depth" if "crypto" in domain_id else "Microservices Mesh Status"
    metric_label = "24h Volume / Latency" if "crypto" in domain_id else "P95 Tail Latency"

    if "crypto" in domain_id:
        cards_html = f"""        <div class="p-4 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-2">
          <div class="flex justify-between text-[var(--text-muted)]"><span>Orderbook Liquidity</span><span class="text-emerald-500 font-bold">DEEP</span></div>
          <div class="text-base font-bold text-[var(--text-primary)]"><bdi>$1.42B (24h Depth)</bdi></div>
          <div class="w-full bg-[var(--canvas-bg)] rounded-full h-1.5"><div class="bg-emerald-500 h-1.5 rounded-full" style="width: 96%"></div></div>
        </div>
        <div class="p-4 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-2">
          <div class="flex justify-between text-[var(--text-muted)]"><span>Gas Optimization</span><span class="text-emerald-500 font-bold">&lt; 12 Gwei</span></div>
          <div class="text-base font-bold text-[var(--text-primary)]"><bdi>0.02% Avg Slippage</bdi></div>
          <div class="w-full bg-[var(--canvas-bg)] rounded-full h-1.5"><div class="bg-emerald-500 h-1.5 rounded-full" style="width: 94%"></div></div>
        </div>
        <div class="p-4 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-2">
          <div class="flex justify-between text-[var(--text-muted)]"><span>Multi-Chain Routing</span><span class="text-sky-500 font-bold">OPTIMAL</span></div>
          <div class="text-base font-bold text-[var(--text-primary)]"><bdi>Curve + Uniswap v3</bdi></div>
          <div class="w-full bg-[var(--canvas-bg)] rounded-full h-1.5"><div class="bg-sky-500 h-1.5 rounded-full" style="width: 90%"></div></div>
        </div>
        <div class="p-4 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-2">
          <div class="flex justify-between text-[var(--text-muted)]"><span>Proof of Reserves</span><span class="text-emerald-500 font-bold">100% VERIFIED</span></div>
          <div class="text-base font-bold text-[var(--text-primary)]"><bdi>Zero Deficit</bdi></div>
          <div class="w-full bg-[var(--canvas-bg)] rounded-full h-1.5"><div class="bg-emerald-500 h-1.5 rounded-full" style="width: 100%"></div></div>
        </div>"""
    else:
        cards_html = f"""        <div class="p-4 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-2">
          <div class="flex justify-between text-[var(--text-muted)]"><span>Ingress Router</span><span class="text-emerald-500 font-bold">OPTIMAL</span></div>
          <div class="text-base font-bold text-[var(--text-primary)]"><bdi>0.82 ms (p50)</bdi></div>
          <div class="w-full bg-[var(--canvas-bg)] rounded-full h-1.5"><div class="bg-emerald-500 h-1.5 rounded-full" style="width: 98%"></div></div>
        </div>
        <div class="p-4 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-2">
          <div class="flex justify-between text-[var(--text-muted)]"><span>Payload Pipeline</span><span class="text-emerald-500 font-bold">SYNCED</span></div>
          <div class="text-base font-bold text-[var(--text-primary)]"><bdi>42,100 ops/s</bdi></div>
          <div class="w-full bg-[var(--canvas-bg)] rounded-full h-1.5"><div class="bg-emerald-500 h-1.5 rounded-full" style="width: 92%"></div></div>
        </div>
        <div class="p-4 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-2">
          <div class="flex justify-between text-[var(--text-muted)]"><span>Throughput Buffer</span><span class="text-amber-500 font-bold">64.2%</span></div>
          <div class="text-base font-bold text-[var(--text-primary)]"><bdi>Sub-second Finality</bdi></div>
          <div class="w-full bg-[var(--canvas-bg)] rounded-full h-1.5"><div class="bg-amber-500 h-1.5 rounded-full" style="width: 64%"></div></div>
        </div>
        <div class="p-4 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-2">
          <div class="flex justify-between text-[var(--text-muted)]"><span>Consensus Engine</span><span class="text-emerald-500 font-bold">VERIFIED</span></div>
          <div class="text-base font-bold text-[var(--text-primary)]"><bdi>Zero Slashing</bdi></div>
          <div class="w-full bg-[var(--canvas-bg)] rounded-full h-1.5"><div class="bg-emerald-500 h-1.5 rounded-full" style="width: 100%"></div></div>
        </div>"""

    return f"""
    <!-- Archetype 1: Dense Telemetry HUD -> Service Telemetry Grid -->
    <section id="telemetry" class="mt-12 pt-8 border-t border-[var(--border-subtle)]" aria-labelledby="telemetry-heading">
      <div class="flex flex-wrap items-center justify-between gap-4 mb-6">
        <div>
          <h2 id="telemetry-heading" class="text-2xl font-bold tracking-tight font-mono">{title1}</h2>
          <p class="text-xs text-[var(--text-muted)] mt-1">Real-time throughput telemetry, state synchronization, and execution depth.</p>
        </div>
        <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-lg bg-[var(--surface-bg)] border border-[var(--border-subtle)] font-mono text-xs">
          <span class="size-2 rounded-full bg-emerald-500 animate-ping"></span>
          <span class="text-emerald-500 font-bold">{tag}://ACTIVE</span>
          <span class="text-[var(--text-muted)]">|</span>
          <span class="text-[var(--text-primary)]">UPTIME: 99.999%</span>
        </div>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 font-mono text-xs">
{cards_html}
      </div>
    </section>

    <!-- Archetype 1: Performance Metrics & SLA Benchmarks -->
    <section id="metrics" class="mt-12 pt-8 border-t border-[var(--border-subtle)]" aria-labelledby="metrics-heading">
      <div class="flex flex-wrap items-center justify-between gap-4 mb-6">
        <div>
          <h2 id="metrics-heading" class="text-2xl font-bold tracking-tight font-mono">Performance & SLA Bounds</h2>
          <p class="text-xs text-[var(--text-muted)] mt-1">Deterministic sub-millisecond execution thresholds.</p>
        </div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 font-mono text-xs">
        <div class="p-5 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow}">
          <div class="text-zinc-500 uppercase tracking-wider mb-1">Tail Latency (p99)</div>
          <div class="text-2xl font-bold text-[var(--accent)] mb-2"><bdi>1.42 ms</bdi></div>
          <p class="text-[var(--text-muted)]">Guaranteed execution bounds under maximum concurrent traffic load.</p>
        </div>
        <div class="p-5 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow}">
          <div class="text-zinc-500 uppercase tracking-wider mb-1">Network Reliability</div>
          <div class="text-2xl font-bold text-emerald-500 mb-2"><bdi>99.999%</bdi></div>
          <p class="text-[var(--text-muted)]">Multi-region active redundancy with sub-second failover routing.</p>
        </div>
        <div class="p-5 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow}">
          <div class="text-zinc-500 uppercase tracking-wider mb-1">Cryptographic Proof</div>
          <div class="text-2xl font-bold text-[var(--text-primary)] mb-2"><bdi>Zero Knowledge</bdi></div>
          <p class="text-[var(--text-muted)]">Every transaction and cluster event verified by immutable state proofs.</p>
        </div>
      </div>
    </section>

    <!-- Archetype 1: Live Terminal Log Console -->
    <section id="terminal" class="mt-12 pt-8 border-t border-[var(--border-subtle)]" aria-labelledby="terminal-heading">
      <div class="flex items-center justify-between mb-4">
        <h2 id="terminal-heading" class="text-2xl font-bold tracking-tight font-mono">Telemetry Event Stream</h2>
        <span class="px-2.5 py-1 text-xs font-mono rounded bg-emerald-500/10 text-emerald-500 border border-emerald-500/20">BUFFER: 10,000 LINES</span>
      </div>
      <div class="p-5 bg-black border border-emerald-900/50 rounded-[var(--radius-container)] font-mono text-xs text-emerald-400 space-y-1.5 overflow-x-auto shadow-2xl">
        <div class="text-zinc-500"># Initializing low-latency streaming pipeline... [SESSION: ESTABLISHED]</div>
        <div>[TELEMETRY] Ingress gateway: handshake verified with remote peer (TLS 1.3)</div>
        <div>[CONSENSUS] State transition validated across 32 quorum nodes</div>
        <div>[METRICS] {metric_label}: optimal delta recorded (&lt; 2.4% standard deviation)</div>
        <div class="text-emerald-300 font-bold animate-pulse">&gt; pipeline stream continuous --live [OK]</div>
      </div>
    </section>
"""


# ----------------------------------------------------------------------
# 2. EDITORIAL ASYMMETRIC SPREAD (Magazine, Luxury, Real Estate)
# ----------------------------------------------------------------------
def _compile_editorial_spread(
    domain_id: str,
    mock_data: Dict[str, Any],
    style_cfg: Dict[str, str],
    card_border: str,
    card_shadow: str
) -> str:
    col_name = "Curated Architectural Portfolio" if "estate" in domain_id else "Seasonal Haute Couture & Rare Editions"

    return f"""
    <!-- Archetype 2: Editorial Asymmetric Spread -> Curated Feature Exhibition -->
    <section id="curated" class="mt-16 pt-10 border-t border-[var(--border-subtle)]" aria-labelledby="curated-heading">
      <div class="max-w-3xl mb-12">
        <span class="text-xs font-bold uppercase tracking-widest text-[var(--accent)] mb-3 block">Curated Edition // 2026</span>
        <h2 id="curated-heading" class="text-3xl sm:text-4xl font-serif font-medium tracking-tight text-[var(--text-primary)] leading-tight">
          {col_name}
        </h2>
        <p class="text-base text-[var(--text-muted)] mt-4 font-serif italic leading-relaxed">
          Crafted with uncompromising discipline, rare materials, and geometric harmony for discerning patrons.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-12 gap-8 items-stretch">
        <div class="md:col-span-7 p-8 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} flex flex-col justify-between space-y-6">
          <div class="space-y-4">
            <span class="inline-flex px-3 py-1 rounded-full text-xs font-serif italic bg-[var(--accent)]/10 text-[var(--accent)]">Special Commission</span>
            <h3 class="text-2xl font-serif font-bold text-[var(--text-primary)]">The Sovereign Collection</h3>
            <p class="text-sm text-[var(--text-muted)] leading-relaxed font-sans">
              Every detail is calibrated to enduring timelessness. Rigorous provenance, bespoke craftsmanship, and acoustic mastery.
            </p>
          </div>
          <div class="pt-6 border-t border-[var(--border-subtle)] flex items-center justify-between">
            <div>
              <div class="text-xs uppercase tracking-wider text-[var(--text-muted)]">Private Valuation</div>
              <div class="text-2xl font-serif font-bold text-[var(--accent)]"><bdi>Available by Consultation</bdi></div>
            </div>
            <a href="#inquire" class="px-5 py-2.5 text-xs font-medium uppercase tracking-wider rounded-[var(--radius-button)] bg-[var(--accent)] text-[var(--vibe-on-primary,#fff)] min-h-[44px] inline-flex items-center transition-opacity hover:opacity-90">
              Request Dossier
            </a>
          </div>
        </div>

        <div class="md:col-span-5 p-8 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} flex flex-col justify-between space-y-6">
          <div class="space-y-3">
            <span class="text-xs uppercase tracking-widest text-[var(--text-muted)]">Editorial Thesis</span>
            <blockquote class="text-lg font-serif italic text-[var(--text-primary)] leading-relaxed border-s-2 border-[var(--accent)] ps-4 my-4">
              "True luxury is quiet, absolute in execution, and void of superficial ornament."
            </blockquote>
            <p class="text-xs text-[var(--text-muted)]">— Curatorial Monograph, Vol. IX</p>
          </div>
          <div class="pt-4 border-t border-[var(--border-subtle)]">
            <div class="text-xs font-semibold text-[var(--accent)] flex items-center gap-1.5">
              <span class="size-1.5 rounded-full bg-[var(--accent)]"></span>
              Verified Provenance & Certified Authenticity
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Archetype 2: Monograph & Materials Exploration -->
    <section id="monograph" class="mt-16 pt-10 border-t border-[var(--border-subtle)]" aria-labelledby="monograph-heading">
      <div class="max-w-2xl mb-8">
        <h2 id="monograph-heading" class="text-3xl font-serif font-bold text-[var(--text-primary)]">Material Monograph</h2>
        <p class="text-sm text-[var(--text-muted)] mt-2 font-serif italic">Disciplined materiality sourced from heritage ateliers.</p>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-2">
          <div class="text-xs font-serif uppercase tracking-widest text-[var(--accent)]">Element I</div>
          <h3 class="text-lg font-serif font-bold">Honed Titanium</h3>
          <p class="text-xs text-[var(--text-muted)] leading-relaxed">Aerospace-grade durability hand-brushed with microscopic satin finish.</p>
        </div>
        <div class="p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-2">
          <div class="text-xs font-serif uppercase tracking-widest text-[var(--accent)]">Element II</div>
          <h3 class="text-lg font-serif font-bold">Italian Full-Grain</h3>
          <p class="text-xs text-[var(--text-muted)] leading-relaxed">Vegetable-tanned leather conditioned with natural beeswax patina.</p>
        </div>
        <div class="p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-2">
          <div class="text-xs font-serif uppercase tracking-widest text-[var(--accent)]">Element III</div>
          <h3 class="text-lg font-serif font-bold">Acoustic Crystal</h3>
          <p class="text-xs text-[var(--text-muted)] leading-relaxed">Hand-blown borosilicate crystal engineered for zero harmonic distortion.</p>
        </div>
      </div>
    </section>

    <!-- Archetype 2: Inquire Form Section -->
    <section id="inquire" class="mt-16 pt-10 border-t border-[var(--border-subtle)]" aria-labelledby="inquire-heading">
      <div class="max-w-xl mx-auto p-8 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} text-center space-y-6">
        <h2 id="inquire-heading" class="text-2xl font-serif font-bold text-[var(--text-primary)]">Private Salon Consultation</h2>
        <p class="text-xs text-[var(--text-muted)] font-serif italic">Appointments are reserved exclusively for private collectors and corporate acquisitions.</p>
        <form class="space-y-4 text-start" onsubmit="event.preventDefault();">
          <div>
            <label for="curated-email" class="block text-xs font-medium text-[var(--text-muted)] mb-1">Direct Liaison Email</label>
            <input type="email" id="curated-email" required placeholder="patron@private-family.com" class="w-full px-4 py-2.5 text-xs rounded-[var(--radius-button)] bg-[var(--canvas-bg)] border border-[var(--border-subtle)] focus:border-[var(--accent)] min-h-[44px] outline-none">
          </div>
          <button type="submit" class="w-full py-3 text-xs font-serif font-medium uppercase tracking-widest rounded-[var(--radius-button)] bg-[var(--accent)] text-[var(--vibe-on-primary,#fff)] min-h-[44px]">Request Confidential Dialogue</button>
        </form>
      </div>
    </section>
"""


# ----------------------------------------------------------------------
# 3. CONVERSION STEPPER FUNNEL (Fintech, Travel, Medical, Mass E-Comm, Food)
# ----------------------------------------------------------------------
def _compile_conversion_funnel(
    domain_id: str,
    mock_data: Dict[str, Any],
    style_cfg: Dict[str, str],
    card_border: str,
    card_shadow: str
) -> str:
    cta_name = "Apply for Approval" if "fintech" in domain_id else ("Reserve Booking" if "travel" in domain_id else "Order Consultation")
    return f"""
    <!-- Archetype 3: Conversion Stepper Funnel -> Transparent Tier & Pricing Matrix -->
    <section id="pricing" class="mt-16 pt-10 border-t border-[var(--border-subtle)]" aria-labelledby="pricing-heading">
      <div class="text-center max-w-2xl mx-auto mb-12">
        <h2 id="pricing-heading" class="text-3xl font-extrabold tracking-tight text-[var(--text-primary)]">
          Transparent Tiers & Guaranteed Value
        </h2>
        <p class="text-sm text-[var(--text-muted)] mt-2">
          Zero hidden commissions, institutional-grade security, and instant digital onboarding.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 items-stretch">
        <!-- Tier 1 -->
        <div class="p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} flex flex-col justify-between space-y-6">
          <div>
            <h3 class="text-lg font-bold">Standard Tier</h3>
            <p class="text-xs text-[var(--text-muted)] mt-1">Essential everyday access with rapid digital delivery.</p>
            <div class="my-4">
              <span class="text-3xl font-extrabold text-[var(--text-primary)]"><bdi>$0</bdi></span>
              <span class="text-xs text-[var(--text-muted)]"> / month</span>
            </div>
            <ul class="text-xs text-[var(--text-muted)] space-y-2 pt-2 border-t border-[var(--border-subtle)]">
              <li class="flex items-center gap-2"><svg class="size-3.5 text-emerald-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>Instant automated approval</li>
              <li class="flex items-center gap-2"><svg class="size-3.5 text-emerald-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>Standard digital protection</li>
            </ul>
          </div>
          <button type="button" class="w-full py-2.5 px-4 text-xs font-semibold rounded-[var(--radius-button)] border border-[var(--border-subtle)] hover:border-[var(--accent)] min-h-[44px] transition-colors">Select Standard</button>
        </div>

        <!-- Tier 2 (Highlighted) -->
        <div class="relative p-6 bg-[var(--surface-bg)] border-2 border-[var(--accent)] rounded-[var(--radius-container)] {card_shadow} flex flex-col justify-between space-y-6">
          <span class="absolute -top-3 start-1/2 -translate-x-1/2 px-3 py-0.5 text-[10px] font-bold uppercase tracking-wider rounded-full bg-[var(--accent)] text-[var(--vibe-on-primary,#fff)]">Recommended</span>
          <div>
            <h3 class="text-lg font-bold">Premier Advantage</h3>
            <p class="text-xs text-[var(--text-muted)] mt-1">Accelerated disbursement, preferential terms, and 24/7 dedicated advisor.</p>
            <div class="my-4">
              <span class="text-3xl font-extrabold text-[var(--accent)]"><bdi>$29</bdi></span>
              <span class="text-xs text-[var(--text-muted)]"> / month</span>
            </div>
            <ul class="text-xs text-[var(--text-primary)] space-y-2 pt-2 border-t border-[var(--border-subtle)]">
              <li class="flex items-center gap-2 font-medium"><svg class="size-3.5 text-emerald-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>Priority sub-hour settlement</li>
              <li class="flex items-center gap-2 font-medium"><svg class="size-3.5 text-emerald-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>Comprehensive warranty & insurance</li>
              <li class="flex items-center gap-2 font-medium"><svg class="size-3.5 text-emerald-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>VIP concierge support</li>
            </ul>
          </div>
          <button type="button" class="w-full py-2.5 px-4 text-xs font-semibold rounded-[var(--radius-button)] bg-[var(--accent)] text-[var(--vibe-on-primary,#fff)] min-h-[44px] transition-opacity hover:opacity-90">{cta_name}</button>
        </div>

        <!-- Tier 3 -->
        <div class="p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} flex flex-col justify-between space-y-6">
          <div>
            <h3 class="text-lg font-bold">Enterprise Institution</h3>
            <p class="text-xs text-[var(--text-muted)] mt-1">Bespoke limits, multi-party custody, and custom SLA agreements.</p>
            <div class="my-4">
              <span class="text-3xl font-extrabold text-[var(--text-primary)]"><bdi>Custom</bdi></span>
              <span class="text-xs text-[var(--text-muted)]"> billing</span>
            </div>
            <ul class="text-xs text-[var(--text-muted)] space-y-2 pt-2 border-t border-[var(--border-subtle)]">
              <li class="flex items-center gap-2"><svg class="size-3.5 text-emerald-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>Custom credit line & underwriting</li>
              <li class="flex items-center gap-2"><svg class="size-3.5 text-emerald-500" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>Dedicated compliance legal officer</li>
            </ul>
          </div>
          <button type="button" class="w-full py-2.5 px-4 text-xs font-semibold rounded-[var(--radius-button)] border border-[var(--border-subtle)] hover:border-[var(--accent)] min-h-[44px] transition-colors">Contact Underwriting</button>
        </div>
      </div>
    </section>

    <!-- Archetype 3: Instant Rate Calculator -->
    <section id="calculator" class="mt-16 pt-10 border-t border-[var(--border-subtle)]" aria-labelledby="calc-heading">
      <div class="max-w-3xl mx-auto p-8 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow}">
        <h2 id="calc-heading" class="text-2xl font-bold mb-2">Estimate Your Rate & Limits</h2>
        <p class="text-xs text-[var(--text-muted)] mb-6">Interactive transparent pricing calculator with instant disbursement simulation.</p>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6 items-center">
          <div class="space-y-4">
            <div>
              <label class="block text-xs font-medium mb-1">Target Volume / Funding Amount</label>
              <input type="range" min="1000" max="50000" value="15000" class="w-full accent-[var(--accent)]">
              <div class="flex justify-between text-[11px] font-mono text-[var(--text-muted)] mt-1"><span>$1,000</span><span>$50,000</span></div>
            </div>
          </div>
          <div class="p-6 bg-[var(--canvas-bg)] rounded-[var(--radius-base)] border border-[var(--border-subtle)] text-center space-y-1">
            <div class="text-xs text-[var(--text-muted)]">Estimated Monthly Return</div>
            <div class="text-3xl font-extrabold text-[var(--accent)]"><bdi>$1,240</bdi></div>
            <div class="text-[11px] text-emerald-500 font-medium">Instant ACH Disbursement</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Archetype 3: Institutional Compliance & Trust -->
    <section id="compliance" class="mt-16 pt-10 border-t border-[var(--border-subtle)]" aria-labelledby="compliance-heading">
      <div class="max-w-2xl mb-8">
        <h2 id="compliance-heading" class="text-2xl font-bold">Institutional Trust & Regulatory Alignment</h2>
        <p class="text-xs text-[var(--text-muted)] mt-1">Audited security architecture protecting transactions globally.</p>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <div class="p-5 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-2">
          <div class="size-8 rounded-full bg-emerald-500/10 text-emerald-500 flex items-center justify-center font-bold text-xs">99.9</div>
          <h3 class="text-sm font-bold">FDIC / SOC2 Insured</h3>
          <p class="text-xs text-[var(--text-muted)]">All balances and transaction flows secured with tier-one custodial protocols.</p>
        </div>
        <div class="p-5 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-2">
          <div class="size-8 rounded-full bg-emerald-500/10 text-emerald-500 flex items-center justify-center font-bold text-xs">256</div>
          <h3 class="text-sm font-bold">End-to-End Encryption</h3>
          <p class="text-xs text-[var(--text-muted)]">Zero plaintext transmission with hardware security modules (HSM).</p>
        </div>
        <div class="p-5 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-2">
          <div class="size-8 rounded-full bg-emerald-500/10 text-emerald-500 flex items-center justify-center font-bold text-xs">24/7</div>
          <h3 class="text-sm font-bold">Real-time Fraud Shield</h3>
          <p class="text-xs text-[var(--text-muted)]">Autonomous ML risk engines intercepting anomalous transactions instantly.</p>
        </div>
      </div>
    </section>
"""


# ----------------------------------------------------------------------
# 4. CREATIVE CANVAS SHOWCASE (Portfolio, Creator, Gaming, Automotive)
# ----------------------------------------------------------------------
def _compile_creative_showcase(
    domain_id: str,
    mock_data: Dict[str, Any],
    style_cfg: Dict[str, str],
    card_border: str,
    card_shadow: str
) -> str:
    return f"""
    <!-- Archetype 4: Creative Canvas Showcase -> Works Gallery & Roster -->
    <section id="showcase" class="mt-16 pt-10 border-t border-[var(--border-subtle)]" aria-labelledby="showcase-heading">
      <div class="flex flex-wrap items-end justify-between gap-4 mb-10">
        <div>
          <span class="text-xs font-bold uppercase tracking-widest text-[var(--accent)]">Selected Commissions</span>
          <h2 id="showcase-heading" class="text-3xl sm:text-4xl font-extrabold tracking-tight text-[var(--text-primary)] mt-1">
            Featured Works & Spatial Experiences
          </h2>
        </div>
        <div class="flex gap-2">
          <span class="px-3 py-1 text-xs font-medium rounded-full bg-[var(--accent)] text-[var(--vibe-on-primary,#fff)]">All Disciplines</span>
          <span class="px-3 py-1 text-xs font-medium rounded-full bg-[var(--surface-bg)] border border-[var(--border-subtle)] text-[var(--text-muted)]">Motion & 3D</span>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div class="group relative p-8 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-4 transition-transform hover:-translate-y-1">
          <div class="h-48 rounded-[var(--radius-base)] bg-gradient-to-tr from-zinc-800 to-zinc-700 flex items-center justify-center text-zinc-400 font-mono text-xs">
            [SPATIAL RENDER // EXHIBITION ALPHA]
          </div>
          <div class="flex justify-between items-center">
            <h3 class="text-xl font-bold">Kinetic Spatial Pavilion</h3>
            <span class="text-xs font-mono text-[var(--accent)]">2026 REEL</span>
          </div>
          <p class="text-xs text-[var(--text-muted)] leading-relaxed">
            Multi-sensory architectural installation exploring fluid dynamics and light refraction across physical glass structures.
          </p>
        </div>

        <div class="group relative p-8 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-4 transition-transform hover:-translate-y-1">
          <div class="h-48 rounded-[var(--radius-base)] bg-gradient-to-tr from-zinc-900 to-indigo-950 flex items-center justify-center text-zinc-400 font-mono text-xs">
            [INTERACTIVE AUDIO ENGINE]
          </div>
          <div class="flex justify-between items-center">
            <h3 class="text-xl font-bold">Sub-Harmonic Synthesizer</h3>
            <span class="text-xs font-mono text-[var(--accent)]">GLOBAL LAUNCH</span>
          </div>
          <p class="text-xs text-[var(--text-muted)] leading-relaxed">
            Real-time DSP sound design platform delivering zero-latency physical audio synthesis for cinematic virtual production.
          </p>
        </div>
      </div>
    </section>

    <!-- Archetype 4: Design Disciplines -->
    <section id="disciplines" class="mt-16 pt-10 border-t border-[var(--border-subtle)]" aria-labelledby="disciplines-heading">
      <div class="max-w-2xl mb-8">
        <h2 id="disciplines-heading" class="text-3xl font-extrabold tracking-tight">Design Disciplines & Craft</h2>
        <p class="text-sm text-[var(--text-muted)] mt-2">Iterative research, generative visual identity, and physical tactile computing.</p>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <div class="p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-2">
          <h3 class="text-base font-bold">Spatial Computing</h3>
          <p class="text-xs text-[var(--text-muted)]">Spatial design systems, 6DOF interface ergonomics, and micro-gestural interaction design.</p>
        </div>
        <div class="p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-2">
          <h3 class="text-base font-bold">Generative Identity</h3>
          <p class="text-xs text-[var(--text-muted)]">Dynamic typographic algorithms and procedural brand assets reacting to environmental inputs.</p>
        </div>
        <div class="p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-2">
          <h3 class="text-base font-bold">Interactive Audio DSP</h3>
          <p class="text-xs text-[var(--text-muted)]">Real-time WebAudio synthesis, spatial binaural feedback, and tactile haptic mapping.</p>
        </div>
      </div>
    </section>

    <!-- Archetype 4: Contact & Commission Inquiries -->
    <section id="contact" class="mt-16 pt-10 border-t border-[var(--border-subtle)]" aria-labelledby="contact-heading">
      <div class="max-w-xl mx-auto p-8 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} text-center space-y-4">
        <h2 id="contact-heading" class="text-2xl font-bold">Commission a Project</h2>
        <p class="text-xs text-[var(--text-muted)]">Currently scheduling exploratory briefs for Q3/Q4 2026.</p>
        <button type="button" class="px-8 py-3 rounded-[var(--radius-button)] bg-[var(--accent)] text-[var(--vibe-on-primary,#fff)] text-xs font-bold uppercase tracking-wider min-h-[44px]">Open Commission Request</button>
      </div>
    </section>
"""


# ----------------------------------------------------------------------
# 5. SPLIT LABORATORY STUDIO (AI Developer, GreenTech, Clinical Wellness)
# ----------------------------------------------------------------------
def _compile_laboratory_studio(
    domain_id: str,
    mock_data: Dict[str, Any],
    style_cfg: Dict[str, str],
    card_border: str,
    card_shadow: str
) -> str:
    return f"""
    <!-- Archetype 5: Split Laboratory Studio -> Interactive Experimentation -->
    <section id="laboratory" class="mt-16 pt-10 border-t border-[var(--border-subtle)]" aria-labelledby="lab-heading">
      <div class="max-w-2xl mb-8">
        <h2 id="lab-heading" class="text-3xl font-extrabold tracking-tight text-[var(--text-primary)]">
          Interactive Laboratory & Benchmarks
        </h2>
        <p class="text-sm text-[var(--text-muted)] mt-2">
          Verify performance thresholds, latency profiles, and model accuracy directly on live datasets.
        </p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        <div class="lg:col-span-7 p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-4">
          <div class="flex justify-between items-center border-b border-[var(--border-subtle)] pb-3">
            <span class="text-xs font-mono font-bold text-[var(--accent)]">// EVALUATION MATRIX</span>
            <span class="text-[11px] font-mono text-emerald-500 font-bold">ACCURACY: 99.8%</span>
          </div>
          <div class="space-y-3 font-mono text-xs">
            <div class="p-3 rounded bg-[var(--canvas-bg)] border border-[var(--border-subtle)] flex justify-between">
              <span>Zero-Shot Inference</span>
              <span class="text-[var(--accent)] font-bold"><bdi>3.2 ms</bdi></span>
            </div>
            <div class="p-3 rounded bg-[var(--canvas-bg)] border border-[var(--border-subtle)] flex justify-between">
              <span>Token Generation Throughput</span>
              <span class="text-emerald-500 font-bold"><bdi>184 tok/s</bdi></span>
            </div>
            <div class="p-3 rounded bg-[var(--canvas-bg)] border border-[var(--border-subtle)] flex justify-between">
              <span>Context Compression Ratio</span>
              <span class="text-amber-500 font-bold"><bdi>12.4x</bdi></span>
            </div>
          </div>
        </div>

        <div class="lg:col-span-5 p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-4">
          <h3 class="text-base font-bold text-[var(--text-primary)]">Developer Quickstart</h3>
          <p class="text-xs text-[var(--text-muted)] leading-relaxed">
            Integrate with two lines of code into any production stack with TypeScript and Python SDKs.
          </p>
          <div class="p-3 bg-black rounded font-mono text-xs text-emerald-400 overflow-x-auto">
            <code>npm install @platform/sdk<br/>import {{ Engine }} from "@platform/sdk";</code>
          </div>
        </div>
      </div>
    </section>

    <!-- Archetype 5: Benchmarks Comparison Table -->
    <section id="benchmarks" class="mt-16 pt-10 border-t border-[var(--border-subtle)]" aria-labelledby="bench-heading">
      <div class="max-w-2xl mb-8">
        <h2 id="bench-heading" class="text-3xl font-extrabold tracking-tight">Independent Hardware Benchmarks</h2>
        <p class="text-sm text-[var(--text-muted)] mt-2">Audited floating-point precision on H100 GPU clusters.</p>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-xs font-mono text-start border-collapse border border-[var(--border-subtle)]">
          <thead class="bg-[var(--surface-bg)] text-[var(--text-muted)]">
            <tr>
              <th class="p-3 border border-[var(--border-subtle)] text-start">Model Architecture</th>
              <th class="p-3 border border-[var(--border-subtle)] text-start">Latency (TTFT)</th>
              <th class="p-3 border border-[var(--border-subtle)] text-start">Memory Footprint</th>
              <th class="p-3 border border-[var(--border-subtle)] text-start">Status</th>
            </tr>
          </thead>
          <tbody>
            <tr class="bg-[var(--canvas-bg)]">
              <td class="p-3 border border-[var(--border-subtle)] font-bold">Vibe-Engine-70B-FP8</td>
              <td class="p-3 border border-[var(--border-subtle)] text-emerald-500 font-bold">12 ms</td>
              <td class="p-3 border border-[var(--border-subtle)]">38.4 GB</td>
              <td class="p-3 border border-[var(--border-subtle)] text-emerald-500">PRODUCTION</td>
            </tr>
            <tr class="bg-[var(--surface-bg)]">
              <td class="p-3 border border-[var(--border-subtle)] font-bold">Vibe-Engine-8B-INT4</td>
              <td class="p-3 border border-[var(--border-subtle)] text-emerald-500 font-bold">3.1 ms</td>
              <td class="p-3 border border-[var(--border-subtle)]">5.8 GB</td>
              <td class="p-3 border border-[var(--border-subtle)] text-emerald-500">EDGE READY</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- Archetype 5: Deployment & SDK Installation -->
    <section id="deploy" class="mt-16 pt-10 border-t border-[var(--border-subtle)]" aria-labelledby="deploy-heading">
      <div class="p-8 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} flex flex-col sm:flex-row items-center justify-between gap-6">
        <div>
          <h2 id="deploy-heading" class="text-2xl font-bold">Deploy to Kubernetes in Minutes</h2>
          <p class="text-xs text-[var(--text-muted)] mt-1">Official Helm chart repository and Docker base images verified daily.</p>
        </div>
        <button type="button" class="px-6 py-3 rounded-[var(--radius-button)] bg-[var(--accent)] text-[var(--vibe-on-primary,#fff)] text-xs font-mono font-bold min-h-[44px]">kubectl apply -f vibe-mesh.yaml</button>
      </div>
    </section>
"""


# ----------------------------------------------------------------------
# 6. CLASSIC STRUCTURED SAAS (Enterprise SaaS, EdTech, Legal, NonProfit)
# ----------------------------------------------------------------------
def _compile_structured_saas(
    domain_id: str,
    mock_data: Dict[str, Any],
    style_cfg: Dict[str, str],
    card_border: str,
    card_shadow: str
) -> str:
    return f"""
    <!-- Archetype 6: Classic Structured SaaS -> Value Architecture & Capabilities -->
    <section id="capabilities" class="mt-16 pt-10 border-t border-[var(--border-subtle)]" aria-labelledby="saas-heading">
      <div class="text-center max-w-2xl mx-auto mb-12">
        <h2 id="saas-heading" class="text-3xl font-extrabold tracking-tight text-[var(--text-primary)]">
          Enterprise Precision & Structural Reliability
        </h2>
        <p class="text-sm text-[var(--text-muted)] mt-2">
          Engineered to scale securely across global teams with zero friction and guaranteed compliance.
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-3">
          <div class="size-10 rounded-lg bg-[var(--accent)]/10 text-[var(--accent)] flex items-center justify-center">
            <svg class="size-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          </div>
          <h3 class="text-lg font-bold">Institutional Compliance</h3>
          <p class="text-xs text-[var(--text-muted)] leading-relaxed">
            Continuous auditing, SOC2 Type II alignment, and immutable audit logging for enterprise governance.
          </p>
        </div>

        <div class="p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-3">
          <div class="size-10 rounded-lg bg-[var(--accent)]/10 text-[var(--accent)] flex items-center justify-center">
            <svg class="size-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
          </div>
          <h3 class="text-lg font-bold">Predictable High Throughput</h3>
          <p class="text-xs text-[var(--text-muted)] leading-relaxed">
            Zero-jitter orchestration with multi-region redundancy and guaranteed sub-second response times.
          </p>
        </div>

        <div class="p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-3">
          <div class="size-10 rounded-lg bg-[var(--accent)]/10 text-[var(--accent)] flex items-center justify-center">
            <svg class="size-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 14 14"/></svg>
          </div>
          <h3 class="text-lg font-bold">Rapid Onboarding SLA</h3>
          <p class="text-xs text-[var(--text-muted)] leading-relaxed">
            Zero-code connectors, automated data migration, and designated solutions engineering support.
          </p>
        </div>
      </div>
    </section>

    <!-- Archetype 6: Solutions Architecture Matrix -->
    <section id="solutions" class="mt-16 pt-10 border-t border-[var(--border-subtle)]" aria-labelledby="sol-heading">
      <div class="max-w-2xl mb-8">
        <h2 id="sol-heading" class="text-3xl font-extrabold tracking-tight">Tailored Solutions by Industry</h2>
        <p class="text-sm text-[var(--text-muted)] mt-2">Turnkey integration templates designed for your specific vertical.</p>
      </div>
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
        <div class="p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-3">
          <h3 class="text-lg font-bold">Financial Services & Banking</h3>
          <p class="text-xs text-[var(--text-muted)] leading-relaxed">Sub-second settlement verification, encrypted customer vaults, and automated KYC pipelines.</p>
        </div>
        <div class="p-6 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-3">
          <h3 class="text-lg font-bold">Healthcare & Clinical Networks</h3>
          <p class="text-xs text-[var(--text-muted)] leading-relaxed">HIPAA compliant patient telemetry, doctor schedule synchronization, and zero-exposure data vaults.</p>
        </div>
      </div>
    </section>

    <!-- Archetype 6: Enterprise FAQ & Support -->
    <section id="faq" class="mt-16 pt-10 border-t border-[var(--border-subtle)]" aria-labelledby="faq-heading">
      <div class="max-w-2xl mb-8">
        <h2 id="faq-heading" class="text-2xl font-bold">Frequently Asked Questions</h2>
        <p class="text-xs text-[var(--text-muted)] mt-1">Direct answers to technical architecture and implementation inquiries.</p>
      </div>
      <div class="space-y-4">
        <div class="p-5 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-2">
          <h3 class="text-sm font-bold">How does the platform ensure zero data residency violations?</h3>
          <p class="text-xs text-[var(--text-muted)] leading-relaxed">All compute nodes and encrypted databases are pinned to your region of choice with cryptographic geofencing.</p>
        </div>
        <div class="p-5 bg-[var(--surface-bg)] {card_border} rounded-[var(--radius-container)] {card_shadow} space-y-2">
          <h3 class="text-sm font-bold">What is the guaranteed SLA for enterprise support?</h3>
          <p class="text-xs text-[var(--text-muted)] leading-relaxed">Enterprise tier clients receive dedicated engineering channels with a 15-minute response SLA 24/7/365.</p>
        </div>
      </div>
    </section>
"""
