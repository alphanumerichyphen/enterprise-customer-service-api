from app.models import TicketPriority, TicketStatus
from app.services import TicketService

def main():
    service = TicketService()

    customer = service.create_customer(
        "C001",
        "Yash",
        "test@mail.com",
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

    service.update_ticket(
        ticket.id,
        "Payment issue resolved",
        "Customer confirmed the issue is fixed",
        TicketPriority.MEDIUM,
        TicketStatus.RESOLVED,
    )

    print("\nUpdated ticket:")
    print(service.get_ticket(ticket.id))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

