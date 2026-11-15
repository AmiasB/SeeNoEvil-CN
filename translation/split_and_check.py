"""split: cut the original dialogue into chunks.  check: validate translated chunks.  merge: build the final file.

python split_and_check.py split
python split_and_check.py check [chunk numbers...]
python split_and_check.py merge <output path>
"""
import glob
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "backup", "GENERIC_DIALOGUE.txt")
CHUNKS = 8
TAG = re.compile(r"^[A-Z]{3}_\d{3}$")
MAX_LINES = 4
MAX_LINE_WIDTH = 860
ASCII_W = [12, 12, 14, 18, 16, 18, 18, 10, 12, 12, 20, 16, 10, 16, 8, 20, 16, 16, 16, 16,
           18, 16, 16, 16, 16, 16, 8, 10, 14, 16, 14, 16, 18, 20, 18, 18, 18, 18, 18, 18,
           16, 16, 16, 18, 18, 18, 18, 18, 18, 18, 20, 16, 16, 16, 20, 18, 20, 20, 18, 12,
           16, 12, 18, 18, 16, 18, 18, 16, 18, 16, 16, 20, 18, 12, 16, 18, 12, 18, 16, 16,
           18, 18, 18, 16, 14, 18, 16, 18, 18, 16, 16, 16, 16, 16, 16]
NO_LINE_START = "，。！？；：、）》」』】”’…—～·,.!?;:)]}%"
NO_LINE_END = "（《「『【“‘([{"


def measure(s):
    return sum(ASCII_W[ord(c) - 32] if 32 <= ord(c) < 127 else 32 for c in s)


def is_word(c):
    return " " < c < "\x80"


def unit_end(text, start):
    end = start + 1
    if is_word(text[start]):
        while end < len(text) and is_word(text[end]):
            end += 1
    return end


def wrap_lines(text):
    """Line count produced by SNE_CN.Wrap (keep in sync with patch/SNE_CN.cs)."""
    text = text.lstrip(" ")
    lines, width, i = 1, 0, 0
    while i < len(text):
        end = unit_end(text, i)
        while end < len(text):
            if text[end] in NO_LINE_START:
                end += 1
            elif text[end - 1] in NO_LINE_END and text[end] != " ":
                end = unit_end(text, end)
            else:
                break
        token = text[i:end]
        if width + measure(token) > MAX_LINE_WIDTH and width > 0:
            lines += 1
            token = token.lstrip(" ")
            width = 0
        width += measure(token)
        i = end
    return lines


def read_lines(path):
    with open(path, encoding="utf-8-sig") as f:
        return f.read().splitlines()


def split():
    lines = read_lines(SRC)
    target = sum(len(l) for l in lines) / CHUNKS
    chunks, current, size = [], [], 0
    for line in lines:
        current.append(line)
        size += len(line)
        if size >= target and len(chunks) < CHUNKS - 1:
            chunks.append(current)
            current, size = [], 0
    chunks.append(current)
    for i, chunk in enumerate(chunks, 1):
        with open(os.path.join(HERE, f"chunk_{i:02d}.en.txt"), "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(chunk) + "\n")
        print(i, len(chunk), sum(len(l) for l in chunk), chunk[0][:7], "->", chunk[-1][:7])


def parse(line):
    if len(line) > 8 and TAG.match(line[:7]) and line[7] == ":":
        return line[:7], line[8:].split(":")
    return None, None


def check_chunk(i):
    en_path = os.path.join(HERE, f"chunk_{i:02d}.en.txt")
    zh_path = os.path.join(HERE, f"chunk_{i:02d}.zh.txt")
    if not os.path.exists(zh_path):
        return [f"chunk {i}: missing {os.path.basename(zh_path)}"]
    en, zh = read_lines(en_path), read_lines(zh_path)
    errors = []
    if len(en) != len(zh):
        errors.append(f"chunk {i}: line count {len(zh)} != {len(en)}")
    for n, (a, b) in enumerate(zip(en, zh), 1):
        tag_a, fa = parse(a)
        if tag_a is None:
            if a != b:
                errors.append(f"chunk {i} line {n}: non-dialogue line changed: {b[:40]!r}")
            continue
        tag_b, fb = parse(b)
        if tag_b != tag_a:
            errors.append(f"chunk {i} line {n}: tag {tag_b} != {tag_a}")
            continue
        if len(fa) != len(fb):
            errors.append(f"chunk {i} line {n} {tag_a}: {len(fb)} fields != {len(fa)} (half-width ':' in text?)")
            continue
        for k in range(0, len(fa), 2):
            if fa[k].strip() != fb[k].strip():
                errors.append(f"chunk {i} line {n} {tag_a}: portrait {fb[k]!r} != {fa[k]!r}")
        for k in range(1, len(fa), 2):
            pa = re.match(r"^\|\d+\|", fa[k])
            pb = re.match(r"^\|\d+\|", fb[k])
            if (pa.group(0) if pa else None) != (pb.group(0) if pb else None):
                errors.append(f"chunk {i} line {n} {tag_a}: cinematic prefix mismatch in field {k}")
            body = fb[k][pb.end():] if pb else fb[k]
            if "|" in body or "\\" in body or "~" in body or "`" in body:
                errors.append(f"chunk {i} line {n} {tag_a}: forbidden character in field {k}")
            if fa[k].strip() and not body.strip():
                errors.append(f"chunk {i} line {n} {tag_a}: empty translation in field {k}")
            if re.search(r"[a-z]{4,}\s+[a-z]{3,}\s+[a-z]{3,}", body):
                errors.append(f"chunk {i} line {n} {tag_a}: looks untranslated in field {k}: {body[:50]!r}")
            lines = wrap_lines(body)
            if lines > MAX_LINES:
                errors.append(f"chunk {i} line {n} {tag_a}: field {k} wraps to {lines} lines (max {MAX_LINES}), shorten it: {body[:30]!r}")
    return errors


def check(nums):
    all_errors = []
    for i in nums:
        errs = check_chunk(i)
        all_errors += errs
        print(f"chunk {i}: {'OK' if not errs else str(len(errs)) + ' errors'}")
    for e in all_errors[:200]:
        print("  ", e)
    return not all_errors


def merge(out_path):
    if not check(range(1, CHUNKS + 1)):
        raise SystemExit("fix errors before merging")
    out = []
    for i in range(1, CHUNKS + 1):
        out += read_lines(os.path.join(HERE, f"chunk_{i:02d}.zh.txt"))
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        f.write("\r\n".join(out) + "\r\n")
    print("wrote", out_path, len(out), "lines")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "split":
        split()
    elif cmd == "check":
        nums = [int(x) for x in sys.argv[2:]] or range(1, CHUNKS + 1)
        sys.exit(0 if check(nums) else 1)
    elif cmd == "merge":
        merge(sys.argv[2])
