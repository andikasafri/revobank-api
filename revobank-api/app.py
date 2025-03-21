from flask import Flask, jsonify
from supabase import create_client
import datetime

app = Flask(__name__)

# Supabase configuration
SUPABASE_URL = 'https://vedhlwtoufauyzrngshg.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZlZGhsd3RvdWZhdXl6cm5nc2hnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDIxODYwMzAsImV4cCI6MjA1Nzc2MjAzMH0.hRERDp7Pq0MwNruYar0Nycs7Lubl_k1Vwraho-YdJfI'

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.route("/")
def index():
    return "RevoBank API is running with Supabase!"

@app.route("/create_revouser")
def create_revouser():
    """
    Endpoint for inserting a new row into the 'revouser' table.
    """
    try:
        # Create a timestamp for the new user
        now_str = datetime.datetime.utcnow().isoformat()

        # Prepare data to insert
        insert_data = {"created_at": now_str}
        
        # Execute the insert operation
        response = supabase.table("revouser").insert(insert_data).execute()

        # Log the raw response for debugging
        print("Raw response:", response)

        # Check if the response contains data
        if response.data:
            return jsonify({
                "message": "Inserted new user successfully!",
                "inserted_data": response.data
            })
        else:
            return "No data returned from Supabase.", 204

    except Exception as e:
        # Log the exception details
        print("Exception occurred:", e)
        return f"An exception occurred: {e}", 500

if __name__ == "__main__":
    app.run(debug=True)