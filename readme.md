> Because the only two things to survive a nuclear apocalypse will be cockroaches and plain-text.

## why my_system

I keep finding myself having 50 projects going on at once, and still only one head.
And I want my digital life decentralized across hardware I control, not in a cloud I can get banned from.
Public, so you can **make it yours**.

## how my_system

`my_system` provides a strict, fractal filesystem grammar that keeps everything human-navigable, grep-friendly, and agent-legible. Structure that both humans and agents can navigate — just point at `my_system.md` and go.

Four files make it work:
- [`my_system.md`](my_system.md) — domain grammar, naming rules, operational mandates.
- [`my_places.md`](my_places.md) — your filesystem layout and hot paths. Fill in, keep private.
- [`ingress-agents.md`](ingress-agents.md) — processing protocol for the capture heap.
- [`_tools/Readme.md`](_tools/Readme.md) — standalone CLI utilities.

### Goes great together with:
- [TO-DAY](https://github.com/Taugeshtu/TO-DAY) - write notes the moment you had a thought.
- [shutton](https://github.com/Taugeshtu/shutton) - minimalist GUI buttons wrapping shell scripts.
- [Future](https://github.com/Taugeshtu/Future) - noun-oriented computing paradigm for Linux.

---

## Usage

### The loop

- **Capture**: dump notes, files, voice memos, half-baked ideas into INGRESS. Zero friction, zero organizing.
- **Process**: visit INGRESS periodically — with an agent if you're that kind of person — and route items to where they belong.
- **Work from WORK**: your dashboard. Active tasks, microprojects, symlinks to project work files. This is what's on your plate _right now_.
- **Let things evolve**: a daily note becomes a task. A task becomes a microproject. A microproject becomes a full project. A project ships and gets archived. Things move backwards and sideways on this scale too. The system flows.

### Tips from the trenches

- Don't fret over following the system strictly — it's a guide, not a thermodynamics law. One more project organized today is progress.
- Nuke symlinks out of WORK for stuff that isn't active. Free up headspace; focus on what actually matters right now.
- Throw things _back_ into INGRESS. This is your "defer" action. Not ready to deal with it? Back in the heap.
- Once a quarter, revisit Captures. These mattered enough to note down, and again to not archive outright. Still relevant? Revive the thread. Otherwise, bury it.

---

## Install

```bash
git clone https://github.com/Taugeshtu/my_system ~/.local/share/my_system
```

Point your agent at [`setup.md`](setup.md) and let it take over. If doing manual setup — read `setup.md` and do your best robot impression.
