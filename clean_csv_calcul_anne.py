from pathlib import Path
import csv

input_path = Path('Power_conso_farm_projet_good_calcul anne.csv')
output_path = Path('Power_conso_farm_projet_good_calcul_anne_cleaned.csv')

with input_path.open('r', encoding='utf-8-sig', errors='replace') as f:
    lines = [line.rstrip('\n\r') for line in f]

header_index = None
for i, line in enumerate(lines):
    if line.startswith('local_time;'):
        header_index = i
        break

if header_index is None:
    raise SystemExit('Could not locate data header line')

header = lines[header_index].split(';')
# rename ambiguous header names to safe names
header = [
    'local_time',
    'wind_electricity_kW',
    'wind_speed_m_s',
    'solar_electricity_kW',
    'solar_electricity_W',
    'consommation_kW'
]

rows = []
for line in lines[header_index+1:]:
    if not line.strip():
        continue
    parts = line.split(';')
    if len(parts) < 6:
        continue
    dt = parts[0].strip().replace('"', '')
    values = [dt]
    for idx, part in enumerate(parts[1:6]):
        value = part.strip().replace('"', '').replace(' ', '').replace(',', '.')
        if idx == 0:
            try:
                value = str(float(value) / 1000)
            except ValueError:
                pass
        values.append(value)
    rows.append(values)

with output_path.open('w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(header)
    writer.writerows(rows)

print(f'Wrote {len(rows)} rows to {output_path}')