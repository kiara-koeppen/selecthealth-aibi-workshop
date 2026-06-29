# Talk track - AI/BI Capabilities one-pager

Casual, spoken delivery (about 2 minutes). This is a quick orientation slide, so do not dwell on
any one card. Keep thinking out loud and tie each one back to Tableau.

---

Okay so, before we get our hands dirty, I just want to give you a quick lay of the land of what AI/BI
dashboards can actually do. Um, you all live in Tableau, so as I go through these, I want you thinking
"okay, where's my equivalent for that." This isn't the exhaustive list, it's just the stuff you'll
actually reach for.

So, top-left, cross-filtering. You click on any chart and the whole dashboard filters to what you
clicked, so it's kind of like a Tableau action, except you don't have to set anything up, it just
works. And right next to it, drilling, so you go from a summary down into the detail in place, like
region down to facility down to provider, without writing a new query.

Then forecasting and AI functions, and this one's kind of fun. So there are built-in functions, like
ai_forecast, where you can project, say, your encounter or readmission volume out a few months. And
there's others like ai_query and ai_classify, so you can do machine learning and even GenAI stuff right
in the dashboard, without leaving it and bugging a data scientist.

Calculated dimensions and measures, um, this is basically your calculated fields. So formula-based
metrics, like a paid-to-charge ratio, or taking age and binning it into age groups, and the nice part
is they recompute automatically as you filter.

Rich interactive visuals, so you've got combo charts, heatmaps, scatter, maps, pivot tables, all the
usual suspects. So that's what you'd lean on for, you know, a provider scorecard or a complication-rate
heatmap across your facilities.

Multipage reporting, so you can split one dashboard into multiple pages or tabs. Which is really handy,
because instead of cramming everything onto one screen, you can have like an Overview page, a Provider
Performance page, and a Geography page, and point different audiences at different views.

Parameterized widgets, um, these are the no-code controls, so dropdowns, date pickers, text inputs, and
they actually change the query underneath. So a business user can set, like, a minimum-encounter
threshold themselves and not have to touch any SQL.

Themes, so that's your colors, fonts, layout, the branding stuff. We're not really focusing on that
today, but just know it's there for when you want it to look on-brand to share out.

And then the last one, Ask Genie, which we're gonna spend real time on later, so I won't go deep now.
But basically you ask a question in plain English right inside the dashboard, and it answers you and
shows you the SQL it wrote.

And honestly the thing I'd leave you with is that line at the bottom: all of this is running on data
that's already in Databricks. So there's no extract, no separate BI server, it's just sitting on your
governed data. So, that's the menu. Let's go actually build with some of it.
