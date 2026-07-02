import urllib.request
import urllib.parse
import re
import csv
import time
import os
from datetime import datetime, timedelta

# Target AJAX URL
url = "https://www.ze-van.fr/wp-admin/admin-ajax.php"

# Calendar IDs and configurations
calendars = [
    {
        "id": "1",
        "name": "T7 California Beach Nomade",
        "referer": "https://www.ze-van.fr/location-van-amenage-california-beach-nomade/",
        "mapping": {
            "wpbs-legend-item-1": "Disponible",
            "wpbs-legend-item-2": "Réservé",
            "wpbs-legend-item-5": "Indisponible"
        }
    },
    {
        "id": "2",
        "name": "T6.1 California Beach Camper",
        "referer": "https://www.ze-van.fr/location-van-amenage-california-beach-camper/",
        "mapping": {
            "wpbs-legend-item-6": "Disponible",
            "wpbs-legend-item-7": "Réservé",
            "wpbs-legend-item-10": "Indisponible"
        }
    },
    {
        "id": "3",
        "name": "T7 California Beach Routard",
        "referer": "https://www.ze-van.fr/location-van-amenage-t7-california-beach-routard/",
        "mapping": {
            "wpbs-legend-item-11": "Disponible",
            "wpbs-legend-item-12": "Réservé",
            "wpbs-legend-item-13": "Indisponible"
        }
    }
]

# Scrape 48 months from January 2024 to December 2027
start_date = datetime(2024, 1, 1)
months_to_scrape = []
for i in range(48):
    year = 2024 + (1 + i - 1) // 12
    month = (1 + i - 1) % 12 + 1
    months_to_scrape.append((year, month))

months_to_scrape = sorted(list(set(months_to_scrape)))

print("Months to scrape:", months_to_scrape)
all_records = []

for cal in calendars:
    print(f"\nScraping calendar for: {cal['name']} (ID {cal['id']})")
    
    for year, month in months_to_scrape:
        print(f"  Fetching {month:02d}/{year}...")
        
        data = {
            "action": "wpbs_refresh_calendar",
            "id": cal["id"],
            "show_title": "0",
            "months_to_show": "1",
            "start_weekday": "1",
            "show_legend": "1",
            "legend_position": "bottom",
            "show_button_navigation": "1",
            "show_selector_navigation": "1",
            "show_week_numbers": "0",
            "current_year": str(year),
            "current_month": str(month),
            "jump_months": "0",
            "highlight_today": "1",
            "history": "1",
            "show_tooltip": "1",
            "show_prices": "1",
            "language": "fr",
            "min_width": "320",
            "max_width": "380",
            "start_date": "0",
            "end_date": "0",
            "changeover_start": "0",
            "changeover_end": "0",
            "currency": "EUR",
            "form_position": "bottom",
            "current_date": "1782950400000",
            "show_first_available_date": "0"
        }
        
        encoded_data = urllib.parse.urlencode(data).encode("utf-8")
        
        req = urllib.request.Request(
            url,
            data=encoded_data,
            headers={
                "Accept": "*/*",
                "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",
                "X-Requested-With": "XMLHttpRequest",
                "Origin": "https://www.ze-van.fr",
                "Referer": cal["referer"]
            }
        )
        
        try:
            with urllib.request.urlopen(req) as response:
                html = response.read().decode("utf-8")
                
                # Regex to extract day options
                pattern = r'<div\s+class="([^"]*wpbs-date[^"]*)"[^>]*data-year="(\d+)"[^>]*data-month="(\d+)"[^>]*data-day="(\d+)"[^>]*data-price="(\d+)"'
                matches = re.findall(pattern, html)
                
                for cls, y, m, d, price in matches:
                    status = "Inconnu"
                    for class_key, status_val in cal["mapping"].items():
                        if class_key in cls:
                            status = status_val
                            break
                    
                    date_str = f"{y}-{m.zfill(2)}-{d.zfill(2)}"
                    all_records.append({
                        "van_name": cal["name"],
                        "calendar_id": cal["id"],
                        "date": date_str,
                        "year": y,
                        "month": m,
                        "day": d,
                        "price": price,
                        "status": status
                    })
            time.sleep(0.4)
        except Exception as e:
            print(f"    Error fetching {month}/{year}: {e}")

# Check if we retrieved anything
import sys
if len(all_records) == 0:
    print("\n[!] CRITICAL ERROR: Scraper retrieved 0 records.")
    print("    This usually means the target website (ze-van.fr hosted on o2switch) is blocking this server's IP address (Render).")
    print("    Aborting CSV overwrite to protect existing database.")
    sys.exit(1)

# Save to workspace CSV
output_csv = "ze_van_availability.csv"
with open(output_csv, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow(["Van Name", "Date", "Year", "Month", "Day", "Price (EUR)", "Status"])
    for r in all_records:
        writer.writerow([r["van_name"], r["date"], r["year"], r["month"], r["day"], r["price"], r["status"]])

print(f"\nDone! Scraped {len(all_records)} date records.")
print(f"Saved data to CSV: {os.path.abspath(output_csv)}")
