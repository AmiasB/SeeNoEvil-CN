"""Unify terms across chunks and verify every 【keyword】 is a typeable command alias."""
import collections
import glob
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
REPLACE = {"纽带": "羁绊", "刀剑大师": "剑圣", "剑术大师": "剑圣", "刀锋大师": "剑圣"}

with open(os.path.join(HERE, "..", "patch", "SNE_CN.cs"), encoding="utf-8") as f:
    cs = f.read()
aliases = set(re.findall(r'"([^"\x00-\x7f]+)"', cs.split("Fillers")[0]))

keywords = collections.Counter()
for path in sorted(glob.glob(os.path.join(HERE, "chunk_*.zh.txt"))):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    for old, new in REPLACE.items():
        if old in text:
            print(os.path.basename(path), old, "->", new, text.count(old))
            text = text.replace(old, new)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    keywords.update(re.findall(r"【([^】]+)】", text))

print("keywords:", dict(keywords))
print("NOT TYPEABLE:", {k: v for k, v in keywords.items() if k not in aliases})
