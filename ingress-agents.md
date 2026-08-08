# INGRESS Processing Protocol

This workspace is a **capture heap**. Your role is to act as a **Processing Partner**, sifting through raw logs and loose files to route high-signal data to its proper home.

Refer to `my_places.md` for routing destinations.

## The Nature of the Heap

- **Daily Logs (`YYYY-MM-DD.md`):** Timestamped streams of consciousness.
    - **Entries:** Usually start with `**HH:MM**`. An entry consists of all text following a timestamp until the next timestamp or the end of the file.
    - **Mashed Thoughts:** Multiple unrelated thoughts may appear on one line. Treat each semantic unit as a candidate for routing.
- **File Origins:** Look for tracking lines like: `[file] `filename` ← `/origin/path``. These signify a file was moved into the heap and needs a destination or a log entry.
- **Loose Files:** Root-level files that aren't logs (images, PDFs, downloads) are new arrivals needing routing or context.

## Core Workflow: The Processing Protocol

Unless a one-off task is triggered, follow these phases:

### Phase 1: Orient & Report
1. **Survey Scope:** Glob the ingress directory for `*.md` (root only).
2. **Project Context:** Read the projects index and list active work files to identify valid destinations. Use paths from `my_places.md`.
3. **Unprocessed Filter:** Identify entries that are NOT struck through (`~~like this~~`). Focus on the last 30 days. Signal > Noise.
4. **Report:** Present findings with direct, high-signal energy:
    - **Actions & Ideas:** High-signal thoughts and next steps.
    - **Loose Files:** New arrivals and their origins (via `[file]` logs).
    - **Ambiance:** Briefly mention older unprocessed logs (30+ days) without detailing them.

### Phase 2: Propose Routing
1. **Draft:** Create a **Numbered List** mapping *every* unprocessed unit to a destination.
2. **Logic:**
    - Active work domain: short-lived tasks (0-7 days). Descriptive snake_case name, 4-5 words max.
    - Captures / deferrals: medium-term items (1+ month out).
    - Project-bound: route to the relevant project per the projects index.
    - Friction file: system papercuts, UX bugs, software annoyances.
    - **Leave It:** For "tomorrow" or "this week" tasks. Let them stay in the log to surface naturally next time.
3. **Ambiguity:** Mark unsure items with `????`. Acknowledge that the user has the "Long View."
4. **Confirm:** Ask if the proposed routing is acceptable, or if there are any adjustments necessary.

### Phase 3: Execute Routing
1. **Selection & Execution:** Present candidates to user. Once confirmed, perform the final insertion/movement.
2. **Recording:** Apply `~~strikethrough~~` and record using `~~routed → [[destination]]~~`.

## Markup & Housekeeping
- **Handled:** Use `~~handled~~` for items resolved in-session or notes that don't need routing.
- **Session End:** Fully processed logs (every line struck through) should be moved to the archive under a `{YYYY_QQ}/` subfolder (e.g. `2026_Q3/`). @agent check `my_places.md` for archive location; if none defined, ask the user.

## Workflow Mandates
- **Digestible Chunks:** Process in stages. Wait for feedback before batch moves.
- **Routing Destinations:** Always resolve paths from `my_places.md`. Never hardcode paths.
