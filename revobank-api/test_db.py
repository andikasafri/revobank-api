from app import create_app, db

app = create_app()

with app.app_context():
    try:
        # Test connection
        conn = db.engine.connect()
        print("✅ SUCCESS: Connected to MySQL database!")
        conn.close()
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")