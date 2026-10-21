/**
 * Vibe UI Model Context Protocol (MCP) Server
 * Standard JSON-RPC 2.0 stdio server providing AI coding agents (Claude Code, Cursor,
 * Windsurf, Antigravity) with direct access to design tokens, section blocks,
 * and real-time code auditing.
 * Zero external dependencies.
 */

import * as readline from 'readline';
import { COMPONENT_REGISTRY } from './registry/components';
import { auditCode } from './audit';
import { VISUAL_CHEMISTRIES } from './index';

interface JsonRpcRequest {
  jsonrpc: '2.0';
  id?: string | number | null;
  method: string;
  params?: any;
}

interface JsonRpcResponse {
  jsonrpc: '2.0';
  id: string | number | null;
  result?: any;
  error?: {
    code: number;
    message: string;
    data?: any;
  };
}

const SERVER_NAME = 'vibe-ui-mcp';
const SERVER_VERSION = '6.4.1';

// Standard 11 visual paradigms data
const PARADIGM_SPECS: Record<string, { description: string; mood: string; bestFor: string; oklchTokens: Record<string, string> }> = {
  'claymorphism': {
    description: 'Soft 3D pillowy surfaces with multi-layered specular drop shadows and rounded organic aesthetics',
    mood: 'Playful, tactile, premium consumer, accessible',
    bestFor: 'Mobile wallets, creative studios, consumer apps, health & wellness',
    oklchTokens: {
      '--vibe-canvas': 'oklch(0.97 0.015 250)',
      '--vibe-surface': 'oklch(0.99 0.01 250)',
      '--vibe-primary': 'oklch(0.62 0.22 265)',
      '--vibe-shadow-clay': '16px 16px 32px oklch(0.85 0.04 250 / 0.5), inset -8px -8px 16px oklch(0.99 0.01 250 / 0.8), inset 8px 8px 16px oklch(0.85 0.04 250 / 0.3)',
      '--card-radius': '2rem',
    },
  },
  'apple-glass': {
    description: 'Sub-pixel optical glass with backdrop-filter blur, thin luminous borders, and fluid lighting',
    mood: 'High-end, refined, architectural, Cupertino luxury',
    bestFor: 'SaaS dashboards, creative portfolios, modern financial platforms',
    oklchTokens: {
      '--vibe-canvas': 'oklch(0.98 0.005 240)',
      '--vibe-surface': 'oklch(0.96 0.01 240 / 0.65)',
      '--vibe-border': 'oklch(0.90 0.01 240 / 0.40)',
      '--vibe-primary': 'oklch(0.55 0.24 260)',
      '--card-radius': '1.25rem',
    },
  },
  'clean-stripe': {
    description: 'Crisp, razor-sharp typography, pure white backgrounds, subtle 1px border lines, and high-trust layout',
    mood: 'Enterprise trust, developer-first, clear, institutional',
    bestFor: 'Fintech, API documentation, B2B SaaS, medical clinics',
    oklchTokens: {
      '--vibe-canvas': 'oklch(0.99 0.002 240)',
      '--vibe-surface': 'oklch(1.0 0 0)',
      '--vibe-border': 'oklch(0.92 0.005 240)',
      '--vibe-primary': 'oklch(0.58 0.22 265)',
      '--card-radius': '0.5rem',
    },
  },
  'neubrutalism': {
    description: 'Bold black outlines (2-3px), hard geometric drop shadows without blur, high saturation accents',
    mood: 'Energetic, unpretentious, expressive, punchy',
    bestFor: 'Creator tools, education, marketing campaigns, modern dev tools',
    oklchTokens: {
      '--vibe-canvas': 'oklch(0.96 0.02 90)',
      '--vibe-surface': 'oklch(0.99 0.01 90)',
      '--vibe-border': 'oklch(0.15 0.01 0)',
      '--vibe-primary': 'oklch(0.68 0.24 140)',
      '--vibe-shadow-brutal': '4px 4px 0px oklch(0.15 0.01 0)',
      '--card-radius': '0.375rem',
    },
  },
  'bento-grid': {
    description: 'Asymmetric multi-column modular grid cards with live telemetry sparklines, HUD chips, and spatial rhythm',
    mood: 'Information-dense, cutting-edge, organized, interactive',
    bestFor: 'Product feature overviews, hardware specs, SaaS landing hero viewports',
    oklchTokens: {
      '--vibe-canvas': 'oklch(0.98 0.005 260)',
      '--vibe-surface': 'oklch(0.96 0.01 260)',
      '--vibe-primary': 'oklch(0.58 0.24 270)',
      '--card-radius': '1.5rem',
    },
  },
};

const MCP_TOOLS = [
  {
    name: 'vibe_get_palette',
    description: 'Retrieve calibrated OKLCH color palettes, contrast tokens, and Tailwind v4 themes for a design domain or mood.',
    inputSchema: {
      type: 'object',
      properties: {
        domain: {
          type: 'string',
          description: 'Target website domain (e.g., healthcare, fintech, creative, devops, luxury, restaurant)',
        },
        paradigm: {
          type: 'string',
          description: 'Visual paradigm (e.g., claymorphism, apple-glass, clean-stripe, neubrutalism, bento-grid)',
        },
      },
    },
  },
  {
    name: 'vibe_list_components',
    description: 'List all production-ready AI UI primitives and full section blocks available in Vibe UI Suite.',
    inputSchema: {
      type: 'object',
      properties: {
        category: {
          type: 'string',
          enum: ['all', 'ai-contracts', 'living-micro-interactions', 'section-blocks'],
          description: 'Filter components by category (default: all)',
        },
      },
    },
  },
  {
    name: 'vibe_get_component',
    description: 'Get the full React TSX source code for a specific Vibe UI primitive or section block.',
    inputSchema: {
      type: 'object',
      properties: {
        name: {
          type: 'string',
          description: 'Exact component or block name (e.g., bento-hero, pricing-matrix, glass-navbar, shimmer-button, device-mockup)',
        },
      },
      required: ['name'],
    },
  },
  {
    name: 'vibe_audit_code',
    description: 'Audit an HTML or React TSX code snippet for WCAG AA contrast, mobile overflow risks, raw unicode emojis, missing semantics, and BiDi RTL isolation.',
    inputSchema: {
      type: 'object',
      properties: {
        code: {
          type: 'string',
          description: 'The HTML or React TSX code content to audit',
        },
        filename: {
          type: 'string',
          description: 'Optional file path or name for reference (e.g., App.tsx)',
        },
      },
      required: ['code'],
    },
  },
  {
    name: 'vibe_expand_intent',
    description: 'Expand a sparse or lazy prompt (e.g. "dental clinic landing page") into a comprehensive architectural UI spec (optimal paradigm, color tokens, layout archetypes, micro-interactions).',
    inputSchema: {
      type: 'object',
      properties: {
        prompt: {
          type: 'string',
          description: 'The user or task prompt describing what to design',
        },
      },
      required: ['prompt'],
    },
  },
];

function handleToolCall(name: string, args: any): any {
  switch (name) {
    case 'vibe_get_palette': {
      const paradigmKey = (args.paradigm || '').toLowerCase().trim();
      const spec = PARADIGM_SPECS[paradigmKey] || PARADIGM_SPECS['clean-stripe'];
      return {
        selectedParadigm: paradigmKey in PARADIGM_SPECS ? paradigmKey : 'clean-stripe',
        mood: spec.mood,
        description: spec.description,
        bestFor: spec.bestFor,
        tokens: spec.oklchTokens,
        tailwindConfig: {
          lightFirst: true,
          contrastRatio: '>= 4.5:1 (WCAG AA)',
          cssVariables: spec.oklchTokens,
        },
      };
    }

    case 'vibe_list_components': {
      const category = args.category || 'all';
      const items = Object.entries(COMPONENT_REGISTRY)
        .filter(([_, comp]) => category === 'all' || comp.category === category)
        .map(([key, comp]) => ({
          name: key,
          filename: comp.filename,
          category: comp.category,
          description: comp.description,
        }));
      return { total: items.length, components: items };
    }

    case 'vibe_get_component': {
      const compName = (args.name || '').toLowerCase().trim();
      const found = COMPONENT_REGISTRY[compName];
      if (!found) {
        const available = Object.keys(COMPONENT_REGISTRY).join(', ');
        throw new Error(`Component "${compName}" not found. Available components: ${available}`);
      }
      return {
        name: found.name,
        filename: found.filename,
        category: found.category,
        description: found.description,
        code: found.code,
      };
    }

    case 'vibe_audit_code': {
      const code = args.code || '';
      const filename = args.filename || '<inline-code>';
      const result = auditCode(code, filename);
      return {
        pass: result.pass,
        score: result.score,
        summary: result.pass
          ? `PASS: High quality UI (Score: ${result.score}/100, ${result.counts.warn} warnings)`
          : `FAIL: Found ${result.counts.fail} critical violations (Score: ${result.score}/100)`,
        counts: result.counts,
        findings: result.findings,
      };
    }

    case 'vibe_expand_intent': {
      const prompt = (args.prompt || '').toLowerCase();
      let recommendedParadigm = 'clean-stripe';
      let layoutArchetype = 'classic_structured_saas';
      let suggestedSections = ['glass-navbar', 'bento-hero', 'feature-grid', 'pricing-matrix', 'faq-accordion', 'conversion-cta'];

      if (/dental|clinic|doctor|medical|health|hospital|care/.test(prompt)) {
        recommendedParadigm = 'clean-stripe';
        layoutArchetype = 'dense_telemetry_hud_or_clinical';
        suggestedSections = ['glass-navbar', 'bento-hero', 'feature-grid', 'pricing-matrix', 'faq-accordion', 'conversion-cta'];
      } else if (/crypto|web3|defi|vault|yield|fintech/.test(prompt)) {
        recommendedParadigm = 'claymorphism';
        layoutArchetype = 'dense_telemetry_hud';
      } else if (/luxury|fashion|editorial|architecture|haute/.test(prompt)) {
        recommendedParadigm = 'apple-glass';
        layoutArchetype = 'editorial_asymmetric_spread';
      } else if (/creator|gaming|play|fun|social/.test(prompt)) {
        recommendedParadigm = 'neubrutalism';
        layoutArchetype = 'creative_canvas_showcase';
      }

      const spec = PARADIGM_SPECS[recommendedParadigm] || PARADIGM_SPECS['clean-stripe'];

      return {
        originalPrompt: args.prompt,
        architecturalBlueprint: {
          recommendedParadigm,
          mood: spec.mood,
          layoutArchetype,
          contrastPolicy: 'Light-First default with dark mode toggle switch',
          suggestedSections,
          tokens: spec.oklchTokens,
          antiSlopMandates: [
            'Zero raw unicode emojis (use inline SVG icons)',
            'Strict WCAG AA contrast (>= 4.5:1)',
            'Responsive mobile drawer (0 invisible navigation)',
            'No hardcoded fixed widths causing horizontal scroll',
          ],
        },
      };
    }

    default:
      throw new Error(`Unknown tool: ${name}`);
  }
}

export function startMcpServer() {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    terminal: false,
  });

  function sendResponse(response: JsonRpcResponse) {
    process.stdout.write(JSON.stringify(response) + '\n');
  }

  rl.on('line', (line) => {
    const trimmed = line.trim();
    if (!trimmed) return;

    let request: JsonRpcRequest;
    try {
      request = JSON.parse(trimmed);
    } catch (e: any) {
      sendResponse({
        jsonrpc: '2.0',
        id: null,
        error: { code: -32700, message: 'Parse error: invalid JSON' },
      });
      return;
    }

    const { id, method, params } = request;

    // MCP JSON-RPC Method Dispatch
    switch (method) {
      case 'initialize': {
        sendResponse({
          jsonrpc: '2.0',
          id: id ?? null,
          result: {
            protocolVersion: '2024-11-05',
            serverInfo: {
              name: SERVER_NAME,
              version: SERVER_VERSION,
            },
            capabilities: {
              tools: {},
            },
          },
        });
        break;
      }

      case 'notifications/initialized': {
        // No response needed for notification
        break;
      }

      case 'tools/list': {
        sendResponse({
          jsonrpc: '2.0',
          id: id ?? null,
          result: {
            tools: MCP_TOOLS,
          },
        });
        break;
      }

      case 'tools/call': {
        const toolName = params?.name;
        const toolArgs = params?.arguments || {};
        try {
          const result = handleToolCall(toolName, toolArgs);
          sendResponse({
            jsonrpc: '2.0',
            id: id ?? null,
            result: {
              content: [
                {
                  type: 'text',
                  text: typeof result === 'string' ? result : JSON.stringify(result, null, 2),
                },
              ],
            },
          });
        } catch (err: any) {
          sendResponse({
            jsonrpc: '2.0',
            id: id ?? null,
            result: {
              isError: true,
              content: [
                {
                  type: 'text',
                  text: `Error executing tool "${toolName}": ${err.message}`,
                },
              ],
            },
          });
        }
        break;
      }

      case 'ping': {
        sendResponse({
          jsonrpc: '2.0',
          id: id ?? null,
          result: {},
        });
        break;
      }

      default: {
        if (id !== undefined) {
          sendResponse({
            jsonrpc: '2.0',
            id: id ?? null,
            error: {
              code: -32601,
              message: `Method not found: ${method}`,
            },
          });
        }
        break;
      }
    }
  });

  process.stderr.write(`[vibe-ui-mcp] Server v${SERVER_VERSION} listening on stdio (JSON-RPC 2.0)...\n`);
}
