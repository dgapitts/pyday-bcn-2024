import redis
from redis.commands.search.field import TagField, VectorField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query

r = redis.Redis(host="localhost", port=6379)

import pandas as pd
import redis

# Load the CSV file
users_df = pd.read_csv('~/Downloads/Users.csv')

# Connect to Redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)

# Load each row into Redis as a hash
for _, row in users_df.iterrows():
    # Create a unique key for each user
    user_key = f"user:{row['UserID']}"
    
    # Use the HMSET command to store the row data as a hash
    r.hmset(user_key, {
        "Name": row['Name'],
        "Age": row['Age'],
        "Gender": row['Gender']
    })



