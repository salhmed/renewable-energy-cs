import fs from "node:fs/promises";
import path from "node:path";

const INPUT_PATH = path.join("solar_data", "ninja_pv_42.7719_2.6995_corrected.csv");
const OUTPUT_PATH = path.join("solar_data", "solar_irradiance_power_per_panel.csv");

const PANEL_EFFICIENCY = 0.18;

function parseCsvLine(line) {
  const values = [];
  let current = "";
  let inQuotes = false;

  for (let i = 0; i < line.length; i += 1) {
    const char = line[i];
    const next = line[i + 1];

    if (char === '"' && inQuotes && next === '"') {
      current += '"';
      i += 1;
    } else if (char === '"') {
      inQuotes = !inQuotes;
    } else if (char === "," && !inQuotes) {
      values.push(current);
      current = "";
    } else {
      current += char;
    }
  }

  values.push(current);
  return values;
}

function formatNumber(value, decimals = 6) {
  if (!Number.isFinite(value)) {
    return "";
  }
  return value.toFixed(decimals).replace(/\.?0+$/, "");
}

function escapeSemicolonCsv(value) {
  const text = String(value ?? "");
  if (/[;"\r\n]/.test(text)) {
    return `"${text.replaceAll('"', '""')}"`;
  }
  return text;
}

function toNumber(value, columnName) {
  const parsed = Number(String(value).trim().replace(",", "."));
  if (!Number.isFinite(parsed)) {
    throw new Error(`Invalid numeric value for ${columnName}: ${value}`);
  }
  return parsed;
}

const input = await fs.readFile(INPUT_PATH, "utf8");
const lines = input.split(/\r?\n/).filter((line) => line.trim() !== "");

const dataLines = lines.filter((line) => !line.startsWith("#"));
const header = parseCsvLine(dataLines[0]);
const columnIndex = Object.fromEntries(header.map((name, index) => [name, index]));

for (const required of [
  "time",
  "local_time",
  "irradiance_direct",
  "irradiance_diffuse",
]) {
  if (!(required in columnIndex)) {
    throw new Error(`Missing required column: ${required}`);
  }
}

const outputRows = [
  [
    "time_utc",
    "date_heure_locale",
    "irradiance_direct",
    "irradiance_diffuse",
    "irradiance_totale",
    "puissance_panneau_kW",
    "puissance_panneau_W",
  ],
];

let rowCount = 0;
let maxIrradianceTotal = 0;
let maxPanelPowerKw = 0;
let annualPanelEnergyKwh = 0;
let annualIrradiance = 0;

for (const line of dataLines.slice(1)) {
  const parts = parseCsvLine(line);
  const direct = toNumber(parts[columnIndex.irradiance_direct], "irradiance_direct");
  const diffuse = toNumber(parts[columnIndex.irradiance_diffuse], "irradiance_diffuse");

  const irradianceTotal = direct + diffuse;
  const panelPowerKw = irradianceTotal * PANEL_EFFICIENCY;
  const panelPowerW = panelPowerKw * 1000;

  outputRows.push([
    parts[columnIndex.time],
    parts[columnIndex.local_time],
    formatNumber(direct),
    formatNumber(diffuse),
    formatNumber(irradianceTotal),
    formatNumber(panelPowerKw),
    formatNumber(panelPowerW, 3),
  ]);

  rowCount += 1;
  maxIrradianceTotal = Math.max(maxIrradianceTotal, irradianceTotal);
  maxPanelPowerKw = Math.max(maxPanelPowerKw, panelPowerKw);
  annualPanelEnergyKwh += panelPowerKw;
  annualIrradiance += irradianceTotal;
}

const output = outputRows
  .map((row) => row.map(escapeSemicolonCsv).join(";"))
  .join("\n");

await fs.writeFile(OUTPUT_PATH, `${output}\n`, "utf8");

console.log(`Input: ${INPUT_PATH}`);
console.log(`Output: ${OUTPUT_PATH}`);
console.log(`Rows: ${rowCount}`);
console.log(`Panel efficiency used: ${PANEL_EFFICIENCY}`);
console.log(`Max total irradiance: ${formatNumber(maxIrradianceTotal, 3)}`);
console.log(`Max panel power: ${formatNumber(maxPanelPowerKw, 3)} kW`);
console.log(`Annual panel energy: ${formatNumber(annualPanelEnergyKwh, 3)} kWh`);
console.log(`Annual irradiance sum: ${formatNumber(annualIrradiance, 3)}`);
