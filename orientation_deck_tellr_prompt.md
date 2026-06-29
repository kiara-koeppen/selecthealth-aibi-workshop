Create a polished, professional orientation deck to open a hands-on AI/BI workshop for the SelectHealth analytics team. Audience is two senior analysts plus their manager, all heavy Tableau users evaluating whether Databricks AI/BI and Genie fit their work. This deck is only the first ~20 minutes of Day 1, before everyone goes hands-on, so keep it short, visual, and confident: around 9 to 11 slides. Use a dark theme (Databricks navy) with one tasteful accent color for callouts. Lead with credibility, not hype: be honest that this is not a one-to-one Tableau replacement. Keep healthcare context in mind (providers, facilities, patient outcomes). Favor comparison tables and side-by-side columns over dense bullet lists.

Use the following content as source material:

---

# SelectHealth AI/BI Workshop: Orientation

Hands-on with Databricks AI/BI Dashboards and Genie

## Framing (set the tone on slide 1 or 2)

This is a learning session, not a feature bake-off. Over two days the team will get hands-on and form an honest opinion about where Databricks AI/BI fits and where they would keep Tableau. The deck should feel candid and practical.

## What to expect

- Two days, hands-on. Light on theory, then you build.
- Day 1 is "what is possible." Day 2 is "build your own scenario."
- You will build two ways: manually, and with Genie and AI assistance.
- Goal: a genuine read on where this makes your work easier.

## Databricks and Unity Catalog in two minutes

- Your data lands once in the lakehouse.
- Unity Catalog governs who can see what.
- AI/BI dashboards and Genie read straight from that governed data.
- No data extract and no separate BI server to maintain.
- The compute is the same compute the team already uses, so this is low friction, not a big new cost. (This matters: cost control is a priority, and Microsoft Fabric tends to lead with cost.)

## What is an AI/BI Dashboard, and what is Genie

- A dashboard is datasets plus visuals on a canvas. Filters, drill-down, and cross-filtering are mostly built in.
- Genie lets anyone ask questions in plain language on the same governed data.
- Every Genie answer shows the SQL it generated, so it is inspectable, not a black box.

## The honest trade-off: AI/BI is not a one-to-one Tableau replacement (key slide, use two columns)

The way people consume analytics is changing, and that is the real story, not pixel-perfect chart parity. Be upfront about both sides.

| Where Tableau still leads | Where AI/BI changes the game |
|---|---|
| Pixel-level formatting control | Plain-language querying with Genie |
| Some advanced chart types | Metrics defined once, governed, and reused |
| Your team's deep muscle memory | AI-assisted authoring |
| | Runs on data already in Databricks: low friction, no big new cost |

The question for the two days is not "is this Tableau," it is "where does this way of working make our lives easier, and where would we keep Tableau."

## How this maps to your Tableau workflow (use a clean mapping table)

| Tableau | Databricks AI/BI |
|---|---|
| Workbook | Dashboard |
| Worksheet | Visualization widget |
| Published data source | Metric view (governed measures and dimensions) |
| Ask Data | Genie (natural language) |
| Calculated field | Dataset column or dashboard calculated measure |
| Dashboard action | Cross-filtering (mostly automatic) |

## Two ways to build, and you will do both (use two columns)

| Build manually | Build with Genie and AI |
|---|---|
| Create datasets with SQL | Ask in plain language and see the SQL |
| Drop in bar, line, and table visuals | Use the assistant to draft visuals |
| Add filters, drill-down, cross-filtering | Save a Genie answer into a dashboard |

## The dataset we will use

- Synthetic medical encounters. No PHI, so everyone can build freely.
- Encounters joined to provider, facility, diagnosis (ICD-10), and procedure.
- Real-looking codes and procedures, including knee replacement.
- Outcomes: 30-day readmission, mortality, and complications.
- Built to aggregate by provider and facility, trend over time, and drill down. This mirrors the provider and facility analysis the team already does.

## Day 2: bring your own scenario

- Pick a question you want answered, or a report you want to recreate.
- If you have a Tableau dashboard in mind, bring it and rebuild it here.
- We build, then share out what surprised us.
- Capture the honest read: where this helps, and where Tableau still wins.

## Closing slide

End on a short, confident line such as "Let's build" and the workshop name.
