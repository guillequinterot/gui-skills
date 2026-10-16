<#
.SYNOPSIS
  Instalador de gui-skills para Windows. Es idempotente: se puede volver a correr sin riesgo.
.DESCRIPTION
  Clona el repo (si falta), crea ~/.gui-skills, enlaza cada skill en ~/.claude/skills con una
  junction, activa los hooks de git y agrega el aviso de actualización a SessionStart.
.EXAMPLE
  powershell -ExecutionPolicy Bypass -File tools\install.ps1 -Alias ana
#>
[CmdletBinding()]
param(
  [string]$RepoUrl = 'https://github.com/guillequinterot/gui-skills.git',
  [string]$RepoDir = '',
  [string]$Alias = '',
  [string]$HomeDir = '',
  [switch]$NoHook
)

$ErrorActionPreference = 'Stop'

function Say([string]$m) { Write-Host $m }
function Fail([string]$m) { Write-Host "ERROR: $m" -ForegroundColor Red; exit 1 }
function Invoke-Native {
  # run a native command without PowerShell 5.1 turning stderr into errors
  $prev = $ErrorActionPreference; $ErrorActionPreference = 'Continue'
  try { & $args[0] @($args | Select-Object -Skip 1) } finally { $ErrorActionPreference = $prev }
}
function Write-Utf8([string]$Path, [string]$Text) {
  [System.IO.File]::WriteAllText($Path, $Text, (New-Object System.Text.UTF8Encoding($false)))
}
function Norm([string]$p) {
  $p = $p -replace '^\\\\\?\\', ''
  return [System.IO.Path]::GetFullPath($p).TrimEnd('\').ToLowerInvariant()
}

if (-not $HomeDir) { $HomeDir = [Environment]::GetFolderPath('UserProfile') }
if (-not (Test-Path -LiteralPath $HomeDir)) { Fail "No existe la carpeta HOME: $HomeDir" }
$HomeDir = (Resolve-Path -LiteralPath $HomeDir).Path

if (-not (Get-Command git -ErrorAction SilentlyContinue)) { Fail 'Falta git. Instálalo (git-scm.com) y vuelve a correr este script.' }

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$selfRoot = Split-Path -Parent $scriptDir
if (-not $RepoDir) {
  if ((Test-Path -LiteralPath (Join-Path $selfRoot '.git')) -and (Test-Path -LiteralPath (Join-Path $selfRoot 'skills'))) {
    $RepoDir = $selfRoot
  } else {
    $RepoDir = Join-Path $HomeDir 'gui-skills'
  }
}
$guiDir = Join-Path $HomeDir '.gui-skills'
$skillsDir = Join-Path $HomeDir '.claude\skills'
$backup = Join-Path $guiDir ('backup-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
$script:backupMade = $false
function Ensure-Backup { if (-not $script:backupMade) { New-Item -ItemType Directory -Force -Path $backup | Out-Null; $script:backupMade = $true } }

# Python >= 3.9 (needed by the update hook)
$pyCmd = $null
foreach ($cand in @(@('python'), @('python3'), @('py', '-3'))) {
  if (-not (Get-Command $cand[0] -ErrorAction SilentlyContinue)) { continue }
  try {
    $extra = @($cand | Select-Object -Skip 1)
    Invoke-Native $cand[0] @extra -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)' 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) { $pyCmd = $cand; break }
  } catch { }
}

# 1. Clone
if (Test-Path -LiteralPath (Join-Path $RepoDir '.git')) {
  Say "[1/6] Repo ya clonado en $RepoDir"
} else {
  if ((Test-Path -LiteralPath $RepoDir) -and (Get-ChildItem -LiteralPath $RepoDir -Force | Select-Object -First 1)) {
    Fail "$RepoDir existe y no es un clon de git. Elige otra ruta con -RepoDir."
  }
  Say "[1/6] Clonando $RepoUrl en $RepoDir"
  Invoke-Native git clone $RepoUrl $RepoDir
  if ($LASTEXITCODE -ne 0) { Fail 'No se pudo clonar. Si ves 401/403, revisa la sección Credenciales del README.' }
}
if (-not (Test-Path -LiteralPath (Join-Path $RepoDir 'skills'))) { Fail "No hay carpeta skills\ en $RepoDir; ¿es el repo correcto?" }
$RepoDir = (Resolve-Path -LiteralPath $RepoDir).Path

# 2. Private config (outside the repo)
New-Item -ItemType Directory -Force -Path $guiDir | Out-Null
$configPath = Join-Path $guiDir 'config.json'
if (Test-Path -LiteralPath $configPath) {
  Say '[2/6] config.json ya existe (no se toca)'
} else {
  $aliasVal = $Alias
  if (-not $aliasVal) {
    try { $aliasVal = Read-Host 'Tu alias (se usa en tus commits y ramas, p. ej. "ana")' } catch { $aliasVal = '' }
  }
  if (-not $aliasVal) { Fail 'Falta el alias: vuelve a correr con -Alias <nombre>.' }
  $aliasVal = ($aliasVal.Trim().ToLowerInvariant() -replace '\s+', '-')
  if ($aliasVal -notmatch '^[a-z0-9][a-z0-9_-]{1,30}$') { Fail 'Alias inválido: usa 2 a 31 caracteres, minúsculas, números, guion o guion bajo.' }
  $cfg = [ordered]@{ alias = $aliasVal; repo_path = $RepoDir }
  Write-Utf8 $configPath (($cfg | ConvertTo-Json) + "`n")
  Say "[2/6] Creado $configPath (alias: $aliasVal)"
}
$termsPath = Join-Path $guiDir 'private-terms.txt'
if (-not (Test-Path -LiteralPath $termsPath)) {
  $terms = @'
# Lista PRIVADA de términos que nunca deben entrar al repo gui-skills (vive solo en esta computadora).
# Una entrada por línea. Texto plano = coincidencia sin distinguir mayúsculas, palabra completa.
# Prefijo "re:" = expresión regular (Python), distingue mayúsculas.
# Las líneas que empiezan con # son comentarios.
#
# Ejemplos (bórralos y escribe los tuyos: tus clientes, marcas, personas, dominios):
# NombreDeUnCliente
# re:PROY-\d{3}
'@
  Write-Utf8 $termsPath ($terms + "`n")
  Say "      Creada la plantilla $termsPath (escribe ahí tus clientes y marcas)"
}
$eqPath = Join-Path $guiDir 'equivalencias.md'
if (-not (Test-Path -LiteralPath $eqPath)) {
  $eq = "# Equivalencias código de caso -> cliente (SOLO en esta computadora, nunca en el repo)`n`n| Código de caso | Cliente / proyecto real |`n|---|---|`n"
  Write-Utf8 $eqPath $eq
}

# 3. Link skills (junctions: no admin rights needed)
Say "[3/6] Enlazando skills en $skillsDir"
New-Item -ItemType Directory -Force -Path $skillsDir | Out-Null
$linked = 0; $kept = 0
foreach ($dir in (Get-ChildItem -LiteralPath (Join-Path $RepoDir 'skills') -Directory | Sort-Object Name)) {
  $name = $dir.Name
  $src = $dir.FullName
  if (-not (Test-Path -LiteralPath (Join-Path $src 'SKILL.md'))) { Say "      - ${name}: sin SKILL.md, se omite"; continue }
  $target = Join-Path $skillsDir $name
  $existing = Get-Item -LiteralPath $target -Force -ErrorAction SilentlyContinue
  if ($existing) {
    $isLink = [bool]($existing.Attributes -band [System.IO.FileAttributes]::ReparsePoint)
    if ($isLink) {
      $cur = $existing.Target | Select-Object -First 1
      if ($cur -and ((Norm $cur) -eq (Norm $src))) { Say "      = ${name}: ya enlazada"; $kept++; continue }
      Ensure-Backup
      Add-Content -LiteralPath (Join-Path $backup 'enlaces-reemplazados.txt') -Value "$name -> $cur" -Encoding UTF8
      [System.IO.Directory]::Delete($target)   # removes the link only, never the target's contents
    } else {
      Ensure-Backup
      try { Move-Item -LiteralPath $target -Destination (Join-Path $backup $name) }
      catch { Fail "No pude mover $target al respaldo (¿abierto en otro programa?): $($_.Exception.Message)" }
      Say "      * ${name}: copia anterior movida a $(Join-Path $backup $name)"
    }
  }
  New-Item -ItemType Junction -Path $target -Value $src | Out-Null
  Say "      + $name"; $linked++
}

# 4. Git config
Say '[4/6] Configurando git en el clon'
Invoke-Native git -C $RepoDir config core.hooksPath .githooks
$curName = (Invoke-Native git -C $RepoDir config --local --get user.name 2>$null)
if (-not $curName) {
  $aliasNow = (Get-Content -LiteralPath $configPath -Raw -Encoding UTF8 | ConvertFrom-Json).alias
  if ($aliasNow) { Invoke-Native git -C $RepoDir config user.name $aliasNow }
}
$curMail = (Invoke-Native git -C $RepoDir config --local --get user.email 2>$null)
if (-not $curMail) {
  $aliasNow = (Get-Content -LiteralPath $configPath -Raw -Encoding UTF8 | ConvertFrom-Json).alias
  if ($aliasNow) { Invoke-Native git -C $RepoDir config user.email "$aliasNow@gui-skills.local" }
}

# 5. SessionStart hook (merged by Python so existing hooks are kept)
$settings = Join-Path $HomeDir '.claude\settings.json'
if ($NoHook) {
  Say '[5/6] Hook de actualización omitido (-NoHook)'
} elseif (-not $pyCmd) {
  Say '[5/6] No encuentro Python 3.9+, omito el hook. Instala Python y vuelve a correr este script.'
} else {
  Say "[5/6] Hook SessionStart en $settings"
  $pyExe = $pyCmd[0]; $pyPre = @($pyCmd | Select-Object -Skip 1)
  $pyName = ($pyCmd -join ' ')
  Invoke-Native $pyExe @pyPre (Join-Path $RepoDir 'tools\settings_hook.py') --settings $settings `
    --python $pyName --script (Join-Path $RepoDir 'tools\check_update.py') --backup-dir $backup
  if ($LASTEXITCODE -ne 0) { Fail 'No se pudo actualizar settings.json (no se modificó). Revisa el mensaje de arriba.' }
}

# 6. Summary
Say "[6/6] Listo. Enlaces nuevos: $linked, ya correctos: $kept."
if ($script:backupMade) { Say "Respaldos en: $backup" }
Say ''
Say "Falta un paso manual: abre $(Join-Path $HomeDir '.claude\CLAUDE.md') y pega el bloque de"
Say "  $(Join-Path $RepoDir 'templates\CLAUDE-snippet.md')"
Say '(el instalador no edita tu CLAUDE.md). Después reinicia Claude Code.'
