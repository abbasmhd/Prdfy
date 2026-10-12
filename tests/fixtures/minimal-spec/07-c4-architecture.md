# C4 architecture

## Level 1: System context

### Purpose

Who touches the booking product, and what it hands to the payment terminal.

### Diagram

```mermaid
C4Context
title System Context for Hall Booking
Person(resident, "Resident", "Books the main hall")
Person(manager, "Manager", "Approves bookings")
System(product, "Hall Booking", "One confirmed booking per slot")
System_Ext(payment, "Payment terminal", "Takes payment")
Rel(resident, product, "Requests a slot")
Rel(manager, product, "Approves or declines a request")
Rel(product, payment, "Sends a payment request")
```

### Narrative

Payment stays outside the product (D-006).

### Boundaries considered and rejected

Taking payment inside the product was rejected (D-006).

## Level 2: Containers

### Purpose

The runnable roles inside Hall Booking.

### Diagram

```mermaid
C4Container
title Containers for Hall Booking
Person(resident, "Resident", "Books the main hall")
Container(client, "Interactive User Client", "Client role", "Request and view slots")
Container(app, "Application Service", "Application role", "Coordinates booking requests")
ContainerDb(state, "Relational State Store", "State role", "Slots and bookings")
Rel(resident, client, "Requests a slot")
Rel(client, app, "Sends the booking request")
Rel(app, state, "Records the booking")
```

### Narrative

No Message Broker: nothing asynchronous was confirmed (D-002).

### Boundaries considered and rejected

A separate Operator Client was rejected because one manager uses the same client (D-002).

## Level 3: Components

### Purpose

Parts inside the Application Service.

### Diagram

Not applicable: the Application Service has one responsibility in the MVP (D-002).

### Narrative

Revisit when recurring bookings arrive (D-003).

### Boundaries considered and rejected

None.

## Level 4: Domain structure

### Purpose

The Booking aggregate with the code removed.

### Diagram

```mermaid
classDiagram
class Booking {
  <<Aggregate>>
  status
  confirm()
  cancel()
}
class Slot {
  <<Value Object>>
  start
  end
}
Booking --> Slot : claims
```

### Narrative

Booking protects INV-001 (D-004).

### Boundaries considered and rejected

None.
