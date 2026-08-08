## Core concepts

[[domain]]: a container for things large enough to need containing. Within a domain you find kindred entities - either by structure, kind, or purpose. Smallest a domain can be is "a folder with files".

[[ingress]]: single entry point into the system. Raw thoughts, daily logs, voice memos, loose files — everything lands here first with zero friction. Sort and route later in batches.

[[task]]: an atomic note file in Work.

[[microproject]]: a single file in Work that tracks either recurring, or small-scale project. Bigger than a task, smaller than a worthy-of-a-folder project. Can evolve into a folder, if need be!

[[entity evolution]] / work [[pipeline]]: things evolve on their own schedule. What started as simple task can spiral into massive rabbit hole. System need facilitate that - therefore gradual and fractal nature of it. Entities ingress the system, get sorted, change as they get worked on and re-shuffled. System is live and flowing.

## Fractal Nature of Domains

Sufficiently complex entities within a domain (such as a large project) can be domains themselves. A domain can host the following standard elements:

- `card.md`: A high-level description of what the domain/entity is. Standard format:
  - Line 1: `# <Entity Title>`
  - Line 2+: `- [[Tag_1]], [[Tag_2]]` (categorization wikilinks)
  - Overview paragraph describing purpose, scope, and key components.
- `readme.md`: explains why it exists, how it does what it claims, and how to make use of it.
- `map.md` (The Guide): Static, human-written guide outlining the folder rules, layout, and how to navigate this specific domain.
- `index.md` (The Catalog): Dynamically compiled list of active items inside the domain, usually rebuilt by scripts in `_tools/`.
- `_archive/`: Cold storage for fully processed, inactive, or historical entities.
- `_live/`: Machine-generated, read-only data imported from external feeds or sensors, automation-produced artifacts.
- `_tools/`: Domain-specific scripts and automation utilities. Because `_tools/` is itself a domain, it often also contains its own `index.md`, `readme.md` etc.

also possibly contains work tracking:
- folder form: `work/` / `todo/`, when there are many things to keep track of. Usually inside you'll find small-size single-task .md files
- file form: `work.md` / `todo.md`, when there are only a handful of items tracked
`work` and `todo` are full synonyms; pick one per domain and stick with it.

## Naming conventions

- Underscore (`_`): use when you mean a singular thing described by several words (e.g., `business_logic`, `ssd_selection`, `fix_mobile_login`).
- Hyphen (`-`): use when you want to point out multiple things intersecting (e.g., `task-fix_mobile_login` is a task about fixing mobile login; `hardware-ssd_selection` sits alongside other `hardware-` items).
- Wikilinks (`[[Concept]]`) over tags. A tag is a link to a note you haven't written yet.
- `[[Maybe: X]]` — candidate for a future project card. Non-committal.
- Link only when the connection is real and technical. No "contrast" linking.

## Operational mandates

To prevent automated systems from corrupting the homogenized data substrate, all agentic and algorithmic processes must adhere to these rules:

- Adding files: always OK.
- Modifying/deleting existing files: requires explicit scoped permission.
    Alternative: add the proposal into domain's Work!
- Assume no git on items that aren't projects — overwrites are permanent, so exercise care.

