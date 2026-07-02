from flask import Flask, jsonify, send_file, request
import csv
import os
import subprocess
import threading

app = Flask(__name__)

# Track scraping status
scrape_status = {
    "status": "idle",  # 'idle', 'running', 'error'
    "last_run": None
}

def run_scraper_thread():
    global scrape_status
    scrape_status["status"] = "running"
    try:
        # Run scrape_calendars.py
        # We assume scrape_calendars.py is in the same directory
        result = subprocess.run(["python", "scrape_calendars.py"], capture_output=True, text=True)
        if result.returncode == 0:
            # Successfully scraped, now rebuild the static HTML report too
            subprocess.run(["python", "generate_report.py"], capture_output=True, text=True)
            scrape_status["status"] = "idle"
        else:
            print("Scraper error output:", result.stderr)
            scrape_status["status"] = "error"
    except Exception as e:
        print("Exception during background scraping:", e)
        scrape_status["status"] = "error"

@app.route('/')
def index():
    # Serve the compiled HTML dashboard
    html_path = "ze_van_dashboard.html"
    if os.path.exists(html_path):
        return send_file(html_path)
    return "Dashboard HTML not generated yet. Please run generate_report.py."

@app.route('/api/data')
def get_data():
    csv_path = "ze_van_availability.csv"
    if not os.path.exists(csv_path):
        return jsonify([])
    
    records = []
    try:
        with open(csv_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f, delimiter=";")
            for row in reader:
                records.append({
                    "van": row["Van Name"],
                    "date": row["Date"],
                    "year": int(row["Year"]),
                    "month": int(row["Month"]),
                    "day": int(row["Day"]),
                    "price": float(row["Price (EUR)"]),
                    "status": row["Status"]
                })
        return jsonify(records)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/refresh', class_methods=['POST'])
@app.route('/api/refresh', methods=['POST'])
def trigger_refresh():
    global scrape_status
    if scrape_status["status"] == "running":
        return jsonify({"status": "already_running"})
    
    # Start background thread
    t = threading.Thread(target=run_scraper_thread)
    t.start()
    return jsonify({"status": "started"})

@app.route('/api/refresh-status')
def get_refresh_status():
    return jsonify(scrape_status)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
