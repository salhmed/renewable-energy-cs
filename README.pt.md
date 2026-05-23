# Dimensionamento solar, eólico e de baterias

Versão oficial: [README.md](README.md) em francês  
English version: [README.en.md](README.en.md)

## Objetivo

Este projeto estima o dimensionamento de um sistema híbrido de energia:

- produção eólica;
- produção solar fotovoltaica;
- armazenamento por baterias;
- consumo elétrico horário.

O objetivo principal é identificar o período mais desfavorável do ano e, em seguida, dimensionar economicamente o número de painéis solares e baterias necessários para cobrir esse período crítico.

## Dados utilizados

O arquivo principal utilizado é:

```text
Power_conso_farm_projet_good_calcul_anne_cleaned.csv
```

Colunas principais:

- `local_time`: data e hora;
- `wind_electricity_kW`: produção eólica horária;
- `solar_electricity_kW`: produção solar de referência para 290 painéis;
- `consommation_kW`: consumo elétrico horário.

Como os dados são horários, os valores em `kW` somados ao longo de uma hora são tratados como `kWh`.

## Método

### 1. Identificação do período crítico

O notebook calcula somas móveis de 15 dias para identificar os períodos de menor produção.

O período crítico selecionado é:

```text
2019-12-03 a 2019-12-17
```

Esse período representa a janela consecutiva de 15 dias mais desfavorável usada no dimensionamento final.

### 2. Dimensionamento econômico no período crítico

O dimensionamento final é feito apenas nesse período crítico.

Custos utilizados:

```text
Custo de um painel solar : 139,66 EUR
Custo de uma bateria     : 449,99 EUR
```

Características da bateria:

```text
Capacidade nominal de uma bateria : 2,40 kWh
Estado de carga permitido         : 20% a 90%
Fração utilizável                 : 70%
Energia utilizável por bateria    : 1,68 kWh
```

Para cada número de painéis testado, o notebook:

1. calcula a produção solar horária;
2. calcula o balanço energético horário:

```text
balanço = produção eólica + produção solar - consumo
```

3. simula a carga e descarga das baterias hora a hora;
4. calcula o número mínimo de baterias necessário;
5. calcula o custo total:

```text
custo total = painéis * 139,66 + baterias * 449,99
```

A solução escolhida é aquela que minimiza esse custo total.

## Principais resultados

Solução econômica selecionada no período crítico:

```text
Número de painéis solares : 1189
Número de baterias        : 924
Capacidade nominal das baterias : 2217,60 kWh
Capacidade utilizável das baterias : 1552,32 kWh
Custo dos painéis  : 166055,74 EUR
Custo das baterias : 415790,76 EUR
Custo total        : 581846,50 EUR
```

Simulação no período crítico, com as baterias inicialmente carregadas a 90%:

```text
SOC mínimo : 20%
SOC máximo : 90%
Energia não atendida : 0 kWh
Energia excedente/descartada : 3474,95 kWh
```

## Verificação anual

A configuração `1189 painéis / 924 baterias` foi simulada em seguida durante todo o ano.

Resultado anual:

```text
Consumo anual : 329595,00 kWh
Produção eólica : 165722,39 kWh
Produção solar : 334941,68 kWh
Produção total : 500664,07 kWh
Balanço antes do armazenamento : +171069,07 kWh
Energia não atendida : 142,70 kWh
Energia excedente/descartada : 172013,47 kWh
SOC mínimo : 20%
SOC máximo : 90%
```

Observação importante: o sistema foi otimizado para o período crítico de 15 dias, não para o ano inteiro. Na simulação cronológica anual ainda existe `142,70 kWh` de energia não atendida, porque as baterias não estão necessariamente a 90% no início do período crítico.

## Gráficos gerados

Gráfico anual:

```text
plot_annee_energie_batterie_generation.png
```

Ele mostra:

- energia consumida por dia;
- energia gerada por dia;
- energia armazenada nas baterias;
- energia excedente/descartada;
- energia não atendida.

Gráfico de dias típicos por estação:

```text
plot_journees_typiques_saisons.png
```

Dias representativos selecionados automaticamente:

```text
Inverno   : 2019-02-13
Primavera : 2019-05-21
Verão     : 2019-06-28
Outono    : 2019-09-27
```

## Arquivos importantes

```text
solar_wind_estimation.ipynb
```

Notebook principal com cálculos, simulações e gráficos.

```text
dimensionnement_panneaux_batteries_periode_critique.csv
```

Resultados do dimensionamento econômico no período crítico.

```text
periode_critique_with_battery.csv
```

Simulação horária do período crítico com o estado das baterias.

```text
simulation_annuelle_1189p_924b.csv
```

Simulação horária anual com `1189` painéis e `924` baterias.

## Como reproduzir

1. Abrir `solar_wind_estimation.ipynb`.
2. Executar as células em ordem.
3. Os arquivos CSV e os gráficos são gerados novamente automaticamente.

Dependências principais:

- Python;
- pandas;
- matplotlib;
- Jupyter Notebook ou JupyterLab.

## Limitações e hipóteses

- A coluna solar é considerada um perfil de referência para `290` painéis.
- A produção solar para `N` painéis é escalada proporcionalmente:

```text
solar_N = solar_290 * N / 290
```

- As baterias são modeladas de forma simplificada, sem eficiência de carga/descarga nem envelhecimento.
- O dimensionamento econômico final é otimizado no período crítico de 15 dias.
- O estado inicial das baterias influencia fortemente o resultado. O período crítico é coberto se as baterias começarem a `90%`.
