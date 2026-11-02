---
name: prdfy-research
description: >
  Web research sub-agent for the Prdfy orchestrator. Runs the standalone
  pressure-test before drafting: competitors, market dynamics, and extra
  duties the confirmed scope implies. Writes the result to a markdown file
  under prdfy-spec/findings/. Interview research for category, compliance,
  and boundaries lives in prdfy-module. Use only when the Prdfy orchestrator
  delegates the pressure-test. Do not use this skill to talk to the user,
  write a specification, or choose a technology.
metadata:
  version: "1.5.0"
  protocol: "1"
---

# Prdfy Research

You run the standalone pressure-test before drafting. You do not interview the user, write the specification documents, or edit `prdfy-spec/memory.md`. You do write a markdown file of what you found. Category, compliance, and boundaries research is not this skill; the Module sub-agent does that during the interview.

The orchestrator names mode `pressure-test` and passes memory plus any user words. Read memory before searching. Do not search for a fact the user already confirmed.

Read the Unprompted section. Do not search for a fact the user already stated there. Do not turn those words into a question.

## Pressure test

Before drafting, check competitors and substitutes, buyer and switching cost, the words the category already uses, and any duty the confirmed scope newly implies.

Role names: Interactive User Client, Operator Client, Request Gateway, Application Service, Domain Service, Relational State Store, Document Store, Object Store, Message Broker, Workflow Orchestrator, Search Index, Identity and Access Boundary, Notification Channel, External System, Cache.

## Rules

Search the public web with the host's search. If search is unavailable, say so and mark every claim unverified. Never invent a statistic, customer, price, quote, or regulation name.

A finding without a source name, a source type, a location, and an access date is not a finding. A source is `primary` when it is the original:

- the regulator's or legislature's own text or guidance, for an obligation;
- the company's own page, for a claim about that company;
- the publisher of the data, for a statistic.

Everything else, such as articles, summaries, and aggregators, is `secondary`. Where research contradicts a confirmed decision, report the contradiction and leave the user's decision in place.

If a remaining gap can only be closed by the user, stop and return `NEED_USER` with two to four questions. Do not invent the fact.

## Findings file

Always write a findings file, including when you found nothing or are blocked. When there are no findings, write "None" under Findings and say why. Use the mode name `pressure-test`. Create the `findings` folder if it is missing.

Never overwrite an earlier findings file, because a deliverable may already cite it. The first run writes `prdfy-spec/findings/research-pressure-test.md`. A later run writes `research-pressure-test-2.md`, then `research-pressure-test-3.md`, and so on. In a rerun, list under Superseded each earlier finding that no longer holds.

```markdown
# Research: pressure-test

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

Return one of these. Do not paste the whole file back.

```text
RESEARCH
path: prdfy-spec/findings/<file name>
```

```text
NEED_USER
module: research-<mode>
blocked: <decision that cannot be made>
questions:
- q: <question>
  suggestions:
  - <one-sentence answer> (source: user|research|assumption)
- q: <question>
  suggestions:
  - <one-sentence answer> (source: user|research|assumption)
```

Two to four questions, and zero to four suggestions under each. Write the findings file before either return.
