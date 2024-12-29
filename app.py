from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

# Configuring SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the database model based on JSON structure
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    end_year = db.Column(db.String(4), nullable=True)
    intensity = db.Column(db.Integer, nullable=False)
    sector = db.Column(db.String(50), nullable=False)
    topic = db.Column(db.String(50), nullable=False)
    insight = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=True)
    region = db.Column(db.String(50), nullable=False)
    start_year = db.Column(db.String(4), nullable=True)
    impact = db.Column(db.String(255), nullable=True)
    added = db.Column(db.String(50), nullable=False)
    published = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    relevance = db.Column(db.Integer, nullable=False)
    pestle = db.Column(db.String(50), nullable=False)
    source = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    likelihood = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Data {self.title}>"

# Load data from JSON and add to the database
def load_data():
    try:
        with open('jsondata.json') as f:
            data = json.load(f)
            for entry in data:
                record = Data(
                    end_year=entry.get('end_year'),
                    intensity=entry.get('intensity'),
                    sector=entry.get('sector'),
                    topic=entry.get('topic'),
                    insight=entry.get('insight'),
                    url=entry.get('url'),
                    region=entry.get('region'),
                    start_year=entry.get('start_year'),
                    impact=entry.get('impact'),
                    added=entry.get('added'),
                    published=entry.get('published'),
                    country=entry.get('country'),
                    relevance=entry.get('relevance'),
                    pestle=entry.get('pestle'),
                    source=entry.get('source'),
                    title=entry.get('title'),
                    likelihood=entry.get('likelihood')
                )
                db.session.add(record)
            db.session.commit()
    except Exception as e:
        print(f"Error loading data: {e}")

# Route to serve the main HTML page
@app.route('/')
def index():
    return render_template('index.html')  # This loads the HTML file


# Endpoint to get data for visualization
@app.route('/data', methods=['GET'])
def get_data():
    filters = request.args  # Capture filter parameters from frontend if any
    query = Data.query
    
    # Apply filters dynamically if present
    if 'region' in filters:
        query = query.filter(Data.region == filters['region'])
    if 'topic' in filters:
        query = query.filter(Data.topic == filters['topic'])
    if 'sector' in filters:
        query = query.filter(Data.sector == filters['sector'])
    
    data = query.all()
    results = []
    for item in data[:5]:  # You can adjust the number of items here
        results.append({
            "intensity": item.intensity,
            "likelihood": item.likelihood,
            "relevance": item.relevance,
            "year": item.end_year or item.start_year,
            "country": item.country,
            "topic": item.topic,
            "region": item.region,
        })
    return jsonify(results)

# Initialize the database and load data
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates all tables
        try:
            load_data()  # Load data from the JSON file into the database
        except Exception as e:
            print(f"Error loading data: {e}")
    
    app.run(debug=False)  # Run the Flask app
