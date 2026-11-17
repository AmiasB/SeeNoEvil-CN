$ErrorActionPreference = "Stop"
$here = $PSScriptRoot
$bundle = Split-Path $here -Parent

function Find-Game([string]$start) {
	foreach ($dir in @($start, (Split-Path $start -Parent))) {
		if ($dir -and (Test-Path (Join-Path $dir "See_No_Evil.exe"))) {
			return $dir
		}
	}
	return $null
}

$game = Find-Game $bundle
if (-not $game) {
	throw "找不到游戏。请在放进游戏根目录的 SeeNoEvil_CHS 文件夹里运行还原.bat。"
}
if (Get-Process -Name "See_No_Evil" -ErrorAction SilentlyContinue) {
	throw "请先退出 See no Evil，再还原。"
}

$data = Join-Path $game "See_No_Evil_Data"
$backup = Join-Path $data "SNE_CN_backup"
$files = @(
	@{ Name = "Assembly-CSharp.dll"; Live = Join-Path $data "Managed\Assembly-CSharp.dll" },
	@{ Name = "sharedassets0.assets"; Live = Join-Path $data "sharedassets0.assets" },
	@{ Name = "mainData"; Live = Join-Path $data "mainData" },
	@{ Name = "level2"; Live = Join-Path $data "level2" },
	@{ Name = "level3"; Live = Join-Path $data "level3" },
	@{ Name = "level4"; Live = Join-Path $data "level4" },
	@{ Name = "level7"; Live = Join-Path $data "level7" },
	@{ Name = "level8"; Live = Join-Path $data "level8" },
	@{ Name = "GENERIC_DIALOGUE.txt"; Live = Join-Path $game "Assets\TEXT DOCS\GENERIC_DIALOGUE.txt" }
)
foreach ($file in $files) {
	$kept = Join-Path $backup $file.Name
	if (-not (Test-Path -LiteralPath $kept)) {
		throw "没有找到原版备份（See_No_Evil_Data\SNE_CN_backup），无法还原。"
	}
}
foreach ($file in $files) {
	Copy-Item -LiteralPath (Join-Path $backup $file.Name) -Destination $file.Live -Force
}
$helper = Join-Path $data "Managed\SNE_CN.dll"
if (Test-Path $helper) { Remove-Item $helper -Force }
Write-Output "已还原为英文原版。备份仍留在 See_No_Evil_Data\SNE_CN_backup。"
