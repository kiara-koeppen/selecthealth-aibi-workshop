# SelectHealth AI/BI Workshop

Hands-on workshop materials for the SelectHealth analytics team's evaluation of **Databricks AI/BI vs. Tableau**. Built for Carla Lange and two senior analysts (one query-focused, one Tableau-focused; mixed Databricks familiarity).

## Purpose

The SelectHealth team builds queries, dashboards, and reports - today largely in Tableau, with their data migrating to Databricks. This workshop is a discovery / bake-off: get the analysts hands-on with AI/BI dashboards (the primary focus) plus Genie for natural-language querying, on a realistic medical dataset, so they can form a genuine opinion on fit.

Two sessions:
- **Day 1 (Wed, ~3h50):** What's possible - dashboard authoring, AI-assisted authoring, the semantic layer, and a Genie segment.
- **Day 2 (Thu, ~1h50):** Build with your own scenario - each analyst builds, then share-outs.

See [`lab_guides/agenda.md`](lab_guides/agenda.md) for the full agenda and
[`lab_guides/workshop_assets.md`](lab_guides/workshop_assets.md) for live links to the
deployed dataset, dashboard, and Genie space (all staged in `kk_test`).

## Architecture / data flow

```
generate_workshop_data.py  ──►  Unity Catalog (kk_test.selecthealth_workshop)
   (Spark, synthetic, no PHI)        ├── dim_provider      (providers, specialty, facility)
                                     ├── dim_facility      (hospitals/clinics, region)
                                     ├── dim_diagnosis     (ICD-10 + description + category)
                                     ├── dim_procedure     (CPT-style code + description)
                                     └── fact_encounters   (one row per encounter; outcomes)
                                              │
                          ┌───────────────────┼───────────────────┐
                          ▼                   ▼                   ▼
                  AI/BI Dashboard       Metric View          Genie Space
                  (provider/facility    (governed KPI        (natural-language
                   aggregations,         definitions =        querying + SQL
                   trends, drill-down)   "published data      dialect help)
                                         source" parity)
```

The dataset is a star schema centered on `fact_encounters`. Outcomes (readmission, mortality, complication) are condition-dependent so dashboards show meaningful variation across diagnoses, providers, and facilities.

## Prerequisites

- Databricks workspace access (workshop staged in `kk_test`); attendees need accounts + UC permissions.
- Databricks CLI authenticated to the target profile (`databricks auth login --profile kk_test`).
- A SQL warehouse / serverless compute available in the workspace.

## How to deploy

1. **Generate the dataset** - run the notebook on serverless (widgets default to `kk_test.selecthealth_workshop`):
   ```
   data_generation/generate_workshop_data.py
   ```
2. **Deploy the dashboard** - import `dashboard/selecthealth_workshop.lvdash.json` into the workspace (Dashboards → Import), or via the Lakeview API.
3. **Create the Genie space** - see `genie/genie_space_config.md` for instructions, sample questions, and the table set.

## File / folder structure

```
selecthealth-aibi-workshop/
├── README.md
├── data_generation/
│   └── generate_workshop_data.py   # Parameterized synthetic data generator (Databricks notebook)
├── dashboard/
│   └── selecthealth_workshop.lvdash.json  # Starter AI/BI (Lakeview) dashboard
├── genie/
│   └── genie_space_config.md       # Genie space setup: instructions + sample questions
└── lab_guides/
    ├── agenda.md                   # Shareable agenda (both days)
    ├── instructor_guide.md         # Detailed facilitator manual: talk tracks, clicks, what to point out
    ├── attendee_workbook.md        # Step-by-step the attendees follow along
    └── workshop_assets.md          # Live links/IDs for the deployed dataset, dashboard, Genie space
```

Orientation slide deck (first ~20 min of Day 1) is a Google Slides deck; link tracked in
`workshop_assets.md`.

## Configuration

All data generation is parameterized via `dbutils.widgets` (catalog, schema, row counts, date range) - nothing hardcoded. Defaults target `kk_test.selecthealth_workshop`.
