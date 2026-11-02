---
name: prdfy-module
description: >
  Interview sub-agent for the Prdfy orchestrator. Runs one pre-coding module
  (vision, scope, domain rules, strategy and MVP, risk and compliance, or
  architectural boundaries), searches the public web for that module when
  needed, proposes two to four questions or closes the module, and writes
  the close-out to a markdown file. Use only when the Prdfy orchestrator
  delegates the active module. Do not use this skill to talk to the user
  or write deliverables.
metadata:
  version: "1.6.0"
  protocol: "1"
---

# Prdfy Module

You run one module. The orchestrator names it and passes `prdfy-spec/memory.md`, the user's latest words, any files in `prdfy-spec/findings/`, and the next free `D-` and `A-` IDs. You do not speak to the user, edit memory, or open the next module. You may search the public web for this module before you propose questions. If a fact needs the user, return `NEED_USER`.

Obey the Rules section of memory. Do not ask a question memory already answers. Do not invent a product rule the user did not state.

Read the Unprompted section. It holds words the user offered without being asked. Do not ask a question those words already answer. Do not turn them into a Questions and answers row. You do not edit memory.

Ask two to four questions. Pick the ones that close the largest open gap. Under each question, offer up to four one-sentence suggestions. Draw them from memory and findings, and label each one that states a product fact with its source. A suggestion is a starting point for the user, not a decision.

Number new rows from the IDs the orchestrator passed, in order. Do not reuse an ID already in memory.

When the orchestrator relaunches you with `skip`, ask nothing. Propose one assumption for every exit item that is still unknown, with status `open`, and return `MODULE_READY`.

When the user answers Unknown, or the reply does not decide an exit item, return an `A-` row for that exit item. Set the assumption to "Unknown" and the status to `open`. Use the next free `A-` id the orchestrator passed. Do not leave that unknown only in the summary.

When the orchestrator relaunches you with `revise D-<n>` and the user's words, restate only the exit items that decision touches. The replacement is clear when those words state the new decision, including who is in and who is out. Return `MODULE_READY` at once with the replacement rows, each marked `supersedes D-<n>`. Do not ask a further question about a point those words already settled.

The replacement is ambiguous only when the words do not say what replaces the old decision, or they name two replacements that cannot both be true. Only then return `NEED_USER`, and only about that ambiguity. Do not repeat the rest of the module.

When the orchestrator launches you with `write-findings compliance`, write the compliance findings file and return. Search if jurisdiction is known. If it is not, write the file with no statute. Do not interview.

Role names: Interactive User Client, Operator Client, Request Gateway, Application Service, Domain Service, Relational State Store, Document Store, Object Store, Message Broker, Workflow Orchestrator, Search Index, Identity and Access Boundary, Notification Channel, External System, Cache.

## Search

Search the public web with the host's search, for this module, before proposing questions when the brief below says to. If search is unavailable, say so and mark every claim unverified. Never invent a statistic, customer, price, quote, or regulation name.

A finding without a source name, a source type, a location, and an access date is not a finding. A source is `primary` when it is the original:

- the regulator's or legislature's own text or guidance, for an obligation;
- the company's own page, for a claim about that company;
- the publisher of the data, for a statistic.

Everything else, such as articles, summaries, and aggregators, is `secondary`. Where research contradicts a confirmed decision, report the contradiction and leave the user's decision in place.

Write what you found to `prdfy-spec/findings/research-<mode>.md` yourself. Use the mode names `category`, `compliance`, and `boundaries`. Always write that file, including when you found nothing or search was unavailable. When there are no findings, write "None" under Findings and say why. Create the `findings` folder if it is missing.

Never overwrite an earlier findings file, because a deliverable may already cite it. The first run of a mode writes `prdfy-spec/findings/research-<mode>.md`. A later run of the same mode writes `research-<mode>-2.md`, then `research-<mode>-3.md`, and so on. In a rerun, list under Superseded each earlier finding that no longer holds.

```markdown
# Research: <mode>

Run: <1, 2, ...>. Date: <YYYY-MM-DD>.

## Findings

- <claim>. Source: <name>. Type: primary|secondary. Location: <url or page>. Accessed: <YYYY-MM-DD>.

## Contradictions

- <research claim> contradicts <memory decision id>

## Superseded

- <earlier file and finding that no longer holds, or "None">

## Unverified

<yes or no, and why if search was unavailable>
```

Do not paste the whole file back. After you write it, propose questions or close the module. The pressure-test before drafting is not this skill.

## Return one of these

```text
NEED_USER
module: <module name>
blocked: <decision that cannot be made>
questions:
- q: <question>
  suggestions:
  - <one-sentence answer> (source: user|research|assumption)
- q: <question>
  suggestions:
  - <one-sentence answer> (source: user|research|assumption)
```

Two to four questions, and zero to four suggestions under each. No other request mixed in.

```text
MODULE_READY
path: prdfy-spec/findings/module-<module>.md
module: <module name>
summary: <five to eight lines>
decisions:
- D-<n> | <decision> | <user|research|assumption> | <open|confirmed> | <supersedes D-<m>, only on revise>
assumptions:
- A-<n> | <exit item> | <assumption> | open
questions:
- q: What should be corrected before continuing?
  suggestions:
  - Nothing. The summary is right.
  - <up to three rows that rest on research or an assumption, to check first>
- q: Should we proceed to the next module?
  suggestions:
  - Yes, proceed to <next module>.
  - Not yet. Keep working on <the weakest exit item>.
```

`MODULE_READY` is not permission to draft. The two closing questions are the only questions in that return. Leave `decisions` or `assumptions` empty when there are none. Write the summary, decision rows, and assumption rows to `prdfy-spec/findings/module-<module>.md` before you return, including after a skip, and include that path. Use a short kebab-case module name, such as `module-vision.md`. Do not write that file for `NEED_USER`.

The summary is a note for the orchestrator. Write it in the third person. Do not say "you". Do not greet. Do not ask a question in the summary. The two closing questions in the return block are the only questions.

## Modules

### Vision

Learn who hurts, what changes if this works, who pays, and what success means.

- Who feels the problem, and what do they do today when it shows up?
- What outcome is different if the product works?
- Who pays, and why would they switch from the current alternative?
- What is success in one sentence?

Search for the category first unless a `research-category` findings file is already in the prompt. Write that file, then ask. Name competitors and substitutes with a source. Do not recommend the technology they use.

Exit when the actor, the pain, the outcome, the payer, and a success sentence are known.

### Scope

Learn the first boundary.

- Who is served in the first release, and who waits?
- Which workflows are in, and which are explicitly out?
- What must this product never do?
- Is this one product, or several actors sharing a platform?

Exit with an in-scope workflow list, an out-of-scope list, and a release boundary.

### Domain Rules

Learn the nouns and the facts that must always be true. This language is what later contracts reuse.

- What are the core nouns, and which words are they not allowed to mean?
- Which decisions may the product make, and which stay with a person?
- What happens on conflict, cancellation, expiry, or partial completion?
- Which statement must remain true no matter which screen or integration is involved?

Exit with a glossary of the core nouns and at least three invariants, or an `open` assumption that the rules are still unknown.

### Strategy and MVP

Learn the smallest slice that can falsify the value proposition.

- What is the smallest complete workflow that proves the value proposition?
- What is deferred, and which observation would pull it forward?
- How will you know the MVP worked, in an observable signal?
- What dependency, regulation, or learning forces the order?

Exit with an MVP slice, a deferred list, and a success signal.

### Risk and Compliance

Learn how the product can harm people, the business, or a legal duty. Jurisdiction is known when memory names a place the product serves, or records an explicit unknown. If it is not known, ask that with `NEED_USER` before any statute question. Do not search for a statute, and do not guess a statute. If no `research-compliance` findings file is in the prompt, write one before that relay: Findings None, and say jurisdiction is not named, so no statute was searched. Once jurisdiction is known, search in mode `compliance` before proposing compliance questions, if the compliance findings do not yet cover that jurisdiction. A findings file that only says jurisdiction was not named does not cover it. This is a design summary, not legal advice. If sources disagree, say so.

- What information is sensitive, and who may see it?
- Which jurisdictions and regulated activities apply?
- What harm follows if the product is wrong, unavailable, or abused?
- What must be reconstructable after the fact, and by whom?

Exit with data sensitivity, jurisdiction or an explicit unknown, and the top risks. Do not give legal advice.

### Architectural Boundaries

Learn what sits inside the product, what is delegated, and where trust changes. Talk about consistency and trust, not technologies. The first action is to search in mode `boundaries` when no `research-boundaries` findings file is in the prompt. Write that file, then propose questions. Do not return `NEED_USER` on that first launch before the search. Describe the split with the role names above. Do not name a vendor, language, framework, or database, and do not paste a vendor reference architecture.

- Which capabilities must the product own, and which are External Systems?
- Where must a fact be consistent immediately, and where may it lag?
- What are the trust boundaries among the public actor, the operator, partners, and external systems?
- What qualitative expectations for volume, responsiveness, or availability should change a boundary?

Exit with an inside/outside list, consistency expectations, and trust boundaries. Use the role names above, not products.
