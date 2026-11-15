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

var used = new HashSet<(string, string)>();
foreach (var type in module.Types)
{
	foreach (var method in type.Methods.Where(m => m.HasBody))
	{
		foreach (var ins in method.Body.Instructions.Where(i => i.OpCode == OpCodes.Ldstr))
		{
			var key = (type.Name, (string)ins.Operand);
			if (replacements.TryGetValue(key, out var value))
			{
				ins.Operand = value;
				used.Add(key);
			}
		}
	}
}
foreach (var key in replacements.Keys.Where(k => !used.Contains(k)))
{
	throw new Exception($"string not found: {key.Item1} {key.Item2}");
}
Console.WriteLine($"replaced {used.Count} string literals");

assembly.Write(outputPath);
Console.WriteLine("wrote " + outputPath);

static string Unescape(string s) => s.Replace("\\n", "\n").Replace("\\t", "\t");
