# Data Storytelling Guide for Medical and Academic Presentations

This document is the primary reference for presenting data with narrative in medical and academic talks. Every instruction here is actionable. Every pattern includes a concrete example from the medical or scientific domain. Use this alongside the Storytelling Guide and Slide Design Guide — data visualization is one component of a complete presentation strategy.

---

## 1. Core Principle — Cole Nussbaumer Knaflic

**Data does not speak for itself.** A p-value of 0.03, a hazard ratio of 0.72, a forest plot with all diamonds to the left — none of these communicate anything on their own. The presenter must provide context, highlight what matters, and tell the audience what the data means for them, their patients, or their field.

This is the most common failure in medical presentations: a researcher shows a slide full of numbers and says "as you can see." The audience cannot see. They have not spent three years staring at this dataset. You have. Your job is to transfer the meaning you have extracted, not to display the raw evidence and hope the audience catches up.

### The Big Idea

Before building any data slide, write one sentence that contains:

1. Your unique point of view on the data
2. What is at stake for the audience if they accept or reject that view

This sentence becomes your north star. Every chart, annotation, and caption on that slide should serve it.

**Template:**
> [My finding / unique interpretation], which means [consequence for patients / clinical practice / future research].

**Medical example — clinical trial result:**
> "Sacubitril/valsartan reduced cardiovascular death by 20% compared to enalapril in heart failure with reduced ejection fraction, meaning clinicians who continue prescribing ACE inhibitors alone as first-line therapy are leaving proven mortality benefit on the table."

**Medical example — epidemiological finding:**
> "Type 2 diabetes is now diagnosed in one in four patients over 65 in our region, meaning the current screening protocol — which flags patients only on referral — is structurally incapable of identifying the majority of prevalent cases."

Write this sentence first. If you cannot write it, you do not yet understand what your data is saying. Do not build the slide until you can.

---

## 2. Choosing the Right Visual

Selecting the wrong chart type forces the audience to do cognitive work that should have been done in advance. Choose the chart that makes the most important comparison or relationship immediately visible.

### Comparison — Bar Chart (Vertical or Horizontal)

Use when you are comparing discrete categories to each other. Vertical bars work for a small number of categories (up to ~6). Horizontal bars work when category labels are long or when there are more than 6 groups.

**Medical example:** Comparing 30-day readmission rates across five hospital departments. Use a horizontal bar chart — department names are long, and ranking bars from top (lowest) to bottom (highest) makes the performance gap immediately clear without requiring axis reading.

**Do not use a bar chart to show trends over many time points.** A bar chart with 12 monthly bars forces the audience to mentally connect the tops of bars. Use a line chart instead.

### Trend Over Time — Line Chart

Use when the data point is the trajectory, not the individual values. The slope of the line is the message.

**Medical example:** Weekly confirmed influenza cases over a 16-week season. A single line chart shows the epidemic curve — when the surge began, when it peaked, when it resolved — at a glance. If you overlay two seasons on the same axes, the audience immediately sees whether this season's peak arrived earlier or later and whether the magnitude differed.

**Rule:** Only overlay multiple lines if the comparison between them is the core message. If you are showing three lines that mostly overlap, your message is probably not about trend — reconsider the chart type.

### Part-to-Whole — Stacked Bar or Simple Pie (Maximum 3 Segments)

Use when you want to show composition. A pie chart is acceptable when there are 2 or 3 segments and one segment is clearly dominant — the arc makes proportionality viscerally obvious. Beyond 3 segments, angles become unreadable; switch to a stacked bar.

**Medical example:** Treatment adherence breakdown — 68% fully adherent, 22% partially adherent, 10% non-adherent. A simple pie chart with direct labels communicates this in two seconds. A table with the same numbers takes five seconds to read and is not remembered.

**Do not use a pie chart to show six payer-mix categories, seven comorbidity subtypes, or any composition where no single segment dominates.** Use a stacked bar chart sorted by the category of interest.

### Correlation — Scatter Plot

Use when you want to show the relationship between two continuous variables across individual observations or studies.

**Medical example:** A meta-analysis scatter plot with mean patient age on the x-axis and effect size (odds ratio) on the y-axis, with one point per included study. A regression line through the points shows whether older patient populations experienced stronger or weaker treatment effects. This reveals effect modification by age that a forest plot cannot show.

**Always label outlier points directly.** An unlabeled outlier in a clinical scatter plot creates anxiety and distrust. If a point is far from the trend, annotate it: "ACCORD trial — intensive glycemic control arm."

### Distribution — Histogram or Box Plot

Use when the shape of variation is the message, not the mean alone.

**Medical example — histogram:** Time from symptom onset to emergency department presentation in STEMI patients. A right-skewed histogram with a long tail shows that while the median is 90 minutes, a meaningful proportion of patients wait over 4 hours. The mean alone hides this clinically critical subgroup.

**Medical example — box plot:** Comparison of creatinine clearance distributions across three treatment arms at 12 months. Box plots across the three arms show medians, interquartile ranges, and outliers simultaneously. A bar chart showing means would hide the variance and make three statistically distinct distributions look nearly identical.

### Survival Data — Kaplan-Meier Curve (Annotated)

The KM curve is the standard for time-to-event data in clinical research. It requires specific annotation to be interpretable.

**Required elements on every KM curve shown in a talk:**

- At-risk table below the x-axis (number of patients remaining at each time point)
- Vertical annotation line at the time point where curves separate meaningfully
- Direct labels on each curve at the right margin (not a legend)
- Hazard ratio and confidence interval stated in the title or as a text annotation, not buried in a legend

**Medical example:** PARADIGM-HF trial primary endpoint. The KM curve shows event-free survival for sacubitril/valsartan vs. enalapril over 36 months. Annotation belongs at month 8, where the curves first visibly separate — draw a vertical dashed line there and annotate: "Curves separate at 8 months." The chart title states the conclusion: "Sacubitril/valsartan reduced the composite endpoint by 20% (HR 0.80, 95% CI 0.73–0.87)."

---

## 3. Annotating Charts

Never show a raw figure and say "as you can see." This phrase is a signal that the presenter has not done the work of deciding what the audience should see.

### The Three Rules of Annotation

**Rule 1 — Point to exactly what matters.** Circle the key data point. Draw an arrow to the separation between curves. Add a callout box to the outlier study. If you do not annotate it, the audience's eye will wander and they may not find it.

**Rule 2 — Label directly.** Remove the legend. Label each series, bar, or line directly at its endpoint or alongside the relevant data region. Legends force the audience to look away from the data to decode color, then look back, then remember. Direct labels eliminate this round-trip.

**Rule 3 — Put the "so what" in the title.** Chart titles should be assertions, not descriptions. A descriptive title ("Figure 3: Survival by treatment arm") tells the audience what to look at. An assertion title ("Immunotherapy extended median survival by 4.7 months in PD-L1-positive patients") tells them what to think. Use assertion titles on every slide shown to a clinical or scientific audience.

### Full Example — Annotated KM Curve

Bad title: "Kaplan-Meier estimates of progression-free survival"
Bad annotations: color legend in the corner, no at-risk table, no callout

Good title: "Pembrolizumab doubled progression-free survival vs. chemotherapy in PD-L1 ≥50% NSCLC (HR 0.50)"
Good annotations:
- At-risk table beneath x-axis
- Vertical dashed line at the month-6 mark where curves diverge
- Text annotation at the divergence: "Curves separate at 6 months and maintain separation"
- Direct curve labels at right margin: "Pembrolizumab (n=154)" and "Chemotherapy (n=151)"
- HR and 95% CI box in the open chart area, not in a legend

The annotated version eliminates the phrase "as you can see" because the annotation has already done that work. You say: "The curves separate at six months and that separation holds through month 24, giving us a hazard ratio of 0.50."

---

## 4. Humanizing Numbers

Statistics describe populations. Clinicians treat individuals. The gap between these two realities is where medical presentations most often lose their audience.

### The Identifiable Victim Effect — Paul Slovic

Research by Slovic and colleagues demonstrates that people respond more powerfully to the story of one identifiable person than to statistics describing thousands. A mortality rate of 12% is abstract. A description of one patient who died from a preventable complication is concrete and motivating.

**Application:** Open your data section with one patient who represents the problem your data addresses. "Maria, 58 years old, managed her type 2 diabetes carefully for 11 years — then presented with her first MI. She is in our dataset 847 times." This grounds the cohort in a person before you show the population-level curves.

**Constraint:** Use a composite or de-identified patient. The technique is about creating identification, not about exploiting an individual's case.

### NNT Framing vs. Relative Risk Reduction

Relative risk reduction inflates the perceived magnitude of an effect. Absolute risk reduction and Number Needed to Treat give a clinically accurate picture.

**Example — statins in primary prevention:**
- Relative risk reduction: "Statins reduce MI risk by 25%." — Sounds large.
- Absolute risk reduction: "Statins reduce MI risk from 2% to 1.5% over 5 years." — Smaller.
- NNT: "You need to treat 200 patients for 5 years to prevent one MI." — Clinical reality.

**Rule for presentations:** Show all three. State the relative risk reduction because it is what the literature reports and your audience expects. Then immediately follow with the absolute risk reduction and NNT. Say: "That 25% relative reduction translates to treating 200 patients for five years to prevent one event — which, in a high-risk population, is a favorable trade-off given the drug's safety profile."

Presenting only relative risk reduction to an audience that will use this number to prescribe or fund treatment is a form of miscommunication, even if unintentional.

### Icon Arrays (Pictographs) Instead of Percentages

Replace "12% of patients experienced the outcome" with a grid of 100 person icons, 12 of which are highlighted. Icon arrays communicate risk magnitude to audiences with low numeracy and high numeracy alike. They are particularly effective when comparing treatment to control.

**Medical example:** Comparing adverse event rates — 8% in the treatment arm vs. 3% in the placebo arm. Show two grids of 100 icons side by side. The visual difference between 8 highlighted icons and 3 highlighted icons is immediate and requires no percentage interpretation. Label each grid: "Treatment (8 of 100 patients)" and "Placebo (3 of 100 patients)."

Tools: R `waffle` package, Python `pywaffle`, or manual icon arrays in PowerPoint using a standard icon grid template.

### Hans Rosling Technique

Rosling's presentations demonstrated that animation, live narration, and deliberately challenged assumptions could make population-level statistics emotionally compelling. The core technique:

1. Start the audience with their existing belief ("Most people assume child mortality has gotten worse over 30 years.")
2. Show the animated data that contradicts the assumption (mortality falling in every region simultaneously).
3. Narrate the movement live — describe what is happening as it unfolds on screen.
4. Name the mechanism that drove the change.

**Medical application:** Animating MRSA bloodstream infection rates across ICUs in a quality improvement initiative. Start with the assumption ("We expected some units to improve and others to worsen"). Animate monthly rates across 12 units simultaneously. Narrate: "Watch Unit 7 — that dramatic drop in month 9 coincides with the introduction of the chlorhexidine bathing protocol. Now watch it spread to Unit 3 in month 11 after the cross-departmental training." The live narration of animated data is more memorable than a static line chart with the same information.

---

## 5. Removing Chart Junk — Tufte

Edward Tufte defined chart junk as visual elements that do not convey data — elements that consume ink without adding information. In medical presentations, chart junk is pervasive because most charts are exported directly from statistical software or Excel with default settings.

### Remove These Elements

- **Gridlines:** Unless the audience needs to read off specific values (they rarely do in a presentation), gridlines create visual noise. Remove them entirely or use minimal, light gray lines only for dense data grids.
- **Borders and boxes around charts:** The slide is already the frame. A box around the chart area is redundant.
- **Legends:** Replace every legend with direct labels. Legends require the audience to look away from the data, decode, and return. Direct labels eliminate this.
- **Background fills:** Gray chart backgrounds, gradient fills, and textured regions behind data reduce contrast and serve no informational purpose.
- **Redundant axis labels:** If the chart title says "Survival probability (%)" the y-axis label does not need to repeat it.
- **Three-dimensional effects:** 3D bars, 3D pies, and extruded charts distort proportions. They make accurate comparison impossible and should never appear in a scientific presentation.

### Keep These Elements

- Data points, bars, lines, and markers — the actual data
- Axis labels (simplified — units only, not repeated descriptions)
- Direct labels on each data series
- Annotations that point to the specific finding you are discussing
- A single, clear assertion title

### Before/After Example — Cleaning Up a Medical Chart

**Before (default Excel output of adverse event table):**
- Gray background fill on chart area
- Gridlines every 5 units on y-axis
- Legend in the upper right corner ("Serious AE", "Non-Serious AE", "Discontinued")
- 3D cylindrical bars
- Border box around entire chart
- Chart title: "Figure 2. Adverse Events by Treatment Group"
- x-axis: Treatment A, Treatment B, Treatment C, Placebo
- y-axis: labeled "Percentage of Patients (%)" (redundant)

**After (Tufte-cleaned version):**
- White background
- No gridlines (or single faint horizontal line at the 10% reference only if a threshold matters clinically)
- No legend — each bar group labeled directly above the bars
- Flat 2D bars
- No border
- Assertion title: "Serious adverse events were rare and balanced across all arms (<5%)"
- Direct percentage labels on each bar
- y-axis label simplified to "%" only

The after version communicates faster, is more legible at a distance, and does not require the audience to decode a legend during a live presentation.

---

## 6. Small Multiples

Small multiples repeat the same chart structure across different subgroups, conditions, or time periods. They allow the audience to compare across panels by holding the visual structure constant — the only thing that changes is the data.

### Why Small Multiples Beat Overlaid Series

When multiple data series are overlaid on a single chart, the audience must track multiple colors or line styles simultaneously. Cognitive load increases with each additional series. At four or more series, most audiences stop reading the chart and wait for you to explain it verbally — which defeats the purpose of showing the chart.

Small multiples give each subgroup its own panel. The audience can read any single panel independently, then scan across panels to compare. Pattern detection becomes effortless.

### Requirements for Effective Small Multiples

- All panels use the same x-axis range and y-axis scale
- All panels use the same chart type and visual encoding
- Each panel carries its own label (the subgroup name), visible without decoding a legend
- Panels are arranged in a meaningful order (by effect size, by sample size, by clinical relevance)

### Medical Example — Subgroup Analyses as Small Multiples

A clinical trial reports a primary endpoint result and then presents subgroup analyses for: age <65 vs. ≥65, sex, smoking status, and baseline LVEF category.

**Standard approach (problematic):** A single forest plot with 12 rows and a shared diamond at the bottom. The audience must read each row's label, find the hazard ratio, locate the confidence interval, and check whether it crosses the null line — for 12 subgroups in sequence. This takes more than 30 seconds and most audiences do not complete the task during the talk.

**Small multiples approach:** Four panels, one per pre-specified subgroup variable. Each panel is a mini forest plot showing only the subgroups within that variable (e.g., the age panel shows two rows: <65 and ≥65). The panel title is the variable name. Panels are arranged in a 2×2 grid. The overall treatment effect is shown as a reference line in each panel.

This layout allows the audience to immediately see whether any subgroup's confidence interval diverges substantially from the others — the primary question in any subgroup analysis — without sequential row-by-row reading.

**Additional medical examples for small multiples:**
- ICU performance metrics (mortality, LOS, readmission) repeated across 8 units in a quality improvement report
- Dose-response curves repeated across 4 patient strata (by renal function quartile)
- Pathogen resistance rates shown as a bar chart, repeated across 6 hospital sites in a stewardship report

---

## Quick Reference Checklist

Before finalizing any data slide, verify:

- [ ] I have written the Big Idea sentence (unique point of view + what is at stake)
- [ ] The chart type matches the question (comparison, trend, composition, correlation, distribution, survival)
- [ ] The chart title is an assertion, not a description
- [ ] Every series or bar is labeled directly — no legend
- [ ] I have annotated the single most important feature of the chart
- [ ] Chart junk has been removed (no gridlines, no 3D, no background fills, no border)
- [ ] If showing risk, absolute risk and NNT accompany the relative risk reduction
- [ ] If showing survival data, the KM curve has an at-risk table and a direct annotation at curve separation
- [ ] If comparing more than 3 subgroups, I have considered small multiples instead of overlaid series
- [ ] I will not say "as you can see" — the annotation says it for me
