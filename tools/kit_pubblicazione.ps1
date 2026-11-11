# Crea sul PC una cartella per ogni uscita del piano con didascalia.txt: quando, formato, dove si trova il file da caricare e la didascalia da copiare.
# Non scarica copie dei file (il disco del PC e' quasi pieno): indica il percorso dell'originale.
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

    $testo = @()
    $testo += "Quando: $($giorni[[int]$d.DayOfWeek]) $($v.data) alle $($v.ora)"
    $testo += "Formato: $($v.tipo)"
    $testo += "Stato: $($v.stato)"
    if ($v.nota) { $testo += "Nota: $($v.nota)" }
    if ($v.file_pc) {
        $testo += ""; $testo += "--- FILE DA CARICARE (in quest'ordine) ---"
        foreach ($f in $v.file_pc) { $testo += $(if (Test-Path $f) { $f } else { "$f   (non trovato sul PC)" }) }
    }
    if ($v.didascalia) { $testo += ""; $testo += "--- DIDASCALIA DA COPIARE ---"; $testo += $v.didascalia }
    [IO.File]::WriteAllText((Join-Path $dir "didascalia.txt"), ($testo -join "`r`n"), (New-Object Text.UTF8Encoding $true))
    Write-Output "ok  $nome"
}
