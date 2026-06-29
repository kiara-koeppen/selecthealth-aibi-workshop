# SelectHealth AI/BI Workshop: Agenda and Setup

Hi Carla, here is the plan for the two days, plus a short setup step so your team can
generate the same practice dataset in your own Databricks workspace ahead of time. The data
is fully synthetic (no PHI), but it is shaped to look like the provider and facility analysis
your team already does.

## Format
Hands-on and light on theory. The focus is AI/BI dashboards, with Genie (natural-language
querying) woven in. We will be candid about where this fits and where you would keep Tableau.

---

## Day 1 (Wednesday): What is possible in AI/BI
*12:00 to 3:50 p.m. CT / 11:00 a.m. to 2:50 p.m. MT, with two 15-minute breaks*

| Time (CT) | Segment | What we will do |
|---|---|---|
| 12:00 to 12:20 | Welcome and orientation | Goals for the two days, a tour of the dataset, and how AI/BI maps to your Tableau workflow. |
| 12:20 to 1:05 | Dashboard authoring I | Connect to the data, build your first charts, and aggregate outcomes by provider and facility. |
| 1:05 to 1:20 | Break | |
| 1:20 to 2:10 | Dashboard authoring II | Trends over time, drill-downs, filters, and cross-filtering between visuals. |
| 2:10 to 2:25 | Break | |
| 2:25 to 3:05 | AI-assisted authoring and the semantic layer | Build visuals from a prompt; metric views as the governed "published data source" equivalent. |
| 3:05 to 3:40 | Genie: ask your data in plain language | Ask questions in natural language, see the generated SQL, and talk through trust and governance. |
| 3:40 to 3:50 | Wrap and Day-2 setup | Recap and confirm the scenario each analyst wants to build on Day 2. |

## Day 2 (Thursday): Build with your own scenario
*12:00 to 1:50 p.m. CT / 11:00 a.m. to 12:50 p.m. MT, with one 10-minute break*

| Time (CT) | Segment | What we will do |
|---|---|---|
| 12:00 to 12:10 | Recap and plan | Quick refresher and lay out the build session. |
| 12:10 to 1:00 | Hands-on build | Each analyst builds a dashboard or answers a question (or rebuilds a Tableau dashboard they bring). |
| 1:00 to 1:10 | Break | |
| 1:10 to 1:40 | Share-outs and advanced asks | Walk through what you built; drill-downs, calculated measures, Genie follow-ups. |
| 1:40 to 1:50 | Wrap and next steps | How this maps to your real SelectHealth data and what comes next. |

---

## Before the workshop: generate the practice dataset

This creates the shared dataset in your workspace so everyone is working from the same tables.
It takes a few minutes. Your two analysts can do this, or we can do it together on a quick call.

1. **Get the workshop files.** I will share the workshop Git repo with you
   (`github.com/kiara-koeppen/selecthealth-aibi-workshop`). You can either add it as a Git folder
   in Databricks (Workspace > Create > Git folder, paste the repo URL), or I can just send you the
   single notebook file `data_generation/generate_workshop_data.py` to import (Workspace > Import).
2. **Open the notebook** `generate_workshop_data.py` and attach it to serverless compute.
3. **Set the widgets** at the top of the notebook:
   - `catalog`: `demo` (or any catalog your team can create a schema in). If a `demo` catalog
     does not exist yet, the notebook will try to create it. If your workspace requires a managed
     storage location for new catalogs, just create the catalog once in the UI
     (Catalog > Create catalog) first, then re-run.
   - `schema`: `selecthealth_workshop`
   - Leave the row count, provider, facility, and date widgets at their defaults.
4. **Run all.** On serverless this takes about one to two minutes. It creates five tables:
   `fact_encounters` plus `dim_provider`, `dim_facility`, `dim_diagnosis`, and `dim_procedure`.
5. **Quick check.** Run `SELECT COUNT(*) FROM demo.selecthealth_workshop.fact_encounters`. You
   should see about 80,000 rows.
6. **Share access.** Grant your two analysts `SELECT` on `demo.selecthealth_workshop` so everyone
   can build during the session.

That is all that is needed to be ready. If you would rather, I am happy to hop on for 15 minutes
and run this with you.

> Optional, and we can do these live together: import the starter dashboard
> (`dashboard/selecthealth_workshop.lvdash.json`, which points at the `demo` catalog) and create a
> Genie space on the five tables. Neither is required to start Day 1.

## What attendees need
- Access to your Databricks workspace, with `SELECT` on `demo.selecthealth_workshop`.
- A running SQL warehouse (serverless or pro).
- No other prep. Optionally, bring a question you want answered or a Tableau dashboard you would
  like to recreate for the Day-2 build.

## A note on the catalog name
We use `demo` as a neutral catalog name for the practice data. If your team prefers a different
catalog, just set the `catalog` widget to that name when you run the notebook. If you do, let me
know and I will point the starter dashboard at the same catalog (it is a one-line change).

## A note on flexibility
This agenda is a guide, not a script. If a topic sparks more interest we will lean in, and if
something lands quickly we will move on. The goal is for the team to get hands-on and form a
genuine opinion.
