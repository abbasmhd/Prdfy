# Prdfy memory

## Rules
Rules the user imposed on this run. Later questions and deliverables obey them.

- R-001: "Bookings must work on the hall's existing payment terminal."

## Decisions
| ID | Module | Decision | Source | Status | Superseded by |
| --- | --- | --- | --- | --- | --- |
| D-001 | Vision | Volunteer hall managers lose evenings reconciling double bookings by phone. | user | confirmed | |
| D-002 | Scope | First release serves residents booking the main hall and one manager approving. | user | confirmed | |
| D-003 | Scope | Recurring bookings are out of scope for the first release. | user | confirmed | |
| D-004 | Domain Rules | A slot can hold at most one confirmed booking. | user | confirmed | |
| D-005 | Strategy and MVP | The MVP is request, approve, and cancel for single bookings. | user | confirmed | |
| D-006 | Architectural Boundaries | Payment stays with the hall's existing payment terminal, an External System. | user | confirmed | |
| D-007 | Scope | Residents may book any room. | user | superseded | D-002 |

## Questions and answers
| ID | Module | Question | Answer |
| --- | --- | --- | --- |
| QA-001 | Vision | Who feels the problem today? | The volunteer managers. |

## Assumptions
| ID | Module | Exit item | Assumption | Status |
| --- | --- | --- | --- | --- |
| A-001 | Risk and Compliance | Jurisdiction | Unknown | open |

## Progress
Phase: writing
Active module: none
Draft: full

| File | Status | Cites |
| --- | --- | --- |
| 00-decision-log.md | pending | |
| 01-business-plan.md | written | D-001, D-005, A-001 |
| 02-prd.md | written | D-002, D-003, D-004, D-006 |
| 03-specifications.md | pending | |
| 04-strategy-roadmap.md | pending | |
| 05-risk-compliance.md | pending | |
| 06-domain-architecture.md | pending | |
| 07-c4-architecture.md | pending | |
| README.md | pending | |
