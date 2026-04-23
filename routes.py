from flask import Flask, request, jsonify
from src.schema_loader import SchemaLoader
from src.db import fetch_calculated_data
from src.calculations import run_calculation_engine

app = Flask(__name__)
loader = SchemaLoader()

@app.route('/', methods=['GET'])
def calculate():
    # If no data is sent, request.get_json() is None, triggers "all true" logic
    data = request.get_json(silent=True) or {}
    toggles = data.get('toggles', {})
    
    # Load config and override includes
    config = loader.get_config(toggles)
    
    # SQL logic for calculations
    sql_results = fetch_calculated_data(config)
    result = run_calculation_engine(sql_results, config)
    
    return jsonify(result)