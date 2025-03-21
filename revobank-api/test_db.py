import os
import psycopg2
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file in the project root directory
load_dotenv(find_dotenv())     

# Set the connection parameters directly with the new credentials
USER = "postgres"
PASSWORD = "lnwxcJNWEdbY3pPp"
HOST = "vedhlwtoufauyzrngshg.supabase.co"
PORT = "5432"
DBNAME = "postgres"

# Compute the absolute path to the certificate file assuming it's in the same folder as this script
cert_path = os.path.join(os.path.dirname(__file__), "prod-ca-2021.crt")

# Display the connection string for debug purposes (without exposing the password)
print("Attempting to connect using new credentials:")
print(f"postgresql://{USER}:***@{HOST}:{PORT}/{DBNAME}")

try:
    # Connect to the PostgreSQL database using psycopg2 with certificate verification (sslmode set to verify-ca)
    connection = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME,
        sslmode='verify-ca',
        sslrootcert=cert_path
    )
    print("✅ SUCCESS: Connected to Supabase PostgreSQL database!")
    
    # Create a cursor to execute SQL queries
    cursor = connection.cursor()
    
    # Create a new table 'test_table' if it does not exist
    create_table_query = """
        CREATE TABLE IF NOT EXISTS test_table (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50) NOT NULL
        );
    """
    cursor.execute(create_table_query)
    connection.commit()
    print("✅ Table 'test_table' created (if it did not already exist).")
    
    # Example query to list all tables
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    tables = cursor.fetchall()
    print("Tables in the database:", [table[0] for table in tables])
    
    # Close the cursor and connection
    cursor.close()
    connection.close()
    print("Connection closed.")
    
except Exception as e:
    print(f"❌ ERROR: {str(e)}")
