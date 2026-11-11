# Crea sul PC una cartella per ogni uscita del piano, con il file da caricare e la didascalia da copiare.
# Uso: powershell -ExecutionPolicy Bypass -File kit_pubblicazione.ps1 "C:\percorso\Ritual content marketing"
# Non pubblica nulla: prepara solo i materiali. La pubblicazione la fa Rocco dall'app.
param([string]$Base = "$env:USERPROFILE\OneDrive\Desktop\Ritual content marketing")

$ErrorActionPreference = "Stop"
$Dest = Join-Path $Base "Pubblicazione"
New-Item -ItemType Directory -Force $Dest | Out-Null
$piano = Invoke-RestMethod "https://raw.githubusercontent.com/Rocco41099/Ritual-barber-studio/main/publish/piano.json"
$giorni = @("Dom", "Lun", "Mar", "Mer", "Gio", "Ven", "Sab")

foreach ($v in $piano.voci) {
    $d = [datetime]::ParseExact($v.data, "yyyy-MM-dd", $null)
    $ora = $v.ora -replace ":", "."
    $nome = "{0} {1} {2} - {3} {4}" -f $v.data, $giorni[[int]$d.DayOfWeek], $ora, $v.tipo, $v.contenuto
    $dir = Join-Path $Dest $nome
    New-Item -ItemType Directory -Force $dir | Out-Null

    $urls = @()
    if ($v.video_url) { $urls += $v.video_url }
    if ($v.image_url) { $urls += $v.image_url }
    if ($v.image_urls) { $urls += $v.image_urls }
    foreach ($u in $urls) {
        $file = Join-Path $dir ([IO.Path]::GetFileName($u))
        if (-not (Test-Path $file)) { Invoke-WebRequest $u -OutFile $file }
    }

    $testo = @()
    $testo += "Quando: $($giorni[[int]$d.DayOfWeek]) $($v.data) alle $($v.ora)"
    $testo += "Formato: $($v.tipo)"
    $testo += "Stato: $($v.stato)"
    if ($v.nota) { $testo += "Nota: $($v.nota)" }
    if ($v.didascalia) { $testo += ""; $testo += "--- DIDASCALIA DA COPIARE ---"; $testo += $v.didascalia }
    [IO.File]::WriteAllText((Join-Path $dir "didascalia.txt"), ($testo -join "`r`n"), (New-Object Text.UTF8Encoding $true))
    Write-Output "ok  $nome"
}
