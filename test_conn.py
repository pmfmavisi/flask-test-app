# test_conn.py

from dotenv import load_dotenv
import os
import pyodbc

# Load .env file
load_dotenv()

# Get the connection string from environment variable
conn_str = os.getenv("AZURE_SQL_CONNECTION")

try:
    # Try to connect
    conn = pyodbc.connect(conn_str)
    print("✅ Connected successfully to Azure SQL!")
    conn.close()
except Exception as e:
    print("❌ Connection failed:")
    print(e)
