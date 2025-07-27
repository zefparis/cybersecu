from flask import Flask, render_template, request, jsonify, send_from_directory, flash, redirect, url_for, session
from pathlib import Path
import os
import json
import random
import uuid
import time
from datetime import datetime
from dotenv import load_dotenv
from scanner.engine import OWASPScanner
from scanner.report_generator import ReportGenerator

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key')

# Configuration
app.config['UPLOAD_FOLDER'] = 'reports'
app.config['ALLOWED_EXTENSIONS'] = {'json', 'pdf'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize the OWASP scanner
scanner = OWASPScanner()

# Store active scans
active_scans = {}

# Store completed scan results
scan_results = {}

# Add context processor to make current datetime available in all templates
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tools')
def tools():
    return render_template('tools.html')

@app.route('/demo', methods=['GET', 'POST'])
def demo():
    if request.method == 'POST':
        target_url = request.form.get('target_url', '').strip()
        if not target_url:
            flash('Veuillez entrer une URL valide', 'error')
            return redirect(url_for('demo'))
        
        # Generate a unique scan ID
        scan_id = str(uuid.uuid4())
        
        # Start the scan in a background thread
        active_scans[scan_id] = {
            'status': 'pending',
            'progress': 0,
            'target': target_url,
            'start_time': int(time.time()),
            'results': None
        }
        
        # Start the scan
        scanner.start_scan(target_url)
        active_scans[scan_id]['status'] = 'scanning'
        
        # Store scan ID in session
        if 'scan_ids' not in session:
            session['scan_ids'] = []
        session['scan_ids'].append(scan_id)
        
        return jsonify({
            'status': 'started',
            'scan_id': scan_id,
            'redirect': url_for('scan_status', scan_id=scan_id)
        })
    
    # Check if we're showing results for a specific scan
    scan_id = request.args.get('scan_id')
    if scan_id and scan_id in scan_results:
        return render_template('demo.html', scan_results=scan_results[scan_id], scan_id=scan_id)
    
    return render_template('demo.html')

@app.route('/certs')
def certs():
    return render_template('certs.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        message = request.form.get('message', '').strip()
        
        # In a real app, you would send an email here
        print(f"New contact form submission from {name} <{email}>: {message}")
        
        flash('Thank you for your message! I will get back to you soon.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

@app.route('/api/scan/status/<scan_id>')
def scan_status(scan_id):
    """Check the status of a scan."""
    if scan_id in active_scans:
        scan = active_scans[scan_id]
        scan_status = scanner.get_scan_status(scan_id)
        
        # Update our local scan status
        scan['status'] = scan_status['status']
        scan['progress'] = scan_status['progress']
        
        # If scan is complete, move to results
        if scan_status['status'] == 'completed':
            scan_results[scan_id] = scan_status
            scan['results'] = scan_status
            active_scans.pop(scan_id, None)
        
        return jsonify(scan_status)
    elif scan_id in scan_results:
        return jsonify({
            'status': 'completed',
            'progress': 100,
            'results': scan_results[scan_id]
        })
    else:
        return jsonify({'error': 'Scan not found'}), 404

@app.route('/api/scan/<scan_id>/report/<format>')
def generate_report(scan_id, format):
    """Generate a report for a completed scan."""
    if scan_id not in scan_results:
        return jsonify({'error': 'Scan results not found'}), 404
    
    if format not in ['pdf', 'json']:
        return jsonify({'error': 'Invalid report format'}), 400
    
    try:
        # Generate the report
        report_gen = ReportGenerator(scan_results[scan_id])
        
        if format == 'pdf':
            filename = f'scan_report_{scan_id}.pdf'
            filepath = report_gen.generate_pdf_report(filename)
            if not filepath:
                return jsonify({'error': 'PDF generation failed. Is reportlab installed?'}), 500
        else:  # json
            filename = f'scan_report_{scan_id}.json'
            filepath = report_gen.generate_json_report(filename)
        
        # Return the file for download
        return send_from_directory(
            os.path.dirname(filepath),
            os.path.basename(filepath),
            as_attachment=True,
            download_name=f'scan_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.{format}'
        )
    except Exception as e:
        app.logger.error(f'Error generating report: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/reports/<filename>')
def download_report(filename):
    """Legacy route for backward compatibility."""
    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename,
        as_attachment=True
    )

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
