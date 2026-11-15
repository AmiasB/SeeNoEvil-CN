# See no Evil 简体中文补丁

See no Evil（Bigfingers.ca，作者 Geremy Walker）的非官方简体中文补丁。本仓库只有补丁源码和译文，**不包含游戏本体**。

针对的是 Unity **4.1** 的完整版。请在自己合法拥有的副本上使用。

## 作者授权

**状态：等待中。**

已准备联系作者，请求允许公开这个汉化补丁。在作者回复之前：

- 本仓库不提供游戏可执行文件或原版资源。
- 请只给自己拥有的游戏打补丁，不要把打过补丁的游戏目录再发出去。
- 若作者拒绝或要求下架，以作者的要求为准。

## 安装

玩家用的压缩包不在 git 历史里，挂在 GitHub Release 上。退出游戏后，把压缩包里 `SeeNoEvil_CHS` 文件夹中的**所有内容**复制到游戏根目录，和 `See_No_Evil.exe` 放在一起。不要只丢进一个子文件夹。

放好之后应该是这样：

```text
See no Evil\
  See_No_Evil.exe
  See_No_Evil_Data\
  Assets\
  安装汉化.bat
  卸载汉化.bat
  汉化说明.txt
  patch\
```

然后双击游戏根目录里的 `安装汉化.bat`。脚本会先把原版文件备份到 `汉化备份`。版本对不上时会自动还原。恢复英文原版，退出游戏后双击 `卸载汉化.bat`。

对话里用【】括起来的词是可以输入的指令，中文和英文都可以。角色名和咒语保持英文。

## 仓库内容

| 路径 | 内容 |
|---|---|
| `patch/SNE_CN.cs` | 运行时换行和中文指令。 |
| `patch/patcher/` | 用 Mono.Cecil 改写玩家自己的 `Assembly-CSharp.dll`。 |
| `patch/strings.tsv` | 写进程序的界面字符串。 |
| `patch/build_dll.ps1`、`patch/make_strings.py` | 编译辅助库并运行补丁器。 |
| `patch/apply_scene_text.py` | 翻译烘焙在场景里的文字。 |
| `translation/` | 对白译文和 `STYLE_GUIDE.md`。 |
| `build_font.py` | 用思源黑体把中文字形写进原版字体图集。 |
| `fonts/` | [思源黑体](https://github.com/adobe-fonts/source-han-sans) Source Han Sans，SIL OFL 1.1。 |
| `make_package.py`、`package_readme.txt` | 生成玩家压缩包。 |

这些内容不在仓库里：游戏备份、反编译、打过补丁的数据文件和 DLL、字体预览，以及玩家压缩包本身。见 `.gitignore`。

## 从源码构建

需要 .NET SDK、Python，以及 Python 包 `UnityPy` 和 `Pillow`。`build_font.py`、`build_dll.ps1`、`make_package.py` 和 `apply_scene_text.py` 里的游戏目录是本机路径，换机器要先改。它们读取 `backup/` 里的未打补丁文件，这个备份不进仓库。

玩家包由 `python make_package.py` 生成，输出 `package/SeeNoEvil_汉化补丁.zip`。改过的游戏文件只以 xdelta 差异放进压缩包，新文件只有译好的对白和 `SNE_CN.dll`。

## 字体和工具许可

思源黑体使用 SIL Open Font License 1.1，不能单独拿去卖，衍生字体也要继续用 OFL。玩家包里的 `xdelta3.exe` 是 [Xdelta](https://github.com/jmacd/xdelta-gpl) 3.1.0，GNU GPL，只用来把差异打进玩家自己的文件。

补丁代码和译文的许可证，等作者授权有结果后再定。
