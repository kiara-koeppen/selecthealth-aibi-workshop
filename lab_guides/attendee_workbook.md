# Attendee Workbook - SelectHealth AI/BI Workshop

Welcome. Over two days you'll get hands-on with Databricks AI/BI dashboards and Genie, working from
a shared synthetic medical dataset (no PHI). This workbook is your step-by-step. Follow along on
your own screen. Ask questions any time.

**A note up front:** AI/BI dashboards are not a one-to-one replacement for Tableau, and that's okay.
The goal is to see where this way of working makes your life easier (and where you'd keep Tableau).
As you go, keep a running list of what you like and what you miss.

## The dataset
Everything lives in `kk_test.selecthealth_workshop`:

| Table | What it is |
|---|---|
| `fact_encounters` | One row per patient encounter. ~80,000 rows over Jan 2023 to Dec 2025. Has outcome flags: `readmitted_30d`, `mortality_flag`, `complication_flag`. |
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

---

# DAY 1

## Part 1 - Your first dashboard: aggregate by provider and facility

**You'll build:** a bar chart of readmission rate by facility, plus a provider table.

1. In the left nav, click **Dashboards**, then **Create dashboard**. Name it `My SelectHealth Workshop`.
2. Go to the **Data** tab, click **Create from SQL**, and paste this. Click **Run** to preview, and
   name the dataset `Facility outcomes`:
   ```sql
   SELECT f.facility_name, f.region,
          COUNT(*)                                          AS encounters,
          ROUND(100.0*SUM(e.readmitted_30d)/COUNT(*), 1)    AS readmit_rate_pct,
          ROUND(100.0*SUM(e.complication_flag)/COUNT(*), 1) AS complication_rate_pct
   FROM kk_test.selecthealth_workshop.fact_encounters e
   JOIN kk_test.selecthealth_workshop.dim_facility f USING (facility_id)
   GROUP BY f.facility_name, f.region
   ```
3. Go to the **Canvas** tab, click **Add a visualization**, choose **Bar**.
   - X axis: `facility_name`
   - Y axis: `readmit_rate_pct` (sort descending)
   - Title: "30-day readmission rate by facility"
4. Add a second dataset called `Provider volume`:
   ```sql
   SELECT p.provider_name, p.specialty, f.facility_name,
          COUNT(*)                          AS encounters,
          ROUND(AVG(e.length_of_stay_days), 1) AS avg_los_days
   FROM kk_test.selecthealth_workshop.fact_encounters e
   JOIN kk_test.selecthealth_workshop.dim_provider p USING (provider_id)
   JOIN kk_test.selecthealth_workshop.dim_facility f USING (facility_id)
   GROUP BY p.provider_name, p.specialty, f.facility_name
   ```
5. Add a **Table** visualization on `Provider volume`. Sort by `encounters` descending.

> **Notice:** the aggregation lives in the dataset, so every widget can reuse it. There's no extract
> and no refresh schedule. You're querying the lakehouse live.

**Checkpoint:** you should have one bar chart and one table.

---

## Part 2 - Make it interactive: trends, filters, drill-down

1. Add a dataset `Monthly trend`:
   ```sql
   SELECT DATE_TRUNC('month', e.admit_date) AS month,
          f.region,
          COUNT(*)                                       AS encounters,
          ROUND(100.0*SUM(e.mortality_flag)/COUNT(*), 2) AS mortality_rate_pct
   FROM kk_test.selecthealth_workshop.fact_encounters e
   JOIN kk_test.selecthealth_workshop.dim_facility f USING (facility_id)
   GROUP BY 1, 2
   ```
2. Add a **Line** visualization: X = `month`, Y = `encounters`, color/series = `region`.
   Title: "Monthly encounter volume by region".
3. Add a **Filter** widget on `region`, and a **Date range** filter on `admit_date`. Select a region
   and watch every bound widget update.
4. **Cross-filtering:** click a bar in your facility chart. Notice the other widgets filter to match
   (this is like a Tableau dashboard action, with no setup).
5. **Drill-down:** on a chart, add the hierarchy `region` then `facility_name` then `provider_name`.
   Click to drill down a level at a time.

> **Notice:** filters, cross-filtering, and drill are mostly default behavior here.

---

## Part 3 - Build with AI: the assistant and the semantic layer

1. Open the dashboard **Assistant** (the sparkle icon). Type a plain-English request, for example:
   - "Show average length of stay by specialty as a bar chart."
   - "Add a chart of complication rate by clinical category."
   Accept the result, then tweak it. You can open and edit the underlying SQL if you want exact control.
2. **Metric views (the semantic layer):** this is the equivalent of a Tableau published data source.
   Measures (like readmission rate) and dimensions are defined once, governed, and reused everywhere,
   so everyone's numbers match. Your instructor will show one.

> **Why it matters:** define "readmission rate" once and every dashboard and Genie answer uses the
> same definition. No more slightly different numbers across analysts.

---

## Part 4 - Build with Genie: ask your data in plain language

1. Open the workshop **Genie space** (your instructor will share the link).
2. Ask a few questions. Try these, then your own:
   - "How many encounters were there in 2024 by region?"
   - "Which providers have the highest 30-day readmission rate, with at least 200 encounters?"
   - "What's the average length of stay for knee replacements?"
3. On any answer, click **Show generated code** to see the Databricks SQL Genie wrote.

> **For the SQL folks:** Genie is a fast way to see the correct Databricks SQL syntax and functions
> when you're translating from what you write today. You can copy that SQL and build on it.
>
> **Trust:** every answer shows its SQL, Genie only sees tables you've been granted, and you can give
> feedback (Yes / Fix it / Request review). It's a fast first draft, not a black box.

---

## End of Day 1
Jot down, for the wrap-up:
- One thing that was faster or easier than Tableau.
- One thing you'd miss from Tableau.
- **Your Day-2 scenario:** a question you want answered, or a report/dashboard you'd like to recreate.
  If you have an existing Tableau dashboard in mind, bring it.

---

# DAY 2 - Build your own scenario

Pick a scenario (yours, or one below) and build it. Instructors will float to help. Aim for something
you can show the group in a few minutes.

**Starter scenarios:**

| Scenario | Good for practicing | Starter query (adapt freely) |
|---|---|---|
| Provider outcomes scorecard | aggregation, ranking, thresholds | `SELECT p.provider_name, COUNT(*) enc, ROUND(100.0*SUM(e.complication_flag)/COUNT(*),1) comp_rate FROM kk_test.selecthealth_workshop.fact_encounters e JOIN kk_test.selecthealth_workshop.dim_provider p USING(provider_id) GROUP BY 1 HAVING enc>200 ORDER BY comp_rate DESC` |
| Knee replacement deep-dive | filtering to a procedure, trend | filter `primary_procedure_code = '27447'`; trend LOS and readmit over time; split by facility |
| Cost vs. outcome | two measures, scatter | `SELECT f.facility_name, AVG(e.total_paid) avg_paid, 100.0*SUM(e.readmitted_30d)/COUNT(*) readmit_rate FROM kk_test.selecthealth_workshop.fact_encounters e JOIN kk_test.selecthealth_workshop.dim_facility f USING(facility_id) GROUP BY 1` |
| Payer mix by region | stacked bar, categorical split | `SELECT f.region, e.payer_type, COUNT(*) enc FROM kk_test.selecthealth_workshop.fact_encounters e JOIN kk_test.selecthealth_workshop.dim_facility f USING(facility_id) GROUP BY 1,2` |
| Genie-first | NL querying, then save to dashboard | ask the Genie space, then add a good answer to a dashboard |
| Rebuild one of your Tableau dashboards | direct comparison | recreate a dashboard you know well and note what's easier and what's missing |

**As you build, try at least one of each:**
- A filter and cross-filtering between two widgets.
- A drill-down hierarchy.
- A question in Genie, with the SQL revealed.

**Share-out:** be ready to show what you built, what surprised you, and your honest read on where this
fits versus Tableau.
