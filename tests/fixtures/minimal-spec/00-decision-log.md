# Decision log

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

## Rules

- R-001: "Bookings must work on the hall's existing payment terminal."
