# Day 2 Lab Guide — Build with your own scenario

**Facilitator:** Kiara (lead) + Clint (floating)
**Duration:** ~1h50 (12:00–1:50 CT). Mostly hands-on.
**Pre-req:** Day-1 scenarios captured per analyst. Pre-stage any extra tables/measures the night before.

---

## 0 · Recap & plan (12:00–12:10)

- 60-second refresher: dataset, dashboards, metric views, Genie.
- Lay out the session: ~50 min build, share-outs after the break.
- Restate each analyst's chosen scenario so expectations are clear.

---

## 1 · Hands-on build (12:10–1:00)

Each analyst builds a dashboard or answers their question on `kk_test.selecthealth_workshop`. Kiara and Clint float.

**Starter scenarios** (offer if someone doesn't have one ready):

| Scenario | Hits | Starter SQL |
|---|---|---|
| **Provider outcomes scorecard** | aggregation, ranking | `SELECT p.provider_name, COUNT(*) enc, ROUND(100.0*SUM(e.complication_flag)/COUNT(*),1) comp_rate FROM fact_encounters e JOIN dim_provider p USING(provider_id) GROUP BY 1 HAVING enc>200 ORDER BY comp_rate DESC` |
| **Knee replacement deep-dive** | filtering, the example Carla named | filter `primary_procedure_code = '27447'`, trend LOS + readmit over time, split by facility |
| **Cost vs. outcome** | scatter, two measures | `SELECT f.facility_name, AVG(e.total_paid) avg_paid, 100.0*SUM(e.readmitted_30d)/COUNT(*) readmit_rate FROM fact_encounters e JOIN dim_facility f USING(facility_id) GROUP BY 1` |
| **Payer mix by region** | stacked bar, categorical | `SELECT f.region, e.payer_type, COUNT(*) enc FROM fact_encounters e JOIN dim_facility f USING(facility_id) GROUP BY 1,2` |
| **Genie-first** (skeptic) | ask, then save answer to dashboard | use the Genie space, then "add to dashboard" on a good answer |

**Coaching cues:**
- **Query-focused analyst:** push on metric views and the SQL behind visuals; show parameters and calculated measures.
- **Tableau-focused analyst:** map every step to the Tableau equivalent; show cross-filtering and drill as the "free" wins.
- **Skeptic:** have them drive Genie and always reveal the SQL; let the tool earn trust.

### Break (1:00–1:10)

---

## 2 · Share-outs & advanced asks (1:10–1:40)

- Each analyst shares their screen for 3–5 min: what they built, what surprised them.
- Tackle advanced asks live as they surface:
  - **Drill-down** hierarchies (region → facility → provider).
  - **Calculated measures** on the dashboard (e.g., paid-to-charge ratio).
  - **Genie follow-ups** and saving answers into a dashboard.
  - Scheduling / sharing / permissions (the "publish" story vs. Tableau Server).

---

## 3 · Wrap & next steps (1:40–1:50)

- Map to reality: "Everything you did sits on synthetic data — but the exact same flow works on your real SelectHealth tables once they're in Databricks." Note governance (Unity Catalog) and that metric views keep definitions consistent across the team.
- Capture the team's honest read (this is an assessment for Carla to advise other teams).
- Next steps: who follows up, what to pilot on real data, any access/enablement gaps.

## Facilitator notes
- Protect build time — keep share-outs tight.
- If energy is high, the eager analyst may want embedding / Genie API / programmatic access; have a pointer ready but don't derail the room.
- Log unanswered questions for the follow-up rather than rabbit-holing live.
