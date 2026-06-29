# Workshop Assets - Live Links & Reference

Everything staged in **`kk_test`** (`adb-669602668219382.2.azuredatabricks.net`). All
synthetic, no PHI.

## Data
- **Catalog/schema:** `kk_test.selecthealth_workshop`
- **Tables:** `fact_encounters` (80,000 rows, Jan 2023–Dec 2025), `dim_provider` (45),
  `dim_facility` (12), `dim_diagnosis` (24 ICD-10 codes), `dim_procedure` (18 incl. knee
  replacement 27447)
- **Baseline outcome rates:** ~14.5% 30-day readmission, ~4.0% mortality, ~12.4% complication

## Starter AI/BI dashboard
- **Name:** SelectHealth Workshop - Encounters & Outcomes
- **ID:** `01f173e9bd5313c2804b68f5edcf8bbb`
- **URL:** https://adb-669602668219382.2.azuredatabricks.net/sql/dashboardsv3/01f173e9bd5313c2804b68f5edcf8bbb
- **Path:** `/Workspace/Users/kiara.koeppen@databricks.com/SelectHealth Workshop - Encounters & Outcomes.lvdash.json`
- Pages: Overview (KPIs, outcomes by facility/category, LOS by specialty, monthly trend by
  region, provider scorecard table) + global Filters (region, clinical category, encounter
  type, payer).

## Genie space
- **Name:** SelectHealth Workshop - Encounters Genie
- **ID:** `01f173e9cad61c2cbd13dd24c3a3cc6f`
- See `genie/genie_space_config.md` for sample questions and suggested instructions.

## Pre-workshop checklist
- [ ] All 3 attendees have access to the `kk_test` workspace (accounts + UC SELECT on
      `kk_test.selecthealth_workshop`).
- [ ] SQL warehouse `ad1dd0025031919f` (or another) is running.
- [ ] Dashboard opens and all widgets render.
- [ ] Genie space answers the knee-replacement sample question.
- [ ] (Optional) Add the curated Genie instructions from `genie_space_config.md`.
- [ ] (Optional) Confirm whether attendees should each clone the dashboard or build their own.

> Note: this is staged in `kk_test` for build/demo. Moving it to a workspace the SelectHealth
> attendees can access (or granting them access here) is a separate step before the session.
