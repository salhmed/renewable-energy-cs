$inputPath = 'Power_conso_farm_projet_good_Calcul anne.csv'
$outputPath = 'Power_conso_farm_projet_good_Calcul_anne_cleaned.csv'

$profile = @{0=30;1=30;2=30;3=30;4=30;5=33;6=35;7=40;8=45;9=50;10=45;11=40;12=35;13=36;14=36;15=36;16=35;17=40;18=47;19=50;20=47;21=40;22=35;23=28}

$lines = Get-Content -Path $inputPath -Encoding UTF8
$start = $lines.FindIndex({ $_ -like 'local_time;*' })
if ($start -lt 0) { throw 'Header line not found' }

$output = @()
$output += 'local_time;electricity_kW;wind_speed_m_s;existing_electricity_kW;Puissance consommée (kW)'

for ($i = $start + 1; $i -lt $lines.Count; $i++) {
    $line = $lines[$i].Trim()
    if ([string]::IsNullOrWhiteSpace($line)) { continue }
    $parts = $line -split ';'
    if ($parts.Count -lt 4) { continue }
    $dt = $parts[0].Trim('"')
    $cleaned = @()
    for ($j = 1; $j -le 3; $j++) {
        $cleaned += $parts[$j].Trim('"').Replace(' ', '')
    }
    $hour = $null
    try { $hour = [int]($dt.Split()[-1].Split(':')[0]) } catch { }
    $cons = ''
    if ($hour -ne $null -and $profile.ContainsKey($hour)) { $cons = $profile[$hour] }
    $output += ($dt + ';' + ($cleaned -join ';') + ';' + $cons)
}

$output | Set-Content -Path $outputPath -Encoding UTF8
Write-Host "Wrote $($output.Count - 1) rows to $outputPath"