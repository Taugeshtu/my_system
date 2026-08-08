#!/usr/bin/env python3
import os
import re
import argparse

def parse_card(card_path):
    with open(card_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
    
    title = ""
    domains = []
    desc_lines = []
    
    for line in content.splitlines():
        line_str = line.strip()
        if not line_str:
            continue
        if line_str.startswith("# "):
            title = line_str[2:].strip()
        elif line_str.startswith("- [[") or line_str.startswith("-[["):
            tags = re.findall(r"\[\[(.*?)\]\]", line_str)
            domains.extend(tags)
        else:
            desc_lines.append(line_str)
            
    desc = " ".join(desc_lines)
    return title, domains, desc

def build_index(target_dir, output_file=None):
    target_dir = os.path.abspath(target_dir)
    dir_name = os.path.basename(target_dir)
    if output_file is None:
        output_file = os.path.join(target_dir, "index.md")
        
    items = []
    for entry in sorted(os.listdir(target_dir)):
        if entry.startswith(".") or entry in ("_archive", "_tools", "_live", "_proposal", "__pycache__"):
            continue
        sub_path = os.path.join(target_dir, entry)
        if os.path.isdir(sub_path):
            card_path = os.path.join(sub_path, "card.md")
            if os.path.isfile(card_path):
                title, domains, desc = parse_card(card_path)
                items.append({
                    "folder": entry,
                    "title": title or entry,
                    "domains": domains,
                    "desc": desc
                })
                
    out = [f"# {dir_name} Index\n", f"Catalog of active items in `{dir_name}/`.\n"]
    out.append("| Name | Domains / Tags | Overview |")
    out.append("| --- | --- | --- |")
    
    for item in items:
        link = f"[{item['title']}]({item['folder']}/card.md)"
        dom_str = ", ".join(f"[[{d}]]" for d in item["domains"])
        out.append(f"| {link} | {dom_str} | {item['desc']} |")
        
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
        
    print(f"Generated {output_file} with {len(items)} items.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build index.md from card.md files across a domain.")
    parser.add_argument("target_dir", nargs="?", default=".", help="Domain directory to scan (default: current directory)")
    parser.add_argument("-o", "--output", default=None, help="Output markdown path (default: index.md in target directory)")
    args = parser.parse_args()
    
    build_index(args.target_dir, args.output)
