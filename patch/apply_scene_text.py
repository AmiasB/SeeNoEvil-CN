"""Translate TextMesh default texts baked into scene files.

Usage: python apply_scene_text.py <output data dir> [source data dir]
Reads the source scenes and writes translated copies into the output directory.
The source defaults to the old-version backup.
"""
import os
import sys

import UnityPy

BACKUP = r"e:\T File\SNE_WORK\backup"

CREDITS_EN_PARTS = {
    "Concept, Script, Coding, Art, Animation,\r\nand pretty much everything\r\nby Geremy Walker":
        "策划、剧本、程序、美术、动画\r\n以及几乎所有的一切\r\nGeremy Walker",
    "Script Coordinator and Quality Assurance": "剧本统筹与质量保证",
    "Playtesters": "测试玩家",
    "Music \r\n": "音乐\r\n",
    "Special Thanks to Casey Johnson \r\nI couldn't do any of this without you. \r\nMuch love. ":
        "特别感谢 Casey Johnson\r\n没有你，这一切都不可能实现。\r\n爱你。\r\n\r\n中文汉化\r\n已授权，由 AmiasBerner（狼因夜北）制作",
}

SIMPLE = {
    "Likes flowers": "喜欢花",
    "Wants to get laid": "想上床",
    "Wants you to bugger off": "想让你滚蛋",
    "Wants bugs": "想要虫子",
    "Wants Orsino to submit": "想让 Orsino【臣服】",
}

FILES = ["mainData", "level2", "level3", "level4", "level7", "level8"]


def translate(text):
    if text in SIMPLE:
        return SIMPLE[text]
    if "Bigfingers.ca" in text and "Playtesters" in text:
        for en, zh in CREDITS_EN_PARTS.items():
            if en not in text:
                raise SystemExit(f"credits fragment not found: {en!r}")
            text = text.replace(en, zh)
        return text
    return None


def main(out_dir, source_dir=None):
    source_dir = source_dir or BACKUP
    os.makedirs(out_dir, exist_ok=True)
    for name in FILES:
        env = UnityPy.load(os.path.join(source_dir, name))
        changed = 0
        for obj in env.objects:
            if obj.type.name != "TextMesh":
                continue
            tree = obj.read_typetree()
            new = translate(tree["m_Text"])
            if new is not None:
                tree["m_Text"] = new
                obj.save_typetree(tree)
                changed += 1
        with open(os.path.join(out_dir, name), "wb") as f:
            f.write(env.file.save())
        print(name, "changed", changed)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
