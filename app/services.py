from typing import Optional
from app.models import Customer, Ticket, TicketPriority, TicketStatus
from app.exceptions import (
    CustomerAlreadyExists,
    CustomerNotFound,
    TicketNotFound,
)

class TicketService:

    def __init__(self):
        self.customers = {}
        self.tickets = {}
        self.next_ticket_id = 1

    def create_customer(self, customer_id: str, name: str, email: str) -> Customer:
        if customer_id in self.customers: # use 'in' to check existence of key when value is not needed
            raise CustomerAlreadyExists("A customer with this id already exists")
        c = Customer(id=customer_id, name=name, email=email)
        self.customers[c.id] = c
        return c

    def get_customer(self, customer_id: str) -> Customer:
        if customer_id not in self.customers:
            raise CustomerNotFound("Customer with this id does not exist")

        return self.customers[customer_id]

    def list_customers(self) -> list[Customer]:
        return list(self.customers.values())

    def create_ticket(self, customer_id: str, title: str, description: str, priority: TicketPriority) -> Ticket:
        if customer_id not in self.customers: # use 'in' to check existence of key when value is not needed
            raise CustomerNotFound("A customer with this id does not exist")
        ticket_id = f"T{self.next_ticket_id:03d}"
        self.next_ticket_id += 1
        t = Ticket(id=ticket_id, customer_id=customer_id, title=title, description=description, priority=priority, status=TicketStatus.OPEN)
        self.tickets[t.id] = t
        return t

    def get_ticket(self, ticket_id: str) -> Ticket:
        if ticket_id not in self.tickets:
            raise TicketNotFound("Ticket with this id does not exist")

        return self.tickets[ticket_id]

    def list_tickets(self, status: Optional[TicketStatus] = None) -> list[Ticket]:
        if status is None:
            return list(self.tickets.values())

        return [ticket for ticket in self.tickets.values() if ticket.status == status]

    def update_ticket(self, ticket_id: str, title: str, description: str, priority: TicketPriority, status: TicketStatus):
        ticket = self.tickets.get(ticket_id)
        if ticket is None:
            raise TicketNotFound("Ticket with this id does not exist")
        ticket.title = title
        ticket.description = description
        ticket.priority = priority
        ticket.status = status
        return ticket