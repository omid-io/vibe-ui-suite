# Harness-Native Browser Evidence

## Ownership boundary

Vibe UI Suite owns design decisions, static inspection, evidence contracts and acceptance rules. The active AI harness owns browser discovery, browser selection, navigation, rendering, interaction and screenshot capture.

The package MUST NOT install, download, launch, attach to, or control a browser or browser automation driver. This keeps the suite independent of browser brand, OS, runtime and harness-specific automation APIs.

The same integration applies whether a host exposes a graphical browser, a remote browser, a built-in browser tool, or no browser at all. When no browser is available, the suite completes its static work and reports runtime verification as `NOT_EVALUATED`.

## Execution protocol

1. Run the design swarm. It writes `.vibe/browser-evidence-request.json` beside the consumer workspace and reports the exact artifact path and SHA-256.
2. Read the request manifest. Use only the browser capability already available in the current harness. Do not invoke an assumed browser MCP, browser brand, local executable or driver.
3. Render the final artifact in its real host environment. For a framework component, use the project's normal runtime rather than a synthetic package-owned browser harness.
4. Inspect the complete page at mobile (390px), tablet (768px), and desktop (1440px). Measure horizontal overflow and visible geometry; check broken images and page/console errors; test real controls, keyboard traversal, menus, forms, dialogs, Escape dismissal and reduced-motion behavior where applicable.
5. Ask a vision-capable reviewer to inspect all supplied screenshots for hierarchy, spacing, typography, clipping, image quality, responsive composition and domain fit.
6. Save a `vibe.browser-evidence/v1` JSON report at `.vibe/browser-evidence.json`. The report must identify the final artifact by SHA-256. For React/TSX output, pass the same `--format tsx` option on the verify-existing invocation.
7. Validate the report before claiming acceptance:

```bash
npx vibe-ui-suite swarm "Build a polished product interface" --output swarm_output.html --verify-existing --browser-evidence .vibe/browser-evidence.json --json
```

Any edit after browser inspection changes the artifact hash and invalidates the prior report. Regenerate evidence after the last source change.

## Report shape

The full machine contract is `schemas/browser-evidence.v1.schema.json`. Its required fields are:

- `schema_version`: exactly `vibe.browser-evidence/v1`.
- `artifact.sha256`: SHA-256 of the exact final file.
- `runtime`: `harness`, `browser`, `browser_version` and `platform`.
- `captured_at`: ISO-8601 timestamp.
- `viewports`: measured mobile, tablet and desktop results, screenshots/attachments, overflow, broken images and console errors.
- `checks`: explicit statuses for responsive layout, runtime errors, accessibility, interaction smoke tests and visual review.
- `visual_review`: reviewer identity, inspected viewport set, summary, score (optional) and findings.

Example (paths are relative to the report unless absolute):

```json
{
  "schema_version": "vibe.browser-evidence/v1",
  "artifact": {
    "path": "swarm_output.html",
    "sha256": "<64-character SHA-256>"
  },
  "runtime": {
    "harness": "active-ai-harness",
    "browser": "browser-provided-by-harness",
    "browser_version": "reported-version",
    "platform": "reported-platform"
  },
  "captured_at": "2026-11-09T17:00:00Z",
  "overall_status": "PASS",
  "viewports": [
    {
      "name": "mobile",
      "width": 390,
      "height": 844,
      "horizontal_overflow": false,
      "broken_images": 0,
      "console_errors": [],
      "screenshot": { "path": "screenshots/mobile.png" }
    },
    {
      "name": "tablet",
      "width": 768,
      "height": 1024,
      "horizontal_overflow": false,
      "broken_images": 0,
      "console_errors": [],
      "screenshot": { "path": "screenshots/tablet.png" }
    },
    {
      "name": "desktop",
      "width": 1440,
      "height": 900,
      "horizontal_overflow": false,
      "broken_images": 0,
      "console_errors": [],
      "screenshot": { "path": "screenshots/desktop.png" }
    }
  ],
  "checks": [
    { "id": "responsive_layout", "status": "PASS", "summary": "No overflow at required viewport profiles" },
    { "id": "runtime_errors", "status": "PASS", "summary": "No uncaught page or console errors" },
    { "id": "accessibility", "status": "PASS", "summary": "Keyboard and accessible-name checks passed" },
    { "id": "interaction_smoke", "status": "PASS", "summary": "Required interactive controls were exercised" },
    { "id": "visual_review", "status": "PASS", "summary": "The screenshots were inspected by a vision-capable reviewer" }
  ],
  "visual_review": {
    "status": "PASS",
    "reviewer": "vision-capable-reviewer",
    "summary": "Responsive composition and hierarchy are consistent across the inspected viewports",
    "inspected_screenshots": ["mobile", "tablet", "desktop"],
    "findings": [],
    "score": 94
  }
}
```

A harness may supply screenshots as local paths, URIs or attachment IDs. Local screenshots can include SHA-256 and byte size. Attachments remain owned by the host; Vibe UI validates the reference and report metadata but does not download them or require a specific capture API.

## Acceptance semantics

| Condition | Outcome |
|---|---|
| No browser capability or no report | `NOT_EVALUATED` / `ACCEPTABLE_WITH_NOTES` |
| Report has wrong schema, missing required viewports/checks, invalid screenshot reference or stale artifact SHA | `NOT_EVALUATED` |
| Valid report with failed overflow, broken media, runtime, accessibility, interaction or visual gates | `FAIL` |
| Valid report, all required checks PASS, and visual reviewer PASS | Browser evidence PASS; the complete swarm may accept only if static/WCAG/critic gates also pass |

The report is an evidence contract, not an instruction to trust the harness blindly. It prevents stale or structurally incomplete evidence from being treated as a successful verification run. Review findings and screenshots remain inspectable by the host agent.
