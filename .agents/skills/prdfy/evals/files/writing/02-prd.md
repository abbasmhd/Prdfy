# Product requirements

## Problem statement

Double bookings of the main hall are found too late (user, D-001).

## Goals and non-goals

Goal: one confirmed booking per slot. Non-goal: recurring bookings (user, D-003).

## Actors

Resident, Manager.

## Jobs to be done

A resident wants a slot they can rely on.

## Journeys

1. A resident requests a slot.
2. The manager approves it.
3. The slot shows as taken to everyone else.

## Functional requirements

| ID | Requirement | Actor | Journey | Acceptance observation | Decisions | Source |
| --- | --- | --- | --- | --- | --- | --- |
| FR-001 | A resident can request a free slot. | Resident | 1 | The request appears to the manager. | D-002 | user |
| FR-002 | A manager can approve a request. | Manager | 2 | The slot shows as taken. | D-004 | user |

## Non-functional requirements

| ID | Quality | Observable expectation | Decisions | Source |
| --- | --- | --- | --- | --- |
| NFR-001 | Auditability | Every approval records who approved it and when. | D-004 | user |

## Constraints

- R-001: "Bookings must work on the hall's existing payment terminal."

## Out of scope

- Recurring bookings (D-003).

## Open questions

- Which jurisdiction applies (A-001)?
