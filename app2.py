# Import Pydantic for validating tool input dictionaries
from pydantic import BaseModel, Field, ValidationError

# Import SQLAlchemy engine and SELECT helper for queries
from sqlalchemy import create_engine, select

# Import ORM base class, column mapping, and session factory pieces
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, sessionmaker

# Import Optional so in_stock can be omitted with a default
from typing import Optional


# Create the declarative base — parent for all ORM table classes
Base = declarative_base()


# ORM class that maps to the products table in SQLite
class Product(Base):
    # Explicit table name in the database
    __tablename__ = "products"

    # Primary key column with auto-increment
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Product display name stored as text
    name: Mapped[str] = mapped_column()

    # Category such as mobile, laptop, etc.
    category: Mapped[str] = mapped_column()

    # Price stored as integer rupees for simple filtering
    price: Mapped[int] = mapped_column()

    # Whether the item is currently in stock
    in_stock: Mapped[bool] = mapped_column()


# SQLite file created in the project folder; echo=False keeps SQL logs quiet
engine = create_engine("sqlite:///e-commerce.db", echo=False)

# Create all tables for classes that inherit from Base (here, products)
Base.metadata.create_all(engine)

# Session factory bound to our engine — each session is one conversation with the DB
SessionLocal = sessionmaker(bind=engine)


# Sample seed rows matching the six-product demo discussed in class
SAMPLE_PRODUCTS = [
    {"name": "iPhone 15", "category": "mobile", "price": 79900, "in_stock": True},
    {"name": "Samsung Galaxy S24", "category": "mobile", "price": 74999, "in_stock": True},
    {"name": "OnePlus 12R", "category": "mobile", "price": 42999, "in_stock": True},
    {"name": "Google Pixel 8", "category": "mobile", "price": 54999, "in_stock": False},
    {"name": "Redmi Note 13", "category": "mobile", "price": 18999, "in_stock": True},
    {"name": "Motorola Edge 40", "category": "mobile", "price": 29999, "in_stock": True},
]


# Pydantic model describing valid search arguments for the search_product tool
class ProductSearchInput(BaseModel):
    # Category is required and cannot be an empty string
    category: str = Field(..., min_length=1)

    # Maximum price filter; must be a positive integer
    max_price: int = Field(..., gt=0)

    # When omitted, default to showing only in-stock items
    in_stock: Optional[bool] = True


def insert_data() -> None:
    """Insert demo products if you are running the script fresh."""
    # Open a short-lived database session
    with SessionLocal() as session:
        # Build ORM Product instances from plain dictionaries
        products = [Product(**row) for row in SAMPLE_PRODUCTS]

        # Stage every row in one batch
        session.add_all(products)

        # Persist inserts to e-commerce.db
        session.commit()


def search_product(input_data: dict):
    """
    Tool function: validate dict input, query ORM, return rows or an error dict.
  """
    try:
        # Unpack the incoming dict into a validated Pydantic object
        validated_input = ProductSearchInput(**input_data)
    except ValidationError as err:
        # Return structured failure instead of raising to the agent runtime
        return {
            "success": False,
            "error": "Invalid input provided",
            "details": err.errors(),
        }

    # New session for the read query
    with SessionLocal() as session:
        # ORM SELECT with filters from validated fields — no hand-written SQL string
        query = select(Product).where(
            Product.category == validated_input.category,
            Product.price <= validated_input.max_price,
            Product.in_stock == validated_input.in_stock,
        )

        # Execute and fetch all matching Product instances
        products_from_db = session.scalars(query).all()

        # Return ORM objects; caller can read fields or shape JSON for the model
        return products_from_db


def agent_flow() -> None:
    """
    Simulated agent step: one hard-coded tool call instead of live LLM routing.
  """
    # In production this list is built from registered tools + LLM choice
    tool_calls = [
        {
            "tool_name": "search_product_tool",
            "arguments": {
                "category": "mobile",
                "max_price": 50000,
                "in_stock": True,
            },
        }
    ]

    # For each chosen tool, pull arguments and invoke the Python function
    for tool_call in tool_calls:
        arguments = tool_call["arguments"]
        tool_output = search_product(arguments)
        print(tool_output)


# Standard entry point when running: seed data, then run the simulated agent flow
if __name__ == "__main__":
    insert_data()
    agent_flow()
