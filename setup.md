# my_system setup

This file is primarily for agents. If you're doing manual setup — do your best robot impression.

## Setup procedure

1. **Choose a deploy location** — ask where the user wants `my_system.md` and `my_places.md` to live (default: `~/.local/share/my_system/`). Copy both files there.

2. **Grill the user** about their filesystem layout. All of these are mandatory — do not proceed without answers:
   - What are their main domains? At minimum: INGRESS, WORK, PROJECTS. Common extras: Knowledge, Media, Documents.
   - What absolute paths map to each domain?
   - Where do **captures** land? (medium-term deferrals — significant items without a clear home yet)
   - Where does the **ingress archive** go? (fully processed daily logs, bucketed by quarter. Default: `{ingress}/_archive/`)
   - Any hot paths — high-frequency files or folders the agent should know about?

3. **Fill in `my_places.md`** in the deploy location using their answers.

4. **Create domain folders** that don't already exist.

5. **Deploy ingress agentic instructions** — copy `ingress-agents.md` to the user's INGRESS directory in a way that gets it picked up as context for any agent session launched there. The exact mechanism depends on the harness (e.g. `AGENTS.md`, `.cursorrules`, a sidecar config). If you're unsure, ask the user how their agent harness discovers per-folder instructions.

6. **Install tools**:
   - Symlink CLI tools to PATH: `ln -sf "$(pwd)/_tools/"* ~/.local/bin/`
   - If your harness supports skills or tool registration, prompt the user to also install the tools via that mechanism. See `_tools/Readme.md`.

7. **Configure agent prompt**: If you can modify the system prompt for future sessions, do so — use the prompt block below, with all `{path/to/...}` placeholders filled in. If you cannot, output the block for the user to paste into their agent harness manually.

   > **Prompt block:**
   >
   > ## Digital Life Layout (System Map)
   > If user wants something that touches their files or projects, or asks/instructs something that refers to:
   > - work
   > - ingress
   > - projects
   > - {your terms/locations of interest / trigger words}
   >
   > You MUST read file at `{path/to/my_system.md}` - it outlines conventions for operating within this computer's folders and files organizational structure.
   > For locations, read file at `{path/to/my_places.md}`
   >
   > ### Work Handling Rule
   > When creating or updating work tracking, tasks, plans, or todo notes:
   > - **Project Context**: If in the context of a project (either directly via CWD or active discussion topic), ALWAYS place work files locally inside that project's folder (e.g., `<project>/work/<task>.md` or `<project>/work.md`).
   > - **Dynamic Work Aggregate**: The WORK domain is mostly compiled dynamically / mirrored from active project work folders. Do NOT default to placing project work files exclusively there - put them in the local project workspace first.

8. **Bootstrap projects**: Go into PROJECTS. Pick 3 projects at random. Show the user the names and ask them to describe each one briefly. Create a `card.md` for each using their descriptions.

9. **Generate projects index**: Run `regenerate_index.py` on the PROJECTS directory to produce `index.md`.

10. **Run work regenerator**: Run `regenerate_work.py` to populate WORK with symlinks to all active project task files.

11. **Create today's daily note** in INGRESS (`YYYY-MM-DD.md`) with two seed entries:
    - System installed successfully.
    - Remaining projects in PROJECTS still need `card.md` files — agent and user should work through them in a future session.

12. **Invite the user** to open a new session pointed at their INGRESS to kick off their first processing run.
