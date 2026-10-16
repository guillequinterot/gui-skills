#requires -Version 5.1
<#
Instala el stack para usar Shotcut vía shotcut-mcp + la skill video-editing-ai-agent en este equipo (Windows). Verificado solo en el equipo del mantenedor (Windows 11).
  -DryRun    muestra lo que haría sin cambiar nada
  -SkillOnly solo enlaza la skill en ~\.claude\skills (si aun no esta)
  -McpCommit commit de shotcut-mcp a fijar (por defecto el probado)
  -WithHyperFrames comprueba los requisitos de HyperFrames (Node>=22, navegador headless) y desactiva su telemetria; NO renderiza ni descarga navegadores
No pide ni guarda claves. Idempotente: si algo ya existe, lo omite.
#>
param([switch]$DryRun, [switch]$SkillOnly, [switch]$WithHyperFrames, [string]$McpCommit = "f1b78d350a9992296f0b7f11a55c04819ea25730")

$ErrorActionPreference = "Stop"
$skillSrc = Split-Path -Parent $PSScriptRoot           # carpeta video-editing-ai-agent
$claudeDir = Join-Path $env:USERPROFILE ".claude"
$skillDst = Join-Path $claudeDir "skills\video-editing-ai-agent"
$mcpDir = Join-Path $claudeDir "mcp-servers\shotcut-mcp"
$sc = Join-Path $env:LOCALAPPDATA "Programs\Shotcut"

function Step($m) { Write-Host "==> $m" -ForegroundColor Cyan }
function Do-It($desc, [scriptblock]$act) { if ($DryRun) { Write-Host "   [dry-run] $desc" -ForegroundColor Yellow } else { & $act } }

# 1. Skill (en el repo gui-skills la instala tools/install.ps1 como enlace a ~/.claude/skills; aqui solo se comprueba)
Step "Skill -> $skillDst"
if ((Resolve-Path $skillSrc).Path -ieq (Resolve-Path (Split-Path $skillDst -Parent)).Path + "\video-editing-ai-agent") {
    Write-Host "   La skill ya se ejecuta desde su destino; nada que hacer."
} elseif (Test-Path $skillDst) {
    Write-Host "   La skill ya esta instalada en el destino (enlace o carpeta); no se copia. Si es una copia vieja, reemplazala por el enlace del repo (tools/install.ps1)."
} else {
    Do-It "crear enlace (junction) $skillDst -> $skillSrc" {
        New-Item -ItemType Directory -Force (Split-Path $skillDst -Parent) | Out-Null
        New-Item -ItemType Junction -Path $skillDst -Target $skillSrc | Out-Null
        Write-Host "   enlazada (la memoria de la skill queda en el repo, en memoria/)."
    }
}
if ($SkillOnly) { Write-Host "Listo (solo skill). Reinicia Claude Code."; return }

# 2. Requisitos
Step "Comprobando requisitos"
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) { throw "Python no encontrado. Instala Python 3.10+ y vuelve a ejecutar." }
$pyv = (python --version) 2>&1
Write-Host "   $pyv"
if (-not (Get-Command git -ErrorAction SilentlyContinue)) { throw "Git no encontrado." }
if (-not (Get-Command claude -ErrorAction SilentlyContinue)) { throw "CLI 'claude' no encontrado en PATH (necesario para registrar el MCP)." }

# 3. Shotcut
Step "Shotcut"
if (Test-Path (Join-Path $sc "melt.exe")) { Write-Host "   ya instalado en $sc" }
else {
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) { throw "winget no disponible: instala Shotcut 26.8.1 desde shotcut.org y vuelve a ejecutar." }
    Do-It "winget install --id Meltytech.Shotcut" { winget install --id Meltytech.Shotcut --accept-package-agreements --accept-source-agreements }
}

# 4. Paquetes Python
Step "Paquetes Python (faster-whisper, pillow, numpy, yt-dlp)"
Do-It "pip install faster-whisper pillow numpy yt-dlp[default]" { python -m pip install --quiet faster-whisper pillow numpy "yt-dlp[default]" }

# 5. shotcut-mcp
Step "shotcut-mcp -> $mcpDir"
if (Test-Path (Join-Path $mcpDir "scripts\shotcut_mcp_server.py")) { Write-Host "   ya clonado." }
else {
    Do-It "git clone matrodrigs/shotcut-mcp + checkout $McpCommit" {
        New-Item -ItemType Directory -Force (Split-Path $mcpDir -Parent) | Out-Null
        git clone https://github.com/matrodrigs/shotcut-mcp $mcpDir
        git -C $mcpDir checkout $McpCommit
    }
}

# 6. Registro MCP (ámbito usuario) — ejecutar desde una carpeta neutra
Step "Registro MCP 'shotcut' (ámbito usuario)"
$already = $false
try { Push-Location $env:USERPROFILE; $already = ((claude mcp list 2>&1) | Select-String "^shotcut:" ) -ne $null } finally { Pop-Location }
if ($already) { Write-Host "   ya registrado (claude mcp list)." }
else {
    $cfg = @{ type = "stdio"; command = "python"
        args = @((Join-Path $mcpDir "scripts\shotcut_mcp_server.py"))
        env = @{ SHOTCUT_PATH = "$sc\shotcut.exe"; SHOTCUT_MELT_PATH = "$sc\melt.exe"; SHOTCUT_FFMPEG_PATH = "$sc\ffmpeg.exe"; SHOTCUT_FFPROBE_PATH = "$sc\ffprobe.exe" } } | ConvertTo-Json -Depth 5 -Compress
    Do-It "claude mcp add-json --scope user shotcut <json>" {
        Push-Location $env:USERPROFILE
        try { claude mcp add-json --scope user shotcut $cfg } finally { Pop-Location }
    }
}

# 7. HyperFrames (opcional): solo comprueba requisitos; no descarga navegadores ni renderiza
if ($WithHyperFrames) {
    Step "HyperFrames (requisitos)"
    $node = Get-Command node -ErrorAction SilentlyContinue
    if (-not $node) { Write-Host "   FALTA Node.js >= 22 (https://nodejs.org)" -ForegroundColor Yellow }
    else {
        $nv = (node --version).TrimStart("v")
        if ([int]($nv.Split(".")[0]) -lt 22) { Write-Host "   Node $nv es anterior a 22: actualiza." -ForegroundColor Yellow } else { Write-Host "   Node $nv OK" }
    }
    $pw = Join-Path $env:LOCALAPPDATA "ms-playwright"
    $shell = $null
    if (Test-Path $pw) { $shell = Get-ChildItem $pw -Recurse -Filter "chrome-headless-shell.exe" -ErrorAction SilentlyContinue | Select-Object -Last 1 }
    if ($shell) { Write-Host "   navegador headless: $($shell.FullName)" }
    else { Write-Host "   FALTA un chrome-headless-shell. En Windows 'chrome.exe --version' abre el navegador completo y HyperFrames se agota; ver references/engine-hyperframes.md (sugerencia SIN PROBAR: npx playwright install chromium-headless-shell)." -ForegroundColor Yellow }
    Do-It "npx hyperframes telemetry disable" { npx --yes hyperframes@0.8.162 telemetry disable }
    Write-Host "   Variables de entorno por proyecto (no globales): HYPERFRAMES_BROWSER_PATH, HYPERFRAMES_FFMPEG_PATH, HYPERFRAMES_FFPROBE_PATH (bloque en references/engine-hyperframes.md)"
}

Step "Fin"
Write-Host @"
Siguiente:
  1) Reinicia Claude Code (las tools mcp__shotcut__* aparecen en sesión nueva).
  2) Verifica:  claude mcp list   ->  shotcut: Connected
  3) En Claude Code: 'ejecuta shotcut_status y shotcut_doctor'  (esperado: doctor status=tested)
  4) python "$skillDst\scripts\handshake.py"
  5) python "$skillDst\scripts\selftest.py"   (esperado: todas las pruebas OK)
"@
