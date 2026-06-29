"""Builds the starter AI/BI (Lakeview) dashboard JSON for the SelectHealth workshop.

Single base dataset at encounter grain (joined to all dims) with widget-level
aggregation, so cross-filtering works out of the box. Writes
selecthealth_workshop.lvdash.json next to this file.
"""
import json, pathlib

CATALOG, SCHEMA = "kk_test", "selecthealth_workshop"

# Base dataset: one row per encounter, joined to dims, with per-row *_pct helper
# columns (0 or 100) so AVG(...) yields a readable percentage in widgets.
BASE_SQL = [
    "SELECT e.encounter_id, e.admit_date, e.encounter_type, e.payer_type, ",
    "       e.length_of_stay_days, e.total_charges, e.total_paid, ",
    "       e.readmitted_30d, e.mortality_flag, e.complication_flag, ",
    "       e.readmitted_30d*100.0 AS readmit_pct, ",
    "       e.mortality_flag*100.0 AS mortality_pct, ",
    "       e.complication_flag*100.0 AS complication_pct, ",
    "       p.provider_name, p.specialty, ",
    "       f.facility_name, f.region, f.facility_type, ",
    "       d.clinical_category ",
    f"FROM {CATALOG}.{SCHEMA}.fact_encounters e ",
    f"JOIN {CATALOG}.{SCHEMA}.dim_provider p USING (provider_id) ",
    f"JOIN {CATALOG}.{SCHEMA}.dim_facility f USING (facility_id) ",
    f"JOIN {CATALOG}.{SCHEMA}.dim_diagnosis d ON e.primary_icd10_code = d.icd10_code ",
]


def text(name, line, x, y, w, h):
    return {"widget": {"name": name, "multilineTextboxSpec": {"lines": [line]}},
            "position": {"x": x, "y": y, "width": w, "height": h}}


def counter(name, expr, fname, title, x, y):
    return {"widget": {"name": name,
            "queries": [{"name": "main_query", "query": {"datasetName": "encounters",
                "fields": [{"name": fname, "expression": expr}], "disaggregated": False}}],
            "spec": {"version": 2, "widgetType": "counter",
                     "encodings": {"value": {"fieldName": fname, "displayName": title}},
                     "frame": {"title": title, "showTitle": True}}},
            "position": {"x": x, "y": y, "width": 2, "height": 3}}


def bar(name, dim, dim_disp, measure_expr, measure_name, measure_disp, title, x, y, w=3, h=6):
    return {"widget": {"name": name,
            "queries": [{"name": "main_query", "query": {"datasetName": "encounters",
                "fields": [{"name": dim, "expression": f"`{dim}`"},
                           {"name": measure_name, "expression": measure_expr}],
                "disaggregated": False}}],
            "spec": {"version": 3, "widgetType": "bar",
                     "encodings": {
                         "x": {"fieldName": dim, "scale": {"type": "categorical"}, "displayName": dim_disp},
                         "y": {"fieldName": measure_name, "scale": {"type": "quantitative"}, "displayName": measure_disp}},
                     "frame": {"title": title, "showTitle": True}}},
            "position": {"x": x, "y": y, "width": w, "height": h}}


def line_by_region(name, title, x, y, w=6, h=6):
    return {"widget": {"name": name,
            "queries": [{"name": "main_query", "query": {"datasetName": "encounters",
                "fields": [{"name": "monthly(admit_date)", "expression": "DATE_TRUNC(\"MONTH\", `admit_date`)"},
                           {"name": "count(encounter_id)", "expression": "COUNT(`encounter_id`)"},
                           {"name": "region", "expression": "`region`"}],
                "disaggregated": False}}],
            "spec": {"version": 3, "widgetType": "line",
                     "encodings": {
                         "x": {"fieldName": "monthly(admit_date)", "scale": {"type": "temporal"}, "displayName": "Month"},
                         "y": {"fieldName": "count(encounter_id)", "scale": {"type": "quantitative"}, "displayName": "Encounters"},
                         "color": {"fieldName": "region", "scale": {"type": "categorical"}, "displayName": "Region"}},
                     "frame": {"title": title, "showTitle": True}}},
            "position": {"x": x, "y": y, "width": w, "height": h}}


def provider_table(name, title, x, y, w=6, h=7):
    fields = [
        {"name": "provider_name", "expression": "`provider_name`"},
        {"name": "specialty", "expression": "`specialty`"},
        {"name": "facility_name", "expression": "`facility_name`"},
        {"name": "count(encounter_id)", "expression": "COUNT(`encounter_id`)"},
        {"name": "avg(readmit_pct)", "expression": "AVG(`readmit_pct`)"},
        {"name": "avg(complication_pct)", "expression": "AVG(`complication_pct`)"},
        {"name": "avg(length_of_stay_days)", "expression": "AVG(`length_of_stay_days`)"},
    ]
    cols = [
        {"fieldName": "provider_name", "displayName": "Provider"},
        {"fieldName": "specialty", "displayName": "Specialty"},
        {"fieldName": "facility_name", "displayName": "Facility"},
        {"fieldName": "count(encounter_id)", "displayName": "Encounters"},
        {"fieldName": "avg(readmit_pct)", "displayName": "Readmit %"},
        {"fieldName": "avg(complication_pct)", "displayName": "Complication %"},
        {"fieldName": "avg(length_of_stay_days)", "displayName": "Avg LOS (days)"},
    ]
    return {"widget": {"name": name,
            "queries": [{"name": "main_query", "query": {"datasetName": "encounters",
                "fields": fields, "disaggregated": False}}],
            "spec": {"version": 2, "widgetType": "table",
                     "encodings": {"columns": cols},
                     "frame": {"title": title, "showTitle": True}}},
            "position": {"x": x, "y": y, "width": w, "height": h}}


def filt(name, field, disp, x, y, w=2, h=2):
    qn = f"ds_{field}"
    return {"widget": {"name": name,
            "queries": [{"name": qn, "query": {"datasetName": "encounters",
                "fields": [{"name": field, "expression": f"`{field}`"}], "disaggregated": False}}],
            "spec": {"version": 2, "widgetType": "filter-multi-select",
                     "encodings": {"fields": [{"fieldName": field, "displayName": disp, "queryName": qn}]},
                     "frame": {"showTitle": True, "title": disp}}},
            "position": {"x": x, "y": y, "width": w, "height": h}}


dashboard = {
    "datasets": [{"name": "encounters", "displayName": "Encounters (base)", "queryLines": BASE_SQL}],
    "pages": [
        {"name": "overview", "displayName": "Encounter & Outcomes Overview", "pageType": "PAGE_TYPE_CANVAS",
         "layout": [
            text("title", "# SelectHealth Workshop — Encounters & Outcomes", 0, 0, 6, 1),
            text("subtitle", "Synthetic medical encounters (no PHI). Aggregate by provider and facility, trend over time, drill into outcomes.", 0, 1, 6, 1),
            counter("kpi-encounters", "COUNT(`encounter_id`)", "count(encounter_id)", "Total encounters", 0, 2),
            counter("kpi-readmit", "AVG(`readmit_pct`)", "avg(readmit_pct)", "Readmission rate %", 2, 2),
            counter("kpi-complication", "AVG(`complication_pct`)", "avg(complication_pct)", "Complication rate %", 4, 2),
            text("hdr-outcomes", "## Outcomes by facility and service line", 0, 5, 6, 1),
            bar("bar-readmit-facility", "facility_name", "Facility", "AVG(`readmit_pct`)", "avg(readmit_pct)", "Readmit %", "30-day readmission rate by facility", 0, 6),
            bar("bar-enc-category", "clinical_category", "Clinical category", "COUNT(`encounter_id`)", "count(encounter_id)", "Encounters", "Encounters by clinical category", 3, 6),
            bar("bar-comp-category", "clinical_category", "Clinical category", "AVG(`complication_pct`)", "avg(complication_pct)", "Complication %", "Complication rate by clinical category", 0, 12),
            bar("bar-los-specialty", "specialty", "Specialty", "AVG(`length_of_stay_days`)", "avg(length_of_stay_days)", "Avg LOS (days)", "Average length of stay by specialty", 3, 12),
            text("hdr-trend", "## Volume trend", 0, 18, 6, 1),
            line_by_region("line-monthly-region", "Monthly encounter volume by region", 0, 19),
            text("hdr-providers", "## Provider performance", 0, 25, 6, 1),
            provider_table("table-providers", "Provider scorecard", 0, 26),
         ]},
        {"name": "filters", "displayName": "Filters", "pageType": "PAGE_TYPE_GLOBAL_FILTERS",
         "layout": [
            filt("f-region", "region", "Region", 0, 0),
            filt("f-category", "clinical_category", "Clinical category", 2, 0),
            filt("f-enctype", "encounter_type", "Encounter type", 4, 0),
            filt("f-payer", "payer_type", "Payer", 0, 2),
         ]},
    ],
}

out = pathlib.Path(__file__).parent / "selecthealth_workshop.lvdash.json"
out.write_text(json.dumps(dashboard, indent=2))
print("Wrote", out, "bytes:", out.stat().st_size)
