# System Tools

Command-line utilities for `my_system`.

## 1. Domain Index Builder (`build_index.py`)

Scans a domain directory, parses `card.md` files from immediate subdirectories, and compiles a standardized markdown table in `index.md`.

```bash
python3 _tools/build_index.py [target_dir] [-o output_path]
```

- `target_dir`: Domain root containing subdirectories with `card.md` files (default: current working directory).
- `-o / --output`: Path to write index (default: `<target_dir>/index.md`).

## 2. Text Chunker (`chunkify_text.py`)

Cleans OCR / newline wraps in memory and packs long text or transcripts into size-capped markdown files for LLM context ingestion.

```bash
python3 _tools/chunkify_text.py <input_file> [-o output_dir] [-s size_kb] [-p prefix]
```

- `input_file`: Path to raw text / transcript dump.
- `-o / --output-dir`: Output directory for generated chunks (default: `./chunks`).
- `-s / --size-kb`: Target chunk size in KB (default: `10`).
- `-p / --prefix`: Output filename prefix (default: `chunk`).

## 3. Transcript Yoinker (`yoink.py`)

Extracts clean-ish YouTube video transcripts into markdown paragraphs.

```bash
uv run _tools/yoink.py <youtube_url>
```

- Fetches video transcripts, filters stop-word noise for clean slugs, and outputs formatted markdown paragraphs.

## 4. Work Regenerator (`regenerate_work.py`)

Syncs `WORK/` symlinks to match the current state of `PROJECTS/`. Walks the projects tree, finds any project with a `work/`, `todo/`, `work.md`, or `todo.md`, and creates/removes symlinks in `WORK/` accordingly. Stale symlinks (dangling or pointing into `_archive`) are cleaned up automatically.

```bash
python3 _tools/regenerate_work.py
```

- Reads `WORK_DIR` and `PROJECTS_DIR` from hardcoded `~/05_WORK` and `~/10_PROJECTS` — update these at the top of the script if your paths differ.
- Respects `.gitignore` entries and a built-in exclude list (`node_modules`, `build`, `dist`, etc.).
- For projects with a `work/` _directory_: symlinks the whole dir and drops a `_root.desktop` file inside for easy navigation back to project root.
- For projects with only a `work.md` / `todo.md` _file_: symlinks the file, plus a `root--` symlink to the project root.

## 5. Ingress Router (`to-ingress`)

Moves files or directories into the ingress heap (`~/00_INGRESS`) and appends a timestamped origin trace entry into today's daily log (`YYYY-MM-DD.md`).

```bash
to-ingress <file_or_dir> [more_files...]
```

- Accepts one or more file or directory paths.
- Moves targets directly into `$HOME/00_INGRESS/`.
- Appends a log line formatted with time, filename, and original path to `$HOME/00_INGRESS/YYYY-MM-DD.md`.
- _Note_: Ingress path `$HOME/00_INGRESS` is currently hardcoded in the script and might need to be changed if path layout differs.
