# earnings-analysis

> **Responsible AI:** Analyst-controlled research; verify evidence, disclose AI assistance and protect confidential information. [Policy and project-specific checks](RESPONSIBLE_AI.md).
quick earnings analysis with consensus Wall Street forecast, with past guidance, with peer industry trend.
An Agent Skill for institutional-quality earnings analysis from 10-Q/10-K filings, earnings releases, and call transcripts. Built for buyside-style post-print review that goes beyond beat/miss reporting to diagnose why results deviated, what changed in the forward thesis, and what action follows.
What it does
This skill encodes a structured editorial process distilled from buyside equity research practice. When loaded into an AI tool, it processes raw earnings materials through a four-layer framework:

Parse. Extracts structured financial KPIs, segment data, guidance, non-GAAP reconciliations, balance sheet and cash flow items, and sector-specific metrics from filings, releases, and transcripts.
Compare. Benchmarks results sequentially (QoQ), year-over-year (YoY), against consensus estimates, and against sector peers — flagging surprises and trend breaks.
Diagnose. Attributes deviations to underlying drivers (volume vs price, mix, FX, one-offs, structural shifts), assesses earnings quality, scores management tone from call transcripts, and detects negative triggers.
Translate to action. Converts the analysis into a forward investment view: what's mispriced, what's de-risked, what to watch, and what to do.

The skill ships with a scoring engine, a flag library for earnings quality red flags, sector-specific KPI extensions, and a process discipline checklist to keep analysis honest under time pressure.
What it produces
The skill outputs four deliverables, scaled to the user's request:

One-page earnings sheet. Headline numbers, beat/miss table, segment snapshot, guidance delta, and the 4-layer summary — designed to fit a single screen for morning meetings.
Full earnings memo (Word document). Institutional-format memo covering parse, compare, diagnose, and action layers in detail, with management tone analysis, earnings quality scoring, and a forward catalyst map.
Risk map. Structured inventory of negative triggers, accounting flags, and forward risks with severity tags.
Trade note. Concise actionable summary with directional view, conviction level, key triggers to watch, and position-sizing considerations.

Each output appends a "Fund Manager Questions" section — the questions a PM would ask after reading the work — to surface gaps and force the analyst to defend conclusions.
Installation
Claude.ai

Download this repository as a ZIP file (on the repository's main page, click the green Code button, then Download ZIP).
The downloaded ZIP wraps everything in a earnings-analysis-main/ folder. Open it and re-zip the inner earnings-analysis/ folder so the ZIP contains earnings-analysis/SKILL.md at the root.
Open claude.ai. In the left sidebar, click Customize (the toolbox icon), then go to Skills.
Click the + button, then + Create skill, and upload the ZIP file.
The skill will appear in your Skills list. Make sure its toggle is turned on.

Claude Code
Copy the earnings-analysis/ folder into your project's .claude/skills/ directory (project-scoped) or ~/.claude/skills/ (user-scoped). Claude Code will discover the skill automatically on next launch.
Other agents (ChatGPT, Gemini, etc.)
The SKILL.md follows the open Agent Skills specification and works with any compliant runtime. For tools without native SKILL.md support, paste the body of SKILL.md (everything after the YAML frontmatter) into the system instructions of a custom GPT, Gem, or equivalent. The output structure and reasoning will follow the same framework.
Usage
Once installed, the skill activates automatically when you ask Claude about quarterly earnings. Example prompts:

"Analyze [Company]'s Q3 earnings — I've uploaded the 10-Q and the call transcript."
"What did NVIDIA report this quarter? Give me the full memo."
"How were Microsoft's Q2 results vs consensus? Focus on guidance and segment trends."
"Run a post-print analysis on TSMC's latest quarter and flag any earnings quality concerns."
"One-pager on Costco's Q4 — I just need the trade note."

You can either upload primary materials (filings, releases, transcripts as PDFs) or let the skill pull the latest data via web search. Uploaded files take priority and produce deeper analysis.
When not to use this skill
The skill is purpose-built for post-earnings quarterly review. It's deliberately not the right tool for:

Long-term DCF valuation or intrinsic value modeling
Multi-year growth thesis construction or initiation reports
Technical analysis or chart-based trade setups
Commodity or metals fundamental analysis

Use dedicated skills for those workflows.
Methodology notes
The 4-layer framework draws on standard buyside post-print review practice across long-only and hedge fund equity research desks. Sector-specific KPI extensions cover the metrics that matter most for technology, financials, consumer, healthcare, energy, and industrials. The earnings quality scoring engine and negative trigger library are informed by forensic accounting literature on revenue recognition, working capital manipulation, and non-GAAP gaming.
License
Released under [LICENSE — TBD, e.g. MIT or CC-BY-4.0]. If you use or adapt this skill, attribution is appreciated but not required.
Contributing
Issues and pull requests welcome. Particularly interested in:

Additional sector-specific KPI extensions
New entries for the negative trigger / earnings quality flag library
Refinements to the scoring engine calibration
Output format improvements


Built by Ed. Version 1.5.0.
