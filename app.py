from pydantic import BaseModel, Field, ValidationError
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
#1. Sql Base Class 

class Base(DeclarativeBase):
    pass

#2 Product Class 
class Product(Base):
    _tablename_="products"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    category: Mapped[str]
    price: Mapped[int]
    in_stock: Mapped[bool]

engine = create_engine("sqllite:///ecommerce.db")

Base.metadaba.create_all(engine)

def insert_data():
    with Session(engine) as session:
        products=[
            Product(name="iPhone13", category="mobile", price=79999, in_stock=True),
            Product(name="Samsung S24", category="mobile", price=69999, in_stock=True),
            Product(name="OnePlus 12R", category="mobile", price=39999, in_stock=True),
            Product(name="Nothing Phone 2", category="mobile", price=44999, in_stock=False),
            Product(name="MacBook Air M2", category="laptop", price=89999, in_stock=True),
            Product(name="Dell Inspiron", category="laptop", price=55999, in_stock=True),
        ]
        
        session.add_all(products)
        session.commit()
class ProductSearchInput(BaseModel):
    category: str = Field(min_length=1)
    max_price: int = Field(gt=0)
    only_in_stock: bool = True


def search_product(input_date: dict) -> dict:
    try:
        validatedInput = ProductSearchInput(**input_data)
    except ValidationError as error:
        return {
            "success":"False",
            "error" : "Invalid input provided",
            "details" : error.errors()
        }
    # make a call to DB and search the table

    with SessionLocal() as session:
        query=select(Product).where(
            Product.category == validatedInput.category,
            Product.price <= validatedInput.max_price,
            Product.in_stock == validatedInput.only_in_stock
        )

        products_from_db = session.scalars(query).all()

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
    