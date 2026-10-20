from uuid import uuid4

from app.database import SessionLocal
from app.models import TicketPriority, TicketStatus
from app.services import TicketService


def main():
    customer_id = f"C{uuid4().hex[:8]}"

    with SessionLocal.begin() as session:
        service = TicketService(session)

        customer = service.create_customer(
            customer_id=customer_id,
            name="Demo Customer",
            email=f"{customer_id.lower()}@example.com",
        )

        ticket = service.create_ticket(
            customer_id=customer.id,
            title="Payment failed",
            description="Customer cannot process invoice",
            priority=TicketPriority.HIGH,
        )

        print("Created customer:")
        print(customer)

        print("\nCreated ticket:")
        print(ticket)

        updated_ticket = service.update_ticket(
            ticket_id=ticket.id,
            title="Payment issue resolved",
            description="Customer confirmed the issue is fixed",
            priority=TicketPriority.MEDIUM,
            status=TicketStatus.RESOLVED,
        )

        print("\nUpdated ticket:")
        print(service.get_ticket(ticket.id))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

