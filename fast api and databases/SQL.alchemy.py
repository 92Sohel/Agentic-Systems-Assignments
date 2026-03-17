from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, CheckConstraint, insert, select, update, delete

engine = create_engine("mysql+pymysql://root:password@localhost/my_database")
metadata = MetaData()

students = Table(
    'students', metadata,
    Column('id', Integer, primary_key=True),           # Unique ID for each student
    Column('name', String(50), nullable=False),        # Name cannot be empty
    Column('age', Integer, CheckConstraint('age>=18')), # Age must be 18 or older
    Column('city', String(50))                         # City can be empty (nullable)
)

# This actually sends the "CREATE TABLE" command to MySQL
metadata.create_all(engine)

with engine.connect() as conn:
    
    # STEP A: Insert 3 Students
    # We pass a list of dictionaries to add multiple people at once
    conn.execute(insert(students), [
        {"name": "Rahul", "age": 21, "city": "Mumbai"},
        {"name": "Anjali", "age": 19, "city": "Delhi"},
        {"name": "Vikram", "age": 22, "city": "Bangalore"}
    ])
    conn.commit() # "Commit" saves the changes permanently
    print("Success: 3 students added.")

    # STEP B: Fetch (Show) All Students
    print("\n--- Current List of Students ---")
    all_students = conn.execute(select(students)).fetchall()
    for s in all_students:
        print(f"ID: {s.id} | Name: {s.name} | Age: {s.age} | City: {s.city}")

    # STEP C: Update Rahul's City
    # We find the row where name is 'Rahul' and change the city
    update_task = update(students).where(students.c.name == "Rahul").values(city="Pune")
    conn.execute(update_task)
    conn.commit()
    print("\nSuccess: Rahul moved to Pune.")

    # STEP D: Delete young students (Age < 20)
    delete_task = delete(students).where(students.c.age < 20)
    conn.execute(delete_task)
    conn.commit()
    print("Success: Removed students under 20.")