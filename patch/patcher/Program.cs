using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Mono.Cecil;
using Mono.Cecil.Cil;

// Usage: patcher <original Assembly-CSharp.dll> <SNE_CN.dll> <strings.tsv> <output dll>
string sourcePath = args[0];
string helperPath = args[1];
string stringsPath = args[2];
string outputPath = args[3];

var resolver = new DefaultAssemblyResolver();
resolver.AddSearchDirectory(Path.GetDirectoryName(Path.GetFullPath(sourcePath)));
resolver.AddSearchDirectory(Path.GetDirectoryName(Path.GetFullPath(helperPath)));
var readerParams = new ReaderParameters { AssemblyResolver = resolver };

var assembly = AssemblyDefinition.ReadAssembly(sourcePath, readerParams);
var module = assembly.MainModule;
var helper = AssemblyDefinition.ReadAssembly(helperPath, readerParams).MainModule.GetType("SNE_CN");
MethodReference Helper(string name) => module.ImportReference(helper.Methods.Single(m => m.Name == name));

MethodDefinition Method(string type, string name) =>
	module.GetType(type).Methods.Single(m => m.Name == name);

bool IsLdloc(Instruction i) =>
	i.OpCode == OpCodes.Ldloc || i.OpCode == OpCodes.Ldloc_S || i.OpCode == OpCodes.Ldloc_0 ||
	i.OpCode == OpCodes.Ldloc_1 || i.OpCode == OpCodes.Ldloc_2 || i.OpCode == OpCodes.Ldloc_3;

// TextScript.Update: `Text = text3;` after the space-based word wrap loop.
{
	var update = Method("TextScript", "Update");
	var targets = update.Body.Instructions
		.Where(i => i.OpCode == OpCodes.Stfld && ((FieldReference)i.Operand).Name == "Text" && IsLdloc(i.Previous))
		.ToList();
	if (targets.Count != 1)
	{
		throw new Exception($"TextScript.Update: expected 1 wrap store, found {targets.Count}");
	}
	update.Body.GetILProcessor().InsertBefore(targets[0], Instruction.Create(OpCodes.Call, Helper("Wrap")));
	Console.WriteLine("patched TextScript.Update wrap");
}

// TextLoader.ParseTextCommand: InputText = SNE_CN.Command(InputText) before anything else.
{
	var parse = Method("TextLoader", "ParseTextCommand");
	var field = module.GetType("TextLoader").Fields.Single(f => f.Name == "InputText");
	var il = parse.Body.GetILProcessor();
	var first = parse.Body.Instructions[0];
	il.InsertBefore(first, Instruction.Create(OpCodes.Ldarg_0));
	il.InsertBefore(first, Instruction.Create(OpCodes.Ldarg_0));
	il.InsertBefore(first, Instruction.Create(OpCodes.Ldfld, field));
	il.InsertBefore(first, Instruction.Create(OpCodes.Call, Helper("Command")));
	il.InsertBefore(first, Instruction.Create(OpCodes.Stfld, field));
	Console.WriteLine("patched TextLoader.ParseTextCommand");
}

// TextLoader.OnGUI: textMesh.text = InputText  ->  textMesh.text = SNE_CN.ShowInput(InputText)
{
	var onGui = Method("TextLoader", "OnGUI");
	var targets = onGui.Body.Instructions
		.Where(i => i.OpCode == OpCodes.Ldfld && ((FieldReference)i.Operand).Name == "InputText" &&
			i.Next.OpCode == OpCodes.Callvirt && ((MethodReference)i.Next.Operand).Name == "set_text")
		.ToList();
	if (targets.Count != 1)
	{
		throw new Exception($"TextLoader.OnGUI: expected 1 input display, found {targets.Count}");
	}
	onGui.Body.GetILProcessor().InsertAfter(targets[0], Instruction.Create(OpCodes.Call, Helper("ShowInput")));
	Console.WriteLine("patched TextLoader.OnGUI");
}

// Displayed string literals. TSV columns: type, original, replacement (\n escapes allowed).
var replacements = new Dictionary<(string, string), string>();
foreach (var line in File.ReadAllLines(stringsPath))
{
	if (line.Length == 0 || line.StartsWith("#"))
	{
		continue;
	}
	var cols = line.Split('\t');
	if (cols.Length != 3)
	{
		throw new Exception("bad strings.tsv line: " + line);
	}
	replacements[(cols[0], Unescape(cols[1]))] = Unescape(cols[2]);
}

int replaced = 0;
foreach (var entry in replacements)
{
	string typeName = entry.Key.Item1;
	string english = entry.Key.Item2;
	string chinese = entry.Value;
	int count = ReplaceLiteral(module, typeName, english, chinese);
	if (count == 0)
	{
		count = ReplaceLiteral(module, null, english, chinese);
	}
	if (count == 0)
	{
		Console.WriteLine("skip, not in this build: " + typeName + " " + english.Replace("\n", "\\n"));
		continue;
	}
	replaced += count;
}
Console.WriteLine($"replaced {replaced} string literals");

assembly.Write(outputPath);
Console.WriteLine("wrote " + outputPath);

static int ReplaceLiteral(ModuleDefinition module, string typeName, string english, string chinese)
{
	int count = 0;
	foreach (var type in module.Types)
	{
		if (typeName != null && type.Name != typeName)
		{
			continue;
		}
		foreach (var method in type.Methods.Where(m => m.HasBody))
		{
			foreach (var ins in method.Body.Instructions.Where(i => i.OpCode == OpCodes.Ldstr && (string)i.Operand == english))
			{
				ins.Operand = chinese;
				count++;
			}
		}
	}
	return count;
}

static string Unescape(string s) => s.Replace("\\n", "\n").Replace("\\t", "\t");
