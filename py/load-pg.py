import pandas as pd
import psycopg2

# Load the CSV file into a DataFrame
users_df = pd.read_csv('~/Downloads/Users.csv')

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="test", 
    user="postgres", 
    password="mysecretpassword", 
    host="localhost",
    port="5433"
)
cur = conn.cursor()

# Insert data row by row
for _, row in users_df.iterrows():
    cur.execute(
        "INSERT INTO Users (UserID, Name, Age, Gender) VALUES (%s, %s, %s, %s)",
        (int(row['UserID']), row['Name'], int(row['Age']), row['Gender'])
    )

# Commit and close
conn.commit()
cur.close()
conn.close()

