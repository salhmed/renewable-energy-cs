from pathlib import Path
import csv

input_path = Path('Power_conso_farm_projet_good_Calcul anne.csv')
output_path = Path('Power_conso_farm_projet_good_Calcul_anne_cleaned.csv')

consumption_by_hour = {
    0:30,1:30,2:30,3:30,4:30,5:33,6:35,7:40,8:45,9:50,10:45,11:40,12:35,13:36,14:36,15:36,
    16:35,17:40,18:47,19:50,20:47,21:40,22:35,23:28
}

with input_path.open('r', encoding='utf-8-sig', errors='replace') as f:
    lines = [line.rstrip('\n\r') for line in f]

start = 0
for i, line in enumerate(lines):
    if line.startswith('local_time;'):
        start = i
        break
else:
    raise SystemExit('Could not locate data header line')

rows = []
for line in lines[start+1:]:
    if not line.strip():
        continue
    parts = line.split(';')
    if len(parts) < 4:
        continue
    dt = parts[0].strip().replace('"', '')
    values = []
    for x in parts[1:4]:
        v = x.strip().replace('"', '').replace(' ', '')
        values.append(v)
    hour = None
    try:
        hour = int(dt.split()[-1].split(':')[0])
    except Exception:
        hour = None
    cons = consumption_by_hour.get(hour, '')
    rows.append([dt] + values + [str(cons)])

out_header = ['local_time','electricity_kW','wind_speed_m_s','existing_electricity_kW','Puissance consommée (kW)']
with output_path.open('w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(out_header)
    writer.writerows(rows)

print(f'Wrote {len(rows)} rows to {output_path}')
