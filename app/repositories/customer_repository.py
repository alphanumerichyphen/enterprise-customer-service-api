from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db_models import CustomerDB
from app.models import Customer

class CustomerRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, customer: Customer) -> Customer:
        customer_db = CustomerDB(
            id=customer.id,
            name=customer.name,
            email=customer.email,
        )

        self.session.add(customer_db)
        self.session.flush()

        return customer

    def get(self, customer_id: str) -> Customer | None:
        statement = select(CustomerDB).where(
            CustomerDB.id == customer_id
        )

        customer_db = self.session.scalar(statement)

        if customer_db is None:
            return None

        return Customer(
            id=customer_db.id,
            name=customer_db.name,
            email=customer_db.email,
        )

    def list(self) -> list[Customer]:
        statement = select(CustomerDB).order_by(CustomerDB.id)
        customers_db = self.session.scalars(statement).all()

        # for every customer_db in customers_db, convert to domain object Customer and return list
        return [
            Customer(
                id=customer_db.id,
                name=customer_db.name,
                email=customer_db.email,
            )
            for customer_db in customers_db
        ]