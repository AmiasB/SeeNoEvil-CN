# See no Evil 汉化规范

## 文件格式（必须严格遵守，否则游戏会崩溃或错乱）

每行格式：`TAG_###:头像编号:文本:头像编号:文本:...`

- 行首标签（如 `AGM_000`）、所有头像编号（如 `-31`、`0`、`23`）原样保留，顺序不变。
- 只翻译“文本”字段。字段数量必须与原文完全一致，不能合并或拆分对话框。
- 文本里**绝对不能出现半角冒号 `:`**（它是分隔符），改用全角 `：`。
- 文本开头的 `|数字|` 前缀（如 `|2|`）是过场镜头编号，原样保留在文本最前面。
- 以 `//` 开头的注释行、`-------` 分隔行原样保留。
- 每个输入行对应一个输出行，行数、顺序完全一致。不要添加任何额外说明。
- 不要使用半角竖线 `|`（除了保留的前缀）、反斜杠 `\`、反引号、波浪号 `~`。

## 角色名：保持英文

Orsino、Orsino Jack、Barrod（Lord Barrod 译作“Barrod 大人”）、Boulder、Agmago、Mags（Orsino 对 Agmago 的昵称）、Ciz、Hup、Grampy（可译“爷爷”）。
中文与英文名之间不加空格，例如：“Boulder 递给 Orsino 一本书”中英之间可以加一个半角空格以便阅读，全文保持一致：**中文与英文单词之间加一个半角空格**。

## 指令关键词（原文中全大写的单词）

原文中全大写的单词是玩家需要输入的文字指令。翻译时写成中文并用【】括起来，玩家可以直接输入括号中的中文：

| 英文 | 中文写法 |
|---|---|
| SUGGEST | 【提议】 |
| OFFER | 【提供】 |
| SUMMON | 【召唤】 |
| RESEARCH | 【研究】 |
| LOOK / EXAMINE | 【查看】 |
| SUBMIT | 【臣服】 |
| EXIT / QUIT | 【退出】 |
| HELP | 【帮助】 |
| REPEAT | 【重复】 |
| LEAVE | 【离开】 |
| SHOW | 【展示】 |
| ITEM | 物品（不加括号） |
| BEER | 【啤酒】 |
| CIGAR | 【雪茄】 |
| LIGHT | 【点火】 |
| SMOKE | 【抽烟】 |
| HONEY | 【蜂蜜】 |
| RAZOR | 【剃刀】 |
| SHAVE | 【刮毛】 |
| GRIMOIRE | 【魔典】 |
| FUCK（作为契约条款） | 【上床】 |
| BLOWJOB | 【口交】 |
| MOUTH | 【嘴】 |
| TOUCH | 【触碰】 |
| END / PGDN | END / PGDN（按键名，保持英文不加括号） |

- 示例：`OFFER a FUCK for the GRIMOIRE` → `向我【提供】一次【上床】，换取【魔典】`
- 示例：`OFFER me the RAZOR in exchange for a SHAVE` → `向我【提供】【剃刀】，换取一次【刮毛】`
- 咒语保持英文大写，不加括号：FULMINUS、SOLVUS、PYRAX、GERMINAS、PORTAS、SUNIMLUF、SUVLOS、XARYP、SANIMREG、SATROP。
- 对于不是指令、只是用来强调语气的大写词（如 I AM、THAT、REALLY、WILL FORGET），正常翻译即可，可以不加括号。
- 物品名在非指令语境下（小写出现）正常翻译为同一个中文词但不加括号：beer→啤酒，razor→剃刀，cigar→雪茄，honey→蜂蜜，grimoire→魔典，cumquat→精桔（谐音“金桔”的黄色双关，保留双关）。

## 术语表

| 英文 | 中文 |
|---|---|
| Mortal | 凡人（称呼语） |
| pact | 契约 |
| The pact is writ! | 契约已成！ |
| Thou art beholden to me, and I to thee! | 汝受我之约束，我亦受汝之约束！ |
| thrall | 奴仆 |
| thralldom | 奴役 |
| demon / demonkind | 恶魔 / 恶魔一族 |
| Demon Lord | 魔王 |
| Limbo | 灵薄狱 |
| Grimoire Rosettas | 罗塞塔魔典 |
| incantation | 咒语 |
| ritual | 仪式 |
| lectern | 经台 |
| archive / library | 书库 |
| palace | 宫殿 |
| Hell | 地狱 |
| realm | 界域（mortal realm 凡间） |
| summon | 召唤 |
| Crux of Flesh | 血肉十字 |
| Vortex of Howls | 嚎叫漩涡 |
| Chambre Vitae / Thalamum Vitae | 生命之室 |
| Immolatorium | 焚献室 |
| Eyrie | 鹰巢 |

## 文风

- 忠实原文，保留成人内容、粗口、性描写和双关，不要弱化或审查。
- Orsino：口语化、随性、爱开玩笑、经常爆粗（shit→妈的/靠，fuck→操/他妈的，boner→硬了/勃起）。
- Barrod：华丽、带古风的诱惑腔，用“汝”“吾”“尔”等可适度点缀，整体典雅而危险。
- Agmago：庄重、克制、文雅的古典腔调，略带羞涩。
- Boulder：博学、傲慢中带着急切，偶尔诗意。
- Ciz：伦敦市井口音、油滑，常用昵称（poppet→小宝贝，pup→小崽子，love→亲爱的，deary→亲爱的），可用“咱”“俺”“嘛”等口语体现。
- Hup：按原文语气。
- 旁白（头像编号 0）：中性叙述。
- 标点使用中文全角标点：，。！？“”‘’……——（）。省略号统一用“……”。
- 每个对话框文字长度与原文大致相当，避免过度扩写。
