"""Build and install the Chinese patch into the game directory.

python build_all.py [--test-dialogue]
"""
import os
import shutil
import subprocess
import sys

WORK = os.path.dirname(os.path.abspath(__file__))
GAME = r"e:\T File\SNE_FULL"
DATA = os.path.join(GAME, "See_No_Evil_Data")
DIALOGUE = os.path.join(GAME, "Assets", "TEXT DOCS", "GENERIC_DIALOGUE.txt")
BUILD = os.path.join(WORK, "build")


def run(*args):
    print(">", " ".join(args))
    subprocess.run(args, check=True, cwd=WORK)


def gb2312_level1():
    chars = []
    for hi in range(0xB0, 0xD8):
        for lo in range(0xA1, 0xFF):
            try:
                chars.append(bytes([hi, lo]).decode("gb2312"))
            except UnicodeDecodeError:
                pass
    return "".join(chars)


def main():
    os.makedirs(BUILD, exist_ok=True)
    dialogue = os.path.join(BUILD, "GENERIC_DIALOGUE.txt")
    if "--test-dialogue" in sys.argv:
        shutil.copy(os.path.join(WORK, "test_dialogue.txt"), dialogue)
    else:
        run(sys.executable, os.path.join(WORK, "translation", "split_and_check.py"), "merge", dialogue)

    sources = [dialogue, os.path.join(WORK, "patch", "strings.tsv"),
               os.path.join(WORK, "patch", "SNE_CN.cs"), os.path.join(WORK, "patch", "apply_scene_text.py")]
    text = gb2312_level1() + "“”‘’…—–·～、。，！？；：（）《》【】「」『』"
    for path in sources:
        with open(path, encoding="utf-8") as f:
            text += f.read()
    charset = os.path.join(BUILD, "charset.txt")
    with open(charset, "w", encoding="utf-8") as f:
        f.write(text)

    run(sys.executable, "build_font.py", charset, os.path.join(BUILD, "sharedassets0.assets"), os.path.join(BUILD, "atlas_preview.png"))
    run(sys.executable, os.path.join("patch", "apply_scene_text.py"), BUILD)

    shutil.copy(os.path.join(BUILD, "sharedassets0.assets"), DATA)
    for name in ["mainData", "level2", "level3", "level4", "level7", "level8"]:
        shutil.copy(os.path.join(BUILD, name), DATA)
    shutil.copy(os.path.join(WORK, "patch", "Assembly-CSharp.dll"), os.path.join(DATA, "Managed"))
    shutil.copy(os.path.join(WORK, "patch", "SNE_CN.dll"), os.path.join(DATA, "Managed"))
    shutil.copy(dialogue, DIALOGUE)
    print("installed")


if __name__ == "__main__":
    main()
