using System.Collections.Generic;
using System.Text;
#if !TEST
using UnityEngine;
#endif

public static class SNE_CN
{
	private const int MaxLineWidth = 860;

	private const int WideWidth = 32;

	private static readonly int[] AsciiWidths = new int[95]
	{
		12, 12, 14, 18, 16, 18, 18, 10, 12, 12, 20, 16, 10, 16, 8, 20, 16, 16, 16, 16,
		18, 16, 16, 16, 16, 16, 8, 10, 14, 16, 14, 16, 18, 20, 18, 18, 18, 18, 18, 18,
		16, 16, 16, 18, 18, 18, 18, 18, 18, 18, 20, 16, 16, 16, 20, 18, 20, 20, 18, 12,
		16, 12, 18, 18, 16, 18, 18, 16, 18, 16, 16, 20, 18, 12, 16, 18, 12, 18, 16, 16,
		18, 18, 18, 16, 14, 18, 16, 18, 18, 16, 16, 16, 16, 16, 16
	};

	private const string NoLineStart = "，。！？；：、）》」』】”’…—～·,.!?;:)]}%";

	private const string NoLineEnd = "（《「『【“‘([{";

	private static readonly string[][] CommandAliases = new string[][]
	{
		new string[] { "SUGGEST", "提议", "建议", "提出" },
		new string[] { "OFFER", "提供", "献上", "给予", "交易" },
		new string[] { "SUMMON", "召唤" },
		new string[] { "RESEARCH", "研究", "查阅", "查找" },
		new string[] { "LOOK", "查看", "观察", "检查", "端详", "看看", "看" },
		new string[] { "SUBMIT", "臣服", "屈服", "顺从" },
		new string[] { "EXIT", "退出", "离开游戏" },
		new string[] { "HELP", "帮助", "提示", "操作说明" },
		new string[] { "SAVE", "存档", "保存" },
		new string[] { "LOAD", "读档", "读取" },
		new string[] { "REPEAT", "重复" },
		new string[] { "SHOW", "展示", "出示" },
		new string[] { "LEAVE", "离开" },
		new string[] { "TAKE", "拿走", "拿", "拾取", "捡起", "捡" },
		new string[] { "TALK", "交谈", "说话", "对话", "聊天" },
		new string[] { "OPEN", "打开" },
		new string[] { "USE", "使用" },
		new string[] { "GO", "前往", "进入" },
		new string[] { "FORM PACT", "缔结契约", "订立契约", "签订契约" },
		new string[] { "MAKE SPARKS", "制造火花", "擦出火花" },
		new string[] { "PACT", "契约" },
		new string[] { "DEAL", "协议" },
		new string[] { "BEER", "啤酒" },
		new string[] { "CIGAR", "雪茄" },
		new string[] { "LIGHT", "点火", "点烟", "点燃" },
		new string[] { "SMOKE", "抽烟" },
		new string[] { "HONEY", "蜂蜜" },
		new string[] { "GOO", "黏液" },
		new string[] { "JAR", "罐子", "罐" },
		new string[] { "RAZOR", "剃刀" },
		new string[] { "BLADE", "刀刃", "利刃" },
		new string[] { "KNIFE", "小刀", "刀" },
		new string[] { "WEAPON", "武器" },
		new string[] { "SHAVE", "刮毛", "剃毛", "刮" },
		new string[] { "OIL", "油" },
		new string[] { "CUMQUAT", "精桔", "金桔" },
		new string[] { "GRIMOIRE", "魔典", "魔法书" },
		new string[] { "ROSETTAS", "罗塞塔" },
		new string[] { "KNOWLEDGE", "知识" },
		new string[] { "FUCK", "上床", "做爱", "操" },
		new string[] { "SEX", "性爱", "性交" },
		new string[] { "HUMP", "干" },
		new string[] { "BLOWJOB", "口交" },
		new string[] { "ORAL", "口活" },
		new string[] { "SUCK", "吸", "舔" },
		new string[] { "MOUTH", "嘴巴", "嘴" },
		new string[] { "TOUCH", "触碰", "碰触", "抚摸", "触摸", "摸" },
		new string[] { "HUG", "拥抱", "抱抱" },
		new string[] { "HOLD", "抱住", "抱" },
		new string[] { "CUDDLE", "搂抱", "依偎" },
		new string[] { "THRALL", "奴仆" },
		new string[] { "AGMAGO", "阿格玛戈" },
		new string[] { "MAGS", "小玛" },
		new string[] { "BOULDER", "博尔德" },
		new string[] { "CIZ", "西兹" },
		new string[] { "HUP", "哈普" },
		new string[] { "BARROD", "巴罗德" },
		new string[] { "ASSHOLE", "屁眼", "后庭" },
		new string[] { "ANUS", "肛门" },
		new string[] { "ASS", "屁股" },
		new string[] { "BUTT", "臀部" },
		new string[] { "PENIS", "阴茎" },
		new string[] { "DICK", "鸡巴", "老二" },
		new string[] { "BALLS", "蛋蛋" },
		new string[] { "NUTS", "睾丸" },
		new string[] { "BALLSACK", "阴囊" },
		new string[] { "JUNK", "下体" },
		new string[] { "KNOB", "龟头" },
		new string[] { "FORESKIN", "包皮" },
		new string[] { "NIPPLES", "乳头" },
		new string[] { "FEET", "脚" },
		new string[] { "HANDS", "手" },
		new string[] { "BELLY", "肚子" },
		new string[] { "SKIN", "皮肤" }
	};

	private static readonly string[] Fillers = new string[]
	{
		"作为交换", "以换取", "来换取", "换取", "交换", "换", "我的", "一下", "一个", "一次", "出来", "过来",
		"给", "把", "用", "向", "对", "和", "跟", "的", "请", "吧", "了", "你", "他", "我",
		"以", "为", "来", "个", "次", "下", "去", "在", "这", "那", "里"
	};

	private static readonly string[] Verbs = new string[]
	{
		"SUGGEST", "OFFER", "SUMMON", "RESEARCH", "LOOK", "L", "EXAMINE", "EXAM", "EX", "INSPECT", "SUBMIT",
		"EXIT", "QUIT", "HELP", "CONTROLS", "HINT", "SAVE", "LOAD", "REPEAT", "SHOW", "LEAVE", "TAKE", "GET",
		"GRAB", "TALK", "SAY", "GO", "ENTER", "OPEN", "USE", "FORM", "MAKE"
	};

	private static readonly string[] Names = new string[] { "AGMAGO", "MAGS", "BOULDER", "CIZ", "HUP", "BARROD" };

	private static List<KeyValuePair<string, string>> aliasTable;

	public static string Wrap(string wrapped)
	{
		string text = wrapped.Replace('\n', ' ').TrimStart(' ');
		StringBuilder result = new StringBuilder(" ");
		StringBuilder line = new StringBuilder();
		int lineWidth = 0;
		int i = 0;
		while (i < text.Length)
		{
			int end = UnitEnd(text, i);
			while (end < text.Length)
			{
				if (NoLineStart.IndexOf(text[end]) >= 0)
				{
					end++;
				}
				else if (NoLineEnd.IndexOf(text[end - 1]) >= 0 && text[end] != ' ')
				{
					end = UnitEnd(text, end);
				}
				else
				{
					break;
				}
			}
			string token = text.Substring(i, end - i);
			int tokenWidth = Measure(token);
			if (lineWidth + tokenWidth > MaxLineWidth && line.Length > 0)
			{
				result.Append(line.ToString().TrimEnd(' '));
				result.Append('\n');
				line.Length = 0;
				lineWidth = 0;
				token = token.TrimStart(' ');
				tokenWidth = Measure(token);
			}
			line.Append(token);
			lineWidth += tokenWidth;
			i = end;
		}
		result.Append(line.ToString());
		return result.ToString();
	}

	public static string Command(string input)
	{
		if (aliasTable == null)
		{
			BuildAliasTable();
		}
		StringBuilder output = new StringBuilder();
		StringBuilder unknown = new StringBuilder();
		int i = 0;
		while (i < input.Length)
		{
			char c = input[i];
			if (c < '\u0080')
			{
				FlushUnknown(output, unknown);
				output.Append(c);
				i++;
				continue;
			}
			if (char.IsWhiteSpace(c) || char.IsPunctuation(c) || c == '\u3000')
			{
				FlushUnknown(output, unknown);
				output.Append(' ');
				i++;
				continue;
			}
			string match = null;
			string replacement = null;
			foreach (KeyValuePair<string, string> alias in aliasTable)
			{
				if (string.CompareOrdinal(input, i, alias.Key, 0, alias.Key.Length) == 0)
				{
					match = alias.Key;
					replacement = alias.Value;
					break;
				}
			}
			if (match != null)
			{
				FlushUnknown(output, unknown);
				if (replacement.Length > 0)
				{
					output.Append(' ').Append(replacement).Append(' ');
				}
				else
				{
					output.Append(' ');
				}
				i += match.Length;
			}
			else
			{
				unknown.Append(c);
				i++;
			}
		}
		FlushUnknown(output, unknown);
		string[] parts = output.ToString().Split(new char[1] { ' ' }, System.StringSplitOptions.RemoveEmptyEntries);
		if (parts.Length == 0)
		{
			return input;
		}
		return string.Join(" ", VerbFirst(parts));
	}

	private static string[] VerbFirst(string[] parts)
	{
		int verb = -1;
		for (int i = 0; i < parts.Length; i++)
		{
			if (System.Array.IndexOf(Verbs, parts[i].ToUpper()) >= 0)
			{
				verb = i;
				break;
			}
		}
		if (verb <= 0)
		{
			return parts;
		}
		string verbWord = parts[verb].ToUpper();
		bool dropNames = verbWord == "OFFER" || verbWord == "SUGGEST";
		List<string> ordered = new List<string>();
		ordered.Add(parts[verb]);
		for (int i = 0; i < verb; i++)
		{
			if (!dropNames || System.Array.IndexOf(Names, parts[i].ToUpper()) < 0)
			{
				ordered.Add(parts[i]);
			}
		}
		for (int i = verb + 1; i < parts.Length; i++)
		{
			ordered.Add(parts[i]);
		}
		return ordered.ToArray();
	}

#if !TEST
	public static string ShowInput(string typed)
	{
		Input.imeCompositionMode = IMECompositionMode.On;
		Input.compositionCursorPos = new Vector2(Screen.width / 2, Screen.height - 60);
		string composing = Input.compositionString;
		if (string.IsNullOrEmpty(composing))
		{
			return typed;
		}
		return typed + composing;
	}
#endif

	private static void BuildAliasTable()
	{
		aliasTable = new List<KeyValuePair<string, string>>();
		foreach (string[] group in CommandAliases)
		{
			for (int i = 1; i < group.Length; i++)
			{
				aliasTable.Add(new KeyValuePair<string, string>(group[i], group[0]));
			}
		}
		foreach (string filler in Fillers)
		{
			aliasTable.Add(new KeyValuePair<string, string>(filler, string.Empty));
		}
		aliasTable.Sort((KeyValuePair<string, string> a, KeyValuePair<string, string> b) => b.Key.Length.CompareTo(a.Key.Length));
	}

	private static void FlushUnknown(StringBuilder output, StringBuilder unknown)
	{
		if (unknown.Length > 0)
		{
			output.Append(' ').Append(unknown.ToString()).Append(' ');
			unknown.Length = 0;
		}
	}

	private static int UnitEnd(string text, int start)
	{
		int end = start + 1;
		if (IsWordChar(text[start]))
		{
			while (end < text.Length && IsWordChar(text[end]))
			{
				end++;
			}
		}
		return end;
	}

	private static bool IsWordChar(char c)
	{
		return c > ' ' && c < '\u0080';
	}

	private static int Measure(string s)
	{
		int width = 0;
		foreach (char c in s)
		{
			if (c >= ' ' && c < '\u007f')
			{
				width += AsciiWidths[c - ' '];
			}
			else
			{
				width += WideWidth;
			}
		}
		return width;
	}
}
