from uuid import uuid4

import pytest

from app.database import SessionLocal
from app.services import TicketService


@pytest.fixture
def db_session():
    with SessionLocal() as session:
        try:
            yield session
        finally:
            session.rollback()


@pytest.fixture
def service(db_session):
    return TicketService(db_session)


@pytest.fixture
def customer_factory(service):
    def create_customer():
        unique_id = uuid4().hex[:8]

        return service.create_customer(
            customer_id=f"C{unique_id}",
            name="Test Customer",
            email=f"{unique_id}@example.com",
        )

    return create_customer
