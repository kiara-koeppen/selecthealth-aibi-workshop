# Attendee Workbook - SelectHealth AI/BI Workshop

Welcome. Over two days you'll get hands-on with Databricks AI/BI dashboards and Genie, working from a shared synthetic medical dataset (no PHI). This workbook is your step-by-step. Follow along on your own screen, and ask questions any time.

**A note up front:** AI/BI dashboards are not a one-to-one replacement for Tableau, and that's okay. The goal is to see where this way of working makes your life easier, and where you'd keep Tableau. As you go, keep a running list of what you like and what you miss.

## The dataset
Everything lives in `demo.selecthealth_workshop`:

| Table | What it is |
|---|---|
| `fact_encounters` | One row per patient encounter. ~80,000 rows over Jan 2023 to Dec 2025. Outcome flags: `readmitted_30d`, `mortality_flag`, `complication_flag`. |
| `dim_provider` | Providers, their specialty, and primary facility. |
| `dim_facility` | Hospitals and clinics, with type, city, state, region. |
| `dim_diagnosis` | ICD-10 codes with plain-language descriptions and clinical category. |
| `dim_procedure` | Procedure codes (incl. 27447 total knee replacement). |

**Tableau translation cheat sheet** (keep this handy):

| Tableau | Databricks AI/BI |
|---|---|
| Workbook | Dashboard |
| Worksheet | Visualization widget |
| Published data source / LOD calc | Metric view (governed measures + dimensions) |
| Ask Data | Genie (natural-language querying) |
| Calculated field | Dataset column or dashboard calculated measure |
| Quick filter | Filter widget |
| Dashboard action | Cross-filtering (mostly automatic) |

## How AI/BI dashboards work (read this first)
An AI/BI dashboard has two tabs at the top, and this trips everyone up at first:

- **Data tab:** where you define **datasets** (SQL queries). A dataset is just the data. On its own it does not show anything on the canvas.
- **Canvas tab:** where you lay out the **visuals**. You add a visualization widget and point it at a dataset.

**The core loop you'll repeat all day:** define a dataset on the Data tab, then go to the Canvas tab and drop a visualization that reads from it.

**How to add any visualization (you'll do this constantly):**

- Go to the **Canvas** tab.
- Click **Add a visualization** and draw the box on the canvas.
- In the config panel on the right: pick the **Dataset**, then the **Visualization** type (table, bar, line, combo, heatmap, map, pivot, counter), then choose which fields to show.

That's it. Everywhere below where it says "add a table" or "add a combo chart," that means this same loop.

---

# DAY 1

> **Capabilities we will cover today:** rich interactive visuals (combo, heatmap, map, pivot, scorecard), calculated dimensions and measures, parameterized widgets, cross-filtering, drilling, forecasting and AI functions, multipage reporting, and Ask Genie from a published dashboard. The companion one-pager has a quick reference for each.

## Part 1 - The dataset is your analytics engine (window functions, ranking, period-over-period)

The key idea: a dataset is **full Databricks SQL**. The things you do with table calcs, LOD expressions, and rank in Tableau are just window functions here, defined once in the dataset and reused by every widget. We'll go straight to the kind of analysis you actually do.

**Step 1 · Create the dashboard.**

- In the left nav, click **Dashboards**, then **Create dashboard**. Name it "My SelectHealth Workshop".
- You'll open on the **Canvas** tab, with a **Data** tab right next to it at the top.

**Step 2 · Create the `Provider performance` dataset.** This ranks providers by risk outcome with a percentile and quartile (min 200 encounters).

- Go to the **Data** tab and click **Create from SQL**.
- Paste the query below, click **Run** to preview the rows, and name the dataset `Provider performance`.

```sql
WITH prov AS (
  SELECT p.provider_name, p.specialty, COUNT(*) AS enc,
         AVG(e.readmitted_30d)*100 AS readmit_rate,
         AVG(e.complication_flag)*100 AS comp_rate,
         AVG(e.length_of_stay_days) AS avg_los
  FROM demo.selecthealth_workshop.fact_encounters e
  JOIN demo.selecthealth_workshop.dim_provider p USING (provider_id)
  GROUP BY p.provider_name, p.specialty
  HAVING COUNT(*) >= 200
)
SELECT provider_name, specialty, enc,
       ROUND(readmit_rate,1) AS readmit_rate_pct,
       ROUND(comp_rate,1)    AS comp_rate_pct,
       ROUND(avg_los,1)      AS avg_los_days,
       ROUND(PERCENT_RANK() OVER (ORDER BY readmit_rate),2) AS readmit_pctile,
       NTILE(4) OVER (ORDER BY readmit_rate) AS readmit_quartile
FROM prov
```

**Step 3 · Put it on the canvas as a table.**

- Go to the **Canvas** tab and click **Add a visualization**.
- In the config panel: set **Dataset** = `Provider performance`, and **Visualization** = **Table**.
- The table shows your dataset columns. In the table's settings, add **conditional formatting** to color `readmit_quartile` (or `readmit_rate_pct`) on a red-to-green scale.
- That's your provider scorecard: ranked and risk-binned, with no table-calc plumbing.

**Step 4 · Create the `Outcome trend` dataset and add a combo chart.** This is period-over-period with a rolling average (LAG + a windowed AVG).

- **Data** tab → **Create from SQL** → paste the query below → name it `Outcome trend`.

```sql
WITH m AS (
  SELECT DATE_TRUNC('month', admit_date) AS month, COUNT(*) AS encounters,
         AVG(readmitted_30d)*100 AS readmit_rate
  FROM demo.selecthealth_workshop.fact_encounters
  GROUP BY 1
)
SELECT month, encounters,
       encounters - LAG(encounters,1)  OVER (ORDER BY month) AS mom_change,
       ROUND(100.0*(encounters - LAG(encounters,12) OVER (ORDER BY month))
             / LAG(encounters,12) OVER (ORDER BY month), 1) AS yoy_pct,
       ROUND(AVG(encounters) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW),0)
             AS rolling_3mo,
       ROUND(readmit_rate,1) AS readmit_rate_pct
FROM m
```

- **Canvas** tab → **Add a visualization** → **Dataset** = `Outcome trend`, **Visualization** = **Combo**.
- Set bars = `encounters` and a line = `rolling_3mo` on a second axis. Optionally add `yoy_pct` as a second line or a small separate chart.

**Step 5 · Add calculated fields (no code).** You don't have to do everything in SQL.

- On a dataset (Data tab), add a **calculated measure** with a formula, for example a paid-to-charge ratio: `SUM(total_paid) / SUM(total_charges)`.
- Add a **calculated dimension** that bins a field, for example an age band: `CASE WHEN patient_age < 40 THEN '<40' WHEN patient_age < 65 THEN '40-64' ELSE '65+' END`.
- Use them in any visual. They recompute automatically as filters change.

> **Tableau translation:** `PERCENT_RANK` / `NTILE` replace your rank table calcs; `LAG` and the windowed `AVG` replace the running/difference table calcs and the trailing-average trick; the calculated measure/dimension is your calculated field. They live in the dataset, governed and reusable, instead of per-worksheet.

---

## Part 2 - Advanced visuals, parameters, and benchmarks

Same loop as before (Data tab to define, Canvas tab to visualize). This part adds interactivity and the richer chart types.

**Step 1 · Parameterized widget (like a Tableau parameter).**

- Add a dashboard **parameter** named `min_encounters` (whole number, default `200`).
- Edit the `Provider performance` dataset and change the HAVING line to use it:

```sql
HAVING COUNT(*) >= :min_encounters
```

- Bind the parameter widget on the canvas. Now the whole scorecard re-thresholds live as you change the value.

**Step 2 · Benchmark vs peer group (a window over a grouped aggregate).**

- **Data** tab → **Create from SQL** → name it `Facility vs region`.

```sql
SELECT f.region, f.facility_name,
       ROUND(AVG(e.readmitted_30d)*100,1) AS rate_pct,
       ROUND(AVG(e.readmitted_30d)*100
             - AVG(AVG(e.readmitted_30d)*100) OVER (PARTITION BY f.region),1) AS vs_region_avg_pts
FROM demo.selecthealth_workshop.fact_encounters e
JOIN demo.selecthealth_workshop.dim_facility f USING (facility_id)
GROUP BY f.region, f.facility_name
```

- Add a **Table** on it (Canvas → Add a visualization → Dataset = `Facility vs region` → Table). Apply diverging conditional formatting on `vs_region_avg_pts` (red below 0, green above): instantly shows which facilities run hot or cold versus their region.

**Step 3 · Heatmap.**

- **Data** tab → **Create from SQL** → name it `Category x region`.

```sql
SELECT d.clinical_category, f.region,
       ROUND(AVG(e.complication_flag)*100,1) AS comp_rate_pct, COUNT(*) AS enc
FROM demo.selecthealth_workshop.fact_encounters e
JOIN demo.selecthealth_workshop.dim_facility f USING (facility_id)
JOIN demo.selecthealth_workshop.dim_diagnosis d ON e.primary_icd10_code = d.icd10_code
GROUP BY d.clinical_category, f.region
```

- Add a **Heatmap** (Canvas → Add a visualization → Dataset = `Category x region` → Heatmap): x = `region`, y = `clinical_category`, color = `comp_rate_pct`.

**Step 4 · Map.**

- **Data** tab → **Create from SQL** → name it `By state`.

```sql
SELECT f.state, COUNT(*) AS enc, ROUND(AVG(e.readmitted_30d)*100,1) AS readmit_rate_pct
FROM demo.selecthealth_workshop.fact_encounters e
JOIN demo.selecthealth_workshop.dim_facility f USING (facility_id)
GROUP BY f.state
```

- Add a **Choropleth map** keyed on `state`, colored by `readmit_rate_pct`.

**Step 5 · Pivot table.**

- Add a **Pivot** visualization on the encounters: rows = `clinical_category`, columns = `encounter_type`, value = count of encounters. (Point it at a dataset that selects those fields, or reuse one that has them.)

**Step 6 · Forecasting and AI functions.** Project the next six months of volume with the built-in `ai_forecast` function.

- **Data** tab → **Create from SQL** → name it `Volume forecast`.

```sql
WITH monthly AS (
  SELECT DATE_TRUNC('month', admit_date) AS ds, COUNT(*)::DOUBLE AS y
  FROM demo.selecthealth_workshop.fact_encounters
  GROUP BY 1
)
SELECT ds, y AS encounters, NULL AS forecast, NULL AS lower, NULL AS upper FROM monthly
UNION ALL
SELECT ds, NULL, y_forecast, y_lower, y_upper
FROM AI_FORECAST(TABLE(monthly), horizon => '2026-06-01', time_col => 'ds', value_col => 'y')
```

- Add a **Line** chart plotting `encounters` and `forecast`, with `lower`/`upper` as a band. Other built-in AI functions you can call the same way in SQL: `ai_query`, `ai_classify`, `ai_extract`, `ai_summarize`.

**Step 7 · Interactivity: filters, cross-filtering, drill.**

- Add a **Filter** widget on `region` and a **Date range** filter on `admit_date` (Canvas → Add a visualization → choose Filter). Selecting a value updates every bound widget.
- **Cross-filter:** click a mark in any chart and watch the other widgets filter to match (like a Tableau dashboard action, no setup).
- **Drill-down:** on a chart, add a hierarchy `region` then `facility_name` then `provider_name`, and click to drill a level at a time.

**Step 8 · Multipage reporting.**

- Use the **page tabs** at the top of the canvas to split the dashboard into pages, for example **Overview** (KPIs + trend + forecast), **Provider performance** (the scorecard + parameter), and **Geography** (map + region benchmark). Filters can be shared across pages.

**Step 9 · Themes (optional).**

- Under dashboard settings you can apply a **theme** (colors, fonts) for a branded look. We're not focusing on branding today, but it's there for when you share externally.

> **Honest trade-off:** Tableau is still ahead on a few things: very fine-grained reference lines/bands, some niche chart types, and certain LOD nuances. The counter that matters for you: rich interactive visuals, cross-filtering, drilling, parameters, calculated fields, forecasting, and multipage reports are all here, and anything you can express in SQL is first-class, so you're rarely boxed in.

---

## Part 3 - Build with AI: the assistant and the semantic layer

**Step 1 · AI-assisted authoring.**

- On the dashboard, open the **Assistant** (the sparkle icon) and type a plain-English request, for example "Show average length of stay by specialty as a bar chart," or "Add a chart of complication rate by clinical category."
- Accept the result, then tweak it. You can open and edit the underlying SQL if you want exact control.

**Step 2 · Metric views (the semantic layer).**

- This is the equivalent of a Tableau published data source. Measures (like readmission rate) and dimensions are defined once, governed, and reused everywhere, so everyone's numbers match. Your instructor will show one.

> **Why it matters:** define "readmission rate" once and every dashboard and Genie answer uses the same definition. No more slightly different numbers across analysts.

---

## Part 4 - Publish your dashboard and turn it into a Genie space

Now the fun part. You'll publish the dashboard you just built, spin up a Genie space directly from it, give it a few instructions, and ask questions in plain language.

**Step 1 · Publish.**

- Click **Publish** (top right) to publish your dashboard.

**Step 2 · Create a Genie space from the dashboard.**

- From your published dashboard, use the **Genie** / "Create Genie space" control on the dashboard. This builds a Genie space on your dashboard's data.

**Step 3 · Add instructions.**

- Open the new Genie space and find the **Instructions** area. Paste in the block below (your instructor also shares it). Save.

Instructions block to paste:
```
This Genie space answers questions about synthetic hospital encounters. There is no PHI.

Data model:
- fact_encounters is the central fact table, one row per patient encounter.
- Join to dim_provider on provider_id, dim_facility on facility_id,
  dim_diagnosis on primary_icd10_code = icd10_code, and dim_procedure on
  primary_procedure_code = procedure_code. (These foreign keys are already defined.)

Metric definitions (express all rates as a percentage from 0 to 100):
- Readmission rate = AVG(readmitted_30d) * 100
- Mortality rate = AVG(mortality_flag) * 100
- Complication rate = AVG(complication_flag) * 100
- Average length of stay = AVG(length_of_stay_days), in days

Conventions:
- When ranking providers or facilities by a rate, only include those with at least
  200 encounters unless the user asks otherwise.
- Show plain-language names in results (provider_name, facility_name, region,
  clinical_category, procedure_description), not the id columns.
- "knee replacement" means primary_procedure_code = '27447'.
- Round rates to one decimal place and currency to whole dollars.
```

**Step 4 · Ask a few questions.** Try these, then your own:

- "How many encounters were there in 2024 by region?"
- "Which providers have the highest 30-day readmission rate, with at least 200 encounters?"
- "What is the average length of stay for a knee replacement?"

**Step 5 · Show the SQL.** On any answer, click **Show generated code** to see the Databricks SQL Genie wrote.

> **Why this is so quick:** the dataset is fully documented (every column has a description and the table relationships are defined), so Genie already knows how to join the tables. You only add a few instructions on top.
>
> **For the SQL folks:** Genie writes Databricks SQL, so it's a fast way to see the correct syntax and functions when you translate from what you write today. Copy it and build on it.
>
> **Trust:** every answer shows its SQL, Genie only sees tables you've been granted, and you can give feedback (Yes / Fix it / Request review). It's a fast first draft, not a black box.

---

## End of Day 1
Jot down, for the wrap-up:

- One thing that was faster or easier than Tableau.
- One thing you'd miss from Tableau.
- **Your Day-2 scenario:** a question you want answered, or a report/dashboard you'd like to recreate. If you have an existing Tableau dashboard in mind, bring it.

---

# DAY 2 - Build your own scenario

Pick a scenario (yours, or one below) and build it. Instructors will float to help. Aim for something you can show the group in a few minutes. Same loop as Day 1: define a dataset on the Data tab, then add visualizations on the Canvas.

**Starter scenarios:**

| Scenario | Good for practicing | Starter query (adapt freely) |
|---|---|---|
| Provider outcomes scorecard | aggregation, ranking, thresholds | `SELECT p.provider_name, COUNT(*) enc, ROUND(100.0*SUM(e.complication_flag)/COUNT(*),1) comp_rate FROM demo.selecthealth_workshop.fact_encounters e JOIN demo.selecthealth_workshop.dim_provider p USING(provider_id) GROUP BY 1 HAVING enc>200 ORDER BY comp_rate DESC` |
| Knee replacement deep-dive | filtering to a procedure, trend | filter `primary_procedure_code = '27447'`; trend LOS and readmit over time; split by facility |
| Cost vs. outcome | two measures, scatter | `SELECT f.facility_name, AVG(e.total_paid) avg_paid, 100.0*SUM(e.readmitted_30d)/COUNT(*) readmit_rate FROM demo.selecthealth_workshop.fact_encounters e JOIN demo.selecthealth_workshop.dim_facility f USING(facility_id) GROUP BY 1` |
| Payer mix by region | stacked bar, categorical split | `SELECT f.region, e.payer_type, COUNT(*) enc FROM demo.selecthealth_workshop.fact_encounters e JOIN demo.selecthealth_workshop.dim_facility f USING(facility_id) GROUP BY 1,2` |
| Genie-first | NL querying, then save to dashboard | ask the Genie space, then add a good answer to a dashboard |
| Rebuild one of your Tableau dashboards | direct comparison | recreate a dashboard you know well and note what's easier and what's missing |

**As you build, try at least one of each:**

- A filter and cross-filtering between two widgets.
- A drill-down hierarchy.
- A question in Genie, with the SQL revealed.

**Share-out:** be ready to show what you built, what surprised you, and your honest read on where this fits versus Tableau.
