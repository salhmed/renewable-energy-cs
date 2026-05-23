# Solar, Wind and Battery Sizing

Official version: [README.md](README.md) in French  
Portuguese version: [README.pt.md](README.pt.md)

## Goal

This project estimates the sizing of a hybrid energy system:

- wind generation;
- photovoltaic solar generation;
- battery storage;
- hourly electricity demand.

The main goal is to identify the most difficult period of the year, then economically size the number of solar panels and batteries required to cover that critical period.

## Input Data

The main input file is:

```text
Power_conso_farm_projet_good_calcul_anne_cleaned.csv
```

Main columns:

- `local_time`: date and time;
- `wind_electricity_kW`: hourly wind generation;
- `solar_electricity_kW`: reference solar generation for 290 panels;
- `consommation_kW`: hourly electricity demand.

Since the dataset is hourly, summed `kW` values are treated as `kWh` over each hour.

## Method

### 1. Critical Period Identification

The notebook computes 15-day rolling sums to identify the weakest generation periods.

The selected critical period is:

```text
2019-12-03 to 2019-12-17
```

This is the worst consecutive 15-day period used for the final sizing step.

### 2. Economic Sizing on the Critical Period

The final sizing is performed only on the critical period.

Costs used:

```text
Solar panel cost : 139.66 EUR
Battery cost     : 449.99 EUR
```

Battery characteristics:

```text
Nominal capacity per battery : 2.40 kWh
Allowed state of charge      : 20% to 90%
Usable capacity fraction     : 70%
Usable energy per battery    : 1.68 kWh
```

For each tested number of panels, the notebook:

1. computes hourly solar generation;
2. computes the hourly energy balance:

```text
balance = wind generation + solar generation - demand
```

3. simulates battery charge and discharge hour by hour;
4. computes the minimum required number of batteries;
5. computes total cost:

```text
total cost = panels * 139.66 + batteries * 449.99
```

The selected solution is the one with the lowest total cost.

## Main Results

Best economic solution on the critical period:

```text
Number of solar panels : 1189
Number of batteries    : 924
Nominal battery capacity : 2217.60 kWh
Usable battery capacity  : 1552.32 kWh
Panel cost   : 166055.74 EUR
Battery cost : 415790.76 EUR
Total cost   : 581846.50 EUR
```

Critical-period simulation, with batteries initially charged to 90%:

```text
Minimum SOC : 20%
Maximum SOC : 90%
Unserved energy : 0 kWh
Curtailed energy : 3474.95 kWh
```

## Full-Year Check

The `1189 panels / 924 batteries` configuration was then simulated over the full year.

Annual result:

```text
Annual demand : 329595.00 kWh
Wind generation : 165722.39 kWh
Solar generation : 334941.68 kWh
Total generation : 500664.07 kWh
Balance before storage : +171069.07 kWh
Unserved energy : 142.70 kWh
Curtailed energy : 172013.47 kWh
Minimum SOC : 20%
Maximum SOC : 90%
```

Important note: the system was optimized on the 15-day critical period, not on the full year. In the chronological annual simulation, there is still `142.70 kWh` of unserved energy because the batteries are not necessarily at 90% when the critical period starts.

## Generated Plots

Annual plot:

```text
plot_annee_energie_batterie_generation.png
```

It shows:

- daily consumed energy;
- daily generated energy;
- energy stored in batteries;
- curtailed energy;
- unserved energy.

Typical seasonal days plot:

```text
plot_journees_typiques_saisons.png
```

Automatically selected representative days:

```text
Winter : 2019-02-13
Spring : 2019-05-21
Summer : 2019-06-28
Autumn : 2019-09-27
```

## Important Files

```text
solar_wind_estimation.ipynb
```

Main notebook containing calculations, simulations and plots.

```text
low_15_day_windows.csv
```

Summary of the worst 15-day windows.

```text
dimensionnement_panneaux_batteries_periode_critique.csv
```

Economic sizing results on the critical period.

```text
periode_critique_with_battery.csv
```

Hourly critical-period simulation with battery state.

```text
simulation_annuelle_1189p_924b.csv
```

Full-year hourly simulation with `1189` panels and `924` batteries.

## Reproducing the Results

1. Open `solar_wind_estimation.ipynb`.
2. Run the cells in order.
3. The CSV files and plots are regenerated automatically.

Main dependencies:

- Python;
- pandas;
- matplotlib;
- Jupyter Notebook or JupyterLab.

## Limits and Assumptions

- The solar column is considered as a reference profile for `290` panels.
- Solar generation for `N` panels is scaled proportionally:

```text
solar_N = solar_290 * N / 290
```

- Batteries are modeled simply, without charge/discharge efficiency or aging.
- The final economic sizing is optimized on the 15-day critical period.
- The initial battery state has a strong impact. The critical period is covered if batteries start at `90%`.
