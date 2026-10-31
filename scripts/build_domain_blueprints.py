"""
Generates data/domain_blueprints.json with comprehensive architectural specifications
for all 24 domains, including section flow, signature widget, 3 layout flavors,
smart theme bias, ambient motion spec, and realistic mock data.
"""

import json
from pathlib import Path

BLUEPRINTS = {
    "beauty_clinical_wellness": {
        "domain_id": "beauty_clinical_wellness",
        "theme_bias": "light",
        "primary_styles": ["quiet_luxury", "soft_humanist", "editorial_magazine"],
        "section_flow": [
            {"id": "hero", "name": "Aesthetic Serenity Hero", "type": "split_hero", "purpose": "Immediate sense of calm luxury with appointment booking trigger"},
            {"id": "services", "name": "Treatment Carousel & Menu", "type": "service_tabs", "purpose": "Interactive category switching with transparent pricing"},
            {"id": "signature", "name": "Before/After Slider & Doctor Credentials", "type": "signature_widget", "purpose": "Physical clinical proof of results"},
            {"id": "social_proof", "name": "Verified Patient Testimonials", "type": "masonry_reviews", "purpose": "Real patient stories with dermatological outcome stars"},
            {"id": "booking_footer", "name": "VIP Concierge Booking & Location", "type": "booking_card", "purpose": "Calendar slot selection with zero friction"}
        ],
        "signature_widget": {
            "name": "Clinical Before/After Visualizer & Slot Picker",
            "type": "slider_with_calendar",
            "props": {
                "interactive_slider": True,
                "drag_physics": "smooth_lerp",
                "default_comparison_tag": "Laser Rejuvenation - 4 Weeks Post",
                "slot_picker_active": True
            }
        },
        "layout_flavors": [
            {"flavor_id": "luxury_warm_light", "name": "Quiet Warm Luxury", "hero_layout": "asymmetric_split", "card_style": "subtle_border_sand"},
            {"flavor_id": "editorial_spa", "name": "Editorial Spa & Wellness", "hero_layout": "centered_curated", "card_style": "minimal_frame"},
            {"flavor_id": "clinical_high_tech", "name": "Dermatology High Precision", "hero_layout": "bento_compact", "card_style": "glass_card_white"}
        ],
        "ambient_motion": {
            "type": "spotlight_cursor_soft",
            "bg_gradient": "radial-gradient(circle at center, oklch(0.97 0.015 85) 0%, oklch(0.94 0.01 75) 100%)",
            "motion_hint": "subtle floating botanical or soft light refraction",
            "lcp_safe": True
        },
        "mock_data": {
            "en": {
                "headline": "Advanced Aesthetic Dermatology & Regenerative Care",
                "subheadline": "Board-certified specialists delivering natural, luminous results with clinically certified protocols.",
                "cta_primary": "Book Private Consultation",
                "cta_secondary": "Explore Treatment Catalog",
                "metrics": [{"label": "Patient Satisfaction", "value": "99.4%"}, {"label": "Board Certified Dermatologists", "value": "12"}, {"label": "Clinical Case Studies", "value": "18,000+"}]
            },
            "fa": {
                "headline": "مراقبت پیشرفته پوست، زیبایی و جوانسازی بالینی",
                "subheadline": "متخصصان دارای بورد با پروتکل های تایید شده بین المللی برای نتایج طبیعی و درخشان.",
                "cta_primary": "رزرو وقت مشاوره تخصصی",
                "cta_secondary": "مشاهده تعرفه و لیست خدمات",
                "metrics": [{"label": "رضایت مراجعین", "value": "۹۹.۴٪"}, {"label": "پزشک متخصص بورد", "value": "۱۲"}, {"label": "پرونده موفق بالینی", "value": "+۱۸,۰۰۰"}]
            }
        }
    },
    "fintech_banking": {
        "domain_id": "fintech_banking",
        "theme_bias": "light",
        "primary_styles": ["clean_stripe", "minimal_swiss", "editorial_magazine"],
        "section_flow": [
            {"id": "hero", "name": "Institutional Trust Hero", "type": "split_hero", "purpose": "Immediate high-net-worth authority and APY yields"},
            {"id": "signature", "name": "Interactive Yield Calculator & Virtual Card", "type": "signature_widget", "purpose": "Live slider showing compounding interest & 3D holographic card"},
            {"id": "security", "name": "Tier-1 Compliance & Audit Badges", "type": "security_grid", "purpose": "SOC2, FDIC insurance, zero-liability guarantees"},
            {"id": "pricing", "name": "Transparent Fee Comparison Table", "type": "comparison_matrix", "purpose": "Direct contrast with legacy banking markups"},
            {"id": "footer", "name": "Institutional Compliance Footer", "type": "dense_footer", "purpose": "Legal disclaimers, licensing, swift routing"}
        ],
        "signature_widget": {
            "name": "High-Yield APY Compounding Simulator",
            "type": "financial_calculator",
            "props": {
                "interactive_slider": True,
                "range_min": 1000,
                "range_max": 250000,
                "default_val": 25000,
                "apy_rate": 0.052,
                "tabular_nums": True
            }
        },
        "layout_flavors": [
            {"flavor_id": "stripe_engineered", "name": "Engineered Precision Stripe", "hero_layout": "split_hero_card", "card_style": "slate_subtle_border"},
            {"flavor_id": "swiss_wealth", "name": "Swiss Private Banking", "hero_layout": "asymmetric_editorial", "card_style": "crisp_hairline_frame"},
            {"flavor_id": "modern_treasury", "name": "Corporate Treasury Dashboard", "hero_layout": "dense_hud_summary", "card_style": "flat_tabular_card"}
        ],
        "ambient_motion": {
            "type": "subtle_geometric_grid",
            "bg_gradient": "linear-gradient(180deg, oklch(0.98 0.005 240) 0%, oklch(0.95 0.01 240) 100%)",
            "motion_hint": "hairline grid with gentle micro-glow on active inputs",
            "lcp_safe": True
        },
        "mock_data": {
            "en": {
                "headline": "Institutional Wealth Management & Modern Treasury",
                "subheadline": "Automated cash yield, multi-currency accounts, and zero-fee corporate transfers with institutional-grade security.",
                "cta_primary": "Open Treasury Account",
                "cta_secondary": "Calculate Net Yield",
                "metrics": [{"label": "Assets Monitored", "value": "$4.8B"}, {"label": "FDIC Insured Up To", "value": "$5,000,000"}, {"label": "Average Annual Yield", "value": "5.25% APY"}]
            },
            "fa": {
                "headline": "مدیریت ثروت نهادی و خزانه داری شرکتی هوشمند",
                "subheadline": "سوددهی خودکار موجودی، حساب های چندارزی و انتقالات بدون کارمزد با امنیت بانکی سطح اول.",
                "cta_primary": "افتتاح حساب شرکتی",
                "cta_secondary": "محاسبه سود مرکب سالانه",
                "metrics": [{"label": "حجم دارایی تحت نظارت", "value": "$۴.۸B"}, {"label": "پوشش بیمه حساب", "value": "$۵,۰۰۰,۰۰۰"}, {"label": "میانگین سود سالانه", "value": "۵.۲۵٪ APY"}]
            }
        }
    },
    "crypto_trading_web3": {
        "domain_id": "crypto_trading_web3",
        "theme_bias": "dark",
        "primary_styles": ["linear_dark", "data_dense_terminal", "clean_stripe"],
        "section_flow": [
            {"id": "hero", "name": "Live Market Telemetry Hero", "type": "ticker_hero", "purpose": "Real-time ticker stream with sparklines and instant buy widget"},
            {"id": "signature", "name": "Live Orderbook & Slippage Simulator", "type": "signature_widget", "purpose": "Live bid/ask depth chart with instant convert calculator"},
            {"id": "assets", "name": "24h Volume & Gainer Matrix", "type": "tabular_market_grid", "purpose": "Sortable high-frequency market data"},
            {"id": "security", "name": "Cold Storage & Multi-Sig Proof", "type": "proof_cards", "purpose": "Proof-of-reserves Merkle tree verification"},
            {"id": "cta", "name": "Pro Trader Terminal Access", "type": "terminal_cta", "purpose": "Zero-latency API keys and web interface"}
        ],
        "signature_widget": {
            "name": "Zero-Slippage Quick Swap & Depth Sparkline",
            "type": "crypto_swap_telemetry",
            "props": {
                "live_sparklines": True,
                "swap_currencies": ["BTC", "ETH", "USDT", "SOL"],
                "show_gas_tracker": True,
                "tabular_nums": True
            }
        },
        "layout_flavors": [
            {"flavor_id": "linear_terminal_dark", "name": "Minimalist Linear Dark", "hero_layout": "split_chart_hero", "card_style": "pitch_charcoal_1px"},
            {"flavor_id": "cyber_glass_hud", "name": "Cyberpunk Glass HUD", "hero_layout": "multi_pane_hud", "card_style": "deep_tint_glass_border"},
            {"flavor_id": "swiss_fintech_crypto", "name": "Swiss Web3 Protocol", "hero_layout": "asymmetric_contrast", "card_style": "sharp_mono_cards"}
        ],
        "ambient_motion": {
            "type": "subtle_particle_glow",
            "bg_gradient": "radial-gradient(ellipse at 50% 0%, oklch(0.22 0.04 150) 0%, oklch(0.12 0.01 240) 80%)",
            "motion_hint": "pulsing green/red micro-glows on price updates",
            "lcp_safe": True
        },
        "mock_data": {
            "en": {
                "headline": "Sub-Millisecond Crypto Derivatives & Spot Exchange",
                "subheadline": "Trade 300+ markets with institutional deep liquidity, 0% maker fees, and on-chain Proof of Reserves.",
                "cta_primary": "Start Trading Now",
                "cta_secondary": "View Live Orderbook",
                "metrics": [{"label": "24h Trading Volume", "value": "$1.42B"}, {"label": "Matching Latency", "value": "<12µs"}, {"label": "Proof of Reserves", "value": "100% Backed"}]
            },
            "fa": {
                "headline": "صرافی اسپات و مشتقه ارز دیجیتال با تاخیر زیر میلی ثانیه",
                "subheadline": "معامله بیش از ۳۰۰ رمزارز با نقدینگی عمیق، کارمزد صفر میکر و تاییدیه شفاف اثبات ذخایر آنچین.",
                "cta_primary": "شروع آنی معاملات",
                "cta_secondary": "مشاهده زنده عمق بازار",
                "metrics": [{"label": "حجم معاملات ۲۴ ساعته", "value": "$۱.۴۲B"}, {"label": "سرعت مچینگ سفارشات", "value": "<۱۲µs"}, {"label": "تعهد ذخایر اثبات شده", "value": "۱۰۰٪ کامل"}]
            }
        }
    },
    "devops_cloud_terminal": {
        "domain_id": "devops_cloud_terminal",
        "theme_bias": "dark",
        "primary_styles": ["data_dense_terminal", "linear_dark", "minimal_swiss"],
        "section_flow": [
            {"id": "hero", "name": "Cluster Health & Telemetry HUD", "type": "hud_hero", "purpose": "Immediate node health badges, latency radar and CLI curl snippet"},
            {"id": "signature", "name": "Interactive Shell & Diff Inspector", "type": "signature_widget", "purpose": "Live streaming log preview and YAML pipeline validator"},
            {"id": "benchmarks", "name": "Throughput & P99 Latency Benchmarks", "type": "latency_chart", "purpose": "Comparative performance against AWS/GCP"},
            {"id": "architecture", "name": "Topology & Ingress Gateway Graph", "type": "interactive_nodes", "purpose": "Microservice mesh status visualizer"},
            {"id": "footer", "name": "Developer Doc Hub & Status Ticker", "type": "dense_dev_footer", "purpose": "All systems operational 99.999%"}
        ],
        "signature_widget": {
            "name": "Live Kubectl Pod Terminal & Log Streamer",
            "type": "cli_emulator",
            "props": {
                "copyable_command": "curl -sSL https://get.coreos.sh | bash",
                "tab_switcher": ["STDOUT", "K8s Events", "Raw Metrics"],
                "font_family": "JetBrains Mono, monospace"
            }
        },
        "layout_flavors": [
            {"flavor_id": "dense_ops_hud", "name": "Dense 12-Column HUD", "hero_layout": "multi_pane_terminal", "card_style": "terminal_carbon_1px"},
            {"flavor_id": "minimalist_infra", "name": "Minimalist Linear Infra", "hero_layout": "split_hero_code", "card_style": "slate_subtle_wireframe"},
            {"flavor_id": "cyber_observability", "name": "Cyber Observability Matrix", "hero_layout": "bento_dense", "card_style": "glass_terminal_border"}
        ],
        "ambient_motion": {
            "type": "matrix_subtle_raster",
            "bg_gradient": "linear-gradient(180deg, oklch(0.14 0.01 240) 0%, oklch(0.10 0.005 240) 100%)",
            "motion_hint": "subtle green telemetry pulses and blinking cursor",
            "lcp_safe": True
        },
        "mock_data": {
            "en": {
                "headline": "Zero-Config Kubernetes Ingress & Edge Orchestration",
                "subheadline": "Deploy global container clusters in seconds with automatic TLS, wireguard mesh, and sub-10ms P99 latency.",
                "cta_primary": "Deploy In 30 Seconds",
                "cta_secondary": "Read Architecture RFC",
                "metrics": [{"label": "P99 Edge Latency", "value": "8.4ms"}, {"label": "Global PoPs", "value": "120+"}, {"label": "SLA Uptime", "value": "99.999%"}]
            },
            "fa": {
                "headline": "ارکستراسیون کوبرنتیز و اینگرس لبه با پیکربندی صفر",
                "subheadline": "استقرار کلاسترهای جهانی در چند ثانیه با TLS خودکار، شبکه مش و تاخیر لبه زیر ۱۰ میلی ثانیه.",
                "cta_primary": "استقرار فوری در ۳۰ ثانیه",
                "cta_secondary": "مطالعه معماری فنی",
                "metrics": [{"label": "تاخیر لبه P99", "value": "۸.۴ms"}, {"label": "نقاط دسترسی جهانی", "value": "+۱۲۰"}, {"label": "پایداری تضمین شده SLA", "value": "۹۹.۹۹۹٪"}]
            }
        }
    },
    "saas_b2b_enterprise": {
        "domain_id": "saas_b2b_enterprise",
        "theme_bias": "light",
        "primary_styles": ["clean_stripe", "minimal_swiss", "editorial_magazine"],
        "section_flow": [
            {"id": "hero", "name": "Executive ROI & Product Preview Hero", "type": "split_hero_mockup", "purpose": "High-impact value proposition with interactive dashboard screenshot"},
            {"id": "social_proof", "name": "Fortune 500 Enterprise Logos", "type": "logo_ticker", "purpose": "Instant institutional credibility"},
            {"id": "signature", "name": "Interactive Feature Bento & ROI Calculator", "type": "signature_widget", "purpose": "Directly calculating enterprise engineering hours saved"},
            {"id": "security", "name": "SOC2 Type II, HIPAA & Single Sign-On", "type": "compliance_badge_grid", "purpose": "Neutralizing enterprise procurement objections"},
            {"id": "pricing", "name": "Transparent Team & Enterprise Plans", "type": "pricing_tier_matrix", "purpose": "Monthly/Annual toggle with clear enterprise tier"}
        ],
        "signature_widget": {
            "name": "Enterprise Productivity ROI Calculator",
            "type": "roi_slider_bento",
            "props": {
                "seat_slider": True,
                "default_seats": 50,
                "annual_savings_multiplier": 1400,
                "currency": "$"
            }
        },
        "layout_flavors": [
            {"flavor_id": "clean_enterprise_stripe", "name": "Clean Stripe Light", "hero_layout": "split_hero_browser", "card_style": "subtle_white_lifted"},
            {"flavor_id": "swiss_executive", "name": "Swiss Corporate Editorial", "hero_layout": "asymmetric_bento", "card_style": "sharp_mono_border"},
            {"flavor_id": "modern_saas_hybrid", "name": "Modern Hybrid Bento", "hero_layout": "center_hero_bento", "card_style": "pill_badge_modern"}
        ],
        "ambient_motion": {
            "type": "subtle_mesh_glow",
            "bg_gradient": "radial-gradient(ellipse at 50% 0%, oklch(0.96 0.02 240) 0%, oklch(0.98 0.005 240) 100%)",
            "motion_hint": "smooth stagger on bento card reveal with spring easing",
            "lcp_safe": True
        },
        "mock_data": {
            "en": {
                "headline": "Unified Enterprise Intelligence & Workflow Orchestration",
                "subheadline": "Connect disconnected data silos, eliminate manual reporting, and accelerate delivery across 500+ seat organizations.",
                "cta_primary": "Request Executive Demo",
                "cta_secondary": "Calculate Enterprise ROI",
                "metrics": [{"label": "Time-To-Value", "value": "14 Days"}, {"label": "Engineering Hours Saved/Mo", "value": "1,200h"}, {"label": "SOC2 Type II", "value": "Certified"}]
            },
            "fa": {
                "headline": "هوش سازمانی یکپارچه و ارکستراسیون هوشمند جریان کار",
                "subheadline": "اتصال پایگاه های داده مجزا، حذف گزارش های دستی و افزایش سرعت تصمیم گیری در سازمان های بزرگ.",
                "cta_primary": "درخواست دموی سازمانی",
                "cta_secondary": "محاسبه بازگشت سرمایه ROI",
                "metrics": [{"label": "زمان راه اندازی کامل", "value": "۱۴ روز"}, {"label": "صرفه جویی ساعتی ماهانه", "value": "۱,۲۰۰ ساعت"}, {"label": "استاندارد امنیتی", "value": "SOC2 تایید شده"}]
            }
        }
    },
    "ai_developer_platform": {
        "domain_id": "ai_developer_platform",
        "theme_bias": "dark",
        "primary_styles": ["linear_dark", "modern_glass_2", "data_dense_terminal"],
        "section_flow": [
            {"id": "hero", "name": "Neural Canvas & Live Prompt Studio", "type": "interactive_prompt_hero", "purpose": "Immediate hands-on demonstration of intelligence"},
            {"id": "signature", "name": "Multi-Model Arena & Latency Benchmark HUD", "type": "signature_widget", "purpose": "Live comparison of token latency, accuracy, and reasoning step"},
            {"id": "features", "name": "Agentic Reasoning & Tool-Call Mesh", "type": "bento_agentic", "purpose": "Visualizing function calling, sandbox memory, and DAG execution"},
            {"id": "code_snippet", "name": "SDK Integration in 3 Lines", "type": "tabbed_sdk_code", "purpose": "Python, TypeScript, and cURL instant copy"},
            {"id": "footer", "name": "Developer Community & Model Registry", "type": "community_footer", "purpose": "Discord, GitHub stars, API uptime"}
        ],
        "signature_widget": {
            "name": "Live Reasoning Step & Token Telemetry Drawer",
            "type": "thinking_drawer_arena",
            "props": {
                "streaming_demo": True,
                "tokens_per_second": 142,
                "latency_first_token_ms": 18,
                "model_selector": ["Claude 3.7", "Gemini 2.5 Pro", "DeepSeek R1"]
            }
        },
        "layout_flavors": [
            {"flavor_id": "linear_ai_dark", "name": "Linear Minimalist AI", "hero_layout": "split_prompt_canvas", "card_style": "pitch_charcoal_subtle"},
            {"flavor_id": "glass_nebula", "name": "Modern Luxury Glass 2.0", "hero_layout": "nebula_glow_hero", "card_style": "layered_glass_frost"},
            {"flavor_id": "terminal_arena", "name": "High-Velocity Benchmark HUD", "hero_layout": "arena_split", "card_style": "dense_mono_card"}
        ],
        "ambient_motion": {
            "type": "glowing_edge_shimmer",
            "bg_gradient": "radial-gradient(circle at 50% 10%, oklch(0.25 0.05 280) 0%, oklch(0.12 0.01 260) 90%)",
            "motion_hint": "shimmering border beam on model selection card",
            "lcp_safe": True
        },
        "mock_data": {
            "en": {
                "headline": "The Autonomous Intelligence Engine for Mission-Critical Agents",
                "subheadline": "Sub-20ms first-token latency, native tool orchestration, and deterministic schema enforcement at planetary scale.",
                "cta_primary": "Get Instant API Key",
                "cta_secondary": "Try Live Reasoning Canvas",
                "metrics": [{"label": "First Token Latency", "value": "18ms"}, {"label": "Tokens / Second", "value": "145 t/s"}, {"label": "Schema Compliance", "value": "100%"}]
            },
            "fa": {
                "headline": "موتور هوش مصنوعی خودمختار برای ایجنت های مقیاس پذیر",
                "subheadline": "تاخیر اولین توکن زیر ۲۰ میلی ثانیه، هماهنگی بومی ابزارها و خروجی های ساختاریافته بدون خطا.",
                "cta_primary": "دریافت رایگان کلید API",
                "cta_secondary": "تست محیط استدلال زنده",
                "metrics": [{"label": "تاخیر اولین توکن", "value": "۱۸ms"}, {"label": "سرعت تولید توکن", "value": "۱۴۵ t/s"}, {"label": "دقت تطابق با اسکیما", "value": "۱۰۰٪ کامل"}]
            }
        }
    },
    "food_restaurant_cafe": {
        "domain_id": "food_restaurant_cafe",
        "theme_bias": "dark",
        "primary_styles": ["editorial_magazine", "quiet_luxury", "soft_humanist"],
        "section_flow": [
            {"id": "hero", "name": "Atmospheric Culinary Showcase", "type": "cinematic_hero", "purpose": "High-appetite food photography with live open/closed status badge"},
            {"id": "signature", "name": "Interactive Category Menu & Table Reservation", "type": "signature_widget", "purpose": "Seamless tabbed menu with dietary badges and 1-click table booking"},
            {"id": "story", "name": "Chef Philosophy & Farm-to-Table Ingredients", "type": "artisan_story", "purpose": "Establishing organic quality and craft pedigree"},
            {"id": "reviews", "name": "Culinary Press & Michelin Mentions", "type": "press_quotes", "purpose": "Prestigious dining reviews"},
            {"id": "location", "name": "Operating Hours, Map & Parking Concierge", "type": "interactive_map_hours", "purpose": "Zero ambiguity for arriving guests"}
        ],
        "signature_widget": {
            "name": "Live Tabbed Menu & Table Booking Drawer",
            "type": "menu_booking_card",
            "props": {
                "tabs": ["Main Courses", "Artisan Starters", "Desserts", "Cocktails"],
                "live_status_badge": "Open Now Until 11:30 PM",
                "table_reservation_modal": True,
                "dietary_pills": ["Vegan", "Gluten-Free", "Chef's Signature"]
            }
        },
        "layout_flavors": [
            {"flavor_id": "bistronomy_dark", "name": "Moody Bistro Charcoal", "hero_layout": "split_cinematic_hero", "card_style": "warm_slate_dark"},
            {"flavor_id": "warm_editorial_terroir", "name": "Warm Editorial Terroir", "hero_layout": "asymmetric_food_grid", "card_style": "terracotta_paper_border"},
            {"flavor_id": "modern_minimal_cafe", "name": "Japanese Zen Cafe", "hero_layout": "zen_whitespace", "card_style": "subtle_wash_card"}
        ],
        "ambient_motion": {
            "type": "subtle_warm_glow",
            "bg_gradient": "radial-gradient(circle at 50% 20%, oklch(0.20 0.03 40) 0%, oklch(0.12 0.01 30) 100%)",
            "motion_hint": "soft candlelight warmth and micro-hover zoom on menu dishes",
            "lcp_safe": True
        },
        "mock_data": {
            "en": {
                "headline": "Artisanal Wood-Fired Dining & Seasonal Terroir",
                "subheadline": "Locally sourced heirloom produce, slow-fermented sourdough, and natural wines crafted by Chef Julien.",
                "cta_primary": "Reserve Your Table",
                "cta_secondary": "Explore Seasonal Menu",
                "metrics": [{"label": "Current Status", "value": "Open Tonight"}, {"label": "Seating Capacity", "value": "45 Intimate Guests"}, {"label": "Michelin Guide", "value": "2026 Recommended"}]
            },
            "fa": {
                "headline": "تجربه دست ساز طعم های اصیل و فصلی در فضایی صمیمی",
                "subheadline": "مواد اولیه ارگانیک و دستچین شده از مزارع محلی با طبخ آرام هیزمی و دستپخت سرآشپز بین المللی.",
                "cta_primary": "رزرو آنلاین میز",
                "cta_secondary": "مشاهده منوی فصلی غذاها",
                "metrics": [{"label": "وضعیت پذیرش", "value": "هم اکنون باز است"}, {"label": "ظرفیت سالن", "value": "۴۵ مهمان اختصاصی"}, {"label": "امتیاز رضایت", "value": "۴.۹ از ۵ ستاره"}]
            }
        }
    },
    "real_estate_architecture": {
        "domain_id": "real_estate_architecture",
        "theme_bias": "light",
        "primary_styles": ["editorial_magazine", "minimal_swiss", "quiet_luxury"],
        "section_flow": [
            {"id": "hero", "name": "Architectural Statement & Multi-Filter Search", "type": "split_search_hero", "purpose": "Stunning 16:9 property visual with instantaneous buy/rent filter bar"},
            {"id": "signature", "name": "Interactive Property Card Grid & 3D Tour", "type": "signature_widget", "purpose": "Floor plans, bedroom/bath specs, sqft tags, and virtual walkthrough trigger"},
            {"id": "curated", "name": "Featured Off-Market Residences", "type": "luxury_carousel", "purpose": "Exclusive high-value estates"},
            {"id": "neighborhood", "name": "District Amenities & Transit Radar", "type": "neighborhood_map", "purpose": "WalkScore, nearby private schools, airport transit"},
            {"id": "contact", "name": "Private Broker Consultation", "type": "concierge_broker_card", "purpose": "Direct WhatsApp/Call with lead architect/broker"}
        ],
        "signature_widget": {
            "name": "Multi-Parameter Architectural Property Filter",
            "type": "property_filter_grid",
            "props": {
                "filters": ["Buy", "Rent", "Off-Plan"],
                "price_slider": True,
                "bedroom_selector": [1, 2, 3, 4, "5+"],
                "aspect_ratio": "aspect-video"
            }
        },
        "layout_flavors": [
            {"flavor_id": "swiss_architectural", "name": "Swiss Architectural Editorial", "hero_layout": "asymmetric_split_16_9", "card_style": "razor_thin_border"},
            {"flavor_id": "luxury_residence_light", "name": "Ultra-Luxury Penthouse Light", "hero_layout": "full_screen_panoramic", "card_style": "sandstone_soft_shadow"},
            {"flavor_id": "modern_urban_grid", "name": "Modern Urban Development", "hero_layout": "bento_spatial", "card_style": "clean_pill_badge"}
        ],
        "ambient_motion": {
            "type": "clean_monochrome_pan",
            "bg_gradient": "linear-gradient(180deg, oklch(0.98 0.005 60) 0%, oklch(0.95 0.01 60) 100%)",
            "motion_hint": "crisp geometry with smooth image pan and zero layout shift",
            "lcp_safe": True
        },
        "mock_data": {
            "en": {
                "headline": "Curated Modernist Estates & Architectural Landmarks",
                "subheadline": "Exclusive residential portfolios engineered with sustainable materials, panoramic floor-to-ceiling glass, and private sanctuaries.",
                "cta_primary": "Explore Available Residences",
                "cta_secondary": "Request Private Tour",
                "metrics": [{"label": "Total Portfolio Value", "value": "$850M+"}, {"label": "Architectural Awards", "value": "18"}, {"label": "Average Days on Market", "value": "24 Days"}]
            },
            "fa": {
                "headline": "کلکسیون اختصاصی عمارت های مدرن و املاک شاخص معماری",
                "subheadline": "واحدهای لوکس مهندسی شده با پنجره های قدی پانوراما، متریال پایدار و موقعیت های ممتاز شهری.",
                "cta_primary": "مشاهده املاک موجود",
                "cta_secondary": "درخواست بازدید حضوری",
                "metrics": [{"label": "ارزش پورتفولیوی املاک", "value": "+$۸۵۰M"}, {"label": "جوایز بین المللی معماری", "value": "۱۸"}, {"label": "میانگین زمان فروش", "value": "۲۴ روز"}]
            }
        }
    },
    "healthcare_hospital_medical": {
        "domain_id": "healthcare_hospital_medical",
        "theme_bias": "light",
        "primary_styles": ["clean_stripe", "soft_humanist", "minimal_swiss"],
        "section_flow": [
            {"id": "hero", "name": "Clinical Trust & Urgent Care Access", "type": "emergency_care_hero", "purpose": "Instant appointment triage with live wait times"},
            {"id": "signature", "name": "Doctor Specialization Finder & Slot Picker", "type": "signature_widget", "purpose": "Search by symptom or department with instant calendar booking"},
            {"id": "departments", "name": "Centers of Excellence", "type": "card_department_grid", "purpose": "Cardiology, Oncology, Neurology, Pediatrics"},
            {"id": "insurance", "name": "In-Network Insurance & Telehealth", "type": "insurance_badges", "purpose": "Immediate financial reassurance"},
            {"id": "faq", "name": "Patient Preparation & Hospital Guidelines", "type": "accordion_faq", "purpose": "Admission instructions and visitor hours"}
        ],
        "signature_widget": {
            "name": "Symptom Triage & Physician Scheduling Hub",
            "type": "medical_scheduler",
            "props": {
                "symptom_search": True,
                "wait_time_counter": "7 mins average wait",
                "telehealth_toggle": True,
                "accessible_contrast": "WCAG_AAA_17_TO_1"
            }
        },
        "layout_flavors": [
            {"flavor_id": "clean_hospital_blue", "name": "Nordic Healthcare Trust", "hero_layout": "split_hero_telehealth", "card_style": "frost_blue_border"},
            {"flavor_id": "warm_humanist_clinic", "name": "Warm Humanist Clinic", "hero_layout": "approachable_centered", "card_style": "soft_cream_border"},
            {"flavor_id": "high_precision_medical", "name": "High-Precision Medical Institute", "hero_layout": "dense_triage_hud", "card_style": "crisp_hairline_medical"}
        ],
        "ambient_motion": {
            "type": "calm_stable_lighting",
            "bg_gradient": "linear-gradient(180deg, oklch(0.98 0.01 220) 0%, oklch(0.95 0.015 220) 100%)",
            "motion_hint": "solid, zero-flicker calming surfaces designed for anxious patients",
            "lcp_safe": True
        },
        "mock_data": {
            "en": {
                "headline": "World-Class Academic Medicine & Compassionate Clinical Care",
                "subheadline": "Leading specialists, state-of-the-art diagnostic imaging, and seamless in-person and telehealth consultations.",
                "cta_primary": "Book Immediate Appointment",
                "cta_secondary": "Find Your Doctor",
                "metrics": [{"label": "Board Certified Physicians", "value": "350+"}, {"label": "Emergency Wait Time", "value": "<10 Mins"}, {"label": "Patient Safety Score", "value": "Grade A"}]
            },
            "fa": {
                "headline": "مرکز تخصصی درمان، پژوهش بالینی و مراقبت دلسوزانه بیمار",
                "subheadline": "برترین اساتید پزشکی، تجهیزات پیشرفته تصویربرداری و نوبت دهی آنلاین حضوری و تله مدیسین.",
                "cta_primary": "رزرو آنلاین نوبت ویزیت",
                "cta_secondary": "جستجوی پزشک متخصص",
                "metrics": [{"label": "پزشک و جراح فوق تخصص", "value": "+۳۵۰"}, {"label": "میانگین انتظار اورژانس", "value": "<۱۰ دقیقه"}, {"label": "رتبه ایمنی و کیفیت درمان", "value": "درجه یک A"}]
            }
        }
    },
    "education_edtech_lms": {
        "domain_id": "education_edtech_lms",
        "theme_bias": "light",
        "primary_styles": ["clean_stripe", "playful_consumer", "editorial_magazine"],
        "section_flow": [
            {"id": "hero", "name": "Outcome-Driven Learning Hero", "type": "split_learning_hero", "purpose": "Interactive course preview with student graduation proof"},
            {"id": "signature", "name": "Interactive Syllabus Explorer & Project Canvas", "type": "signature_widget", "purpose": "Collapsible syllabus modules with live coding exercise demo"},
            {"id": "instructors", "name": "Industry Practitioner Mentors", "type": "mentor_roster", "purpose": "Mentors from Google, Stripe, Apple"},
            {"id": "outcomes", "name": "Hiring Partners & Career Trajectory", "type": "alumni_salary_grid", "purpose": "Audited salary placement data"},
            {"id": "pricing", "name": "Flexible Tuition & Scholarship Aid", "type": "tuition_calculator", "purpose": "Monthly installments vs upfront savings"}
        ],
        "signature_widget": {
            "name": "Live Curriculum Module & Exercise Player",
            "type": "syllabus_player_card",
            "props": {
                "module_accordion": True,
                "interactive_quiz_preview": True,
                "completion_progress_bar": True,
                "project_deliverables": ["Production SaaS API", "Custom Design System"]
            }
        },
        "layout_flavors": [
            {"flavor_id": "modern_edtech_clean", "name": "Clean Stripe EdTech", "hero_layout": "split_hero_preview", "card_style": "subtle_white_card"},
            {"flavor_id": "campus_editorial", "name": "Academic Editorial", "hero_layout": "asymmetric_scholar", "card_style": "warm_sand_border"},
            {"flavor_id": "developer_academy", "name": "Interactive Dev Bootcamp", "hero_layout": "bento_interactive", "card_style": "terminal_light_card"}
        ],
        "ambient_motion": {
            "type": "dynamic_progress_glow",
            "bg_gradient": "radial-gradient(circle at 50% 0%, oklch(0.97 0.02 260) 0%, oklch(0.98 0.005 260) 100%)",
            "motion_hint": "fluid progress bars with positive reinforcement micro-animations",
            "lcp_safe": True
        },
        "mock_data": {
            "en": {
                "headline": "Master Modern Software Engineering & Systems Architecture",
                "subheadline": "Project-based curriculum mentored by staff engineers. Build 4 production-grade systems and accelerate your career.",
                "cta_primary": "Enroll in Next Cohort",
                "cta_secondary": "Download Full Syllabus",
                "metrics": [{"label": "Alumni Placement Rate", "value": "94.2%"}, {"label": "Average Starting Salary", "value": "$128k"}, {"label": "Hiring Partners", "value": "240+"}]
            },
            "fa": {
                "headline": "آموزش پروژه محور مهندسی نرم افزار و معماری سیستم",
                "subheadline": "سرفصل های عملی با منتورشیپ مهندسان ارشد صنعت. ساخت ۴ پروژه پروداکشن برای ورود قدرتمند به بازار کار.",
                "cta_primary": "ثبت نام در دوره جدید",
                "cta_secondary": "دریافت سرفصل های کامل",
                "metrics": [{"label": "نرخ استخدام دانش آموختگان", "value": "۹۴.۲٪"}, {"label": "میانگین افزایش درآمد", "value": "+۱۴۰٪"}, {"label": "شرکت های همکار استخدامی", "value": "+۲۴۰"}]
            }
        }
    },
    "creative_portfolio_agency": {
        "domain_id": "creative_portfolio_agency",
        "theme_bias": "dark",
        "primary_styles": ["neobrutalism", "editorial_magazine", "minimal_swiss"],
        "section_flow": [
            {"id": "hero", "name": "Bold Creative Statement & Featured Reel", "type": "bold_statement_hero", "purpose": "High-confidence typographic hook with magnetic cursor attraction"},
            {"id": "signature", "name": "Case Study Interactive Filter & Gallery", "type": "signature_widget", "purpose": "Asymmetric bento project showcase with tactile hover reveals"},
            {"id": "services", "name": "Core Capabilities & Engineering Stack", "type": "capabilities_marquee", "purpose": "Brand Identity, Full-Stack Design Systems, 3D WebGL"},
            {"id": "awards", "name": "Design Honors & Recognition", "type": "award_ticker", "purpose": "Awwwards, FWA, Red Dot historical wins"},
            {"id": "cta", "name": "Direct Project Inquiries & Pitch Deck", "type": "bold_contact_footer", "purpose": "High-energy conversation starter"}
        ],
        "signature_widget": {
            "name": "Magnetic Bento Project Showcase with Hover Reveal",
            "type": "magnetic_bento_gallery",
            "props": {
                "cursor_magnetic_effect": True,
                "project_tags": ["Design Systems", "Web3 HUD", "Fintech Mobile", "Editorial"],
                "aspect_ratio_matrix": ["span-2", "span-1", "span-1", "span-2"]
            }
        },
        "layout_flavors": [
            {"flavor_id": "brutalist_mono_dark", "name": "High-Contrast Neobrutalism", "hero_layout": "bold_editorial_typography", "card_style": "hard_offset_shadow_card"},
            {"flavor_id": "swiss_minimal_dark", "name": "Swiss High-Contrast Portfolio", "hero_layout": "asymmetric_monochrome", "card_style": "hairline_grid_card"},
            {"flavor_id": "luxury_creative_atelier", "name": "Dark Luxury Atelier", "hero_layout": "cinematic_staggered", "card_style": "frost_glass_atelier"}
        ],
        "ambient_motion": {
            "type": "spotlight_cursor_bold",
            "bg_gradient": "radial-gradient(circle at center, oklch(0.18 0.02 280) 0%, oklch(0.10 0.005 280) 100%)",
            "motion_hint": "tactile cursor spring physics with crisp responsive hover offsets",
            "lcp_safe": True
        },
        "mock_data": {
            "en": {
                "headline": "Engineering Brand Chemistry & High-Conversion Digital Flags",
                "subheadline": "We partner with visionary founders to build category-defining interfaces that convert attention into enterprise value.",
                "cta_primary": "Initiate New Project",
                "cta_secondary": "Explore Selected Works",
                "metrics": [{"label": "Client Valuation Created", "value": "$1.2B+"}, {"label": "International Design Awards", "value": "34"}, {"label": "Average Conversion Lift", "value": "+42%"}]
            },
            "fa": {
                "headline": "خلق تجربه های دیجیتال پیشرو و دیزاین سیستم های مقیاس پذیر",
                "subheadline": "همکاری با برترین برندها برای طراحی محصولاتی که توجه کاربر را به ارزش پایدار تجاری تبدیل می کند.",
                "cta_primary": "شروع همکاری در پروژه",
                "cta_secondary": "مشاهده نمونه کارهای منتخب",
                "metrics": [{"label": "ارزش آفرینی برای مشتریان", "value": "+$۱.۲B"}, {"label": "جوایز بین المللی طراحی", "value": "۳۴"}, {"label": "میانگین رشد نرخ تبدیل", "value": "+۴۲٪"}]
            }
        }
    }
}

# Add handcrafted, authentic architectural blueprints for remaining 13 domains (zero bento-slop)
DOMAIN_SPECIFIC_BLUEPRINTS = {
    "ecommerce_luxury_fashion": {
        "theme_bias": "light",
        "primary_styles": ["quiet_luxury", "editorial_magazine"],
        "name": "Luxury Fashion & Haute Couture",
        "feature_type": "curated_lookbook_stream",
        "feature_name": "Seasonal Runway Lookbook & Editorial Curation",
        "feature_purpose": "High-fashion narrative flow with ample whitespace and tactile garment closeups",
        "flavor_2": ("editorial_lookbook", "Editorial Lookbook", "lookbook_spread", "borderless_canvas"),
        "flavor_3": ("minimal_atelier", "Minimal Atelier", "centered_curated", "hairline_linen_border"),
        "en": {
            "headline": "Timeless Silhouette, Artisanal Tailoring & Quiet Elegance",
            "subheadline": "Limited atelier collections handcrafted from certified organic silks and virgin wools.",
            "cta_primary": "Explore Autumn/Winter Lookbook",
            "cta_secondary": "Request Private Fitting",
            "metrics": [{"label": "Atelier Origin", "value": "Milan & Paris"}, {"label": "Crafting Hours / Piece", "value": "42h"}, {"label": "Certified Natural Fibers", "value": "100%"}]
        },
        "fa": {
            "headline": "شکوه سادگی، دوخت اصیل دست‌دوز و ظرافت ماندگار",
            "subheadline": "کالکشن‌های محدود فصلی بافته شده از ابریشم‌های خالص و پشم مرینوس ممتاز با هویت اختصاصی.",
            "cta_primary": "مشاهده لوک‌بوک پاییز و زمستان",
            "cta_secondary": "درخواست پرو و فیتینگ اختصاصی",
            "metrics": [{"label": "خاستگاه آتلیه", "value": "میلان و پاریس"}, {"label": "ساعت کار دست در هر لباس", "value": "۴۲ ساعت"}, {"label": "الیاف طبیعی شناسنامه‌دار", "value": "۱۰۰٪"}]
        }
    },
    "ecommerce_mass_market": {
        "theme_bias": "light",
        "primary_styles": ["clean_stripe", "playful_consumer"],
        "name": "High-Volume Consumer Commerce",
        "feature_type": "product_catalog_stream",
        "feature_name": "Instant Dynamic Category Grid & Quick Filter",
        "feature_purpose": "Fast-loading category browsing with 1-click variant preview and transparent pricing",
        "flavor_2": ("express_catalog", "Express Stream", "infinite_stream", "elevated_product_card"),
        "flavor_3": ("flash_deal_grid", "Flash Dynamic Grid", "segmented_flash", "contrast_badge_card"),
        "en": {
            "headline": "Everyday Essentials Delivered With Uncompromising Speed",
            "subheadline": "Over 20,000 verified products with same-day dispatch and zero-hassle 30-day returns.",
            "cta_primary": "Browse Trending Categories",
            "cta_secondary": "Check Local Delivery Times",
            "metrics": [{"label": "Dispatched Same-Day", "value": "98.7%"}, {"label": "Verified Reviews", "value": "240k+"}, {"label": "Average Delivery", "value": "2.4h"}]
        },
        "fa": {
            "headline": "کالاهای منتخب روزمره با ارسال فوق‌سریع و ضمانت اصالت",
            "subheadline": "بیش از ۲۰ هزار کالای بررسی‌شده با ارسال همان‌روز و ضمانت بی قید و شرط مرجوعی ۳۰ روزه.",
            "cta_primary": "مشاهده دسته‌بندی‌های پربازدید",
            "cta_secondary": "استعلام زمان تحویل در منطقه شما",
            "metrics": [{"label": "ارسال به موقع همان‌روز", "value": "۹۸.۷٪"}, {"label": "نظرات تایید شده خریداران", "value": "+۲۴۰ هزار"}, {"label": "میانگین زمان تحویل", "value": "۲.۴ ساعت"}]
        }
    },
    "media_editorial_magazine": {
        "theme_bias": "light",
        "primary_styles": ["editorial_magazine", "minimal_swiss"],
        "name": "Journalism, Cultural Essays & Magazine",
        "feature_type": "editorial_column_spread",
        "feature_name": "Three-Column Journalistic Layout & Deep-Dive Essays",
        "feature_purpose": "Rich typographic hierarchy, multi-column editorial cadence and pull quotes",
        "flavor_2": ("broadsheet_split", "Broadsheet Layout", "asymmetric_columns", "print_hairline_frame"),
        "flavor_3": ("essay_stream", "Longform Stream", "single_column_essay", "minimal_serif_canvas"),
        "en": {
            "headline": "In-Depth Investigation, Cultural Essays & Critical Thought",
            "subheadline": "Independent long-form journalism unconstrained by newsfeed algorithms or sponsored bias.",
            "cta_primary": "Read Today's Lead Story",
            "cta_secondary": "Explore The Complete Archive",
            "metrics": [{"label": "Print & Digital Readers", "value": "180k"}, {"label": "Investigative Awards", "value": "14"}, {"label": "Independent Columnists", "value": "35"}]
        },
        "fa": {
            "headline": "روزنامه‌نگاری تحقیقی، جستارهای فرهنگی و تحلیل بی‌پروا",
            "subheadline": "روایت‌های عمیق تحلیلی به دور از هیاهوی الگوریتم‌های شبکه‌های اجتماعی و آگهی‌های اسپانسری.",
            "cta_primary": "مطالعه پرونده ویژه امروز",
            "cta_secondary": "مرور آرشیو مقالات تحلیلی",
            "metrics": [{"label": "خوانندگان ماهانه نسخه چاپی و آنلاین", "value": "+۱۸۰ هزار"}, {"label": "جوایز مستقل روزنامه‌نگاری", "value": "۱۴"}, {"label": "نویسندگان و تحلیل‌گران", "value": "۳۵"}]
        }
    },
    "travel_hospitality_tourism": {
        "theme_bias": "light",
        "primary_styles": ["editorial_magazine", "quiet_luxury"],
        "name": "Boutique Hospitality & Expedition Booking",
        "feature_type": "destination_showcase_cards",
        "feature_name": "Panoramic Destination Cards & Expedition Itineraries",
        "feature_purpose": "Full-bleed landscape imagery, day-by-day expedition pacing, and lodge amenities",
        "flavor_2": ("panoramic_lodge", "Panoramic Expedition", "immersive_lodge_hero", "warm_sandstone_card"),
        "flavor_3": ("curated_safari", "Curated Journey", "itinerary_timeline_hero", "raw_canvas_card"),
        "en": {
            "headline": "Hand-Picked Wilderness Lodges & Private Expeditions",
            "subheadline": "Rare travel experiences designed by local naturalists and culinary artisans.",
            "cta_primary": "Explore 2026 Expeditions",
            "cta_secondary": "Request Private Itinerary",
            "metrics": [{"label": "Verified Sanctuary Lodges", "value": "48"}, {"label": "Naturalist Guide Ratio", "value": "1 : 4"}, {"label": "Zero Carbon Journeys", "value": "100%"}]
        },
        "fa": {
            "headline": "اقامتگاه‌های بوم‌گردی بکر و سفرهای اختصاصی طبیعت‌گردی",
            "subheadline": "تجربه‌های نادر گردشگری طراحی‌شده توسط راهنمایان بومی و کارشناسان حفاظت از تنوع زیستی.",
            "cta_primary": "مشاهده مقاصد و سفرهای سال",
            "cta_secondary": "درخواست تدوین برنامه اختصاصی",
            "metrics": [{"label": "اقامتگاه‌های تاییدشده اکولوژیک", "value": "۴۸"}, {"label": "نسبت لیدر بومی به مسافر", "value": "۱ به ۴"}, {"label": "سفرهای با ردپای کربن صفر", "value": "۱۰۰٪"}]
        }
    },
    "legal_compliance_law": {
        "theme_bias": "light",
        "primary_styles": ["minimal_swiss", "clean_stripe"],
        "name": "Corporate Law & Regulatory Compliance",
        "feature_type": "practice_areas_accordion",
        "feature_name": "Structured Practice Areas & Precedent Directory",
        "feature_purpose": "Dignified corporate structure, clear dispute jurisdiction breakdown, and partner bios",
        "flavor_2": ("monochrome_legal", "Swiss Legal Heritage", "dignified_split", "hairline_monochrome"),
        "flavor_3": ("regulatory_brief", "Regulatory Briefing", "dense_precedent_table", "slate_legal_frame"),
        "en": {
            "headline": "Cross-Border Corporate Governance, M&A & Regulatory Counsel",
            "subheadline": "Trusted senior counsel navigating complex multijurisdictional transactions and arbitration.",
            "cta_primary": "Consult Corporate Practice Lead",
            "cta_secondary": "Review Regulatory Insights",
            "metrics": [{"label": "Advising Experience", "value": "32 Years"}, {"label": "Completed M&A Transactions", "value": "$14.2B"}, {"label": "Senior Partners", "value": "26"}]
        },
        "fa": {
            "headline": "مشاوره حقوقی شرکتی، ادغام و تملک و حل‌وفصل دعاوی تجاری",
            "subheadline": "همراهی حقوقی وکلای باسابقه در معاملات پیچیده بین‌المللی، داوری و انطباق با مقررات مالی.",
            "cta_primary": "درخواست جلسه با شرکای ارشد",
            "cta_secondary": "مطالعه آخرین تحولات مقرراتی",
            "metrics": [{"label": "سابقه وکالت و داوری تخصصی", "value": "۳۲ سال"}, {"label": "حجم معاملات ادغام هدایت‌شده", "value": "+$۱۴.۲B"}, {"label": "وکلای پایه یک و شرکای ارشد", "value": "۲۶"}]
        }
    },
    "gaming_entertainment_streaming": {
        "theme_bias": "dark",
        "primary_styles": ["linear_dark", "modern_glass_2"],
        "name": "Next-Gen Gaming Guild & Streaming Hub",
        "feature_type": "interactive_media_deck",
        "feature_name": "Live Roster Broadcast, Match Ticker & Media Deck",
        "feature_purpose": "High-energy esports schedule, tournament brackets and zero-lag stream feed",
        "flavor_2": ("tournament_bracket", "Esports Tournament HUD", "bracket_arena", "neon_cyber_card"),
        "flavor_3": ("creator_lounge", "Creator Streaming Deck", "stream_feed_split", "charcoal_mesh_card"),
        "en": {
            "headline": "Real-Time Tournament Arena & Competitive Guild Network",
            "subheadline": "Watch 4K zero-lag tournament feeds, track real-time match stats, and participate in community scims.",
            "cta_primary": "Watch Live Broadcast",
            "cta_secondary": "View Bracket Schedule",
            "metrics": [{"label": "Broadcast FPS", "value": "120 FPS"}, {"label": "Active Competitive Guilds", "value": "1,400"}, {"label": "Global Servers", "value": "28"}]
        },
        "fa": {
            "headline": "آرنای مسابقات زنده، شبکه کلن‌های رقابتی و پخش گیمینگ",
            "subheadline": "تماشای زنده استریم‌های رقابتی با بالاترین کیفیت، پیگیری جدول مسابقات و چالش‌های درون‌جامعه‌ای.",
            "cta_primary": "ورود به پخش زنده تورنمنت",
            "cta_secondary": "مشاهده جدول رده‌بندی مسابقات",
            "metrics": [{"label": "نرخ فریم ریت پخش", "value": "۱۲۰ FPS"}, {"label": "تیم‌های رسمی فعال در تورنمنت", "value": "۱,۴۰۰"}, {"label": "سرورهای متمرکز منطقه‌ای", "value": "۲۸"}]
        }
    },
    "automotive_ev_mobility": {
        "theme_bias": "dark",
        "primary_styles": ["linear_dark", "clean_stripe"],
        "name": "EV Mobility & Autonomous Vehicle Fleet",
        "feature_type": "spec_comparison_grid",
        "feature_name": "Powertrain Specs, Aerodynamics & Interactive 360 Exterior",
        "feature_purpose": "Range simulator, dual-motor torque benchmarks, and charging speed timeline",
        "flavor_2": ("aerodynamic_fluid", "Aerodynamic Fluid Dark", "panoramic_ev_canvas", "sleek_obsidian_frame"),
        "flavor_3": ("engineering_telemetry", "Fleet Telemetry HUD", "dense_spec_matrix", "carbon_fiber_card"),
        "en": {
            "headline": "Aerodynamic Precision, 620-Mile Range & Intelligent Autonomy",
            "subheadline": "Dual-motor electric architecture engineered with solid-state cell thermal efficiency.",
            "cta_primary": "Configure Vehicle Spec",
            "cta_secondary": "Schedule Autonomous Drive",
            "metrics": [{"label": "0-60 MPH Acceleration", "value": "2.1s"}, {"label": "Certified Range (WLTP)", "value": "620 Mi"}, {"label": "Supercharging Rate", "value": "280kW"}]
        },
        "fa": {
            "headline": "مهندسی آیرودینامیک، برد ۱۰۰۰ کیلومتری و هدایت هوشمند",
            "subheadline": "معماری پیشرانه دو موتوره الکتریکی با مدیریت حرارتی باتری‌های نسل جدید حالت جامد.",
            "cta_primary": "شخصی‌سازی مشخصات فنی خودرو",
            "cta_secondary": "رزرو تست درایو هدایت خودکار",
            "metrics": [{"label": "شتاب صفر تا صد", "value": "۲.۱ ثانیه"}, {"label": "پیمایش تایید شده (WLTP)", "value": "۱۰۰۰ کیلومتر"}, {"label": "نرخ شارژ فوق‌سریع", "value": "۲۸۰ کیلووات"}]
        }
    },
    "logistics_supply_chain": {
        "theme_bias": "light",
        "primary_styles": ["clean_stripe", "minimal_swiss"],
        "name": "Global Freight & Predictive Logistics",
        "feature_type": "pipeline_flow_diagram",
        "feature_name": "Multi-Modal Freight Pipeline & Real-Time Tracking Flow",
        "feature_purpose": "Container tracking nodes, customs clearance timelines, and automated bill of lading",
        "flavor_2": ("freight_corridor", "Freight Corridor Map", "interactive_route_split", "hairline_logistics_card"),
        "flavor_3": ("customs_compliance", "Customs Matrix", "tabular_container_grid", "flat_data_card"),
        "en": {
            "headline": "Autonomous Freight Clearing, Route Optimization & Cold Chain",
            "subheadline": "Real-time vessel telematics and automated freight clearing across 420 international shipping ports.",
            "cta_primary": "Track Active Container",
            "cta_secondary": "Request Freight Quote",
            "metrics": [{"label": "Ports Monitored", "value": "420"}, {"label": "On-Time Arrival Rate", "value": "97.4%"}, {"label": "Customs Auto-Clearance", "value": "<4h"}]
        },
        "fa": {
            "headline": "ترخیص خودکار بار، بهینه‌سازی مسیرهای ترانزیت و زنجیره سرد",
            "subheadline": "پایش لحظه‌ای موقعیت کانتینرها و اسناد گمرکی در ۴۲۰ بندر و گذرگاه بین‌المللی حمل‌ونقل.",
            "cta_primary": "رهگیری برخط محموله",
            "cta_secondary": "استعلام نرخ ترانزیت و باربری",
            "metrics": [{"label": "بنادر بین‌المللی تحت پوشش", "value": "۴۲۰"}, {"label": "نرخ رسیدن به موقع محموله", "value": "۹۷.۴٪"}, {"label": "میانگین زمان ترخیص گمرکی", "value": "<۴ ساعت"}]
        }
    },
    "energy_greentech_sustainability": {
        "theme_bias": "light",
        "primary_styles": ["clean_stripe", "soft_humanist"],
        "name": "Clean Energy Grid & Carbon Accounting",
        "feature_type": "impact_metrics_matrix",
        "feature_name": "Decarbonization Calculator & Renewable Grid Flow",
        "feature_purpose": "Audited Scope 1-3 carbon tracking, renewable storage telemetry, and ESG reporting",
        "flavor_2": ("solar_grid_light", "Solar Clean Grid", "flow_grid_canvas", "leaf_green_subtle_frame"),
        "flavor_3": ("esg_audit", "ESG Audited Ledger", "metric_audit_cards", "recycled_sand_card"),
        "en": {
            "headline": "Verifiable Carbon Accounting & Distributed Renewable Microgrids",
            "subheadline": "Automated Scope 1-3 emissions accounting integrated directly with industrial energy telemetry.",
            "cta_primary": "Calculate Facility Footprint",
            "cta_secondary": "Download Audit Standards",
            "metrics": [{"label": "CO2 Reduction Verified", "value": "420,000t"}, {"label": "Renewable Storage Managed", "value": "2.4GWh"}, {"label": "Audit Standard", "value": "GHG Protocol"}]
        },
        "fa": {
            "headline": "محاسبه تاییدپذیر ردپای کربن و مدیریت ریزشبکه‌های انرژی تجدیدپذیر",
            "subheadline": "اندازه‌گیری انتشار گازهای گلخانه‌ای زنجیره تولید متصل به سنسورهای پایش بلادرنگ صنعتی.",
            "cta_primary": "محاسبه ردپای کربن مجموعه شما",
            "cta_secondary": "دریافت مستندات استانداردهای پایش",
            "metrics": [{"label": "کاهش کربن تایید شده", "value": "۴۲۰ هزار تن"}, {"label": "ذخیره‌سازی انرژی پاک تحت مدیریت", "value": "۲.۴ گیگاوات ساعت"}, {"label": "انطباق با پروتکل", "value": "GHG استاندارد"}]
        }
    },
    "nonprofit_charity_social": {
        "theme_bias": "light",
        "primary_styles": ["soft_humanist", "editorial_magazine"],
        "name": "Direct Social Impact & Philanthropy",
        "feature_type": "story_impact_timeline",
        "feature_name": "Field Impact Timeline, Community Stories & Fund Allocation",
        "feature_purpose": "Transparent ledger of donation deployment, village case studies, and volunteer hubs",
        "flavor_2": ("humanist_story", "Humanist Impact Story", "story_timeline_hero", "warm_terracotta_card"),
        "flavor_3": ("ledger_transparency", "Audited Ledger Transparency", "allocation_chart_split", "clean_paper_frame"),
        "en": {
            "headline": "Transparent Humanitarian Relief, Clean Water & Micro-Grants",
            "subheadline": "94 cents of every dollar deployed directly into vetted local community infrastructure projects.",
            "cta_primary": "Deploy Direct Donation",
            "cta_secondary": "View Live Spending Ledger",
            "metrics": [{"label": "Direct Project Allocation", "value": "94%"}, {"label": "Clean Water Wells Built", "value": "310"}, {"label": "Audited Fiscal Transparency", "value": "100%"}]
        },
        "fa": {
            "headline": "امدادرسانی شفاف، دسترسی به آب شرب پایدار و توانمندسازی محلی",
            "subheadline": "اختصاص مستقیم ۹۴ درصد از هر ریال اهدایی به زیرساخت‌های پایدار روستایی با گزارش مالی ماهانه.",
            "cta_primary": "مشارکت در طرح‌های جاری",
            "cta_secondary": "مشاهده دفتر کل گزارش هزینه‌کرد",
            "metrics": [{"label": "تخصیص مستقیم به پروژه‌ها", "value": "۹۴٪"}, {"label": "چاه و تصفیه‌خانه آب تکمیل شده", "value": "۳۱۰"}, {"label": "شفافیت مالی حسابرسی‌شده", "value": "۱۰۰٪"}]
        }
    },
    "personal_branding_creator": {
        "theme_bias": "dark",
        "primary_styles": ["neobrutalism", "linear_dark"],
        "name": "Creator Economy & Thought Leadership",
        "feature_type": "selected_works_gallery",
        "feature_name": "Selected Case Studies, Keynote Archive & Writing Shelf",
        "feature_purpose": "High-craft portfolio cards, longform essay teasers, and podcast episode embeds",
        "flavor_2": ("bold_creator_mono", "Bold Mono Creator", "typography_hero_mono", "hard_offset_shadow"),
        "flavor_3": ("editorial_author", "Author & Essayist", "essay_reading_room", "minimal_charcoal_border"),
        "en": {
            "headline": "Engineering Scalable Software, Systems Architecture & Thought",
            "subheadline": "Writing, keynotes, and open-source contributions read by over 40,000 systems architects.",
            "cta_primary": "Read Technical Essays",
            "cta_secondary": "View Conference Keynotes",
            "metrics": [{"label": "Newsletter Architects", "value": "42k"}, {"label": "Open Source Stars", "value": "18.4k"}, {"label": "Technical Keynotes", "value": "38"}]
        },
        "fa": {
            "headline": "معماری سیستم‌های نرم‌افزاری مقیاس‌پذیر، تفکر سیستمی و خلق محصول",
            "subheadline": "یادداشت‌های فنی، ارائه‌های کنفرانس و پروژه‌های متن‌باز برای مهندسان زیرساخت و معماری.",
            "cta_primary": "مطالعه جستارهای فنی",
            "cta_secondary": "مشاهده ارائه‌ها و سخنرانی‌ها",
            "metrics": [{"label": "خوانندگان خبرنامه تخصصی", "value": "+۴۲ هزار"}, {"label": "ستاره‌های پروژه‌های متن‌باز", "value": "+۱۸.۴ هزار"}, {"label": "ارائه‌های کنفرانس", "value": "۳۸"}]
        }
    },
    "cybersecurity_identity_auth": {
        "theme_bias": "dark",
        "primary_styles": ["linear_dark", "data_dense_terminal"],
        "name": "Zero-Trust Identity & Threat Intelligence",
        "feature_type": "threat_matrix_terminal",
        "feature_name": "Zero-Trust Policy Matrix & Real-Time Anomaly Telemetry",
        "feature_purpose": "SOC telemetry terminal, continuous credential rotation, and mutual TLS inspection",
        "flavor_2": ("dense_soc_terminal", "SOC Operational Terminal", "terminal_split_matrix", "dense_mono_border"),
        "flavor_3": ("zero_trust_radar", "Zero-Trust Radar", "radar_security_split", "obsidian_glass_frame"),
        "en": {
            "headline": "Continuous Zero-Trust Authorization & Automated Threat Quarantines",
            "subheadline": "Sub-5ms policy enforcement across Kubernetes clusters, API gateways, and employee devices.",
            "cta_primary": "Deploy Ingress Enforcer",
            "cta_secondary": "Inspect Policy Architecture",
            "metrics": [{"label": "Policy Decision Latency", "value": "<4.8ms"}, {"label": "Automated Threat Quarantines", "value": "100%"}, {"label": "Compliance Verification", "value": "SOC2 / ISO 27001"}]
        },
        "fa": {
            "headline": "احراز هویت پیوسته زیرو تراست و قرنطینه خودکار تهدیدات امنیتی",
            "subheadline": "اعمال قوانین دسترسی امن در کمتر از ۵ میلی‌ثانیه روی تمامی ورودی‌های API، کانتینرها و سشن‌های کاربری.",
            "cta_primary": "استقرار ماژول بازرسی امنیتی",
            "cta_secondary": "بررسی سند معماری انطباق",
            "metrics": [{"label": "تاخیر تصمیم‌گیری پالیسی امنیتی", "value": "<۴.۸ میلی‌ثانیه"}, {"label": "قرنطینه خودکار نقض سیاست‌ها", "value": "۱۰۰٪"}, {"label": "استاندارد بازرسی تایید شده", "value": "SOC2 / ISO 27001"}]
        }
    },
    "general_modern_saas": {
        "theme_bias": "light",
        "primary_styles": ["clean_stripe", "minimal_swiss"],
        "name": "Modern High-Velocity Software Platform",
        "feature_type": "feature_columns_dynamic",
        "feature_name": "Interactive Feature Tabs & Integrated Workspace Preview",
        "feature_purpose": "Tabbed exploration of core workflows with live UI previews and keyboard shortcuts",
        "flavor_2": ("stripe_light_saas", "Crisp Stripe Precision", "tabbed_workspace_hero", "subtle_white_card"),
        "flavor_3": ("swiss_mono_saas", "Swiss High-Density SaaS", "dense_metric_columns", "sharp_slate_frame"),
        "en": {
            "headline": "High-Velocity Workspace For Modern Product & Engineering Teams",
            "subheadline": "Eliminate fragmented tools, automate repetitive tasks, and ship software with clarity.",
            "cta_primary": "Start Free 14-Day Trial",
            "cta_secondary": "Explore Interactive Tour",
            "metrics": [{"label": "Sprint Velocity Increase", "value": "+34%"}, {"label": "Deployment Lead Time", "value": "18 Mins"}, {"label": "Team Adoption Rate", "value": "99.2%"}]
        },
        "fa": {
            "headline": "محیط کار یکپارچه برای تیم‌های پرسرعت توسعه محصول و مهندسی",
            "subheadline": "حذف ابزارهای پراکنده، خودکارسازی تسک‌های روزمره و افزایش هماهنگی اعضای تیم با شفافیت کامل.",
            "cta_primary": "شروع دوره رایگان ۱۴ روزه",
            "cta_secondary": "مشاهده تور تعاملی امکانات",
            "metrics": [{"label": "افزایش سرعت تحویل اسپرینت‌ها", "value": "+۳۴٪"}, {"label": "میانگین زمان استقرار", "value": "۱۸ دقیقه"}, {"label": "نرخ استقبال اعضای تیم", "value": "۹۹.۲٪"}]
        }
    }
}

for d_id, data in DOMAIN_SPECIFIC_BLUEPRINTS.items():
    theme_b = data["theme_bias"]
    styles = data["primary_styles"]
    name = data["name"]
    feat_type = data["feature_type"]
    feat_name = data["feature_name"]
    feat_purp = data["feature_purpose"]
    fl_2 = data["flavor_2"]
    fl_3 = data["flavor_3"]

    BLUEPRINTS[d_id] = {
        "domain_id": d_id,
        "theme_bias": theme_b,
        "primary_styles": styles,
        "section_flow": [
            {"id": "hero", "name": f"{name} Hero Section", "type": "split_hero", "purpose": "Clear value hook and primary conversion action"},
            {"id": "signature", "name": f"Interactive {name} Core Engine", "type": "signature_widget", "purpose": "Engaging interactive widget demonstrating core value"},
            {"id": "features", "name": feat_name, "type": feat_type, "purpose": feat_purp},
            {"id": "proof", "name": "Audited Results & Testimonials", "type": "proof_cards", "purpose": "High-trust evidence and social validation"},
            {"id": "footer", "name": "Complete Navigation & Legal Hub", "type": "standard_footer", "purpose": "Zero-friction secondary discovery"}
        ],
        "signature_widget": {
            "name": f"Interactive {name} Showcase",
            "type": "interactive_tabs_widget",
            "props": {"interactive": True, "domain": d_id}
        },
        "layout_flavors": [
            {"flavor_id": f"{d_id}_clean", "name": f"Clean {name}", "hero_layout": "split_hero", "card_style": "subtle_card"},
            {"flavor_id": f"{d_id}_{fl_2[0]}", "name": fl_2[1], "hero_layout": fl_2[2], "card_style": fl_2[3]},
            {"flavor_id": f"{d_id}_{fl_3[0]}", "name": fl_3[1], "hero_layout": fl_3[2], "card_style": fl_3[3]}
        ],
        "ambient_motion": {
            "type": "subtle_gradient_wash",
            "bg_gradient": "linear-gradient(180deg, oklch(0.98 0.005 240) 0%, oklch(0.94 0.01 240) 100%)" if theme_b == "light" else "linear-gradient(180deg, oklch(0.16 0.01 240) 0%, oklch(0.10 0.005 240) 100%)",
            "motion_hint": "subtle stagger and zero-lag CSS transitions",
            "lcp_safe": True
        },
        "mock_data": {
            "en": data["en"],
            "fa": data["fa"]
        }
    }

output_path = Path("data/domain_blueprints.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump({
        "version": "3.3.0",
        "description": "Architectural blueprints for 24 domains: bespoke section flows, domain-authentic signature widgets, layout flavors, and human mock data.",
        "domains": BLUEPRINTS
    }, f, indent=2, ensure_ascii=False)

print(f"Successfully generated {output_path} with {len(BLUEPRINTS)} domain blueprints.")
