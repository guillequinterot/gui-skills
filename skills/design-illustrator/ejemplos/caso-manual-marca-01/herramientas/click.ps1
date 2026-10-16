param([int]$dx, [int]$dy, [string]$shotName)
Add-Type -AssemblyName System.Drawing
Add-Type @"
using System; using System.Runtime.InteropServices;
public class C { [DllImport("user32.dll")] public static extern bool SetCursorPos(int x, int y);
 [DllImport("user32.dll")] public static extern void mouse_event(uint f, uint x, uint y, uint d, UIntPtr e);
 [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
 [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
 [DllImport("user32.dll")] public static extern bool SetProcessDPIAware();
 [DllImport("user32.dll")] public static extern bool SetWindowPos(IntPtr h, IntPtr after, int x, int y, int cx, int cy, uint flags);
 [DllImport("user32.dll")] public static extern bool IsWindow(IntPtr h);
 [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
 [StructLayout(LayoutKind.Sequential)] public struct RECT { public int L, T, R, B; } }
"@
[C]::SetProcessDPIAware() | Out-Null
$h = [IntPtr]2297610
"existe=" + [C]::IsWindow($h) + " visible=" + [C]::IsWindowVisible($h)
[C]::SetWindowPos($h, [IntPtr](-1), 0, 0, 0, 0, 0x43) | Out-Null   # TOPMOST, sin mover ni cambiar tamaño, mostrar
Start-Sleep -Milliseconds 500
$r = New-Object C+RECT
[C]::GetWindowRect($h, [ref]$r) | Out-Null
if ($dx -ge 0) {
  [C]::SetCursorPos($r.L + $dx, $r.T + $dy) | Out-Null
  Start-Sleep -Milliseconds 200
  [C]::mouse_event(2, 0, 0, 0, [UIntPtr]::Zero)   # left down
  Start-Sleep -Milliseconds 80
  [C]::mouse_event(4, 0, 0, 0, [UIntPtr]::Zero)   # left up
  Start-Sleep -Milliseconds 700
}
$w = $r.R - $r.L; $hh = $r.B - $r.T
if ($shotName) {
  $bmp = New-Object System.Drawing.Bitmap $w, $hh
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $g.CopyFromScreen($r.L, $r.T, 0, 0, (New-Object System.Drawing.Size $w, $hh))
  $bmp.Save((Join-Path $env:TEMP $shotName))
}
"ok rect $($r.L),$($r.T) ${w}x${hh}"
