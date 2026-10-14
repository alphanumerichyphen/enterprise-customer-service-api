import pytest
from uuid import uuid4

from app.database import SessionLocal
from app.models import Customer, Ticket, TicketPriority, TicketStatus
from app.repositories.customer_repository import CustomerRepository
from app.repositories.ticket_repository import TicketRepository


@pytest.fixture # creates SQLAlchemy session for each test, rollbacks any uncommitted changes
def db_session():
    with SessionLocal() as session:
        try:
            yield session
        finally:
            session.rollback()


@pytest.mark.integration
def test_customer_repository_create_and_get(db_session):
    customer_id = f"C{uuid4().hex[:8]}"

    # create Customer record
    customer = Customer(
        id=customer_id,
        name="Repository Test",
        email=f"{customer_id}@example.com",
    )

    # create CustomerRepository record
    repository = CustomerRepository(db_session)

    created_customer = repository.create(customer)
    retrieved_customer = repository.get(customer_id)

    assert created_customer == customer
    assert retrieved_customer is not None
    assert retrieved_customer.id == customer_id
    assert retrieved_customer.name == "Repository Test"
    assert retrieved_customer.email == f"{customer_id}@example.com"


@pytest.mark.integration
def test_ticket_repository_create_get_filter_and_update(db_session):
    customer_id = f"C{uuid4().hex[:8]}"

    customer = Customer(
        id=customer_id,
        name="Ticket Repository Test",
        email=f"{customer_id}@example.com",
    )

    CustomerRepository(db_session).create(customer)

    repository = TicketRepository(db_session)

    open_ticket = Ticket(
        id=f"T{uuid4().hex[:8]}",
        customer_id=customer_id,
        title="Payment failed",
        description="Testing ticket creation",
        priority=TicketPriority.HIGH,
        status=TicketStatus.OPEN,
    )

    resolved_ticket = Ticket(
        id=f"T{uuid4().hex[:8]}",
        customer_id=customer_id,
        title="Password reset",
        description="Testing status filtering",
        priority=TicketPriority.LOW,
        status=TicketStatus.RESOLVED,
    )

    repository.create(open_ticket)
    repository.create(resolved_ticket)

    # Test retrieval
    retrieved = repository.get(open_ticket.id)

    assert retrieved is not None
    assert retrieved == open_ticket

    # Test filtering
    open_tickets = repository.list_tickets(TicketStatus.OPEN)
    open_ticket_ids = {ticket.id for ticket in open_tickets}

    assert open_ticket.id in open_ticket_ids
    assert resolved_ticket.id not in open_ticket_ids

    # Test update
    updated_ticket = Ticket(
        id=open_ticket.id,
        customer_id=customer_id,
        title="Payment issue fixed",
        description="The customer confirmed resolution",
        priority=TicketPriority.MEDIUM,
        status=TicketStatus.IN_PROGRESS,
    )

    result = repository.update(updated_ticket)

    assert result == updated_ticket

    # Verify the updated values can be retrieved
    retrieved_after_update = repository.get(open_ticket.id)

    assert retrieved_after_update == updated_ticket