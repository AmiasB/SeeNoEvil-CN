"""Build the distributable Chinese patch (no original game files included).

python make_package.py
Modified original files ship as xdelta3 diffs against the player's own copy; only
new files (translated dialogue, helper DLL) ship in full.
"""
import hashlib
import os
import shutil
import subprocess
import zipfile

WORK = os.path.dirname(os.path.abspath(__file__))
BACKUP = os.path.join(WORK, "backup")
GAME_DATA = r"e:\T File\SNE_FULL\See_No_Evil_Data"
XDELTA = os.path.join(WORK, "tools", "xdelta3-3.1.0-x86_64.exe")
OUT = os.path.join(WORK, "package", "SeeNoEvil_CHS")
ZIP = os.path.join(WORK, "package", "SeeNoEvil_汉化补丁.zip")

PATCHED = {
    "See_No_Evil_Data/sharedassets0.assets": "sharedassets0.assets",
    "See_No_Evil_Data/Managed/Assembly-CSharp.dll": "Assembly-CSharp.dll",
    "See_No_Evil_Data/mainData": "mainData",
    "See_No_Evil_Data/level2": "level2",
    "See_No_Evil_Data/level3": "level3",
    "See_No_Evil_Data/level4": "level4",
    "See_No_Evil_Data/level7": "level7",
    "See_No_Evil_Data/level8": "level8",
}
REPLACED = {"Assets/TEXT DOCS/GENERIC_DIALOGUE.txt": os.path.join(WORK, "build", "GENERIC_DIALOGUE.txt")}
ADDED = {"See_No_Evil_Data/Managed/SNE_CN.dll": os.path.join(WORK, "patch", "SNE_CN.dll")}


def sha1(path):
    h = hashlib.sha1()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def win(rel):
    return rel.replace("/", "\\")


def main():
    shutil.rmtree(OUT, ignore_errors=True)
    os.makedirs(os.path.join(OUT, "patch", "files"))
    shutil.copy(XDELTA, os.path.join(OUT, "patch", "xdelta3.exe"))

    for rel, backup_name in PATCHED.items():
        original = os.path.join(BACKUP, backup_name)
        modified = os.path.join(GAME_DATA, *rel.split("/")[1:])
        delta = os.path.join(OUT, "patch", os.path.basename(rel) + ".xdelta")
        subprocess.run([XDELTA, "-e", "-9", "-f", "-B", str(1 << 29), "-s", original, modified, delta], check=True)
        print(f"{rel}: {os.path.getsize(delta) / 1e6:.2f} MB diff")

    for rel, src in {**REPLACED, **ADDED}.items():
        shutil.copy(src, os.path.join(OUT, "patch", "files", os.path.basename(rel)))

    write_install()
    write_uninstall()
    shutil.copy(os.path.join(WORK, "package_readme.txt"), os.path.join(OUT, "汉化说明.txt"))

    if os.path.exists(ZIP):
        os.remove(ZIP)
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for root, _, files in os.walk(OUT):
            for name in files:
                full = os.path.join(root, name)
                z.write(full, os.path.relpath(full, os.path.dirname(OUT)))
    print("package:", ZIP, f"{os.path.getsize(ZIP) / 1e6:.2f} MB")


def bat_header(title):
    return [
        "@echo off",
        "chcp 65001 >nul",
        "setlocal EnableExtensions",
        f"title {title}",
        'cd /d "%~dp0"',
        'if not exist "See_No_Evil.exe" (',
        "  echo 请把本补丁的所有文件解压到游戏根目录（与 See_No_Evil.exe 同一文件夹）后再运行。",
        "  pause & exit /b 1",
        ")",
    ]


def write_install():
    lines = bat_header("See no Evil 汉化补丁 - 安装") + [
        'if exist "汉化备份\\installed.txt" (',
        "  echo 汉化补丁已经安装过了。如需重新安装，请先运行“卸载汉化.bat”。",
        "  pause & exit /b 1",
        ")",
        'tasklist /FI "IMAGENAME eq See_No_Evil.exe" | find /I "See_No_Evil.exe" >nul && (',
        "  echo 请先关闭游戏再安装。",
        "  pause & exit /b 1",
        ")",
        "echo 正在备份原始文件……",
        'mkdir "汉化备份" 2>nul',
    ]
    for rel in list(PATCHED) + list(REPLACED):
        lines.append(f'if not exist "{win(rel)}" ( echo 找不到 {win(rel)}，游戏文件不完整。 & pause & exit /b 1 )')
        lines.append(f'copy /y "{win(rel)}" "汉化备份\\{os.path.basename(rel)}" >nul || goto :fail')
    lines.append("echo 正在应用补丁……")
    for rel in PATCHED:
        name = os.path.basename(rel)
        lines.append(
            f'"patch\\xdelta3.exe" -d -f -s "{win(rel)}" "patch\\{name}.xdelta" "{win(rel)}.chs" || goto :fail'
        )
    for rel in PATCHED:
        lines.append(f'move /y "{win(rel)}.chs" "{win(rel)}" >nul || goto :fail')
    for rel in list(REPLACED) + list(ADDED):
        lines.append(f'copy /y "patch\\files\\{os.path.basename(rel)}" "{win(rel)}" >nul || goto :fail')
    lines += [
        'echo installed> "汉化备份\\installed.txt"',
        "echo.",
        "echo 汉化安装完成！原始文件已备份到“汉化备份”文件夹，运行“卸载汉化.bat”可还原。",
        "pause",
        "exit /b 0",
        ":fail",
        "echo.",
        "echo 安装失败：游戏文件与补丁要求的版本不一致（需要 See no Evil 完整版 Unity 4.1 原版文件）。",
        "echo 正在还原……",
    ]
    for rel in PATCHED:
        lines.append(f'del /q "{win(rel)}.chs" 2>nul')
    for rel in list(PATCHED) + list(REPLACED):
        lines.append(f'if exist "汉化备份\\{os.path.basename(rel)}" copy /y "汉化备份\\{os.path.basename(rel)}" "{win(rel)}" >nul')
    for rel in ADDED:
        lines.append(f'del /q "{win(rel)}" 2>nul')
    lines += ["pause", "exit /b 1"]
    write_bat("安装汉化.bat", lines)


def write_uninstall():
    lines = bat_header("See no Evil 汉化补丁 - 卸载") + [
        'if not exist "汉化备份\\installed.txt" (',
        "  echo 没有找到汉化备份，无法卸载。",
        "  pause & exit /b 1",
        ")",
    ]
    for rel in list(PATCHED) + list(REPLACED):
        lines.append(f'copy /y "汉化备份\\{os.path.basename(rel)}" "{win(rel)}" >nul || goto :fail')
    for rel in ADDED:
        lines.append(f'del /q "{win(rel)}" 2>nul')
    lines += [
        'rmdir /s /q "汉化备份"',
        "echo 已还原为英文原版。",
        "pause",
        "exit /b 0",
        ":fail",
        "echo 还原失败，请检查“汉化备份”文件夹是否完整，或确认游戏已关闭。",
        "pause",
        "exit /b 1",
    ]
    write_bat("卸载汉化.bat", lines)


def write_bat(name, lines):
    with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\r\n") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
