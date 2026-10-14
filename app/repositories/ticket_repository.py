from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db_models import TicketDB
from app.models import Ticket, TicketPriority, TicketStatus

class TicketRepository:

    def __init__(self, session: Session):
        self.session = session

    # takes a TicketDB and returns Ticket
    @staticmethod
    def _to_domain(ticket_db: TicketDB) -> Ticket:
        return Ticket(
            id=ticket_db.id,
            customer_id=ticket_db.customer_id,
            title=ticket_db.title,
            description=ticket_db.description,
            priority=TicketPriority(ticket_db.priority),
            status=TicketStatus(ticket_db.status)
        )

    # takes a Ticket, creates TicketDB, returns Ticket from _to_domain for some reason
    def create(self, ticket: Ticket) -> Ticket:
        ticket_db = TicketDB(
            id=ticket.id,
            customer_id=ticket.customer_id,
            title=ticket.title,
            description=ticket.description,
            priority=ticket.priority.value,
            status=ticket.status.value,
        )
        self.session.add(ticket_db)
        self.session.flush()

        return self._to_domain(ticket_db)

    # takes an id, finds if TicketDB exists, returns Ticket from _to_domain
    def get(self, ticket_id: str) -> Ticket | None:
        ticket_db = self.session.get(TicketDB, ticket_id)

        if ticket_db is None:
            return None

        return self._to_domain(ticket_db)

    # takes ticket status, creates query statement, queries TicketDBs, returns Ticket from _to_domain
    def list_tickets(self, status: TicketStatus | None = None) -> list[Ticket]:
        statement = select(TicketDB)

        if status is not None:
            statement = statement.where(TicketDB.status == status.value)

        statement = statement.order_by(TicketDB.id)
        results = self.session.scalars(statement).all()

        return [
            self._to_domain(ticket_db) for ticket_db in results
        ]

    # takes Ticket, fetches/updates TicketDB, returns Ticket
    def update(self, ticket: Ticket) -> Ticket | None:
        ticket_db = self.session.get(TicketDB, ticket.id)

        if ticket_db is None:
            return None

        ticket_db.title = ticket.title
        ticket_db.description = ticket.description
        ticket_db.priority = ticket.priority.value
        ticket_db.status = ticket.status.value

        self.session.flush()

        return self._to_domain(ticket_db)