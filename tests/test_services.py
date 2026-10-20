import pytest
from uuid import uuid4

from app.exceptions import (
    CustomerAlreadyExists,
    CustomerNotFound,
    TicketNotFound,
)
from app.models import TicketPriority, TicketStatus

pytestmark = pytest.mark.integration

def test_create_customer(service, customer_factory):
    customer = customer_factory()

    assert customer.id.startswith("C")
    assert customer.name == "Test Customer"
    assert customer.email.endswith("@example.com")


def test_create_customer_stores_customer(service, customer_factory):
    customer = customer_factory()

    retrieved = service.get_customer(customer.id)

    assert retrieved == customer


def test_create_duplicate_customer(service, customer_factory):
    customer = customer_factory()

    with pytest.raises(CustomerAlreadyExists):
        service.create_customer(
            customer.id,
            customer.name,
            customer.email,
        )


def test_get_missing_customer(service):
    with pytest.raises(CustomerNotFound):
        service.get_customer(f"C{uuid4().hex[:8]}")


def test_list_customers(service, customer_factory):
    customer = customer_factory()

    customers = service.list_customers()

    customer_ids = {item.id for item in customers}
    assert customer.id in customer_ids


def test_create_ticket(service, customer_factory):
    customer = customer_factory()

    ticket = service.create_ticket(
        customer_id=customer.id,
        title="Payment failed",
        description="Customer cannot process invoice",
        priority=TicketPriority.HIGH,
    )

    assert ticket.id.startswith("T")
    assert ticket.customer_id == customer.id
    assert ticket.title == "Payment failed"
    assert ticket.priority == TicketPriority.HIGH
    assert ticket.status == TicketStatus.OPEN


def test_create_ticket_for_missing_customer(service):
    with pytest.raises(CustomerNotFound):
        service.create_ticket(
            customer_id=f"C{uuid4().hex[:8]}",
            title="Payment failed",
            description="Customer cannot process invoice",
            priority=TicketPriority.HIGH,
        )


def test_get_ticket(service, customer_factory):

    customer = customer_factory()
    ticket = service.create_ticket(
        customer_id=customer.id,
        title="Payment failed",
        description="Customer cannot process invoice",
        priority=TicketPriority.HIGH,
    )
    assert service.get_ticket(ticket.id) == ticket


def test_get_missing_ticket(service):
    with pytest.raises(TicketNotFound):
        service.get_ticket(f"T{uuid4().hex[:16]}")


def test_list_tickets_filters_by_status(service, customer_factory):
    customer = customer_factory()

    open_ticket = service.create_ticket(
        customer.id,
        "Payment failed",
        "Payment was declined",
        TicketPriority.HIGH,
    )

    resolved_ticket = service.create_ticket(
        customer.id,
        "Password reset",
        "Password reset completed",
        TicketPriority.LOW,
    )

    service.update_ticket(
        resolved_ticket.id,
        resolved_ticket.title,
        resolved_ticket.description,
        resolved_ticket.priority,
        TicketStatus.RESOLVED,
    )

    open_tickets = service.list_tickets(TicketStatus.OPEN)
    resolved_tickets = service.list_tickets(TicketStatus.RESOLVED)

    open_ids = {ticket.id for ticket in open_tickets}
    resolved_ids = {ticket.id for ticket in resolved_tickets}

    assert open_ticket.id in open_ids
    assert resolved_ticket.id not in open_ids
    assert resolved_ticket.id in resolved_ids
    assert open_ticket.id not in resolved_ids


def test_update_ticket(service, customer_factory):
    customer = customer_factory()

    ticket = service.create_ticket(
        customer.id,
        "Payment failed",
        "Customer cannot process invoice",
        TicketPriority.LOW
    )

    updated_ticket = service.update_ticket(
        ticket.id,
        "Payment issue resolved",
        "Customer confirmed the issue is fixed",
        TicketPriority.HIGH,
        TicketStatus.RESOLVED,
    )

    assert updated_ticket.id == ticket.id
    assert updated_ticket.title == "Payment issue resolved"
    assert updated_ticket.description == "Customer confirmed the issue is fixed"
    assert updated_ticket.priority == TicketPriority.HIGH
    assert updated_ticket.status == TicketStatus.RESOLVED


def test_update_missing_ticket(service):
    with pytest.raises(TicketNotFound):
        service.update_ticket(
            f"T{uuid4().hex[:16]}",
            "Updated Title",
            "Updated Description",
            TicketPriority.HIGH,
            TicketStatus.RESOLVED,
        )
