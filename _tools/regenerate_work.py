#!/usr/bin/env python3
import os

WORK_DIR, PROJECTS_DIR = os.path.expanduser('~/05_WORK'), os.path.expanduser('~/10_PROJECTS')
EXCLUDES = {'.git', 'node_modules', 'target', 'build', 'dist', 'bin', 'obj', 'venv', '.venv', 'Library', 'Temp', 'Logs', '_archive'}

print("Scan started...")
for f in os.scandir(WORK_DIR):
    if f.is_symlink():
        target = os.path.realpath(f.path)
        if not os.path.exists(f.path) or '_archive' in target.split(os.sep):
            os.unlink(f.path)

scanned, linked = 0, 0
for root, dirs, files in os.walk(PROJECTS_DIR):
    if '_archive' in root.split(os.sep):
        dirs.clear()
        continue
    local_excludes = set(EXCLUDES)
    if '.gitignore' in files:
        try:
            with open(os.path.join(root, '.gitignore'), 'r', errors='ignore') as gf:
                for line in gf:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        clean = line.rstrip('/').lstrip('/*')
                        if clean: local_excludes.add(clean)
        except Exception: pass

    is_project = '.git' in dirs or '.git' in files or '.project-root' in files
    dirs[:] = [d for d in dirs if d not in local_excludes and not d.startswith('.')]
    scanned += 1
    if scanned % 100 == 0:
        print(f"\rScanning... {scanned} folders checked", end="", flush=True)
    
    if is_project:
        kebab = os.path.relpath(root, PROJECTS_DIR).replace(os.sep, '-')
        todo_file = next((os.path.join(root, f) for f in os.listdir(root) if f.lower() in ('todo.md', 'work.md') and os.path.isfile(os.path.join(root, f))), None)
        work_dir = next((os.path.join(root, d) for d in os.listdir(root) if d.lower() in ('work', 'todo') and os.path.isdir(os.path.join(root, d))), None)

        if work_dir or todo_file:
            linked += 1

        if work_dir:
            desktop = os.path.join(work_dir, '_root.desktop')
            try:
                with open(desktop, 'w') as df:
                    df.write(f"[Desktop Entry]\nType=Link\nName=_root\nURL=file://{os.path.abspath(root)}\nIcon=folder\n")
            except Exception: pass
            try:
                sym_path = os.path.join(WORK_DIR, kebab)
                if not os.path.lexists(sym_path):
                    os.symlink(work_dir, sym_path)
                    print(f"\nLinked dir: {kebab} -> {work_dir}")
            except Exception: pass

        if todo_file:
            try:
                sym_path = os.path.join(WORK_DIR, f"{kebab}.md")
                if not os.path.lexists(sym_path):
                    os.symlink(todo_file, sym_path)
                    print(f"\nLinked file: {kebab}.md -> {todo_file}")
            except Exception: pass
            if not work_dir:
                try:
                    sym_path = os.path.join(WORK_DIR, f"root--{kebab}")
                    if not os.path.lexists(sym_path):
                        os.symlink(root, sym_path)
                        print(f"Linked project root: root--{kebab} -> {root}")
                except Exception: pass

print(f"\nDone! Checked {scanned} folders. Linked {linked} projects.")
