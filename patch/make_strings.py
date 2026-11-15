"""Generate strings.tsv (type, original, replacement) for the DLL patcher."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ASCII_W = [12, 12, 14, 18, 16, 18, 18, 10, 12, 12, 20, 16, 10, 16, 8, 20, 16, 16, 16, 16,
           18, 16, 16, 16, 16, 16, 8, 10, 14, 16, 14, 16, 18, 20, 18, 18, 18, 18, 18, 18,
           16, 16, 16, 18, 18, 18, 18, 18, 18, 18, 20, 16, 16, 16, 20, 18, 20, 20, 18, 12,
           16, 12, 18, 18, 16, 18, 18, 16, 18, 16, 16, 20, 18, 12, 16, 18, 12, 18, 16, 16,
           18, 18, 18, 16, 14, 18, 16, 18, 18, 16, 16, 16, 16, 16, 16]
SPACE_W = ASCII_W[0]


def width(s):
    return sum(ASCII_W[ord(c) - 32] if 32 <= ord(c) < 127 else 32 for c in s)


HINT_SAVED_EN = "Up : Inspect    Down : Interact    R : Repeat         Save Slot "
HINT_UNSAVED_EN = "Up : Inspect    Down : Interact    R : Repeat      Progress not Saved"
HINT = "上：查看    下：互动    R：重复"
HINT_SAVED_ZH = HINT + " " * round((width(HINT_SAVED_EN) - width(HINT + "存档位 ")) / SPACE_W) + "存档位 "
HINT_UNSAVED_ZH = HINT + " " * round((width(HINT_UNSAVED_EN) - width(HINT + "进度未保存")) / SPACE_W) + "进度未保存"

ROWS = [
    ("TextScript", HINT_SAVED_EN, HINT_SAVED_ZH),
    ("TextScript", HINT_UNSAVED_EN, HINT_UNSAVED_ZH),
    ("TextScript", "Press Enter to Input Text Commands", "按回车键输入文字指令"),
    ("TextScript", "VOL ", "音乐 "),
    ("TextScript", "\n -  +\nSFX ", "\n -  +\n音效 "),
    ("TITLE_PAGE_SCRIPT", "Fill out LICENSE.TXT to activate this game", "请填写 LICENSE.TXT 以激活本游戏"),
    ("TITLE_PAGE_SCRIPT", "Full Version - Licensed to ", "完整版 - 授权给 "),
    ("TITLE_PAGE_SCRIPT", "Press Enter to Start a New Game \nor use 1-4 to load a saved file", "按回车键开始新游戏\n或按 1-4 读取存档"),
    ("TITLE_PAGE_SCRIPT", "SAVE FILE 1 - ", "存档 1 - "),
    ("TITLE_PAGE_SCRIPT", "\nSAVE FILE 2 - ", "\n存档 2 - "),
    ("TITLE_PAGE_SCRIPT", "\nSAVE FILE 3 - ", "\n存档 3 - "),
    ("TITLE_PAGE_SCRIPT", "\nSAVE FILE 4 - ", "\n存档 4 - "),
    ("TextLoader", "8:I can't find anything called ", "8:我在仪式书里找不到任何叫作“"),
    ("TextLoader", " in the ritual book.", "”的东西。"),
    ("TextLoader", "4:Right, my ", "4:没错，我的 "),
    ("TextLoader", ". Present and accounted-for.", "。好端端的，一样不少。"),
    ("TextLoader", "11:I am not carrying anything I would describe as a ", "11:我身上没带任何可以称作“"),
    ("TextLoader", ".", "”的东西。"),
    ("DEMON_DETAILS_SCRIPT", "Wants to be summoned", "想被【召唤】"),
    ("DEMON_DETAILS_SCRIPT", "Wants honey for a blowjob", "想要【蜂蜜】，以【口交】回报"),
    ("DEMON_DETAILS_SCRIPT", "Wants honey and is open to suggestions", "想要【蜂蜜】，愿意听取【提议】"),
    ("DEMON_DETAILS_SCRIPT", "Wants bugs", "想要虫子"),
    ("DEMON_DETAILS_SCRIPT", "Wants Orsino's touch for a light", "想要 Orsino 的【触碰】，以【点火】回报"),
    ("DEMON_DETAILS_SCRIPT", "Wants to be touched and is open to suggestions", "想被【触碰】，愿意听取【提议】"),
    ("DEMON_DETAILS_SCRIPT", "Wants to touch Orsino but dares not", "想触碰 Orsino，却不敢"),
    ("DEMON_DETAILS_SCRIPT", "Will light Orsino's cigar and is open to suggestions", "愿为 Orsino【点火】，愿意听取【提议】"),
    ("DEMON_DETAILS_SCRIPT", "Wants Orsino to submit", "想让 Orsino【臣服】"),
    ("DEMON_DETAILS_SCRIPT", "Wants a fuck for the grimoire", "想要【上床】，以【魔典】回报"),
    ("DEMON_DETAILS_SCRIPT", "Wants the razor for a shave", "想要【剃刀】，以【刮毛】回报"),
    ("DEMON_DETAILS_SCRIPT", "Wants the razor and is open to suggestions", "想要【剃刀】，愿意听取【提议】"),
    ("DEMON_DETAILS_SCRIPT", "Wants Orsino to show him a new blade", "想让 Orsino 给他看一种新的刀刃"),
    ("DEMON_DETAILS_SCRIPT", "Wants Orsino to bugger off", "想让 Orsino 滚蛋"),
    ("OrsinoScript", "ORSINO'S HOUSE", "ORSINO 的家"),
    ("OrsinoScript", "BARROD'S PALACE", "BARROD 的宫殿"),
    ("OrsinoScript", "NEIGHBOR'S HOUSE?", "邻居家？"),
    ("OrsinoScript", "NEIGHBOR'S HOUSE", "邻居家"),
    ("OrsinoScript", "FOREST PATH", "林间小径"),
    ("OrsinoScript", "THRONE ROOM", "王座厅"),
    ("OrsinoScript", "SCARY CASTLE", "恐怖城堡"),
    ("OrsinoScript", "GARDEN", "花园"),
    ("OrsinoScript", "FRONT GATE", "前门"),
    ("OrsinoScript", "CRUX OF FLESH", "血肉十字"),
    ("OrsinoScript", "COURT", "庭院"),
    ("OrsinoScript", "HALL", "大厅"),
    ("OrsinoScript", "THALAMUM VITAE", "生命之室"),
    ("OrsinoScript", "LIBRARY", "书库"),
    ("OrsinoScript", "DUNGEON", "地牢"),
    ("OrsinoScript", "EYRIE", "鹰巢"),
    ("OrsinoScript", "KITCHEN", "厨房"),
    ("OrsinoScript", "VORTEX OF HOWLS", "嚎叫漩涡"),
    ("OrsinoScript", "IMMOLATORIUM", "焚献室"),
]


def esc(s):
    return s.replace("\t", "\\t").replace("\n", "\\n")


with open(os.path.join(HERE, "strings.tsv"), "w", encoding="utf-8", newline="\n") as f:
    for type_name, en, zh in ROWS:
        f.write(f"{type_name}\t{esc(en)}\t{esc(zh)}\n")
print(repr(HINT_SAVED_ZH), width(HINT_SAVED_ZH), width(HINT_SAVED_EN))
print(repr(HINT_UNSAVED_ZH), width(HINT_UNSAVED_ZH), width(HINT_UNSAVED_EN))
