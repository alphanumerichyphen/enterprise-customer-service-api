import pytest

from app.models import TicketPriority, TicketStatus
from app.services import (
    TicketService,
    CustomerAlreadyExists,
    CustomerNotFound,
    TicketNotFound
)

def test_create_customer():
    service = TicketService()
    customer = service.create_customer(
        "C001",
        "Yash",
        "test@mail.com"
    )

    assert customer.id == "C001"
    assert customer.name == "Yash"
    assert customer.email == "test@mail.com"

def test_create_customer_stores_customer():
    service = TicketService()
    service.create_customer(
        "C001",
        "Yash",
        "test@mail.com"
    )
    customer = service.get_customer("C001")
    assert customer.name == "Yash"
    assert customer.email == "test@mail.com"

def test_create_duplicate_customer():
    service = TicketService()
    service.create_customer(
        "C001",
        "Yash",
        "test@mail.com"
    )
    with pytest.raises(CustomerAlreadyExists):
        service.create_customer(
            "C001",
            "Yash",
            "test@mail.com"
        )

def test_get_missing_customer():
    service = TicketService()
    with pytest.raises(CustomerNotFound):
        service.get_customer("C999")

def test_create_ticket():
    service = TicketService()

    service.create_customer(
        "C001",
        "Yash",
        "test@mail.com"
    )

    ticket = service.create_ticket(
        customer_id="C001",
        title="Payment failed",
        description="Customer cannot process invoice",
        priority=TicketPriority.HIGH,
    )

    assert ticket.id == "T001"
    assert ticket.customer_id == "C001"
    assert ticket.title == "Payment failed"
    assert ticket.description == "Customer cannot process invoice"
    assert ticket.priority == TicketPriority.HIGH
    assert ticket.status == TicketStatus.OPEN

def test_create_multiple_tickets_generate_unique_ids():
    service = TicketService()

    service.create_customer(
        "C001",
        "Yash",
        "test@mail.com"
    )

    ticket_1 = service.create_ticket(
        customer_id="C001",
        title="First issue",
        description="First description",
        priority=TicketPriority.LOW,
    )

    ticket_2 = service.create_ticket(
        customer_id="C001",
        title="Second issue",
        description="Second description",
        priority=TicketPriority.HIGH,
    )

    assert ticket_1.id == "T001"
    assert ticket_2.id == "T002"

def test_create_ticket_with_missing_customer():
    service = TicketService()

    with pytest.raises(CustomerNotFound):
        service.create_ticket(
            customer_id="C999",
            title="Payment failed",
            description="Customer cannot process invoice",
            priority=TicketPriority.HIGH,
        )

def test_get_ticket():
    service = TicketService()

    service.create_customer(
        "C001",
        "Yash",
        "test@mail.com"
    )

    ticket = service.create_ticket(
        customer_id="C001",
        title="Payment failed",
        description="Customer cannot process invoice",
        priority=TicketPriority.HIGH,
    )

    retrieved_ticket = service.get_ticket(ticket.id)

    assert retrieved_ticket.id == ticket.id
    assert retrieved_ticket.customer_id == "C001"
    assert retrieved_ticket.title == "Payment failed"
    assert retrieved_ticket.description == "Customer cannot process invoice"
    assert retrieved_ticket.priority == TicketPriority.HIGH
    assert retrieved_ticket.status == TicketStatus.OPEN

def test_get_missing_ticket():
    service = TicketService()

    with pytest.raises(TicketNotFound):
        service.get_ticket("T999")

def test_list_tickets_filters_by_status():
    service = TicketService()
    service.create_customer(
        "C001",
        "Yash",
        "test@mail.com"
    )

    ticket_1 = service.create_ticket(
        "C001",
        "Issue 1",
        "Description 1",
        TicketPriority.LOW,
    )

    ticket_2 = service.create_ticket(
        "C001",
        "Issue 2",
        "Description 2",
        TicketPriority.HIGH,
    )

    ticket_3 = service.create_ticket(
        "C001",
        "Issue 3",
        "Description 3",
        TicketPriority.MEDIUM,
    )

    service.update_ticket(
        ticket_3.id,
        "Issue 3",
        "Description 3",
        TicketPriority.MEDIUM,
        TicketStatus.RESOLVED,
    )

    open_tickets = service.list_tickets(TicketStatus.OPEN)
    resolved_tickets = service.list_tickets(TicketStatus.RESOLVED)

    assert len(open_tickets) == 2
    assert len(resolved_tickets) == 1
    assert resolved_tickets[0].id == ticket_3.id

def test_update_ticket():
    service = TicketService()
    service.create_customer(
        "C001",
        "Yash",
        "test@mail.com"
    )

    ticket = service.create_ticket(
        customer_id="C001",
        title="Payment failed",
        description="Customer cannot process invoice",
        priority=TicketPriority.LOW
    )

    updated_ticket = service.update_ticket(
        ticket.id,
        "Payment issue resolved",
        "Customer confirmed the issue is fixed",
        TicketPriority.HIGH,
        TicketStatus.RESOLVED,
    )

    assert updated_ticket.id == "T001"
    assert updated_ticket.title == "Payment issue resolved"
    assert updated_ticket.description == "Customer confirmed the issue is fixed"
    assert updated_ticket.priority == TicketPriority.HIGH
    assert updated_ticket.status == TicketStatus.RESOLVED

def test_update_missing_ticket():
    service = TicketService()

    with pytest.raises(TicketNotFound):
        service.update_ticket(
            "T999",
            "Some Title",
            "Some Description",
            TicketPriority.HIGH,
            TicketStatus.RESOLVED,
        )