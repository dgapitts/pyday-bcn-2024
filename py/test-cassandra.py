from cassandra.cluster import Cluster

# Connect to the Cassandra cluster
cluster = Cluster(['127.0.0.1'])  # Use '127.0.0.1' if running locally
session = cluster.connect()

# Optional: create a keyspace
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS test_keyspace
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}
""")

# Set the keyspace
session.set_keyspace('test_keyspace')

# Optional: create a table
session.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id UUID PRIMARY KEY,
        name text,
        age int
    )
""")

# Insert a sample record
from uuid import uuid4
session.execute("""
    INSERT INTO users (user_id, name, age) VALUES (%s, %s, %s)
""", (uuid4(), 'Alice', 30))

# Query the data
rows = session.execute('SELECT * FROM users')
for row in rows:
    print(row)

# Close the connection
cluster.shutdown()

