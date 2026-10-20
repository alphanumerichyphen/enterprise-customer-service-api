from uuid import uuid4
from sqlalchemy.orm import Session
from app.exceptions import (
    CustomerAlreadyExists,
    CustomerNotFound,
    TicketNotFound,
)
from app.models import Customer, Ticket, TicketPriority, TicketStatus
from app.repositories.customer_repository import CustomerRepository
from app.repositories.ticket_repository import TicketRepository


class TicketService:

    def __init__(self, session: Session):
        self.customer_repository = CustomerRepository(session)
        self.ticket_repository = TicketRepository(session)

    def create_customer(self, customer_id: str, name: str, email: str) -> Customer:
        if self.customer_repository.get(customer_id) is not None:
            raise CustomerAlreadyExists("Customer with this id already exists")

        customer = Customer(
            id=customer_id,
            name=name,
            email=email,
        )

        return self.customer_repository.create(customer)


    def get_customer(self, customer_id: str) -> Customer:
        customer = self.customer_repository.get(customer_id)
        if customer is None:
            raise CustomerNotFound("Customer with this id does not exist")
        return customer


    def list_customers(self) -> list[Customer]:
        return self.customer_repository.list()


    def create_ticket(self, customer_id: str, title: str, description: str, priority: TicketPriority) -> Ticket:
        customer = self.customer_repository.get(customer_id)

        if customer is None:
            raise CustomerNotFound("Customer with this id does not exist")

        ticket = Ticket(
            id=f"T{uuid4().hex[:16]}",
            customer_id=customer_id,
            title=title,
            description=description,
            priority=priority,
            status=TicketStatus.OPEN,
        )
        # created in local now pass it to ticket repository which stores in database and returns a domain object
        return self.ticket_repository.create(ticket)


    def get_ticket(self, ticket_id: str) -> Ticket:
        ticket = self.ticket_repository.get(ticket_id)
        if ticket is None:
            raise TicketNotFound("Ticket with this id does not exist")
        return ticket

    # Ignores the status value and returns all tickets
    def list_tickets(self, status: TicketStatus | None = None) -> list[Ticket]:
        return self.ticket_repository.list_tickets(status)


    def update_ticket(self, ticket_id: str, title: str, description: str, priority: TicketPriority, status: TicketStatus) -> Ticket:
        existing_ticket = self.ticket_repository.get(ticket_id)
        if existing_ticket is None:
            raise TicketNotFound("Ticket with this id does not exist")
        updated_ticket = Ticket(
            id=existing_ticket.id,
            customer_id=existing_ticket.customer_id,
            title=title,
            description=description,
            priority=priority,
            status=status,
        )

        result = self.ticket_repository.update(updated_ticket)

        if result is None:
            raise TicketNotFound("Ticket with this id does not exist")
        return result