# Plan: Course Factory Lite

A lighter rebuild of an earlier education pipeline. Same job, same gates, no chat platform,
runs entirely inside Claude Code (CLI) or Claude Desktop (Code tab). Every output is a
markdown file plus a PDF.

Status: v0.1 complete (phases 0 to 7). Open items are in docs/dry-run-1.md under "Not proven yet".

## 1. What we are building

You type one request, for example `/new-course Intro to SQL, level: high school`. A team of
agents researches the topic, designs a syllabus, writes decks, quizzes and labs, and a QA
agent checks the package. A human approves at three fixed gates. Nothing moves past a gate
without a named approval.

Deliverables per course: viability brief, source pack, syllabus, one deck per module (student
and instructor PDFs), one quiz, answer key and TA feedback pack per module, one lab per module, a QA report
and alignment matrix, the status and approval log, and after publish a TA grounding manifest
and TA digests. About 19 markdown files for a two-module course, each with a PDF.

## 2. What the reference does and what we keep or cut

Reference facts that drive the cut: 9 agent briefs totalling about 190 KB, a 1 MB status file
from the one real course, 650 commits to build it, three lanes and many extra evidence files.
It is heavy because it was built to run a chat fleet. We keep the discipline and drop the
machinery.

| Reference piece | Lite decision | Why |
| --- | --- | --- |
| Chat platform spaces, daemon, souls, DMs | Cut | Claude Code session replaces all of it |
| 9 agents | Keep 8, cut video-producer | No video in lite |
| Workshop vs course lane | One lane, 1 to 4 modules, 3 gates | Simpler to run and explain |
| Gate 0, Gate 1, Gate 2 | Keep | You asked for the gates |
| Exact `APPROVE ...` string rule | Replaced: plain "yes" approves the pending gate | You asked for easy approval |
| video-producer | Removed, no video anywhere | Out of scope for lite |
| ta-agent | Kept and wired in as the post-publish stage | You asked for it in the pipeline |
| Claim ledger, coverage matrix, misconception map, examples files, UI captures | Cut | Replaced by one source pack with `SP-` IDs |
| `SP-` claim IDs cited on slides | Keep, light | Traceability is the core discipline |
| Student and instructor wall | Keep | Hard rule, cheap to keep |
| Quiz with key and distractor reasons | Keep | |
| Assignments and rubrics | Cut from default | Optional later |
| TA feedback packs | Keep, one per module | The ta-agent needs them |
| Lab as branches of a project repo | Cut | Lab is one self-contained document per module |
| Lab verification transcripts and sandbox | Cut | Labs are written, unexecuted steps carry a disclosure |
| Demo script, narration, video package | Cut | |
| QA with 18 checks | Keep about 11, half of them as a script | See section 7 |
| STYLE.md 110 KB | Rewrite to about 100 lines | Agents read it every run |
| Renderer, 700 lines, 3 themes | Port and trim, 2 themes | Keep the proven markdown to PDF path |
| Agent briefs 17 to 27 KB each | 3 to 5 KB each | Cheaper, easier to maintain |

Topic-agnostic: the reference is tuned to teaching Claude Code. Lite works for any topic.

## 3. Runtime design (CLI and Desktop)

Both Claude Code surfaces read the same project files, so one repo serves both: `CLAUDE.md`,
`.claude/agents/`, `.claude/commands/`, `.claude/settings.json`. To be verified in the dry
run: that Desktop picks up the commands and agents identically.

Three platform facts shape the design:

1. Subagents cannot spawn subagents. So the main session is the producer. `CLAUDE.md` tells it
   how to run the state machine. A `course-producer` subagent exists only for bookkeeping
   (writing STATUS.md, counting the package) so the main context stays small.
2. Subagents cannot chat. The reference's "post in the course space and tag the producer"
   becomes a fixed final report from each agent: Done, Paths, Counts, Gaps, Needs a human.
3. State must survive session ends. `STATUS.md` is the memory. At session start, `CLAUDE.md`
   tells the main session to read any non-published `STATUS.md` and offer to continue.

Subagents get no Bash tool (same as the workshop lane). The main session renders PDFs after
each stage and runs the checker. Research-analyst gets web tools; Firecrawl is available as an
MCP server if wanted.

## 4. Pipeline and gates

```
proposed
  -> viability-review         research-analyst
  -> GATE 0  viability        human
  -> syllabus-draft           curriculum-architect
  -> GATE 1  syllabus         human
  -> in-production            deck-writer + assessment-designer + lab-engineer in parallel
  -> qa-review                qa-reviewer, after the script checker passes
  -> GATE 2  package          human
  -> published                tag {slug}-v1.0, TA grounding manifest built
  -> maintenance              ta-agent answers student questions, weekly digest
```

Rejection returns the course to the preceding draft state with the human's notes passed to the
owning agent verbatim. Digest findings that need a content fix open an improvement item, which
goes back through the same gates.

### Approval protocol: plain language

The human approves by replying to a gate request in ordinary words: "yes", "good to go",
"looks great", "ship it", "approved", any clearly positive reply.

- The producer treats a reply as approval only when a gate is pending in `STATUS.md` and the
  reply is clearly positive and unconditional. It then appends a line to `APPROVALS.md` with
  the date, gate, decision and the user's words quoted verbatim.
- Mixed replies ("yes but change X"), questions and anything ambiguous are not approvals. The
  producer treats feedback as a rejection with notes, and asks one short question when unsure.
- Negative replies ("no", "redo this", notes) are rejections. Notes go to the owning agent
  verbatim.
- Subagents never write `APPROVALS.md` and never advance a gate. Their briefs say so, and the
  main session alone writes that file.
- A `PreToolUse` hook enforces ordering by reading `APPROVALS.md`: no writes to `01-syllabus/`
  before the viability approval, none to `02-deck/`, `03-assessments/`, `04-labs/` before the
  syllabus approval, none to `qa/` before the package is complete, and no subagent edits to
  `APPROVALS.md`.
- Honest limit: with plain-language approval, the guarantee is that a human's positive reply
  exists in the conversation and is quoted in the log. Nothing mechanical can prove the main
  session read it correctly. Hooks are guardrails, not security.

### Gate request message

The producer posts this at each gate: course, state, what finished, PDF paths to read,
markdown paths they came from, what is blocked meanwhile, and one line: "Reply yes to approve,
or tell me what to change."

### Maintenance stage

After Gate 2 the producer tags the repo and has qa-reviewer write
`qa/ta-grounding-manifest.md`, the exact file list the ta-agent may read: syllabus, decks,
labs, student quizzes and TA feedback packs, never the instructor tree. Then:

- `/ask-ta <question>` runs the ta-agent as a student would use it.
- `/ta-digest` has the ta-agent write `maintenance/ta-digest-<date>.md` with question themes
  and suspected content defects, no student names. The producer opens improvement items from it.

## 5. Repository layout

```
CLAUDE.md                     orchestration: flow, gates, outputs, rules
README.md                     how to run it in CLI and Desktop
STYLE.md                      lite house style, about 100 lines
.claude/
  agents/                     8 subagent files, full brief in each
  commands/                   new-course, status, continue, render, qa, ask-ta, ta-digest
  settings.json               hooks and permissions
build/
  render.py  themes/  fonts/  markdown to PDF, ported from the reference
scripts/
  check_package.py            mechanical QA checks
  hooks/                      stage-order write guard
  readiness-check.ps1 / .sh   five PASS or FAIL lines
templates/                    one skeleton per artifact type
courses/{slug}/
  STATUS.md  APPROVALS.md
  00-viability/   viability-brief.md  source-pack.md
  01-syllabus/    syllabus.md
  02-deck/        deck-mNN.md
  03-assessments/ student/quiz-mNN.md   instructor/quiz-mNN-key.md
                  instructor/ta-feedback-pack-mNN.md
  04-labs/        lab-mNN.md
  qa/             qa-report.md  alignment-matrix.md  ta-grounding-manifest.md
  maintenance/    ta-digest-<date>.md
  dist/           PDFs mirroring the folders above
reference/                    a clone of the earlier pipeline, gitignored, not shipped
run.ps1 / run.sh              render wrappers
```

## 6. The agents

All are markdown files in `.claude/agents/` with frontmatter `name`, `description`, `tools`,
`model`. Each ends with the same final-report format. Each states its write folder and never
writes outside it.

| Agent | Model | Tools | Writes | Output |
| --- | --- | --- | --- | --- |
| course-producer | sonnet | Read, Write, Edit, Glob, Grep | STATUS.md | Status updates, package counts, gate request text. Never content, never approves |
| research-analyst | opus | Read, Write, WebSearch, WebFetch | 00-viability | Pass 1: two-page brief with demand, audience fit, durability, competitors, GO/NO-GO/DEFER, plus a source pack holding the claims the brief cites (`SP-0.n`). Pass 2 after Gate 0: extends the source pack with module claims (`SP-1.n` and up), each with URL, date, mechanism |
| curriculum-architect | opus | Read, Write | 01-syllabus | Metadata, prerequisites, 3 to 9 outcomes scaled to module count (`LO-n`, measurable verbs, majority applied), one capstone artifact, module table with depth marks and minutes, out of scope, rot watch, revision log |
| deck-writer | sonnet | Read, Write | 02-deck | One deck per module in the slide schema, drawn SVG visuals, 80 to 150 word notes, glossary slide, `SP-` citations |
| assessment-designer | sonnet | Read, Write | 03-assessments | 8 to 12 item quiz, key with distractor reasoning, predict and reflect prompts, one transfer item, TA feedback pack per module (rubric and misconception explanations, no literal answers) |
| lab-engineer | sonnet | Read, Write | 04-labs | Lab per module: Step 0 in five minutes, steps with prediction, action, evidence, recovery, planted defect with stated requirement, debrief, troubleshooting table. No execution, unexecuted steps disclosed |
| qa-reviewer | opus | Read, Glob, Grep, Write | qa | Alignment matrix, then verdict PASS / PASS WITH FIXES / FAIL with numbered issues. On PASS also writes the TA grounding manifest. Reports, never edits |
| ta-agent | haiku | Read, Write | maintenance | Answers from the files in the grounding manifest only, never grades, never reveals keys, escalates to the human. Writes the weekly digest. Runs after publish via `/ask-ta` and `/ta-digest` |

Two things from the reference are kept verbatim in spirit because they were learned from real
failures: a worked example must state its source of truth before the verdict (the "over 100"
bug), and nothing is invented to fill a gap, a gap is declared.

## 7. QA: script first, model second

Mechanical checks move to `scripts/check_package.py` so they cost no tokens and never drift:

- Package manifest complete for the module count in the syllabus.
- Every `.md` has a PDF in `dist/` that is not older than the source.
- Zero em dashes, sentence-case headings.
- Quiz has 8 to 12 items, every item has a key entry, no instructor file referenced from the
  student tree.
- Deck slides: max four bullets, max eight words each, every slide has `Covers:`, no
  placeholder visual, SVG has `viewBox`, notes word count, longest run of abstract slides.
- Every `SP-` cited in a deck exists in the source pack.

The qa-reviewer then does the judgment checks: alignment matrix with no empty cells, a 10-claim
spot check against the source pack, worked-example soundness and boundary cases, level fit on
three sampled explanations, vocabulary against prerequisites, notes substance. The reference's
checks 4, 8 and 13 (execution, demo package, evidence pack) are dropped with their artifacts.

## 8. Rendering

Port `build/render.py`, `_base.css`, a neutral theme and one accent theme from the reference.
Chrome is installed here and `uv` is on the path, so the reference's path works as is:
`uv run --with markdown --with pygments python build/render.py <slug> [--only stage]`.
`run.ps1` and `run.sh` wrap it. Decks render two PDFs each: 16:9 student, and instructor with
notes. Instructor material gets the "Instructor only" ribbon. Unverified until phase 2 runs it.

## 9. Build phases, each ends in a commit and a push

| Phase | Work | Commit |
| --- | --- | --- |
| 0 | Repo, reference clone, gitignore | done |
| 1 | This plan, STYLE.md, templates, folder skeleton | plan, then style and templates |
| 2 | Port renderer and themes, `run.*`, readiness check, render a fixture course to PDF | renderer, then fixture |
| 3 | `check_package.py` with tests against the fixture | checker |
| 4 | Agents, one commit per one or two agents, in pipeline order | 4 to 5 commits |
| 5 | `CLAUDE.md`, slash commands including `/ask-ta` and `/ta-digest`, settings and stage-order hook, hook tests | orchestration, then hooks |
| 6 | Dry run on a small real topic through all three gates and a TA question round, fix what breaks | one commit per fix batch |
| 7 | README for CLI and Desktop, troubleshooting, tag v0.1 | docs |

Acceptance: from a fresh clone, `claude` then `/new-course ...` reaches Gate 0 with a PDF; after
three plain "yes" replies the full package exists as md and PDF, `check_package.py` passes,
every `APPROVALS.md` line quotes the human's own words, and `/ask-ta` answers from the
grounding pack and refuses a key request.

## 10. Risks

- Subagent quality drops when briefs shrink from 20 KB to 4 KB. Mitigation: the dry run, and
  keep the rules that came from real failures.
- Context growth in one long session. Mitigation: STATUS.md as memory, agents return short
  reports, the main session never reads full artifacts unless gating.
- Renderer on Windows is untested here. Mitigation: phase 2 proves it before agents depend on it.
- Desktop parity is assumed, not verified. Mitigation: test in phase 6.
- Cost: opus on three agents. Mitigation: switch to sonnet by editing one frontmatter line.

## 11. Decisions (locked)

1. Modules: configurable 1 to 4, default 2.
2. Topic-agnostic.
3. Labs written, not executed, unexecuted steps disclosed.
4. `dist/` ignored by git; PDFs can be snapshotted at a gate on request.
5. Approval is plain language from the user, no name list.
6. video-producer removed. ta-agent is part of the pipeline as the maintenance stage.
