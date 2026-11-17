$ErrorActionPreference = "Stop"
$here = $PSScriptRoot
$bundle = Split-Path $here -Parent

function Find-Game([string]$start) {
	foreach ($dir in @($start, (Split-Path $start -Parent))) {
		if ($dir -and (Test-Path (Join-Path $dir "See_No_Evil.exe")) -and (Test-Path (Join-Path $dir "See_No_Evil_Data\Managed\Assembly-CSharp.dll"))) {
			return $dir
		}
	}
	return $null
}

$game = Find-Game $bundle
if (-not $game) {
	throw "找不到游戏。请把整个 SeeNoEvil_CHS 文件夹放进游戏根目录，和 See_No_Evil.exe 放在同一层，再运行打补丁.bat。"
}
if (Get-Process -Name "See_No_Evil" -ErrorAction SilentlyContinue) {
	throw "请先退出 See no Evil，再运行打补丁。"
}

$data = Join-Path $game "See_No_Evil_Data"
$managed = Join-Path $data "Managed"
$backup = Join-Path $data "SNE_CN_backup"
New-Item -ItemType Directory -Force -Path $backup | Out-Null

$files = @(
	@{ Name = "Assembly-CSharp.dll"; Live = Join-Path $managed "Assembly-CSharp.dll" },
	@{ Name = "sharedassets0.assets"; Live = Join-Path $data "sharedassets0.assets" },
	@{ Name = "mainData"; Live = Join-Path $data "mainData" },
	@{ Name = "level2"; Live = Join-Path $data "level2" },
	@{ Name = "level3"; Live = Join-Path $data "level3" },
	@{ Name = "level4"; Live = Join-Path $data "level4" },
	@{ Name = "level7"; Live = Join-Path $data "level7" },
	@{ Name = "level8"; Live = Join-Path $data "level8" },
	@{ Name = "GENERIC_DIALOGUE.txt"; Live = Join-Path $game "Assets\TEXT DOCS\GENERIC_DIALOGUE.txt" }
)

$helper = Join-Path $managed "SNE_CN.dll"
$backupDll = Join-Path $backup "Assembly-CSharp.dll"
if ((Test-Path $helper) -and -not (Test-Path $backupDll)) {
	throw "游戏里已经有汉化文件，但没有原版备份（See_No_Evil_Data\SNE_CN_backup）。这次没有改动任何东西。如果装的是旧版补丁，请先运行游戏根目录里的「卸载汉化.bat」。"
}
foreach ($file in $files) {
	if (-not (Test-Path -LiteralPath $file.Live)) {
		throw "找不到 $($file.Live)。请确认这是 See no Evil 完整版。"
	}
	$kept = Join-Path $backup $file.Name
	if (-not (Test-Path -LiteralPath $kept)) {
		Copy-Item -LiteralPath $file.Live -Destination $kept
	}
}

$sha1 = (Get-FileHash -LiteralPath $backupDll -Algorithm SHA1).Hash.ToLower()
$variant = $null
foreach ($line in Get-Content -LiteralPath (Join-Path $here "versions.txt") -Encoding UTF8) {
	if ($line.Trim().Length -eq 0 -or $line.StartsWith("#")) { continue }
	$parts = $line.Split("`t")
	if ($parts[0].ToLower() -eq $sha1) { $variant = $parts[1] }
}
if (-not $variant) {
	throw "这个游戏文件对不上。补丁只对应以前的 Unity 4.1 完整版，和现在官网发的完整版。如果你已经装过旧版补丁，请先还原再重试。"
}

$xd = Join-Path $here "xdelta3.exe"
$diffDir = Join-Path $here $variant
$ready = @()
foreach ($file in $files) {
	if ($file.Name -eq "GENERIC_DIALOGUE.txt") { continue }
	$src = Join-Path $backup $file.Name
	$diff = Join-Path $diffDir ($file.Name + ".vcdiff")
	$tmp = Join-Path $backup ($file.Name + ".patched")
	if (Test-Path -LiteralPath $tmp) { Remove-Item -LiteralPath $tmp -Force }
	& $xd -d -f -s $src $diff $tmp
	if ($LASTEXITCODE -ne 0) {
		Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue
		throw "补丁失败（$($file.Name)）。这个文件不是对应版本的原版文件。"
	}
	$ready += @{ Live = $file.Live; Tmp = $tmp }
}
foreach ($item in $ready) {
	Copy-Item -LiteralPath $item.Tmp -Destination $item.Live -Force
	Remove-Item -LiteralPath $item.Tmp -Force
}
Copy-Item -LiteralPath (Join-Path $here "GENERIC_DIALOGUE.txt") -Destination (Join-Path $game "Assets\TEXT DOCS\GENERIC_DIALOGUE.txt") -Force
Copy-Item -LiteralPath (Join-Path $here "SNE_CN.dll") -Destination $helper -Force
Copy-Item -LiteralPath (Join-Path $here "SeeNoEvil中文攻略.txt") -Destination (Join-Path $game "SeeNoEvil中文攻略.txt") -Force
Write-Output "补丁已装好。原版文件在 See_No_Evil_Data\SNE_CN_backup。中文攻略在游戏根目录。启动游戏即可。"
