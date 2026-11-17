"""Build the player folder. It sits beside See_No_Evil.exe; the bat is run from inside it.

python make_package.py
Two xdelta sets are packed: the previous Unity 4.1 build, and the current
DRM-free build sold on the official site. The installer picks by the original DLL.
"""
import hashlib
import os
import shutil
import subprocess
import zipfile

WORK = os.path.dirname(os.path.abspath(__file__))
BACKUP = os.path.join(WORK, "backup")
DRM = r"e:\T File\SNE_FULL_DRM_FREE\See_No_Evil_Data"
XDELTA = os.path.join(WORK, "tools", "xdelta3-3.1.0-x86_64.exe")
OUT = os.path.join(WORK, "package", "SeeNoEvil_CHS")
CN = os.path.join(OUT, "cn_patch")
ZIP = os.path.join(WORK, "package", "SeeNoEvil_CN.zip")

# name -> (original, patched) for each supported build
FILES = ["Assembly-CSharp.dll", "sharedassets0.assets", "mainData", "level2", "level3", "level4", "level7", "level8"]
VARIANTS = {
    "old": {
        "Assembly-CSharp.dll": (os.path.join(BACKUP, "Assembly-CSharp.dll"), os.path.join(WORK, "build", "old", "Assembly-CSharp.dll")),
        "sharedassets0.assets": (os.path.join(BACKUP, "sharedassets0.assets"), os.path.join(WORK, "build", "sharedassets0.assets")),
        "mainData": (os.path.join(BACKUP, "mainData"), os.path.join(WORK, "build", "old", "mainData")),
        "level2": (os.path.join(BACKUP, "level2"), os.path.join(WORK, "build", "old", "level2")),
        "level3": (os.path.join(BACKUP, "level3"), os.path.join(WORK, "build", "old", "level3")),
        "level4": (os.path.join(BACKUP, "level4"), os.path.join(WORK, "build", "old", "level4")),
        "level7": (os.path.join(BACKUP, "level7"), os.path.join(WORK, "build", "old", "level7")),
        "level8": (os.path.join(BACKUP, "level8"), os.path.join(WORK, "build", "old", "level8")),
    },
    "new": {
        "Assembly-CSharp.dll": (os.path.join(DRM, "Managed", "Assembly-CSharp.dll"), os.path.join(WORK, "build", "drm", "Assembly-CSharp.dll")),
        "sharedassets0.assets": (os.path.join(DRM, "sharedassets0.assets"), os.path.join(WORK, "build", "drm", "sharedassets0.assets")),
        "mainData": (os.path.join(DRM, "mainData"), os.path.join(WORK, "build", "drm", "mainData")),
        "level2": (os.path.join(DRM, "level2"), os.path.join(WORK, "build", "drm", "level2")),
        "level3": (os.path.join(DRM, "level3"), os.path.join(WORK, "build", "drm", "level3")),
        "level4": (os.path.join(DRM, "level4"), os.path.join(WORK, "build", "drm", "level4")),
        "level7": (os.path.join(DRM, "level7"), os.path.join(WORK, "build", "drm", "level7")),
        "level8": (os.path.join(DRM, "level8"), os.path.join(WORK, "build", "drm", "level8")),
    },
}


def sha1(path):
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def utf8_bom(path, text):
    with open(path, "w", encoding="utf-8-sig", newline="\r\n") as f:
        f.write(text)


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(CN)
    shutil.copy(XDELTA, os.path.join(CN, "xdelta3.exe"))
    shutil.copy(os.path.join(WORK, "patch", "SNE_CN.dll"), os.path.join(CN, "SNE_CN.dll"))
    shutil.copy(os.path.join(WORK, "build", "GENERIC_DIALOGUE.txt"), os.path.join(CN, "GENERIC_DIALOGUE.txt"))

    version_lines = []
    for name, files in VARIANTS.items():
        dest = os.path.join(CN, name)
        os.makedirs(dest)
        original_dll = files["Assembly-CSharp.dll"][0]
        version_lines.append(f"{sha1(original_dll)}\t{name}")
        for filename in FILES:
            original, patched = files[filename]
            if not os.path.isfile(original) or not os.path.isfile(patched):
                raise SystemExit(f"missing {name} {filename}")
            delta = os.path.join(dest, filename + ".vcdiff")
            subprocess.run(
                [XDELTA, "-e", "-9", "-f", "-B", str(1 << 29), "-s", original, patched, delta],
                check=True,
            )
            print(f"{name}/{filename}: {os.path.getsize(delta) / 1e6:.2f} MB")

    utf8_bom(os.path.join(CN, "versions.txt"), "\n".join(version_lines) + "\n")
    for script in ("apply.ps1", "restore.ps1"):
        text = open(os.path.join(WORK, "package", script), encoding="utf-8-sig").read()
        utf8_bom(os.path.join(CN, script), text)
    for name in ("打补丁.bat", "还原.bat"):
        text = open(os.path.join(WORK, "package", name), encoding="utf-8").read().replace("\r\n", "\n").replace("\n", "\r\n")
        with open(os.path.join(OUT, name), "w", encoding="ascii", newline="") as f:
            f.write(text)
    shutil.copy(os.path.join(WORK, "package_readme.txt"), os.path.join(OUT, "使用说明.txt"))

    check_roundtrip("new", "mainData")
    check_roundtrip("new", "Assembly-CSharp.dll")
    check_roundtrip("old", "mainData")

    if os.path.exists(ZIP):
        os.remove(ZIP)
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for root, _, files in os.walk(OUT):
            for name in files:
                full = os.path.join(root, name)
                z.write(full, os.path.relpath(full, os.path.dirname(OUT)))
    print("package:", ZIP, f"{os.path.getsize(ZIP) / 1e6:.2f} MB")


def check_roundtrip(variant, filename):
    original, patched = VARIANTS[variant][filename]
    delta = os.path.join(CN, variant, filename + ".vcdiff")
    out = os.path.join(WORK, "build", "_roundtrip_" + filename)
    subprocess.run([XDELTA, "-d", "-f", "-s", original, delta, out], check=True)
    if sha1(out) != sha1(patched):
        raise SystemExit(f"roundtrip mismatch {variant} {filename}")
    os.remove(out)
    print(f"roundtrip ok {variant} {filename}")


if __name__ == "__main__":
    main()
