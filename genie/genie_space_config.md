# Genie Space - SelectHealth Workshop

Pre-built Genie space for the natural-language querying segment (Day 1) and the
"Genie-first" Day-2 scenario.

## Live space
- **Name:** SelectHealth Workshop - Encounters Genie
- **Space ID:** `01f173e9cad61c2cbd13dd24c3a3cc6f`
- **Workspace:** `kk_test` (adb-669602668219382.2.azuredatabricks.net)
- **Tables:** `kk_test.selecthealth_workshop.{fact_encounters, dim_provider, dim_facility, dim_diagnosis, dim_procedure}`

## Description (configured)
Natural-language querying over the synthetic medical dataset (no PHI). One row per
patient encounter joined to provider, facility, diagnosis (ICD-10), and procedure
dimensions. Every answer shows the generated Databricks SQL - useful for translating
between SQL dialects (the hook for the query-focused / AI-skeptic analyst).

## Sample questions (configured, shown to users)
1. How many encounters were there in 2024 by region?
2. Which 10 providers have the highest 30-day readmission rate, with at least 200 encounters?
3. What is the average length of stay for total knee arthroplasty (procedure 27447)?
4. Show the monthly encounter volume trend for the last 2 years.
5. Which facilities have the highest complication rate?
6. Compare mortality rate by clinical category.
7. What is the average total paid per encounter by payer type?

## Verified
Asked "What is the average length of stay for total knee arthroplasty (procedure 27447)?"
→ Genie generated correct SQL and returned **2.27 days**.

## Suggested instructions to add in the UI (optional polish before the workshop)
Genie answers improve with a few curated instructions. In the space's **Instructions**:
- "readmission rate" = `AVG(readmitted_30d)` (the column is 1/0); show as a percentage.
- "mortality rate" = `AVG(mortality_flag)`; "complication rate" = `AVG(complication_flag)`.
- When ranking providers or facilities by a rate, default to a minimum of 200 encounters
  unless the user says otherwise.
- Join `fact_encounters` to `dim_diagnosis` on `primary_icd10_code = icd10_code` and to
  `dim_procedure` on `primary_procedure_code = procedure_code`.
- Prefer plain-language labels: use `clinical_category`, `provider_name`, `facility_name`,
  and `region` in groupings rather than IDs.

## Facilitator tips
- Let the **AI-skeptic analyst** drive, and always click **Show generated code** so they
  see the Databricks SQL behind each answer.
- Use the provider-ranking question to show how Genie handles thresholds ("at least 200
  encounters") in plain language.
- If an answer looks off, use the **Fix it** / feedback flow to show the human-in-the-loop
  trust model rather than a black box.
