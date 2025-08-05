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
    """Main page"""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 
