$ErrorActionPreference = "Stop"
$here = $PSScriptRoot
$work = Split-Path $here
$managed = "e:\T File\SNE_FULL\See_No_Evil_Data\Managed"
$csc = "C:\Program Files\dotnet\sdk\10.0.202\Roslyn\bincore\csc.dll"

Set-Location $here
python make_strings.py
dotnet $csc -nologo -noconfig -nostdlib -target:library -langversion:7.3 -optimize "-out:SNE_CN.dll" `
    "-r:$managed\mscorlib.dll" "-r:$managed\System.dll" "-r:$managed\UnityEngine.dll" SNE_CN.cs
if ($LASTEXITCODE) { throw "csc failed" }
dotnet run --project patcher -- "$work\backup\Assembly-CSharp.dll" "$here\SNE_CN.dll" "$here\strings.tsv" "$here\Assembly-CSharp.dll"
if ($LASTEXITCODE) { throw "patcher failed" }
