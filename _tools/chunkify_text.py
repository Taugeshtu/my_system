#!/usr/bin/env python3
import os
import argparse

def chunkify(input_path, output_dir, target_kb=10, prefix="chunk"):
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    paragraphs = content.split("\n\n")
    merged = []
    if paragraphs:
        current = paragraphs[0].strip()
        for p in paragraphs[1:]:
            p = p.strip()
            if not p:
                continue
            if p[0].islower():
                current += " " + p
            else:
                merged.append(current)
                current = p
        if current:
            merged.append(current)

    os.makedirs(output_dir, exist_ok=True)
    target_bytes = target_kb * 1024
    chunk_idx = 1
    chunk_paras = []
    chunk_size = 0

    def write_chunk(idx, paras):
        out_path = os.path.join(output_dir, f"{prefix}_{idx:03d}.md")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write("\n\n".join(paras) + "\n")

    for para in merged:
        p_size = len(para.encode("utf-8")) + 2
        if chunk_size + p_size > target_bytes and chunk_paras:
            write_chunk(chunk_idx, chunk_paras)
            chunk_idx += 1
            chunk_paras = []
            chunk_size = 0
        chunk_paras.append(para)
        chunk_size += p_size

    if chunk_paras:
        write_chunk(chunk_idx, chunk_paras)

    print(f"Split '{input_path}' into {chunk_idx} chunks in '{output_dir}/' (~{target_kb}KB each).")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean paragraphs and pack text into sized markdown chunks.")
    parser.add_argument("input_file", help="Path to input text or markdown file")
    parser.add_argument("-o", "--output-dir", default="chunks", help="Destination folder (default: 'chunks')")
    parser.add_argument("-s", "--size-kb", type=int, default=10, help="Target chunk size in KB (default: 10)")
    parser.add_argument("-p", "--prefix", default="chunk", help="Chunk filename prefix (default: 'chunk')")
    args = parser.parse_args()
    chunkify(args.input_file, args.output_dir, args.size_kb, args.prefix)
