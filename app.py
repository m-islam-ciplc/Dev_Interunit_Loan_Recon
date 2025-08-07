"""
Interunit Loan Reconciliation - Main Flask Application
Modular architecture with service-based backend and route blueprints.
"""
import os
from flask import Flask, render_template
from core.routes import register_blueprints

app = Flask(__name__)

# Create upload folder
os.makedirs('uploads', exist_ok=True)

# Register all route blueprints
register_blueprints(app)

@app.route('/')
def index():
    """Main page - redirects to tally-upload"""
    return render_template('index.html', active_tab='tally-upload')

@app.route('/tally-upload')
def tally_upload():
    """Tally Ledger Parser page"""
    return render_template('index.html', active_tab='tally-upload')

@app.route('/reconciliation')
def reconciliation():
    """Reconciliation page"""
    return render_template('index.html', active_tab='reconciliation')

@app.route('/data-table')
def data_table():
    """Transaction Data page"""
    return render_template('index.html', active_tab='data-table')

@app.route('/pairs-table')
def pairs_table():
    """Upload Pairs page"""
    return render_template('index.html', active_tab='pairs-table')

@app.route('/matched-results')
def matched_results():
    """Matched Results page"""
    return render_template('index.html', active_tab='matched-results')

@app.route('/unmatched-results')
def unmatched_results():
    """Unmatched Results page"""
    return render_template('index.html', active_tab='unmatched-results')

@app.route('/database-tools')
def database_tools():
    """Database Tools page"""
    return render_template('index.html', active_tab='database-tools')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 
