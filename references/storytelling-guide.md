# Storytelling Guide for Medical and Academic Presentations

This document is the primary reference for constructing compelling narratives in academic and medical talks. Every instruction here is actionable. Every pattern includes a concrete example from the medical/academic domain. Read this in full before building any presentation structure.

---

## 1. Macro Narrative Structure

### ABT — And, But, Therefore (Randy Olson)

ABT is the single most reliable template for scientific storytelling. It forces you to establish context, introduce tension, and show how your work resolves it. Audiences are wired for this three-part arc.

**Template:**
> [WORLD/CONTEXT], AND [ADDITIONAL CONTEXT], BUT [PROBLEM/TENSION], THEREFORE [YOUR WORK/RESOLUTION].

**Full medical example:**
> "Antibiotic resistance is one of the greatest threats to global health, AND we have relied on the same drug classes for decades, BUT novel discovery pipelines have dried up entirely — no new antibiotic class has reached the clinic in 35 years, THEREFORE we turned to AI-driven molecular screening to identify structurally novel compounds in microbial dark matter."

**Why ABT works:** The "But" is the engine. It creates the need for your talk to exist. Without tension, there is no reason to listen.

**Contrast — what to avoid:**

- **AAA (And, And, And):** "We studied diabetes, and we looked at insulin resistance, and we also examined beta-cell function, and we used a cohort of 2,000 patients, and we found some interesting results." This is a list. No tension. No reason to care.
- **DHY (Despite, However, Yet):** "Despite significant advances, however, challenges remain, yet there is some hope." This is the academic abstract voice — it signals uncertainty without committing to a clear problem. Audiences disengage.

**ABT works at multiple scales:**

- **Whole talk:** The ABT above frames why the entire project exists.
- **Each section:** "We had a drug candidate that looked promising in silico, AND it passed initial toxicity screens, BUT it completely failed in our first animal model, THEREFORE we redesigned the delivery mechanism."
- **Individual slides:** A single slide about a forest plot can follow ABT: "All previous meta-analyses showed benefit, AND sample sizes were large, BUT heterogeneity was extreme, THEREFORE we restricted to RCTs with active comparators." One slide, one ABT arc.

### SCR — Situation, Complication, Resolution (Barbara Minto)

SCR is the consulting world's version of ABT. It works especially well when your audience expects structured analytical thinking — grand rounds presentations, grant committee pitches, clinical trial readouts.

- **Situation** = what is already known and accepted. This is NOT your contribution. "Sepsis kills 270,000 Americans annually and is the leading cause of hospital mortality."
- **Complication** = the gap, contradiction, or failure in current knowledge. "Current early-warning tools have a 60% false-positive rate, causing alert fatigue and delayed response to genuine crises."
- **Resolution** = what your work does about it. "We developed and validated a real-time sepsis prediction model using routinely collected EHR data, achieving 91% sensitivity with a false-positive rate under 10% — trialed across three ICUs."

**Key distinction from ABT:** SCR keeps the resolution explicitly tied to your data. Use SCR when you need to signal analytical rigor. Use ABT when you want emotional propulsion.

---

## 2. Emotional Rhythm

### Sparkline — What Is / What Could Be (Nancy Duarte)

Duarte's analysis of transformative speeches reveals a consistent oscillating pattern: the speaker moves repeatedly between the current painful reality ("what is") and a compelling envisioned future ("what could be"). This oscillation creates emotional energy. Without it, talks flatline.

**Template for each oscillation:**
> "Today, [painful/limited current reality — what is]. Imagine if [desired future state — what could be]..."

**Rule:** Oscillate at least 3–4 times across the talk. End with "new bliss" — the world after your solution is adopted.

**Medical example — three oscillations in a talk on pediatric epilepsy surgery:**

1. *"Today, 30% of children with epilepsy have seizures that cannot be controlled with medication. [What is.] Imagine if we could identify, in advance, which children would be medication-resistant — so surgeons could intervene before years of developmental damage accumulate. [What could be.]*"

2. *"Right now, surgical candidacy evaluation requires a 10-day inpatient stay costing $80,000, which disqualifies most patients globally. [What is.] What if a two-hour outpatient protocol using high-density EEG and ML could replicate those findings at 5% of the cost? [What could be.]*"

3. *"Currently, outcomes after resection vary enormously — 40% of patients still have seizures post-operatively. [What is.] Now picture a future where connectome mapping tells us, before the first incision, exactly where to resect for seizure freedom. [What could be.]*"

**New bliss close:** "Five years from now, a child in Lagos gets a 90-minute outpatient evaluation, the algorithm identifies the resection target, and she leaves the hospital seizure-free. That is not science fiction. That is what this work makes possible."

### STAR Moment — Something They'll Always Remember (Nancy Duarte)

Place one STAR moment at approximately two-thirds through the talk. This is the peak emotional beat — the moment audience members will describe when someone asks "what was that talk about?"

**Types of STAR moments (with medical examples):**

- **Shocking statistic, made visceral:** Not just "1 in 8 women will develop breast cancer." Instead: "In the time it takes me to give this 20-minute talk, 13 women in the United States will receive a breast cancer diagnosis. By the time you drive home tonight, 40 more."
- **Live demonstration:** Running the diagnostic model live on a real ECG from a patient whose outcome the audience doesn't yet know. Then revealing it.
- **Powerful image:** A single before/after MRI — a child's brain at age 3, before treatment, and at age 7 after gene therapy. No words needed for 10 seconds.
- **Personal revelation / vulnerability:** "I have to tell you something about this dataset. The seventh patient in our pilot — patient ID 0007 — that was my father."
- **Audio or video:** A 90-second clip of a Parkinson's patient unable to walk, then 30 seconds post-DBS, walking unassisted.
- **Patient on stage:** Brief, ethically cleared appearance by a patient who embodies the outcome you're describing.

**Reference:** Bill Gates at TED 2009 released mosquitoes into the audience to make malaria visceral. You don't need mosquitoes — you need one moment that makes the abstract concrete and the statistic human.

---

## 3. Structural Constraints

These are not suggestions. They are constraints that prevent structural failure.

### Rule of Three — Maximum 3 Key Messages Per Talk

Audiences reliably retain three things. Giving them seven guarantees they remember zero. Before building any slide deck, write three sentences:
1. The single most important thing I want this audience to believe after my talk.
2. The second most important thing.
3. The third.

Everything else in the talk exists to support these three messages — not to add new ones.

### One Slide, One Message

Every slide communicates exactly one idea. If you can't state the message of a slide in one sentence, split the slide. Title lines should state the conclusion, not the topic. "Mortality Outcomes" is a topic. "Treatment A Reduced 30-Day Mortality by 22% (p=0.003)" is a message.

### Bookend Heavy — Primacy and Recency

Audiences remember best what they hear first and last. Structure accordingly:
- **First 20%** of the talk: establish stakes, deliver the most compelling problem framing, introduce the story that will carry the whole talk.
- **Last 20%**: deliver the most important clinical/scientific implication, the call to action, and the emotional close.
- The middle 60% is for evidence — necessary, but not where you win or lose the audience.

### Attention Reset — Every 10 Minutes (John Medina, Brain Rules)

The brain's attention cycle resets approximately every 10 minutes. Plan a deliberate reset at each interval using one of:
- A brief story or anecdote
- A direct question to the audience ("How many of you have seen this pattern in your own patients?")
- A modality shift (from slides to live demo, from speaking to a short video clip, from lecture to a show-of-hands poll)

In a 45-minute talk, you need at least 3 planned resets at the 10-, 20-, and 30-minute marks.

---

## 4. Opening Techniques

The first 60 seconds determine whether the audience lends you attention or starts checking email. Never squander this window on logistics.

**Never open with:**
- "Thank you for having me / for the kind introduction"
- An agenda slide (you are telegraphing the story before telling it)
- Reading the title slide aloud

---

### Cold Open / In Medias Res

Drop the audience into the middle of a scene, no context given. Create immediate sensory or emotional immersion.

> "3:47 AM. The ICU pager goes off. A 12-year-old is coding. The team runs the standard sepsis protocol. All the boxes are checked. She dies at 6:12 AM. The autopsy reveals a rare metabolic disorder — one that a genomic panel, ordered two days earlier, could have identified. The results arrived in her chart at 9:15 AM."

Then step back: "That case is why my team spent five years building a faster diagnostic pathway. Let me show you what we found."

### Provocative Question

Ask a question that subverts a comfortable assumption the audience holds.

> "What if the most dangerous moment in a hospital isn't the surgery? What if it's the 72 hours after?"

Pause. Let the question land. Then build the case. Do not answer it immediately — let tension accumulate.

### Startling Statistic, Made Visceral

Raw numbers rarely land. Scale them to something human.

> "Every 36 seconds, someone in the United States dies from cardiovascular disease. In the time between when I was introduced and when I finish this sentence — one person just died."

### Personal Story

A brief, authentic connection to the topic. This is not biography — it is a bridge to stakes.

> "I became interested in this problem the year my lab produced what we thought was a promising compound. We celebrated. Fourteen months later, it failed Phase II. I sat with the principal investigator for an hour without either of us speaking. That failure is what sent me back to first principles — and led directly to the method I'm showing you today."

### Contrarian Statement

Directly challenge a consensus belief to jolt the audience into active listening.

> "Everything you learned about cholesterol in medical school was probably wrong. Or at least — significantly incomplete. And if you're still prescribing based on LDL alone, you may be doing some patients harm."

Immediately follow with: "I know that's a strong claim. Here's the evidence."

---

## 5. Closing Techniques

The close is where the talk lives in memory. Never drift into it — engineer it deliberately.

**Never close with:**
- "Any questions?" as the last slide
- An acknowledgments slide read aloud (show it, say one sentence, move on)
- "That's all I have" or "That's everything"
- A summary slide as the final emotional beat (data recap is not inspiration)

---

### Callback Close

Return to the opening story and resolve the tension you created.

> "Remember Emma — the 12-year-old I described at the start, the one whose genomic results arrived too late? Last month, we ran a retrospective analysis. If our pipeline had been deployed at that hospital in 2019, her result would have been available in under 4 hours from sample collection. I can't change what happened to Emma. But the next Emma — she's why this matters."

### Challenge / Call to Action

Give a specific, achievable next step that lands on Monday morning.

> "On Monday morning, change one thing: before you discharge your next patient with heart failure, check if they've been screened for sleep-disordered breathing. One order. That's the ask."

### Vision of the Future

Paint the world after your solution is adopted — specific, not generic.

> "Ten years from now, no child in a high-income country will be diagnosed with Type 1 diabetes without a genetic risk score calculated at birth. The question is whether we choose to build that infrastructure now, while the evidence base is still forming, or wait until the cost of inaction is unmistakable."

### Patient Quote

End with a human voice — not yours.

> "I'll end with what one participant told me at her six-month follow-up. She said: 'For the first time in 30 years, I woke up without pain. I didn't know that was still possible for me.' That is what this data means outside this room."

---

## 6. Connectors and Bridges Between Slides

Slide transitions are the seams of narrative. Audiences feel every clumsy one. The words "next we'll discuss" or "moving on to" are narrative resets — they break immersion and remind the audience they are watching a presentation rather than following a story.

**Never use:**
- "Next we'll discuss..."
- "Moving on to..."
- "Let me now talk about..."
- "As you can see on this slide..."

---

### Narrative Bridge

Carry the story forward by showing how one finding creates the next question.

> "So we know the biomarker is accurate. Sensitivity of 94%, specificity of 88% — in a controlled research setting. But accuracy in a clean lab sample is one thing. What happens when you run this in a busy emergency department at 2 AM, with samples that sat in a tube for 6 hours? That's exactly what we tested next."

### Callback Connector

Re-activate a character or case introduced earlier to create structural resonance.

> "Remember Maria from the beginning — the patient who'd been on three immunosuppressants for 18 months with no improvement? She's about to become very relevant again. Because the mechanism I'm about to show you is exactly what was happening in her T-cell compartment."

### Rhetorical Question Bridge

Use a question the audience is already asking to pivot naturally.

> "We had a test that worked in the lab. Reproducible, cost-effective, fast. But here's the question I kept getting from every clinician I showed this to: 'Would it work in real patients, with real comorbidities, on real timelines?' That question shaped everything that came next."

### Contrast Bridge

Use opposition to create forward momentum.

> "The compound worked beautifully in mice. Tumor volume reduced by 70% at day 14. Survival curves looked extraordinary. But as every researcher in this room knows — mice lie. So we moved to an orthotopic human tumor xenograft model. And the results were very different."

### Signpost

Explicitly orient the audience at structural transitions without using filler language.

> "That was the 'what' — what the intervention is and what the trial looked like. Now comes the 'so what.' And this is the part that surprised even us."

### Physical and Vocal Transitions

Complement verbal bridges with physical ones. At major structural transitions:
- Pause 2–3 full seconds before advancing the slide
- Change position (step to the other side of the stage or toward the audience)
- Shift vocal energy — drop volume to draw in, or increase pace to build momentum

These physical signals tell the audience: something new is beginning. Pay attention.

---

## 7. Advanced Narrative Patterns

### Patient Story Bookend

One of the most reliable structures for medical talks:

1. **Open with a patient case — leave it unresolved.** Introduce a real (de-identified) or composite patient with a specific problem. Give them a name. Leave their outcome unknown.
2. **Present your data** in the middle of the talk as usual.
3. **Return to the patient at the close** and reveal the outcome — now meaningful because the audience has just absorbed the mechanism.

This works because narrative curiosity about an individual human outperforms abstract curiosity about population-level data.

### Nested Loops

Open 2–3 separate narrative threads at the beginning of the talk. Close them in reverse order at the end. Each closure provides a satisfying click of resolution.

Example threads in a genomics talk:
- Loop 1 (outermost): "A family with four affected siblings, no diagnosis after 15 years."
- Loop 2 (middle): "A technical challenge — our variant calling pipeline kept flagging false positives in repeat regions."
- Loop 3 (innermost): "A single variant of uncertain significance that kept appearing across all four siblings."

Close: Resolve Loop 3 (the variant was pathogenic), then Loop 2 (how solving the technical problem enabled the finding), then Loop 1 (the family received a diagnosis; treatment began; two siblings are now in remission).

### The Vulnerability Move

Researchers are trained to present confidence. A single moment of disclosed uncertainty — handled well — dramatically increases trust and credibility.

> "I have to be honest with you. When we got the first results from the Phase II interim analysis, I thought we'd made an error. The effect size was larger than anything in the literature. I asked the statistician to re-run it three times. I still didn't believe it until we saw the same pattern in the validation cohort."

Use once per talk. Never apologize for your work — disclose one moment of genuine surprise or doubt, then show how you resolved it rigorously.

### Analogy and Metaphor Bridge

Abstract mechanisms become navigable when anchored to a familiar system.

> "Think of CRISPR like find-and-replace in a word processor. Your genome is a 3-billion-letter document. CRISPR lets you search for a specific 20-letter sequence, find it — every instance of it — and replace it with a different sequence. The difference is: in the genome, a typo can be lethal. So the precision of the search matters enormously."

Good analogies have limits — state them explicitly: "Like all analogies, this one breaks down at a certain point. CRISPR doesn't just edit; it can also activate or silence genes without cutting. But for understanding the core mechanism, the word processor model holds."

### SUCCESs Test (Chip and Dan Heath, Made to Stick)

Before finalizing each slide, run it through the SUCCESs checklist:

- **S — Simple:** Is the single core message of this slide immediately clear?
- **U — Unexpected:** Does this slide contain one element the audience doesn't already know or expect?
- **C — Concrete:** Is the claim made in specific, sensory, tangible terms — not abstract ones?
- **C — Credible:** Is there a source, data point, or authority that makes this believable?
- **E — Emotional:** Does this slide connect to something the audience cares about personally?
- **S — Story:** Is there a human element — a patient, a researcher, a decision — embedded here?

A slide that fails three or more of these criteria should be redesigned or cut.

### The "Make Me Care" Principle (Andrew Stanton, Pixar)

Stanton's core principle: you do not earn attention — you earn the right to the audience's attention by establishing what is at stake for them, or for someone they can identify with, within the first 60 seconds.

Stakes for a medical audience can be:
- A patient who will die without the advance you're describing
- A clinical practice that is currently causing harm
- A diagnostic gap that is affecting their patients right now
- A professional identity challenge — "what you believe to be true may not be"

If by 60 seconds the audience cannot answer "why does this matter to me, my patients, or my field?" — the opening has failed. Rebuild it.

---

## Quick-Reference Checklist Before Finalizing Any Talk

- [ ] Can you state the talk's ABT in two sentences?
- [ ] Are there exactly three key messages — no more?
- [ ] Does each slide carry one and only one message?
- [ ] Does the opening use one of the six approved opening techniques?
- [ ] Is there a STAR moment placed at approximately the 2/3 mark?
- [ ] Does the emotional rhythm oscillate at least 3 times (sparkline)?
- [ ] Is there a planned attention reset every 10 minutes?
- [ ] Does the close use one of the four approved closing techniques?
- [ ] Are all slide transitions genuine narrative bridges (not "next we'll discuss")?
- [ ] Have the three most important slides been tested against the SUCCESs framework?
- [ ] Are the first 20% and last 20% structurally the strongest sections?
