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

@app.route('/api/calendar.ics')
def get_ical():
    csv_path = "ze_van_availability.csv"
    if not os.path.exists(csv_path):
        return "No data available. Please refresh first.", 404
        
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
    except Exception as e:
        return str(e), 500

    # Group bookings
    detected_bookings = []
    ordered_vans = [
        "T6.1 California Beach Camper",
        "T7 California Beach Nomade",
        "T7 California Beach Routard"
    ]
    
    from datetime import datetime, timedelta
    for van_name in ordered_vans:
        van_reservations = [r for r in records if r["van"] == van_name and r["status"] == "Réservé"]
        van_reservations.sort(key=lambda x: x["date"])
        
        if not van_reservations:
            continue
            
        current_booking = None
        for r in van_reservations:
            r_date = datetime.strptime(r["date"], "%Y-%m-%d")
            if not current_booking:
                current_booking = {
                    "van": van_name,
                    "start": r_date,
                    "end": r_date,
                    "revenue": r["price"]
                }
            else:
                if (r_date - current_booking["end"]).days <= 1:
                    current_booking["end"] = r_date
                    current_booking["revenue"] += r["price"]
                else:
                    detected_bookings.append(current_booking)
                    current_booking = {
                        "van": van_name,
                        "start": r_date,
                        "end": r_date,
                        "revenue": r["price"]
                    }
        if current_booking:
            detected_bookings.append(current_booking)

    # Build ICS
    ical = []
    ical.append("BEGIN:VCALENDAR")
    ical.append("VERSION:2.0")
    ical.append("PRODID:-//Ze-Van//Analytics//FR")
    ical.append("CALSCALE:GREGORIAN")
    ical.append("METHOD:PUBLISH")
    
    for i, b in enumerate(detected_bookings):
        start_str = b["start"].strftime("%Y%m%d")
        end_str = (b["end"] + timedelta(days=1)).strftime("%Y%m%d")
        uid = f"booking-{i}-{start_str}-{b['van'].replace(' ', '-')[:15]}@ze-van.fr"
        
        ical.append("BEGIN:VEVENT")
        ical.append(f"UID:{uid}")
        ical.append(f"DTSTART;VALUE=DATE:{start_str}")
        ical.append(f"DTEND;VALUE=DATE:{end_str}")
        ical.append(f"SUMMARY:[{b['van'].split(' ')[-1]}] Réservé")
        ical.append(f"DESCRIPTION:Réservation du van {b['van']} - CA: {b['revenue']} EUR")
        ical.append("END:VEVENT")
        
    ical.append("END:VCALENDAR")
    ical_content = "\r\n".join(ical)
    
    response = app.response_class(
        response=ical_content,
        status=200,
        mimetype='text/calendar'
    )
    response.headers["Content-Disposition"] = "attachment; filename=ze_van_bookings.ics"
    return response

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
