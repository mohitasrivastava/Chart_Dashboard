from app import app, db, Data

# Create all tables in the database
with app.app_context():
    db.create_all()
    print("Database tables created successfully!")
    records = Data.query.all()
    print(records, "records")


