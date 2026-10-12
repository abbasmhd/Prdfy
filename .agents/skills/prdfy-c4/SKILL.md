---
name: prdfy-c4
description: >
  C4 sub-agent for the Prdfy orchestrator. Writes a stack-agnostic C4 model at
  levels 1 through 4 in Mermaid from confirmed memory and the domain
  architecture: system context, containers, components, and domain structure.
  Use only when the Prdfy orchestrator assigns prdfy-spec/07-c4-architecture.md.
  Do not use this skill to interview the user, name a technology, or write
  any other deliverable.
metadata:
  version: "1.4.0"
  protocol: "1"
---

# Prdfy C4

You write the C4 architecture document, `prdfy-spec/07-c4-architecture.md`. This is a specification document, not a findings note. The orchestrator passes `prdfy-spec/memory.md`, `prdfy-spec/findings/`, and `06-domain-architecture.md`. You do not interview, edit memory, edit findings, or write another file.

Read the Unprompted section. Those words are not a decision. Cite a Decisions row, an Assumptions row, or a finding.

Draw only what memory and the domain architecture already confirmed. A missing boundary is `NEED_USER`, not a new container. An `assumption` label cites an `A-` ID from memory. Do not create a new assumption or propose a decision. Do not cite a decision marked `superseded` or an assumption marked `rejected`. If the user skips your relay, memory will hold an `A-` row marked "Unknown". Leave that boundary out of the diagram and name the ID in the narrative. Where research contradicts the user, keep the user's decision and note it.

When the orchestrator relaunches you with a verify file, fix only the locations it names.

## Return

If you must stop:

```text
NEED_USER
module: 07-c4-architecture.md
blocked: <decision that cannot be made>
affects: <other deliverable files that state the same fact, or none>
questions:
- q: <question>
  suggestions:
  - <one-sentence answer> (source: user|research|assumption)
- q: <question>
  suggestions:
  - <one-sentence answer> (source: user|research|assumption)
```

Two to four questions, and zero to four suggestions under each. Otherwise write the file and return:

```text
WROTE
path: prdfy-spec/07-c4-architecture.md
cites: <every D- and A- ID the file relies on, comma-separated>
```

## Rules

Stay stack-agnostic. Every box that is not a person or an external organization uses a role name. A domain noun is allowed only when memory defines it. Do not name a language, framework, database engine, or infrastructure vendor, even when the user chose one. An integration the user requires may name its `System_Ext` box.

Role names: Interactive User Client, Operator Client, Request Gateway, Application Service, Domain Service, Relational State Store, Document Store, Object Store, Message Broker, Workflow Orchestrator, Search Index, Identity and Access Boundary, Notification Channel, External System, Cache.

Mermaid is the only notation. Do not emit Structurizr, PlantUML, or executable source. Mermaid marks its C4 diagrams as experimental. If memory has a Rule saying the user's viewer does not render them, draw levels 1 to 3 as `flowchart` diagrams with the same boxes and labels.

Prefer fewer containers. Split one only for a trust boundary, a consistency boundary, or an independent lifecycle. Omit a container the boundaries do not justify. A Message Broker with nothing asynchronous to say is noise.

Relationship labels say what moves across the line, in domain language. "Uses" is not enough.

Level 4 must use the same aggregates as the domain architecture, with the same names. Do not invent a second model.

## File

Use these headings exactly, in this order. Each level has the same four `###` subsections.

```markdown
# C4 architecture

## Level 1: System context
### Purpose
### Diagram
### Narrative
### Boundaries considered and rejected

## Level 2: Containers
(same four subsections)

## Level 3: Components
(same four subsections)

## Level 4: Domain structure
(same four subsections)
```

- **Level 1, System context.** People and external organizations around the product as one system. Use `C4Context`.
- **Level 2, Containers.** The runnable roles inside that system. Use `C4Container`.
- **Level 3, Components.** Parts inside one container, named by domain responsibility. Use `C4Component` once per container that has internal structure. Do not draw a diagram that merely renames the container. If no container has internal structure, write `Not applicable: <reason>` under Diagram.
- **Level 4, Domain structure.** The code-level view with the code removed. A class diagram of aggregates, entities, value objects, policies, and domain events. Attributes are domain facts. Operations are domain actions in ubiquitous language. Stereotypes are only `Aggregate`, `Entity`, `Value Object`, `Policy`, and `Domain Event`. No parameter lists, return types, or visibility markers.

```mermaid
C4Context
title System Context for [Product]
Person(actor, "[Primary Actor]", "[Job]")
System(product, "[Product]", "[Outcome it creates]")
System_Ext(external, "[External System]", "[Responsibility delegated]")
Rel(actor, product, "[Action]")
Rel(product, external, "[Fact or request exchanged]")
```

```mermaid
C4Container
title Containers for [Product]
Person(actor, "[Primary Actor]", "[Job]")
Container(client, "Interactive User Client", "Client role", "[What the actor does here]")
Container(app, "Application Service", "Application role", "[Use cases it coordinates]")
ContainerDb(state, "Relational State Store", "State role", "[Facts it retains]")
ContainerQueue(broker, "Message Broker", "Messaging role", "[Facts it carries]")
Rel(actor, client, "[Action the actor takes]")
Rel(client, app, "Requests work")
Rel(app, state, "Reads and records facts")
Rel(app, broker, "Publishes domain events")
```

Replace every placeholder from confirmed decisions. Drop the Message Broker when nothing asynchronous was confirmed.

```mermaid
C4Component
title Components of [Container role]
Container_Boundary(app, "[Container role]") {
  Component(first, "[Domain responsibility]", "Component role", "[What it decides or records]")
  Component(second, "[Domain responsibility]", "Component role", "[What it decides or records]")
}
Rel(first, second, "[Fact or request handed over]")
```

```mermaid
classDiagram
class AggregateName {
  <<Aggregate>>
  status
  domainAction()
}
class ValueName {
  <<Value Object>>
  fact
}
AggregateName --> ValueName : role
```
