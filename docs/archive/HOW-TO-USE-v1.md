# How to Use the Earnings Analysis Skill with Claude Code

## What This Is

The files in this repository encode a systematic four-layer process for reviewing public-company earnings — parse the inputs, compare them against multiple reference frames, run a deterministic scoring engine, and translate the result into an investment-grade memo. When placed in the right location, Claude Code will automatically discover the skill and apply it whenever you ask for an earnings review.

Think of it as teaching Claude Code the analytical standards of a senior buyside analyst — once, in a folder of files — so that every quarterly review it produces follows the same rigorous protocol and feeds into the same scoring engine.

## Requirements

- **Python 3.8+** is required to run `scripts/score_earnings.py`. The scorer uses only the Python standard library — no external packages need to be installed.
- **Claude Code** installed and authenticated. See [Anthropic's installation docs](https://docs.claude.com/en/docs/claude-code/quickstart) for setup.
- For the full memo deliverable, the `docx` skill (bundled with Claude) handles Word document generation. No additional installation needed inside Claude Code.

## Setup: Where to Put the Files

### Option A — Project-level skill (recommended)

Place the skill inside the `.claude/skills/` directory of your research project:

```
my-research/
├── .claude/
│   └── skills/
│       └── earnings-analysis/
│           ├── SKILL.md             ← top-level instructions
│           ├── scripts/
│           │   └── score_earnings.py
│           └── references/
│               ├── scoring-engine.md
│               └── parsing-checklist.md
├── tickers/
│   ├── NVDA/
│   └── MSFT/
└── notes/
```

Commands to set this up from this repository:

```
cd /path/to/my-research
mkdir -p .claude/skills/earnings-analysis
cp -r /path/to/this-repo/SKILL.md /path/to/this-repo/scripts /path/to/this-repo/references .claude/skills/earnings-analysis/
```

This makes the skill available whenever you run Claude Code from within this project directory.

### Option B — Global skill (available across all projects)

Place it under your home directory's `.claude/skills/`:

```
mkdir -p ~/.claude/skills/earnings-analysis
cp -r /path/to/this-repo/SKILL.md /path/to/this-repo/scripts /path/to/this-repo/references ~/.claude/skills/earnings-analysis/
```

This makes the skill available in every project you open with Claude Code.

## Using the Skill

### Step 1: Open your research project

Open your terminal in your research directory. If you keep earnings materials in subfolders by ticker, navigate to the parent directory so Claude Code has access to all of them.

### Step 2: Launch Claude Code

```
claude
```

Claude Code starts an interactive session. It will automatically detect the skill in `.claude/skills/`.

### Step 3: Ask for an analysis

Here are example prompts, ordered from broadest to most targeted.

**Full quarterly review (auto-detected deliverable):**

```
Analyze Microsoft's latest quarter. The press release and 10-Q are in
tickers/MSFT/Q4-FY25/.
```

```
Walk me through Nvidia's Q3 FY26 print. Pull the call transcript from
tickers/NVDA/ and run the full framework.
```

In both cases, Claude Code will read the materials, parse them through the four-layer workflow, run the scoring engine, and choose the deliverable format based on the verdict tier — a one-page sheet for clean strong quarters, a full memo (with risk map) for everything else.

**Specifying the output format:**

```
Give me a trade note on Snowflake's Q4. Three paragraphs, position-ready.
```

```
Build a full earnings memo for ServiceNow's quarter — I want all six pages
with the appendix.
```

```
Just give me the risk map for Boeing's print. I'm tracking the operational
flags, not the headline numbers.
```

**Targeted analysis (one layer only):**

```
Run only the scoring engine on these inputs for Tesla's Q4:
revenue beat 1.2%, EPS beat 0.5%, guidance maintained, gross margin
down 80bps QoQ, OCF/NI 0.85, management tone cautious, stock down 8%
on the print, stock up 95% over the past year.
```

```
Diagnose only the cash quality and balance sheet for Intel's latest
quarter. Skip the management signals and the deliverable.
```

**Multi-quarter comparison:**

```
Compare AMD's Q3 FY25 and Q4 FY25 prints side by side. Which scorer
flags shifted between the two quarters?
```

**Scenario stress-testing the scorer:**

```
Run the scorer for Novo Nordisk Q4 2025 with these inputs: [paste]. Then
re-run with stock_reaction=positive to see how the regime classification
changes.
```

### Step 4: Review the output

For full reviews, Claude Code will produce one of the following deliverables:

- **One-page earnings sheet** — STRONG_QUARTER cases. A condensed Word document with verdict, key metrics, what changed, drivers, scenario table, and action.
- **Full earnings memo** — SOLID, MIXED, WEAK, PROBLEMATIC cases, plus any STRONG case with peak-cycle or expectations-overrun modifiers. A 4–6 page Word document covering parsed financials, comparison matrix, full diagnosis, decision framework, and an appendix with paraphrased management quotes.
- **Risk map** — Produced alongside the memo whenever the scorer's `output_recommendation` includes it. A structured table of risk categories, specific risks, probability/impact/trend assessments, and monitoring metrics.
- **Trade note** — Produced on request. 3–5 paragraphs for a portfolio manager or trading desk.

Each deliverable includes the scorer's mechanical verdict at the top so the reader sees both the composite score and the analyst's written interpretation.

### Step 5: Iterate

Earnings analysis benefits from a back-and-forth. Common follow-ups:

```
Push back on the scorer's expectations regime classification. Why did
it call this 'overrun' rather than 'constructive'?
```

```
Re-run the diagnosis treating the inventory build as growth-capex-mode
rather than a demand risk. The capex-to-revenue ratio is 28%.
```

```
Override the verdict to MIXED. The scorer is missing the regulatory
overhang from the EU antitrust review. Update the memo accordingly.
```

The skill is designed to be challenged. The scorer is the mechanical anchor; the diagnosis is where judgment lives.

## Tips for Best Results

**State your position upfront.** "Long at $X, sized at Y% of the book" or "Currently flat, evaluating for entry" changes the recommendation framework. The decide step is position-specific.

**Bring consensus numbers if you have them.** The scorer's expectations regime classifier depends on knowing whether the print beat or missed expectations. If you have Visible Alpha, Bloomberg, or even Seeking Alpha numbers, paste them. Otherwise the skill will search for them, but coverage varies.

**Provide stock context.** The expectations elevation classifier uses three inputs: trailing 12-month return, recovery from 52-week low, drawdown from all-time high. For high-conviction names where elevation matters (Nvidia, Eli Lilly, Costco), having these numbers handy makes the regime classification much sharper.

**Use the scorer as a hypothesis generator, not an oracle.** When the scorer disagrees with your prior, that's a signal worth investigating — but it doesn't mean the scorer is right. Read the flags, identify what the scorer is reacting to, and decide whether the mechanical reading captures the underlying business reality.

**Combine with your own coverage notes.** If your project already has a `CLAUDE.md` describing the names you cover, your sector preferences, or your firm's investment philosophy, the skill complements it — your `CLAUDE.md` provides the portfolio context, the skill provides the analytical workflow.

## What This Skill Does NOT Do

- It does **not** value the company. For DCF, SOTP, or comparable-company valuation work, use a dedicated valuation skill.
- It does **not** generate price targets. The scenario table describes directional repricing paths, not specific price levels.
- It does **not** model future quarters. The output is a backward-looking quality assessment of the just-reported quarter, with forward implications for the thesis.
- It does **not** check accounting in detail. It flags GAAP/non-GAAP gaps and cash quality issues but is not a forensic accounting tool.
- It does **not** provide investment advice. See the disclaimer in `README.md`.

If you need a forward-looking valuation model, a forensic accounting review, or a strategic competitive analysis, those are different tasks and likely call for different skills.
