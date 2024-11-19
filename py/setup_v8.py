from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pgvector.sqlalchemy import Vector

import numpy as np

size=8  



table="v"+str(size)
print (table)


# Define the database URL
DATABASE_URL = "postgresql+psycopg2://postgres:mysecretpassword@localhost:5433"

# Create the engine
engine = create_engine(DATABASE_URL)

# Define the base class for declarative models
Base = declarative_base()

# Define the SQLAlchemy model
class Item(Base):
    __tablename__ = table
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    embedding = Column(Vector(size))  
    
# Create the table in the database
Base.metadata.create_all(engine)

# Create a new session
Session = sessionmaker(bind=engine)
session = Session()



for i in range(0,10):
    for j in range(0,1000):
        # Generate the random numbers
        # print (str(i)+"-"+str(j))
        random_array = np.random.rand(size)

        item = Item(
            name="example_item",
            embedding=random_array
        )

        # Add and commit the item to the database
        session.add(item)
        session.commit()
session.commit()

