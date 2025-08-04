"""
Interunit Loan Reconciliation - Main Flask Application
Modular architecture with service-based backend.
"""
import os
from flask import Flask, request, jsonify, render_template
from core import database

app = Flask(__name__)

# Create upload folder
os.makedirs('uploads', exist_ok=True)

# Legacy helper functions moved to FileService
# Keeping minimal imports for compatibility

@app.route('/api/recent-uploads', methods=['GET'])
def get_recent_uploads():
    """Get recent uploads - REFACTORED to use FileService"""
    from core.services.file_service import FileService
    
    try:
        file_service = FileService()
        uploads = file_service.get_recent_uploads()
        return jsonify({'recent_uploads': uploads})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/clear-recent-uploads', methods=['POST'])
def clear_recent_uploads():
    """Clear recent uploads - REFACTORED to use FileService"""
    from core.services.file_service import FileService
    
    try:
        file_service = FileService()
        file_service.clear_recent_uploads()
        return jsonify({'message': 'Recent uploads cleared.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Helper moved to FileService class

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload and process file - REFACTORED to use FileService"""
    from core.services.file_service import FileService
    
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        sheet_name = request.form.get('sheet_name', 'Sheet1')
        
        # Use FileService for all file operations
        file_service = FileService()
        success, error, rows_processed = file_service.process_single_file(file, sheet_name)
        
        if success:
            return jsonify({
                'message': 'File processed successfully',
                'rows_processed': rows_processed
            })
        else:
            return jsonify({'error': error}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload-pair', methods=['POST'])
def upload_file_pair():
    """Upload and process file pair - REFACTORED to use FileService"""
    from core.services.file_service import FileService
    
    try:
        if 'file1' not in request.files or 'file2' not in request.files:
            return jsonify({'error': 'Both files are required'}), 400
        
        file1 = request.files['file1']
        file2 = request.files['file2']
        sheet_name1 = request.form.get('sheet_name1', 'Sheet1')
        sheet_name2 = request.form.get('sheet_name2', 'Sheet1')
        
        # Use FileService for all file pair operations
        file_service = FileService()
        success, error, pair_id, total_rows = file_service.process_file_pair(
            file1, sheet_name1, file2, sheet_name2
        )
        
        if success:
            return jsonify({
            'message': 'File pair processed successfully',
            'rows_processed': total_rows,
            'pair_id': pair_id
        })
        else:
            return jsonify({'error': error}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/data', methods=['GET'])
def get_data():
    """Get all data"""
    try:
        data = database.get_data()
        # Get column order from database
        column_order = database.get_column_order()
        return jsonify({
            'data': data,
            'column_order': column_order
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/filters', methods=['GET'])
def get_filters():
    """Get filter options"""
    try:
        filters = database.get_filters()
        return jsonify(filters)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export', methods=['GET'])
def export_data():
    """Export filtered data to Excel"""
    try:
        filters = {}
        if request.args.get('lender'):
            filters['lender'] = request.args.get('lender')
        if request.args.get('borrower'):
            filters['borrower'] = request.args.get('borrower')
        if request.args.get('statement_month'):
            filters['statement_month'] = request.args.get('statement_month')
        if request.args.get('statement_year'):
            filters['statement_year'] = request.args.get('statement_year')
        
        data = database.get_data(filters)
        if not data:
            return jsonify({'error': 'No data found'}), 404
        
        df = pd.DataFrame(data)
        export_filename = f"tally_data_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        export_path = os.path.join('uploads', export_filename)
        
        df.to_excel(export_path, index=False)
        
        return send_from_directory('uploads', export_filename, as_attachment=True)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reconcile', methods=['POST'])
def reconcile_transactions():
    """Reconcile interunit transactions - REFACTORED to use ReconciliationService"""
    from core.services.reconciliation_service import ReconciliationService
    
    try:
        data = request.get_json()
        lender_company = data.get('lender_company')
        borrower_company = data.get('borrower_company')
        month = data.get('month')
        year = data.get('year')
        
        # Use ReconciliationService for all matching logic
        reconciliation_service = ReconciliationService()
        matches_found = reconciliation_service.run_reconciliation(
            lender_company, borrower_company, month, year
        )
        
        return jsonify({
            'message': 'Reconciliation complete.',
            'matches_found': matches_found
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/matches', methods=['GET'])
def get_matches():
    """Get matched transactions, optionally filtered by company pair and period"""
    try:
        lender_company = request.args.get('lender_company')
        borrower_company = request.args.get('borrower_company')
        month = request.args.get('month')
        year = request.args.get('year')
        if lender_company and borrower_company:
            matches = database.get_matched_data_by_companies(lender_company, borrower_company, month, year)
        else:
            matches = database.get_matched_data()
        return jsonify({'matches': matches})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/pending-matches', methods=['GET'])
def get_pending_matches():
    """Get matches that need user confirmation"""
    try:
        matches = database.get_pending_matches()
        return jsonify({'matches': matches})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/confirmed-matches', methods=['GET'])
def get_confirmed_matches():
    """Get confirmed matches"""
    try:
        matches = database.get_confirmed_matches()
        return jsonify({'matches': matches})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/accept-match', methods=['POST'])
def accept_match():
    """Accept a match"""
    try:
        data = request.get_json()
        uid = data.get('uid')
        confirmed_by = data.get('confirmed_by', 'User')
        
        if not uid:
            return jsonify({'error': 'uid is required'}), 400
        
        success = database.update_match_status(uid, 'confirmed', confirmed_by)
        
        if success:
            return jsonify({'message': 'Match accepted successfully'})
        else:
            return jsonify({'error': 'Failed to accept match'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reject-match', methods=['POST'])
def reject_match():
    """Reject a match"""
    try:
        data = request.get_json()
        uid = data.get('uid')
        confirmed_by = data.get('confirmed_by', 'User')
        
        if not uid:
            return jsonify({'error': 'uid is required'}), 400
        
        success = database.update_match_status(uid, 'rejected', confirmed_by)
        
        if success:
            return jsonify({'message': 'Match rejected successfully'})
        else:
            return jsonify({'error': 'Failed to reject match'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download-matches', methods=['GET'])
def download_matches():
    """Download matched transactions as Excel - REFACTORED to use ExportService"""
    from core.services.export_service import ExportService
    
    try:
        filters = {
            'lender_company': request.args.get('lender_company'),
            'borrower_company': request.args.get('borrower_company'),
            'month': request.args.get('month'),
            'year': request.args.get('year')
        }
        
        export_service = ExportService()
        return export_service.export_matched_transactions(filters)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Old download routes removed - using ExportService instead

@app.route('/api/detected-pairs', methods=['GET'])
def get_detected_pairs():
    """Get detected company pairs"""
    try:
        pairs = database.detect_company_pairs()
        return jsonify({'pairs': pairs})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/manual-pairs', methods=['GET'])
def get_manual_pairs():
    """Get manual company pairs"""
    try:
        pairs = database.get_manual_company_pairs()
        return jsonify({'pairs': pairs})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/pairs', methods=['GET'])
def get_all_pairs():
    """Get all company pairs"""
    try:
        pairs = database.get_company_pairs()
        return jsonify({'pairs': pairs})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/pair/<pair_id>/data', methods=['GET'])
def get_pair_data(pair_id):
    """Get data for a specific pair"""
    try:
        data = database.get_data_by_pair_id(pair_id)
        return jsonify({'data': data, 'pair_id': pair_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/unmatched', methods=['GET'])
def get_unmatched_data():
    """Get unmatched data with optional filtering"""
    try:
        # Get filter parameters
        lender_company = request.args.get('lender_company')
        borrower_company = request.args.get('borrower_company')
        month = request.args.get('month')
        year = request.args.get('year')
        
        # Apply filters if provided
        if lender_company and borrower_company:
            data = database.get_unmatched_data_by_companies(lender_company, borrower_company, month, year)
        else:
            data = database.get_unmatched_data()
        
        return jsonify({'unmatched': data})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/pair/<pair_id>/unmatched', methods=['GET'])
def get_pair_unmatched_data(pair_id):
    """Get unmatched data for a specific pair"""
    try:
        data = database.get_unmatched_data_by_pair_id(pair_id)
        return jsonify({'unmatched': data, 'pair_id': pair_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reconcile-pair/<pair_id>', methods=['POST'])
def reconcile_pair(pair_id):
    """Reconcile transactions for a specific pair - REFACTORED to use ReconciliationService"""
    from core.services.reconciliation_service import ReconciliationService
    
    try:
        # Use ReconciliationService for pair reconciliation
        reconciliation_service = ReconciliationService()
        matches_found = reconciliation_service.run_pair_reconciliation(pair_id)
        
        return jsonify({
            'message': f'Reconciliation complete for pair {pair_id}.',
            'matches_found': matches_found,
            'pair_id': pair_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/unreconciled-pairs', methods=['GET'])
def get_unreconciled_pairs():
    """Get company pairs that haven't been reconciled yet"""
    try:
        pairs = database.get_unreconciled_company_pairs()
        return jsonify({'pairs': pairs})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 
