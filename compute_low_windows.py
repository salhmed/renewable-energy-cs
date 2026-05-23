from pathlib import Path
import pandas as pd

input_path = Path('Power_conso_farm_projet_good_calcul_anne_cleaned.csv')
output_path = Path('low_15_day_windows.csv')

# Load the cleaned dataset
print(f'Loading {input_path}')
df = pd.read_csv(input_path, sep=';', parse_dates=['local_time'])

# Normalize numeric columns
numeric_cols = [
    'wind_electricity_kW',
    'wind_speed_m_s',
    'solar_electricity_kW',
    'solar_electricity_W',
    'consommation_kW',
]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.', regex=False), errors='coerce')

# Convert wind electricity from W to kW if needed (cleaned file already does this, but keep for safety)
df['wind_electricity_kW'] = df['wind_electricity_kW'] / 1000

# Add time fields
raise_if_missing = not df['local_time'].isna().any()
if not raise_if_missing:
    raise SystemExit('Missing local_time values')
df['date'] = df['local_time'].dt.date

df_daily = df.set_index('local_time').resample('D').sum()

panel_counts = [250, 290, 350]
for n in panel_counts:
    df_daily[f'solar_{n}_direct_kW'] = df_daily['solar_electricity_kW'] * n
    df_daily[f'total_{n}_direct_kW'] = df_daily['wind_electricity_kW'] + df_daily[f'solar_{n}_direct_kW']
    df_daily[f'solar_{n}_from_290_kW'] = df_daily['solar_electricity_kW'] * (n / 290)
    df_daily[f'total_{n}_from_290_kW'] = df_daily['wind_electricity_kW'] + df_daily[f'solar_{n}_from_290_kW']

low_windows = []
for n in panel_counts:
    for method in ['direct', 'from_290']:
        col = f'total_{n}_{method}_kW'
        if col not in df_daily.columns:
            continue
        rolling = df_daily[col].rolling(15).sum()
        low = rolling.nsmallest(5).reset_index()
        low.columns = ['window_end', 'energy_15d_kWh']
        low['window_start'] = low['window_end'] - pd.Timedelta(days=14)
        low['panel_count'] = n
        low['method'] = method
        low_windows.append(low[['panel_count', 'method', 'window_start', 'window_end', 'energy_15d_kWh']])

low_df = pd.concat(low_windows, ignore_index=True)
low_df.to_csv(output_path, sep=';', index=False)
print(f'Wrote low window summary to {output_path}')
print(low_df.head(20).to_string(index=False))
