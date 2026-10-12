# Strategy and roadmap

## MVP

Request, approve, and cancel single bookings. It tests the belief that one approver removes double bookings (user, D-005).

## Now, Next, Later

| Horizon | Decisions | Source |
| --- | --- | --- |
| Now | D-005 | user |
| Next | None confirmed | None confirmed |
| Later | D-003 | user |

## Dependencies

Recurring bookings depend on the single-booking lifecycle.

## Signals

Advance recurring bookings when managers ask for them twice in a month. Kill them if no manager asks during the MVP.

## Non-roadmap

- Recurring bookings in the first release (D-003).
