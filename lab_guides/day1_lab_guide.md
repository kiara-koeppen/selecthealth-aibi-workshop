# Day 1 Lab Guide - What's possible in AI/BI

**Facilitator:** Kiara (lead) + Clint (floating)
**Dataset:** `kk_test.selecthealth_workshop` - `fact_encounters` + `dim_provider`, `dim_facility`, `dim_diagnosis`, `dim_procedure`
**Style:** Hands-on. Everyone follows along in their own browser. Light narration, then clicks.

> **Tableau-parity framing (use throughout):** workbook → **dashboard**, worksheet → **visualization widget**, published data source / LOD calc → **metric view**, Ask Data → **Genie**, calculated field → **dashboard calculated measure / SQL expression**. Anchor each new thing to what they already know.

---

## 0 · Welcome & orientation (12:00–12:20)

**Talk track (5 min):**
- Two days, hands-on. Today = see what's possible; tomorrow = build your own.
- The data is synthetic medical encounters - no PHI - but shaped like the provider/facility outcome analysis you do: diagnoses, procedures, where care happened, and what the outcome was.

**Do together (10 min):**
1. Open the workspace → **Catalog** → `kk_test` → `selecthealth_workshop`.
2. Click `fact_encounters` → **Sample Data** tab. Point out: one row per encounter, `provider_id` / `facility_id` foreign keys, outcome flags (`readmitted_30d`, `mortality_flag`, `complication_flag`).
3. Click **Details** → note the column comments. Mention: good comments make AI/BI and Genie much smarter.
4. Glance at the four `dim_` tables so everyone sees the star schema.

**Skeptic hook:** "Notice you didn't write any SQL to explore this - but the SQL is always one click away. You're never locked out of the detail."

---

## 1 · Dashboard Authoring I - aggregations by provider & facility (12:20–1:05)

**Goal:** First dashboard, first chart, aggregate an outcome by provider and facility.

1. **Dashboards** (left nav) → **Create dashboard**. Name it `My SelectHealth Workshop`.
2. On the **Data** tab → **Create from SQL** (or pick the table). Paste:
   ```sql
   SELECT f.facility_name, f.region,
          COUNT(*)                                   AS encounters,
          ROUND(100.0*SUM(e.readmitted_30d)/COUNT(*), 1) AS readmit_rate_pct,
          ROUND(100.0*SUM(e.complication_flag)/COUNT(*), 1) AS complication_rate_pct
   FROM fact_encounters e
   JOIN dim_facility f USING (facility_id)
   GROUP BY f.facility_name, f.region
   ```
   Name this dataset `Facility outcomes`. **Run** to preview.
3. **Canvas** tab → **Add visualization**. Choose **Bar**.
   - X: `facility_name`, Y: `readmit_rate_pct`. Sort descending.
   - Title: "30-day readmission rate by facility".
4. **Tableau parity moment:** "That's your bar-on-a-shelf, but the aggregation lived in the dataset - reusable across every chart on this dashboard."
5. **Add a second dataset** `Provider volume`:
   ```sql
   SELECT p.provider_name, p.specialty, f.facility_name,
          COUNT(*) AS encounters,
          ROUND(AVG(e.length_of_stay_days), 1) AS avg_los_days
   FROM fact_encounters e
   JOIN dim_provider p USING (provider_id)
   JOIN dim_facility f USING (facility_id)
   GROUP BY p.provider_name, p.specialty, f.facility_name
   ```
6. Add a **Table** visual on `Provider volume`. Sort by `encounters` desc.

**Checkpoint:** everyone has a dashboard with 1 bar + 1 table. Help anyone stuck before the break.

### Break (1:05–1:20)

---

## 2 · Dashboard Authoring II - trends, drill-down, filters (1:20–2:10)

**Goal:** Make it interactive - trends over time, drill from region to provider, filters.

1. **New dataset** `Monthly trend`:
   ```sql
   SELECT DATE_TRUNC('month', e.admit_date) AS month,
          f.region,
          COUNT(*) AS encounters,
          ROUND(100.0*SUM(e.mortality_flag)/COUNT(*), 2) AS mortality_rate_pct
   FROM fact_encounters e
   JOIN dim_facility f USING (facility_id)
   GROUP BY 1, 2
   ```
2. Add a **Line** visual: X `month`, Y `encounters`, color/series by `region`. Title: "Monthly encounter volume by region".
3. **Filters (= Tableau quick filters):**
   - Add a **Filter** widget → field `region` (single/multi-select).
   - Add a **Date range** filter on `admit_date`.
   - Show that selecting a region updates **every** widget bound to it.
4. **Cross-filtering (= Tableau dashboard actions):** click a bar in the facility chart → watch linked widgets filter. Call this out explicitly - it's a big Tableau-action time-saver with zero config.
5. **Drill-down:** on the line/bar chart, add a hierarchy `region → facility_name → provider_name` (drill fields). Click to drill down a level. This is the "aggregate, then drill" pattern Carla asked for.

**Tableau parity moment:** "Filters, actions, and drill - the interactivity you build deliberately in Tableau is mostly default behavior here."

### Break (2:10–2:25)

---

## 3 · AI-assisted authoring + the semantic layer (2:25–3:05)

**Goal:** Build with the assistant; introduce metric views as the governed definition layer.

**AI-assisted authoring (~20 min):**
1. On the dashboard, open the **Assistant** (✨) → type a plain-English ask, e.g.:
   - "Show average length of stay by specialty as a bar chart."
   - "Add a chart of complication rate by clinical category over time."
2. Accept/adjust the generated visual. Show editing the underlying SQL if you want precision.

**The semantic layer / metric views (~20 min):**
1. Frame it: "In Tableau, your published data source holds the blessed calculations everyone reuses. Here that's a **metric view** - governed measures and dimensions in one place."
2. Show the pre-built metric view (or create live):
   ```sql
   -- Example measures: readmission rate, mortality rate, avg LOS, total paid
   -- Dimensions: region, facility, provider, specialty, clinical_category, month
   ```
3. Point at: one definition of "readmission rate," used identically in dashboards and Genie. No more three analysts, three slightly different numbers.

**Skeptic hook:** "This is the governance answer - the metric is defined once, by you, and everything downstream inherits it."

---

## 4 · Genie - ask your data in plain language (3:05–3:40)

**Goal:** Natural-language querying on the same data; show the SQL; talk trust.

1. Open the pre-built **Genie space** (see `genie/genie_space_config.md`).
2. Ask a few sample questions live (let attendees drive):
   - "How many encounters were there in 2024 by region?"
   - "Which providers have the highest 30-day readmission rate, minimum 200 encounters?"
   - "What's the average length of stay for knee replacements?"
3. **For the query-focused / skeptic analyst:** click **Show generated code**. "Genie writes Databricks SQL - a fast way to see the right dialect and functions when you're translating from what you write today."
4. **Trust & governance:** show the "Trusted" badge on assets, the end-user feedback options (Yes / Fix it / Request review), the Analysis view, and that Genie only sees tables you grant.

**Skeptic hook:** "You don't have to trust the black box - every answer comes with the SQL, and you can correct it. It's a faster first draft, not a replacement for your judgment."

---

## Wrap & Day-2 setup (3:40–3:50)

- Recap: dashboards, AI-assisted authoring, metric views, Genie.
- **Confirm each analyst's Day-2 scenario** - a question to answer or a report/dashboard to recreate. Capture it so we can pre-stage anything needed.
- Reminder: tomorrow is mostly hands-on build.

## Facilitator notes
- Keep theory short; if a segment lands fast, push further on drill-downs or metric views (the eager analyst will want this).
- Have the generated SQL ready to paste so nobody stalls on typos.
- If the skeptic pushes back, lean into "the SQL is always visible" and "the metric is defined once, by you."
