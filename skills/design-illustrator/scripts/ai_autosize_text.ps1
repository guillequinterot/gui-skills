# ai_autosize_text.ps1 — activa «Tamaño automático» en TODOS los textos de área del documento ACTIVO de Illustrator,
# para que cada caja se ajuste a su texto (y crezca/encoja sola al editar).
#
# POR QUÉ ASÍ: Illustrator NO expone esa casilla por script (no existe autoSize/autoSizing en TextFrameItem). La única vía
# verificada es: seleccionar los textos de área -> abrir «Opciones de texto de área» (executeMenuCommand 'areatextoptions',
# con alertas activadas) -> marcar la casilla -> OK. Este script hace el clic por ti, pero MUEVE EL RATÓN: no toques el
# ratón ni el teclado hasta que termine (unos 10 s). Con muchos objetos seleccionados la casilla sale en estado intermedio
# (cuadro con «–»): un clic la deja marcada (azul).
#
# Uso: powershell -NoProfile -File ai_autosize_text.ps1 [-NoVerify]
# Requiere: Illustrator con el documento abierto y SIN otro cuadro de diálogo abierto. El cuadro cuelga a Illustrator para
# cualquier script mientras esté abierto.
# Calibrado con Illustrator 31 (Beta) en español a 125 % de escala; los clics son proporcionales al tamaño de la ventana.
param([switch]$NoVerify, [string]$Shots = "")   # -Shots <carpeta>: guarda capturas del cuadro (antes/después de pulsar) para depurar
$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Drawing
Add-Type @"
using System; using System.Text; using System.Runtime.InteropServices; using System.Collections.Generic;
public class AiWin {
  public delegate bool EnumProc(IntPtr h, IntPtr l);
  [DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc p, IntPtr l);
  [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
  [DllImport("user32.dll")] public static extern IntPtr SendMessageTimeout(IntPtr h, uint msg, IntPtr w, StringBuilder l, uint flags, uint timeout, out IntPtr res);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool SetWindowPos(IntPtr h, IntPtr after, int x, int y, int cx, int cy, uint flags);
  [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
  [DllImport("user32.dll")] public static extern void mouse_event(uint f, uint x, uint y, uint d, UIntPtr e);
  [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int L, T, R, B; }
  // título de una ventana SIN colgarse si la app está ocupada (WM_GETTEXT con timeout)
  public static string Title(IntPtr h) { var sb = new StringBuilder(256); IntPtr r; SendMessageTimeout(h, 0x000D, (IntPtr)256, sb, 2, 400, out r); return sb.ToString(); }
  public static IntPtr Find(uint pid, string[] titles) {
    IntPtr found = IntPtr.Zero;
    EnumWindows((h, l) => { uint p; GetWindowThreadProcessId(h, out p); if (p == pid && IsWindowVisible(h)) { string t = Title(h); foreach (var x in titles) if (t.IndexOf(x, StringComparison.OrdinalIgnoreCase) >= 0) { found = h; return false; } } return true; }, IntPtr.Zero);
    return found;
  }
  public static void Click(int x, int y) { SetCursorPos(x, y); System.Threading.Thread.Sleep(200); mouse_event(2, 0, 0, 0, UIntPtr.Zero); System.Threading.Thread.Sleep(80); mouse_event(4, 0, 0, 0, UIntPtr.Zero); System.Threading.Thread.Sleep(700); }
}
"@
[AiWin]::SetProcessDPIAware() | Out-Null
$aiProc = Get-Process Illustrator -ErrorAction Stop | Select-Object -First 1
$ai = New-Object -ComObject Illustrator.Application

# 1) seleccionar los textos de área y abrir el cuadro (la llamada bloquea hasta que el cuadro se cierre: va en un trabajo aparte)
$sel = $ai.DoJavaScript(@"
var d = app.activeDocument, sel = [];
for (var i = 0; i < d.textFrames.length; i++) { if (d.textFrames[i].kind == TextType.AREATEXT) sel.push(d.textFrames[i]); }
d.selection = sel;
d.name + ': ' + sel.length + ' textos de area seleccionados';
"@)
Write-Host $sel
$job = Start-Job -ScriptBlock {
    $a = New-Object -ComObject Illustrator.Application
    $a.DoJavaScript("app.userInteractionLevel = UserInteractionLevel.DISPLAYALERTS; app.executeMenuCommand('areatextoptions'); 'cerrado';")
}
$titles = @("Opciones de texto de", "Area Type Options")   # ASCII: el título completo es «Opciones de texto de área»
$h = [IntPtr]::Zero
for ($k = 0; $k -lt 40 -and $h -eq [IntPtr]::Zero; $k++) { Start-Sleep -Milliseconds 400; $h = [AiWin]::Find([uint32]$aiProc.Id, $titles) }
if ($h -eq [IntPtr]::Zero) { Stop-Job $job; throw "No apareció el cuadro «Opciones de texto de área». ¿Hay textos de área seleccionados y ningún otro diálogo abierto?" }

# 2) traerlo al frente (TOPMOST: SetForegroundWindow falla si otra ventana tiene el foco) y pulsar la casilla
[AiWin]::SetWindowPos($h, [IntPtr](-1), 0, 0, 0, 0, 0x43) | Out-Null
Start-Sleep -Milliseconds 600
$r = New-Object AiWin+RECT
[AiWin]::GetWindowRect($h, [ref]$r) | Out-Null
$w = $r.R - $r.L; $ht = $r.B - $r.T
function PosX([double]$f) { return [int]($r.L + $f * $w) }
function PosY([double]$f) { return [int]($r.T + $f * $ht) }
$cx = PosX (37 / 606); $cy = PosY (648 / 765)
function Shot([string]$name) {
    if (-not $Shots) { return }
    New-Item -ItemType Directory -Force $Shots | Out-Null
    $bmp = New-Object System.Drawing.Bitmap $w, $ht
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.CopyFromScreen($r.L, $r.T, 0, 0, (New-Object System.Drawing.Size $w, $ht))
    $bmp.Save((Join-Path $Shots $name)); $bmp.Dispose()
}
Write-Host ("ventana del cuadro: {0},{1} {2}x{3}; casilla en {4},{5}" -f $r.L, $r.T, $w, $ht, $cx, $cy)
Shot "dialogo-antes.png"

function IsChecked {
    # el centro de la casilla marcada es la «palomita» blanca: se muestrean las esquinas del cuadro (azul si está marcada)
    foreach ($off in @(@(-5, -5), @(5, -5), @(-5, 5), @(5, 5))) {
        $bmp = New-Object System.Drawing.Bitmap 3, 3
        $g = [System.Drawing.Graphics]::FromImage($bmp)
        $g.CopyFromScreen($cx + $off[0] - 1, $cy + $off[1] - 1, 0, 0, (New-Object System.Drawing.Size 3, 3))
        $c = $bmp.GetPixel(1, 1)
        $bmp.Dispose()
        if ($c.B -gt 180 -and $c.R -lt 130 -and ($c.B - $c.R) -gt 80) { return $true }
    }
    return $false
}
$ok = $false
for ($try = 0; $try -lt 2 -and -not $ok; $try++) {
    [AiWin]::Click($cx, $cy)
    Shot "dialogo-despues-$try.png"
    $ok = IsChecked
    if (-not $ok) { Write-Host "casilla aún sin marcar (intento $($try + 1))" }
}
if (-not $ok) {
    [AiWin]::Click((PosX (521 / 606)), (PosY (702 / 765)))     # Cancelar
    Wait-Job $job -Timeout 20 | Out-Null
    throw "No se pudo marcar «Tamaño automático». Hazlo a mano: Texto > Opciones de texto de área > Tamaño automático > OK (los textos de área ya están seleccionados)."
}
[AiWin]::Click((PosX (400 / 606)), (PosY (702 / 765)))         # OK
Wait-Job $job -Timeout 60 | Out-Null
Receive-Job $job | Out-Null

# 3) verificar: con el tamaño automático la caja mide casi exactamente lo que ocupa su texto
if (-not $NoVerify) {
    Write-Host ($ai.DoJavaScript(@"
var d = app.activeDocument, n = 0, aj = 0;
for (var i = 0; i < d.textFrames.length; i++) {
  var t = d.textFrames[i];
  if (t.kind != TextType.AREATEXT) continue;
  n++;
  var ca = t.textRange.characterAttributes;
  if (t.height <= t.lines.length * ca.leading + ca.size * 0.6) aj++;
}
d.selection = null;
'textos de area=' + n + ' | con la altura ajustada al texto=' + aj + (aj == n ? ' (TODOS)' : ' (revisar los demas)');
"@))
}
Write-Host "Guarda el documento (Ctrl+S) si el resultado es correcto."
