# Workshop Assets - Live Links & Reference

The workshop runs in the **SelectHealth workspace**, with the dataset generated into the
**`demo`** catalog (default; set the `catalog` widget when you run the generator). All data
is synthetic, no PHI. See `carla_agenda_and_setup.md` for the setup steps Carla runs.

Kiara also has a **pre-built staging copy in `kk_test`** (`adb-669602668219382.2.azuredatabricks.net`)
for reference and dry-runs; those IDs are listed below and only work in `kk_test`.

## Facilitator materials (Google)
- **Agenda + Setup (send to Carla):** https://docs.google.com/document/d/1kd7ARcb3Xtx9ogEvGm8j4InukW2VVoO-Z5XRst6nkOs/edit
- **Agenda (internal):** https://docs.google.com/document/d/1r2KBrJA35y4f2H9i0cVdtI0KnW4uUZIC7ihB-tVvVXI/edit
- **Instructor Guide:** https://docs.google.com/document/d/17JiaKmYjY5hakjrAfHbhyaAtg_q3t4j8inuLqtbUjCA/edit
- **Attendee Workbook:** https://docs.google.com/document/d/1NcvOOwWWMVBXHzbbCESYlDQ7VNJFwuH5q9nFsmpcQn4/edit
- **Orientation slides:** https://docs.google.com/presentation/d/1bWSTUCplBXFdBKu8kF4qaiSaCB16jETksaXzSzspkJc/edit
  (10 slides, standard layouts - not Databricks-branded, since the corporate template
  was not accessible; apply the brand theme in Slides if you want it branded.)
- Markdown source of truth for the guide + workbook lives in this repo's `lab_guides/`.

## Data
- **Catalog/schema:** `demo.selecthealth_workshop`
- **Tables:** `fact_encounters` (80,000 rows, Jan 2023–Dec 2025), `dim_provider` (45),
  `dim_facility` (12), `dim_diagnosis` (24 ICD-10 codes), `dim_procedure` (18 incl. knee
  replacement 27447)
- **Baseline outcome rates:** ~14.5% 30-day readmission, ~4.0% mortality, ~12.4% complication

## Kiara's staging build (kk_test, for reference / dry-run only)
- **Dashboard:** "SelectHealth Workshop - Encounters & Outcomes", ID `01f173e9bd5313c2804b68f5edcf8bbb`
  - https://adb-669602668219382.2.azuredatabricks.net/sql/dashboardsv3/01f173e9bd5313c2804b68f5edcf8bbb
  - Pages: Overview (KPIs, outcomes by facility/category, LOS by specialty, monthly trend by
    region, provider scorecard) + global Filters (region, clinical category, encounter type, payer).
- **Genie space:** "SelectHealth Workshop - Encounters Genie", ID `01f173e9cad61c2cbd13dd24c3a3cc6f`
- These point at `kk_test.selecthealth_workshop` and only work in Kiara's workspace. In the
  SelectHealth workspace, regenerate the data and import the dashboard JSON (it targets `demo`),
  then create the Genie space per `genie/genie_space_config.md`.

## Pre-workshop checklist (in the SelectHealth workspace)
- [ ] Run the data generator (see `carla_agenda_and_setup.md`) into the `demo` catalog.
- [ ] All 3 attendees have UC SELECT on `demo.selecthealth_workshop`.
- [ ] A SQL warehouse (serverless or pro) is running.
- [ ] Import `dashboard/selecthealth_workshop.lvdash.json` and confirm widgets render.
- [ ] Create the Genie space and confirm it answers the knee-replacement sample question.
- [ ] (Optional) Add the curated Genie instructions from `genie_space_config.md`.
- [ ] (Optional) Decide whether attendees clone the dashboard or build their own.
