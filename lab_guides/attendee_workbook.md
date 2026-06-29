# Attendee Workbook - SelectHealth AI/BI Workshop

Welcome. Over two days you'll get hands-on with Databricks AI/BI dashboards and Genie, working from
a shared synthetic medical dataset (no PHI). This workbook is your step-by-step. Follow along on
your own screen. Ask questions any time.

**A note up front:** AI/BI dashboards are not a one-to-one replacement for Tableau, and that's okay.
The goal is to see where this way of working makes your life easier (and where you'd keep Tableau).
As you go, keep a running list of what you like and what you miss.

## The dataset
Everything lives in `demo.selecthealth_workshop`:

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
   FROM demo.selecthealth_workshop.fact_encounters e
   JOIN demo.selecthealth_workshop.dim_facility f USING (facility_id)
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
   FROM demo.selecthealth_workshop.fact_encounters e
   JOIN demo.selecthealth_workshop.dim_provider p USING (provider_id)
   JOIN demo.selecthealth_workshop.dim_facility f USING (facility_id)
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
   FROM demo.selecthealth_workshop.fact_encounters e
   JOIN demo.selecthealth_workshop.dim_facility f USING (facility_id)
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

## Part 4 - Publish your dashboard and turn it into a Genie space

Now the fun part. You will publish the dashboard you just built, spin up a Genie space directly from
it, give it a few instructions, and ask questions in plain language.

1. **Publish** your dashboard (the **Publish** button, top right).
2. From your dashboard, **create a Genie space from it** (use the Genie / "Create Genie space" control
   on the dashboard). This builds a Genie space on your dashboard's data.
3. Open the new Genie space and find the **Instructions** area. **Paste in** the instructions block
   your instructor shares (it is also below). Save.

   <details><summary>Instructions block to paste</summary>

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
   </details>

4. Ask a few questions. Try these, then your own:
   - "How many encounters were there in 2024 by region?"
   - "Which providers have the highest 30-day readmission rate, with at least 200 encounters?"
   - "What is the average length of stay for a knee replacement?"
5. On any answer, click **Show generated code** to see the Databricks SQL Genie wrote.

> **Why this is so quick:** the dataset is fully documented (every column has a description and the
> table relationships are defined), so Genie already knows how to join the tables. You only add a few
> instructions on top.
>
> **For the SQL folks:** Genie writes Databricks SQL, so it is a fast way to see the correct syntax and
> functions when you translate from what you write today. Copy it and build on it.
>
> **Trust:** every answer shows its SQL, Genie only sees tables you have been granted, and you can give
> feedback (Yes / Fix it / Request review). It is a fast first draft, not a black box.

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

**Share-out:** be ready to show what you built, what surprised you, and your honest read on where this
fits versus Tableau.
