import csv
import json
import os

csv_path = "ze_van_availability.csv"
html_output_path = "ze_van_dashboard.html"

if not os.path.exists(csv_path):
    print(f"Error: {csv_path} not found. Please run scrape_calendars.py first.")
    exit(1)

# Read records from CSV
records = []
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

# Convert records to JSON for embedding
records_json = json.dumps(records)

# Generate HTML Content with Apple Glassmorphism Pro design and the new Shop & Audit tab
html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ze-Van Business Analytics & Manager</title>
    
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

    <style>
        :root {{
            --bg-dark: #07090e;
            --glass-bg: rgba(255, 255, 255, 0.035);
            --glass-border: rgba(255, 255, 255, 0.075);
            --glass-hover: rgba(255, 255, 255, 0.08);
            
            --text-primary: #f5f5f7;
            --text-secondary: #8e8e93;
            
            /* Apple System Colors */
            --color-avail: #30d158; /* Apple Green */
            --color-avail-bg: rgba(48, 209, 88, 0.12);
            --color-avail-border: rgba(48, 209, 88, 0.35);
            
            --color-res: #ff453a; /* Apple Red */
            --color-res-bg: rgba(255, 69, 58, 0.12);
            --color-res-border: rgba(255, 69, 58, 0.35);
            
            --color-unavail: #8e8e93; /* Apple Gray */
            --color-unavail-bg: rgba(142, 142, 147, 0.08);
            --color-unavail-border: rgba(142, 142, 147, 0.25);
            
            --van1-color: #0a84ff; /* Apple Blue */
            --van2-color: #ff9f0a; /* Apple Orange */
            --van3-color: #bf5af2; /* Apple Purple */
            
            --van1-gradient: linear-gradient(135deg, #0a84ff, #0066cc);
            --van2-gradient: linear-gradient(135deg, #ff9f0a, #ff3b30);
            --van3-gradient: linear-gradient(135deg, #bf5af2, #5e5ce6);
        }}
        
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-dark);
            color: var(--text-primary);
            min-height: 100vh;
            padding: 2.5rem;
            overflow-x: hidden;
            position: relative;
        }}
        
        /* Ambient Floating Blur Blobs (Apple Style) */
        .blur-blob {{
            position: fixed;
            border-radius: 50%;
            filter: blur(140px);
            z-index: -1;
            opacity: 0.14;
            pointer-events: none;
            transition: all 0.8s ease;
        }}
        .blob-1 {{
            top: -10%;
            left: 10%;
            width: 500px;
            height: 500px;
            background: #0066cc;
        }}
        .blob-2 {{
            bottom: -10%;
            right: 5%;
            width: 600px;
            height: 600px;
            background: #bf5af2;
        }}
        .blob-3 {{
            top: 40%;
            left: 45%;
            width: 450px;
            height: 450px;
            background: #ff9f0a;
            opacity: 0.08;
        }}
        
        .container {{
            max-width: 1450px;
            margin: 0 auto;
            position: relative;
            z-index: 1;
        }}
        
        /* Glass Card Base */
        .glass-card {{
            background: var(--glass-bg);
            border: 1px solid var(--glass-border);
            border-radius: 24px;
            backdrop-filter: blur(30px) saturate(190%);
            -webkit-backdrop-filter: blur(30px) saturate(190%);
            box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.25);
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }}
        
        .glass-card:hover {{
            border-color: rgba(255, 255, 255, 0.15);
            box-shadow: 0 15px 50px 0 rgba(0, 0, 0, 0.35);
            transform: translateY(-2px);
        }}
        
        header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2.5rem;
            padding-bottom: 1.5rem;
            border-bottom: 1px solid var(--glass-border);
        }}
        
        .header-title h1 {{
            font-family: 'Outfit', sans-serif;
            font-size: 2.75rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            background: linear-gradient(135deg, #ffffff 30%, #a2a2a6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }}
        
        .header-title p {{
            color: var(--text-secondary);
            font-size: 1.05rem;
            font-weight: 400;
        }}
        
        .header-controls {{
            display: flex;
            align-items: center;
            gap: 1rem;
        }}
        
        .btn-link {{
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--glass-border);
            color: var(--text-primary);
            padding: 0.7rem 1.4rem;
            border-radius: 14px;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.85rem;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .btn-link:hover {{
            background: rgba(255, 255, 255, 0.1);
            border-color: rgba(255, 255, 255, 0.2);
            transform: translateY(-1px);
        }}
        
        /* Select controls */
        select {{
            background: rgba(20, 20, 25, 0.8);
            border: 1px solid var(--glass-border);
            color: var(--text-primary);
            padding: 0.7rem 1.4rem;
            border-radius: 14px;
            font-family: inherit;
            font-size: 0.85rem;
            font-weight: 600;
            outline: none;
            cursor: pointer;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }}
        
        select:hover {{
            background: rgba(255, 255, 255, 0.05);
            border-color: rgba(255, 255, 255, 0.2);
        }}
        
        select option {{
            background-color: #1c1c1e;
            color: #f5f5f7;
        }}
        
        /* Navigation Tabs */
        .tabs {{
            display: inline-flex;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--glass-border);
            padding: 4px;
            border-radius: 16px;
            margin-bottom: 2.5rem;
            gap: 4px;
            backdrop-filter: blur(10px);
        }}
        
        .tab-btn {{
            background: transparent;
            border: none;
            color: var(--text-secondary);
            padding: 0.65rem 1.4rem;
            border-radius: 12px;
            font-size: 0.88rem;
            font-weight: 600;
            font-family: inherit;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }}
        
        .tab-btn:hover {{
            color: var(--text-primary);
        }}
        
        .tab-btn.active {{
            color: var(--text-primary);
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }}
        
        .tab-content {{
            display: none;
            animation: fadeIn 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(8px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        /* Stats Grid */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2.5rem;
        }}
        
        .stat-card {{
            padding: 1.75rem;
        }}
        
        .stat-header {{
            display: flex;
            justify-content: space-between;
            color: var(--text-secondary);
            font-size: 0.85rem;
            font-weight: 600;
            margin-bottom: 0.85rem;
        }}
        
        .stat-value {{
            font-size: 2.5rem;
            font-weight: 800;
            font-family: 'Outfit', sans-serif;
            letter-spacing: -0.02em;
            color: var(--text-primary);
        }}
        
        .stat-value.green {{
            color: var(--color-avail);
        }}
        
        .stat-footer {{
            font-size: 0.78rem;
            color: var(--text-secondary);
            margin-top: 0.75rem;
        }}
        
        /* Analytics Grid Layout */
        .analytics-dashboard {{
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 1.5rem;
            margin-bottom: 1.5rem;
        }}
        
        @media (max-width: 1100px) {{
            .analytics-dashboard {{
                grid-template-columns: 1fr;
            }}
        }}
        
        .chart-card {{
            padding: 2rem;
            min-height: 400px;
        }}
        
        .chart-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.35rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            margin-bottom: 1.5rem;
        }}
        
        .van-comparison-list {{
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}
        
        .van-comp-item {{
            background: rgba(255, 255, 255, 0.015);
            border: 1px solid rgba(255, 255, 255, 0.03);
            border-radius: 18px;
            padding: 1.25rem;
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
            transition: all 0.3s ease;
        }}
        
        .van-comp-item:hover {{
            background: rgba(255, 255, 255, 0.03);
            border-color: rgba(255, 255, 255, 0.08);
        }}
        
        .van-comp-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .van-comp-name {{
            font-weight: 700;
            font-size: 0.95rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-family: 'Outfit', sans-serif;
        }}
        
        .van-comp-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
        }}
        .van-comp-dot.van1 {{ background-color: var(--van1-color); }}
        .van-comp-dot.van2 {{ background-color: var(--van2-color); }}
        .van-comp-dot.van3 {{ background-color: var(--van3-color); }}
        
        .van-comp-revenue {{
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            font-size: 1.2rem;
            letter-spacing: -0.02em;
        }}
        
        .van-comp-metrics {{
            display: flex;
            justify-content: space-between;
            font-size: 0.8rem;
            color: var(--text-secondary);
        }}
        
        .van-comp-metrics span strong {{
            color: var(--text-primary);
        }}
        
        .van-comp-progress {{
            height: 5px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            overflow: hidden;
        }}
        
        .van-comp-fill {{
            height: 100%;
            border-radius: 10px;
        }}
        .van-comp-item.van1 .van-comp-fill {{ background: var(--van1-gradient); }}
        .van-comp-item.van2 .van-comp-fill {{ background: var(--van2-gradient); }}
        .van-comp-item.van3 .van-comp-fill {{ background: var(--van3-gradient); }}
        
        /* Table Layout / Card */
        .section-card {{
            padding: 2rem;
            margin-bottom: 2.5rem;
        }}
        
        .card-title-container {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.75rem;
        }}
        
        .card-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.5rem;
            font-weight: 700;
            letter-spacing: -0.02em;
        }}
        
        /* Calendar Grid */
        .calendar-grid {{
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 0.65rem;
            margin-top: 1.5rem;
        }}
        
        .weekday-label {{
            text-align: center;
            font-weight: 700;
            color: var(--text-secondary);
            font-size: 0.8rem;
            padding: 0.5rem 0;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .calendar-day {{
            background: rgba(255, 255, 255, 0.015);
            border: 1px solid rgba(255, 255, 255, 0.03);
            border-radius: 16px;
            aspect-ratio: 1 / 1.05;
            padding: 0.65rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }}
        
        .calendar-day.empty {{
            opacity: 0.12;
            pointer-events: none;
            background: transparent;
            border: none;
        }}
        
        .calendar-day:hover {{
            transform: translateY(-2px);
            background: rgba(255, 255, 255, 0.04);
            border-color: rgba(255, 255, 255, 0.12);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
            z-index: 10;
        }}
        
        .day-num {{
            font-weight: 700;
            font-size: 1.15rem;
            color: var(--text-secondary);
            font-family: 'Outfit', sans-serif;
        }}
        
        .calendar-day:hover .day-num {{
            color: var(--text-primary);
        }}
        
        .day-vans-status {{
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}
        
        .van-mini-bar {{
            height: 20px;
            border-radius: 6px;
            font-size: 0.68rem;
            font-weight: 800;
            display: flex;
            align-items: center;
            padding: 0 0.45rem;
            justify-content: space-between;
        }}
        
        .van-mini-bar.avail {{
            background: var(--color-avail-bg);
            border: 1px solid var(--color-avail-border);
            color: var(--color-avail);
        }}
        
        .van-mini-bar.res {{
            background: var(--color-res-bg);
            border: 1px solid var(--color-res-border);
            color: var(--color-res);
        }}
        
        .van-mini-bar.unavail {{
            background: var(--color-unavail-bg);
            border: 1px solid var(--color-unavail-border);
            color: var(--color-unavail);
        }}
        
        .van-lbl-long {{
            display: inline;
        }}
        
        .van-lbl-short {{
            display: none;
        }}
        
        .van-price-lbl {{
            display: inline;
        }}
        
        /* Table controls */
        .table-filters {{
            display: flex;
            gap: 0.75rem;
            margin-bottom: 1.5rem;
        }}
        
        .search-input {{
            flex: 1;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--glass-border);
            color: var(--text-primary);
            padding: 0.7rem 1.4rem;
            border-radius: 14px;
            font-family: inherit;
            outline: none;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            font-size: 0.88rem;
        }}
        
        .search-input:focus {{
            border-color: #0a84ff;
            background: rgba(255, 255, 255, 0.04);
            box-shadow: 0 0 0 3px rgba(10, 132, 255, 0.15);
        }}
        
        .table-wrapper {{
            overflow-x: auto;
            border-radius: 18px;
            border: 1px solid var(--glass-border);
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.88rem;
        }}
        
        th {{
            background: rgba(20, 20, 25, 0.75);
            padding: 1.1rem;
            font-weight: 700;
            color: var(--text-secondary);
            border-bottom: 1px solid var(--glass-border);
        }}
        
        td {{
            padding: 1.1rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.02);
        }}
        
        tr:last-child td {{
            border-bottom: none;
        }}
        
        tr:hover td {{
            background: rgba(255, 255, 255, 0.015);
        }}
        
        .badge-status {{
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.3rem 0.8rem;
            border-radius: 8px;
            font-size: 0.78rem;
            font-weight: 700;
        }}
        
        .badge-status.avail {{
            background: var(--color-avail-bg);
            border: 1px solid var(--color-avail-border);
            color: var(--color-avail);
        }}
        .badge-status.res {{
            background: var(--color-res-bg);
            border: 1px solid var(--color-res-border);
            color: var(--color-res);
        }}
        .badge-status.unavail {{
            background: var(--color-unavail-bg);
            border: 1px solid var(--color-unavail-border);
            color: var(--color-unavail);
        }}
        
        .badge-trip {{
            display: inline-flex;
            align-items: center;
            padding: 0.3rem 0.8rem;
            border-radius: 8px;
            font-size: 0.78rem;
            font-weight: 700;
            border: 1px solid transparent;
        }}
        .badge-trip.past {{
            background: rgba(142, 142, 147, 0.08);
            border-color: rgba(142, 142, 147, 0.2);
            color: #8e8e93;
        }}
        .badge-trip.active {{
            background: rgba(48, 209, 88, 0.1);
            border-color: rgba(48, 209, 88, 0.25);
            color: #30d158;
        }}
        .badge-trip.future {{
            background: rgba(10, 132, 255, 0.1);
            border-color: rgba(10, 132, 255, 0.25);
            color: #0a84ff;
        }}
        
        .van-column {{ font-weight: 700; }}
        .van-column.van1 {{ color: var(--van1-color); }}
        .van-column.van2 {{ color: var(--van2-color); }}
        .van-column.van3 {{ color: var(--van3-color); }}
        
        .price-column {{
            font-weight: 700;
            font-family: 'Outfit', sans-serif;
            color: var(--text-primary);
        }}
        
        .legend-block {{
            display: flex;
            gap: 1.5rem;
            margin-top: 1.5rem;
            justify-content: center;
            font-size: 0.85rem;
            color: var(--text-secondary);
            font-weight: 600;
        }}
        
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .legend-color {{
            width: 12px;
            height: 12px;
            border-radius: 4px;
        }}
        .legend-color.avail {{ background-color: var(--color-avail); }}
        .legend-color.res {{ background-color: var(--color-res); }}
        .legend-color.unavail {{ background-color: var(--color-unavail); }}
        
        /* New Shop & Audit Grid Layout */
        .shop-dashboard {{
            display: grid;
            grid-template-columns: 3fr 2fr;
            gap: 1.5rem;
        }}
        @media (max-width: 1100px) {{
            .shop-dashboard {{
                grid-template-columns: 1fr;
            }}
        }}
        
        .product-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
            gap: 1rem;
        }}
        
        .product-card {{
            background: rgba(255, 255, 255, 0.01);
            border: 1px solid rgba(255, 255, 255, 0.03);
            border-radius: 18px;
            padding: 1.25rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }}
        
        .product-card:hover {{
            background: rgba(255, 255, 255, 0.03);
            border-color: rgba(255, 255, 255, 0.1);
            transform: translateY(-2px);
        }}
        
        .product-name {{
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            font-size: 0.95rem;
            color: var(--text-primary);
            margin-bottom: 0.5rem;
            line-height: 1.3;
        }}
        
        .product-meta {{
            color: var(--text-secondary);
            font-size: 0.75rem;
            margin-bottom: 1rem;
        }}
        
        .product-footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .product-price {{
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            font-size: 1.15rem;
            color: #ff9f0a;
        }}
        
        .btn-buy {{
            background: rgba(10, 132, 255, 0.12);
            border: 1px solid rgba(10, 132, 255, 0.25);
            color: #0a84ff;
            padding: 0.4rem 0.8rem;
            border-radius: 8px;
            font-size: 0.75rem;
            font-weight: 700;
            text-decoration: none;
            transition: all 0.2s ease;
        }}
        
        .btn-buy:hover {{
            background: #0a84ff;
            color: #fff;
        }}
        
        /* Contact and Security List */
        .info-list {{
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
        }}
        
        .info-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.03);
            padding-bottom: 0.75rem;
        }}
        
        .info-row:last-child {{
            border-bottom: none;
        }}
        
        .info-label {{
            font-size: 0.85rem;
            color: var(--text-secondary);
            font-weight: 500;
        }}
        
        .info-val {{
            font-size: 0.9rem;
            font-weight: 700;
            font-family: 'Outfit', sans-serif;
        }}
        
        /* Security Indicator Badge */
        .security-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.25rem 0.65rem;
            border-radius: 6px;
            font-size: 0.72rem;
            font-weight: 700;
        }}
        .security-badge.ok {{
            background: rgba(48, 209, 88, 0.1);
            color: #30d158;
            border: 1px solid rgba(48, 209, 88, 0.2);
        }}
        .security-badge.warn {{
            background: rgba(255, 159, 10, 0.1);
            color: #ff9f0a;
            border: 1px solid rgba(255, 159, 10, 0.2);
        }}
        
        @keyframes spin {{
            from {{ transform: rotate(0deg); }}
            to {{ transform: rotate(360deg); }}
        }}
        
        /* Mobile layout styling */
        @media (max-width: 768px) {{
            body {{
                padding: 0.75rem;
            }}
            header {{
                flex-direction: column;
                align-items: flex-start;
                gap: 1rem;
                margin-bottom: 1.5rem;
            }}
            .header-title h1 {{
                font-size: 1.85rem;
            }}
            .header-controls {{
                flex-direction: column;
                width: 100%;
                gap: 0.75rem;
            }}
            .header-controls select,
            .header-controls button,
            .header-controls a {{
                width: 100%;
                justify-content: center;
                text-align: center;
            }}
            .tabs {{
                display: flex;
                overflow-x: auto;
                white-space: nowrap;
                width: 100%;
                padding: 4px;
                border-radius: 14px;
                margin-bottom: 1.5rem;
                gap: 4px;
                -webkit-overflow-scrolling: touch;
            }}
            .tabs::-webkit-scrollbar {{
                display: none; /* Hide scrollbar for clean native look */
            }}
            .tab-btn {{
                flex: 0 0 auto;
                padding: 0.5rem 1rem;
                font-size: 0.82rem;
            }}
            .stats-grid {{
                grid-template-columns: 1fr;
                gap: 0.75rem;
                margin-bottom: 1.5rem;
            }}
            .stat-card {{
                padding: 1.25rem;
            }}
            .stat-value {{
                font-size: 1.85rem;
            }}
            .chart-card, .section-card {{
                padding: 1rem;
                margin-bottom: 1.25rem;
            }}
            .card-title-container {{
                flex-direction: column;
                align-items: flex-start;
                gap: 0.75rem;
            }}
            .calendar-grid {{
                gap: 4px;
            }}
            .weekday-label {{
                font-size: 0.7rem;
            }}
            .calendar-day {{
                aspect-ratio: 1 / 1.1;
                padding: 0.35rem 0.2rem;
                border-radius: 10px;
                justify-content: flex-start;
                align-items: center;
                gap: 2px;
            }}
            .day-num {{
                font-size: 0.85rem;
            }}
            .day-vans-status {{
                flex-direction: row;
                justify-content: center;
                gap: 3px;
                width: 100%;
                margin-top: 2px;
            }}
            .van-mini-bar {{
                padding: 2px 0;
                font-size: 0.52rem;
                font-weight: 800;
                border-radius: 4px;
                line-height: 1;
                height: auto;
                flex: 1;
                display: inline-flex;
                justify-content: center;
                align-items: center;
                border: none;
            }}
            .van-lbl-long {{
                display: none !important;
            }}
            .van-lbl-short {{
                display: inline !important;
                color: #fff !important;
            }}
            .van-price-lbl {{
                display: none !important;
            }}
            .van-mini-bar.avail {{
                background-color: var(--color-avail) !important;
            }}
            .van-mini-bar.res {{
                background-color: var(--color-res) !important;
            }}
            .van-mini-bar.unavail {{
                background-color: var(--color-unavail) !important;
            }}
            .legend-block {{
                flex-wrap: wrap;
                gap: 0.65rem;
                font-size: 0.75rem;
            }}
            .table-filters {{
                flex-direction: column;
                gap: 0.5rem;
            }}
            .shop-dashboard {{
                grid-template-columns: 1fr;
                gap: 1.25rem;
            }}
        }}
    </style>
</head>
<body>
    <!-- Background Blur Blobs -->
    <div class="blur-blob blob-1"></div>
    <div class="blur-blob blob-2"></div>
    <div class="blur-blob blob-3"></div>

    <div class="container">
        <header>
            <div class="header-title">
                <h1>Ze-Van Analytics & Réservations</h1>
                <p>Analyse approfondie du Chiffre d'Affaires et des disponibilités des vans</p>
            </div>
            
            <div class="header-controls">
                <!-- Refresh Data Trigger -->
                <button onclick="triggerBackendRefresh()" id="btn-refresh" class="btn-link" style="background: rgba(48, 209, 88, 0.15); border-color: var(--color-avail-border); color: var(--color-avail); cursor: pointer;">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" id="refresh-icon"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"></path></svg>
                    <span id="refresh-text">Actualiser les prix</span>
                </button>

                <!-- Global Year Filter -->
                <select id="select-year-filter" onchange="applyGlobalYearFilter()">
                    <option value="all">Toutes les années</option>
                    <option value="2024">Année 2024</option>
                    <option value="2025">Année 2025</option>
                    <option value="2026" selected>Année 2026</option>
                    <option value="2027">Année 2027</option>
                </select>
                
                <a href="https://www.ze-van.fr/" target="_blank" class="btn-link">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line></svg>
                    Visiter Ze-Van
                </a>
            </div>
        </header>

        <!-- Navigation Tabs -->
        <div class="tabs">
            <button class="tab-btn active" onclick="switchTab('analytics-tab')">Analytique & CA</button>
            <button class="tab-btn" onclick="switchTab('calendar-tab')">Planning Mensuel</button>
            <button class="tab-btn" onclick="switchTab('bookings-tab')">Liste des Réservations</button>
            <button class="tab-btn" onclick="switchTab('raw-data-tab')">Base de Données Brute</button>
            <button class="tab-btn" onclick="switchTab('shop-info-tab')">Boutique & Infos API</button>
        </div>

        <!-- 1. ANALYTICS & CA TAB -->
        <div id="analytics-tab" class="tab-content active">
            <!-- Stats KPI Cards -->
            <div class="stats-grid">
                <div class="stat-card glass-card">
                    <div class="stat-header">
                        <span>Chiffre d'Affaires Estimé (CA)</span>
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--color-avail)" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                    </div>
                    <div class="stat-value green" id="kpi-revenue">0 €</div>
                    <div class="stat-footer">CA cumulé des jours réservés</div>
                </div>
                
                <div class="stat-card glass-card">
                    <div class="stat-header">
                        <span>Taux d'Occupation Moyen</span>
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--van1-color)" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                    </div>
                    <div class="stat-value" id="kpi-occupancy">0 %</div>
                    <div class="stat-footer">Jours réservés / Total jours</div>
                </div>
                
                <div class="stat-card glass-card">
                    <div class="stat-header">
                        <span>Jours Totalement Réservés</span>
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--van2-color)" stroke-width="2.5"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
                    </div>
                    <div class="stat-value" id="kpi-booked-days">0 j</div>
                    <div class="stat-footer">Nombre cumulé de jours de location</div>
                </div>
                
                <div class="stat-card glass-card">
                    <div class="stat-header">
                        <span>Prix Moyen Journalier (ADR)</span>
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--van3-color)" stroke-width="2.5"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path></svg>
                    </div>
                    <div class="stat-value" id="kpi-adr">0 €</div>
                    <div class="stat-footer">Moyenne pondérée du tarif journalier</div>
                </div>
            </div>

            <!-- Charts Section -->
            <div class="analytics-dashboard">
                <div class="chart-card glass-card">
                    <div class="chart-title">Évolution Mensuelle du Chiffre d'Affaires</div>
                    <div style="position: relative; height: 320px; width: 100%;">
                        <canvas id="monthly-revenue-chart"></canvas>
                    </div>
                </div>
                
                <div class="chart-card glass-card">
                    <div class="chart-title">Comparatif de Performance des Vans</div>
                    <div class="van-comparison-list" id="van-comparison-container">
                        <!-- Injected dynamically -->
                    </div>
                </div>
            </div>

            <!-- Double Charts Section (Occupancy & Seasonality) -->
            <div class="analytics-dashboard">
                <div class="chart-card glass-card" style="grid-column: span 2;">
                    <div class="chart-title">Saisonnalité : Taux d'Occupation Mensuel (%)</div>
                    <div style="position: relative; height: 300px; width: 100%;">
                        <canvas id="monthly-occupancy-chart"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <!-- 2. MONTHLY PLANNING TAB -->
        <div id="calendar-tab" class="tab-content">
            <div class="section-card glass-card">
                <div class="card-title-container">
                    <span class="card-title">Calendrier des Disponibilités Croisées</span>
                    <div class="calendar-controls">
                        <select id="select-month" onchange="renderCalendar()">
                            <option value="1">Janvier</option>
                            <option value="2">Février</option>
                            <option value="3">Mars</option>
                            <option value="4">Avril</option>
                            <option value="5">Mai</option>
                            <option value="6">Juin</option>
                            <option value="7">Juillet</option>
                            <option value="8">Août</option>
                            <option value="9">Septembre</option>
                            <option value="10">Octobre</option>
                            <option value="11">Novembre</option>
                            <option value="12">Décembre</option>
                        </select>
                        <select id="select-year" onchange="renderCalendar()">
                            <option value="2024">2024</option>
                            <option value="2025">2025</option>
                            <option value="2026" selected>2026</option>
                            <option value="2027">2027</option>
                        </select>
                    </div>
                </div>

                <div class="calendar-grid">
                    <div class="weekday-label">Lun</div>
                    <div class="weekday-label">Mar</div>
                    <div class="weekday-label">Mer</div>
                    <div class="weekday-label">Jeu</div>
                    <div class="weekday-label">Ven</div>
                    <div class="weekday-label">Sam</div>
                    <div class="weekday-label">Dim</div>
                </div>
                
                <div class="calendar-grid" id="calendar-days-container">
                    <!-- Day cells inject -->
                </div>
                
                <div class="legend-block">
                    <div class="legend-item">
                        <div class="legend-color avail"></div>
                        <span>Disponible</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-color res"></div>
                        <span>Réservé</span>
                    </div>
                    <div class="legend-item">
                        <div class="legend-color unavail"></div>
                        <span>Indisponible</span>
                    </div>
                </div>
            </div>
        </div>

        <!-- 3. LIST OF BOOKINGS TAB -->
        <div id="bookings-tab" class="tab-content">
            <div class="section-card glass-card">
                <div class="card-title-container">
                    <span class="card-title">Séjours & Réservations Détectés</span>
                </div>
                
                <div class="table-filters">
                    <input type="text" id="booking-search-input" class="search-input" placeholder="Rechercher par van..." onkeyup="filterBookingsTable()">
                    <select id="filter-booking-status" onchange="filterBookingsTable()">
                        <option value="">Tous les statuts de trip</option>
                        <option value="En cours">En cours</option>
                        <option value="À venir">À venir</option>
                        <option value="Passée">Passée</option>
                    </select>
                </div>
                
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Van</th>
                                <th>Date Début</th>
                                <th>Date Fin</th>
                                <th>Durée</th>
                                <th>Revenu Estimé</th>
                                <th>Statut Temporel</th>
                            </tr>
                        </thead>
                        <tbody id="bookings-table-body">
                            <!-- Injected dynamically -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- 4. RAW DATABASE TAB -->
        <div id="raw-data-tab" class="tab-content">
            <div class="section-card glass-card">
                <div class="card-title-container">
                    <span class="card-title">Base de Données Journalière</span>
                </div>
                
                <div class="table-filters">
                    <input type="text" id="raw-search-input" class="search-input" placeholder="Filtrer par date (ex: 2026-08) ou van..." onkeyup="filterRawTable()">
                    <select id="filter-raw-status" onchange="filterRawTable()">
                        <option value="">Tous les statuts</option>
                        <option value="Disponible">Disponible</option>
                        <option value="Réservé">Réservé</option>
                        <option value="Indisponible">Indisponible</option>
                    </select>
                </div>
                
                <div class="table-wrapper">
                    <table>
                        <thead>
                            <tr>
                                <th>Van</th>
                                <th>Date</th>
                                <th>Prix Journalier</th>
                                <th>Statut de la Date</th>
                            </tr>
                        </thead>
                        <tbody id="raw-table-body">
                            <!-- Rows inject -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- 5. SHOP & SECURITY AUDIT TAB -->
        <div id="shop-info-tab" class="tab-content">
            <div class="shop-dashboard">
                <!-- Left Column: WooCommerce Products -->
                <div class="section-card glass-card">
                    <div class="chart-title">Produits & Guides Boutique WooCommerce</div>
                    <div class="product-grid">
                        <div class="product-card">
                            <span class="product-name">Carte Cadeau Ze-Van</span>
                            <span class="product-meta">ID: 2530 | Montant au choix (50€ à 500€)</span>
                            <div class="product-footer">
                                <span class="product-price" style="font-size: 0.95rem;">50.00 € – 500.00 €</span>
                                <a href="https://www.ze-van.fr/produit/carte-cadeau-location-van-amenage/" target="_blank" class="btn-buy">Acheter</a>
                            </div>
                        </div>
                        
                        <div class="product-card">
                            <span class="product-name">Guide Road Trip 10j Bretagne</span>
                            <span class="product-meta">ID: 6328 | Format PDF Interactif</span>
                            <div class="product-footer">
                                <span class="product-price">39.00 €</span>
                                <a href="https://www.ze-van.fr/produit/guide-road-trip-10-jours-van-bretagne/" target="_blank" class="btn-buy">Télécharger</a>
                            </div>
                        </div>
                        
                        <div class="product-card">
                            <span class="product-name">Guide Road Trip 3j Auvergne</span>
                            <span class="product-meta">ID: 5199 | Format PDF Interactif</span>
                            <div class="product-footer">
                                <span class="product-price">29.00 €</span>
                                <a href="https://www.ze-van.fr/produit/guide-road-trip-de-3-jours-en-van-en-auvergne/" target="_blank" class="btn-buy">Télécharger</a>
                            </div>
                        </div>

                        <div class="product-card">
                            <span class="product-name">Guide Road Trip 3j Lac du Bourget</span>
                            <span class="product-meta">ID: 5099 | Format PDF Interactif</span>
                            <div class="product-footer">
                                <span class="product-price">29.00 €</span>
                                <a href="https://www.ze-van.fr/produit/guide-road-trip-de-3-jours-en-van-au-lac-du-bourget/" target="_blank" class="btn-buy">Télécharger</a>
                            </div>
                        </div>

                        <div class="product-card">
                            <span class="product-name">T-shirt Officiel Ze-Van</span>
                            <span class="product-meta">ID: 6735 | Textile Coton Bio</span>
                            <div class="product-footer">
                                <span class="product-price">29.00 €</span>
                                <a href="https://www.ze-van.fr/produit/t-shirt-ze-van/" target="_blank" class="btn-buy">Acheter</a>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Right Column: OSINT & Security -->
                <div style="display: flex; flex-direction: column; gap: 1.5rem;">
                    <!-- Contact Cards -->
                    <div class="section-card glass-card" style="margin-bottom: 0;">
                        <div class="chart-title">Contacts Découverts (API)</div>
                        <div class="info-list">
                            <div class="info-row">
                                <span class="info-label">Email Officiel</span>
                                <span class="info-val" style="color: #0a84ff">hello@ze-van.fr</span>
                            </div>
                            <div class="info-row">
                                <span class="info-label">Mobile Gérance</span>
                                <span class="info-val">06 88 06 63 37</span>
                            </div>
                            <div class="info-row">
                                <span class="info-label">Fixe Agence</span>
                                <span class="info-val">04 34 64 97 33</span>
                            </div>
                            <div class="info-row">
                                <span class="info-label">Concepteur Web</span>
                                <span class="info-val" style="color: #bf5af2">contact@nicolafay.com</span>
                            </div>
                        </div>
                    </div>

                    <!-- Calendar Sync -->
                    <div class="section-card glass-card" style="margin-bottom: 0;">
                        <div class="chart-title">Synchronisation Google Calendar</div>
                        <p style="font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 1rem; line-height: 1.4;">
                            Abonnez-vous à vos réservations en temps réel depuis Google Calendar, Apple Calendar ou Outlook.
                        </p>
                        <div class="info-list">
                            <div class="info-row" style="flex-direction: column; align-items: flex-start; gap: 0.5rem; border-bottom: none; padding-bottom: 0;">
                                <span class="info-label">Lien du flux iCal (cliquez pour sélectionner) :</span>
                                <input type="text" id="ical-url-input" class="search-input" readonly style="width: 100%; font-size: 0.72rem; padding: 0.5rem 0.8rem; background: rgba(0,0,0,0.2);" onclick="this.select()" value="Chargement du flux...">
                            </div>
                        </div>
                    </div>

                    <!-- Security Cards -->
                    <div class="section-card glass-card" style="margin-bottom: 0;">
                        <div class="chart-title">Statut d'Audit de Sécurité</div>
                        <div class="info-list">
                            <div class="info-row">
                                <span class="info-label">WordPress XML-RPC</span>
                                <span class="security-badge ok">Désactivé (Sécurisé)</span>
                            </div>
                            <div class="info-row">
                                <span class="info-label">Dépôt Git (.git)</span>
                                <span class="security-badge ok">Bloqué (403/404)</span>
                            </div>
                            <div class="info-row">
                                <span class="info-label">Variable Envs (.env)</span>
                                <span class="security-badge ok">Bloqué (403/404)</span>
                            </div>
                            <div class="info-row">
                                <span class="info-label">WP-Config Backups</span>
                                <span class="security-badge ok">Protégé</span>
                            </div>
                            <div class="info-row">
                                <span class="info-label">API Configurations (SEOPress)</span>
                                <span class="security-badge ok">Auth Requise (401)</span>
                            </div>
                            <div class="info-row">
                                <span class="info-label">API Écriture POS (wc/pos)</span>
                                <span class="security-badge ok">Auth Requise (401)</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Data Injection & Analytical Javascript -->
    <script>
        let records = {records_json};
        
        // System date is 2026-07-02
        const SYSTEM_DATE = new Date("2026-07-02T12:00:00");
        
        const vanColors = {{
            "T7 California Beach Nomade": "#0a84ff",
            "T6.1 California Beach Camper": "#ff9f0a",
            "T7 California Beach Routard": "#bf5af2"
        }};
        
        const vanInitials = {{
            "T7 California Beach Nomade": "Nomade",
            "T6.1 California Beach Camper": "Camper",
            "T7 California Beach Routard": "Routard"
        }};
        
        const vanShortNames = {{
            "T7 California Beach Nomade": "No",
            "T6.1 California Beach Camper": "Ca",
            "T7 California Beach Routard": "Ro"
        }};
        
        const orderedVans = [
            "T6.1 California Beach Camper",
            "T7 California Beach Nomade",
            "T7 California Beach Routard"
        ];
        
        let revenueChart = null;
        let occupancyChart = null;
        let detectedBookings = [];
        let refreshing = false;

        document.addEventListener("DOMContentLoaded", () => {{
            // Check if hosted or local file
            if (window.location.protocol.startsWith('http')) {{
                const icalInput = document.getElementById("ical-url-input");
                if (icalInput) {{
                    icalInput.value = window.location.origin + "/api/calendar.ics";
                }}

                // Fetch dynamic data from the server
                fetch('/api/data')
                    .then(res => res.json())
                    .then(data => {{
                        if (data && data.length > 0) {{
                            records = data;
                            detectBookingsFromDailyRecords();
                            applyGlobalYearFilter();
                            renderCalendar();
                            populateRawTable();
                            populateBookingsTable();
                        }}
                    }})
                    .catch(err => console.log("Static data fallback:", err));
            }} else {{
                // Local file: hide server refresh button since there's no server backend
                const btn = document.getElementById("btn-refresh");
                if (btn) btn.style.display = "none";
                const icalInput = document.getElementById("ical-url-input");
                if (icalInput) {{
                    icalInput.value = "Disponible après déploiement sur Render";
                }}
            }}

            detectBookingsFromDailyRecords();
            
            document.getElementById("select-year-filter").value = "2026";
            document.getElementById("select-month").value = "7";
            document.getElementById("select-year").value = "2026";
            
            applyGlobalYearFilter();
            renderCalendar();
            populateRawTable();
            populateBookingsTable();
        }});

        function triggerBackendRefresh() {{
            if (refreshing) return;
            refreshing = true;
            
            const text = document.getElementById("refresh-text");
            const icon = document.getElementById("refresh-icon");
            if (text) text.textContent = "Mise à jour...";
            if (icon) icon.style.animation = "spin 1.5s linear infinite";
            
            fetch('/api/refresh', {{ method: 'POST' }})
                .then(res => res.json())
                .then(data => {{
                    // Poll refresh status
                    pollRefreshStatus();
                }})
                .catch(err => {{
                    console.error("Refresh trigger error:", err);
                    resetRefreshState();
                }});
        }}
        
        function pollRefreshStatus() {{
            const interval = setInterval(() => {{
                fetch('/api/refresh-status')
                    .then(res => res.json())
                    .then(status => {{
                        if (status.status === 'idle') {{
                            clearInterval(interval);
                            // Refresh page to load new data
                            location.reload();
                        }} else if (status.status === 'error') {{
                            clearInterval(interval);
                            alert("Erreur lors de la mise à jour des données depuis le site.");
                            resetRefreshState();
                        }}
                    }})
                    .catch(err => {{
                        clearInterval(interval);
                        resetRefreshState();
                    }});
            }}, 2000);
        }}
        
        function resetRefreshState() {{
            refreshing = false;
            const text = document.getElementById("refresh-text");
            const icon = document.getElementById("refresh-icon");
            if (text) text.textContent = "Actualiser les prix";
            if (icon) icon.style.animation = "none";
        }}

        function switchTab(tabId) {{
            const contents = document.querySelectorAll(".tab-content");
            contents.forEach(c => c.classList.remove("active"));
            
            const buttons = document.querySelectorAll(".tab-btn");
            buttons.forEach(b => b.classList.remove("active"));
            
            document.getElementById(tabId).classList.add("active");
            event.target.classList.add("active");
        }}

        function detectBookingsFromDailyRecords() {{
            detectedBookings = [];
            
            orderedVans.forEach(vanName => {{
                const vanReservations = records
                    .filter(r => r.van === vanName && r.status === "Réservé")
                    .sort((a, b) => new Date(a.date) - new Date(b.date));
                
                if (vanReservations.length === 0) return;
                
                let currentBooking = null;
                
                vanReservations.forEach(r => {{
                    const recordDate = new Date(r.date);
                    
                    if (!currentBooking) {{
                        currentBooking = {{
                            van: vanName,
                            startDate: r.date,
                            endDate: r.date,
                            days: 1,
                            revenue: r.price,
                            details: [r]
                        }};
                    }} else {{
                        const prevEnd = new Date(currentBooking.endDate);
                        const diffTime = Math.abs(recordDate - prevEnd);
                        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
                        
                        if (diffDays <= 1) {{
                            currentBooking.endDate = r.date;
                            currentBooking.days += 1;
                            currentBooking.revenue += r.price;
                            currentBooking.details.push(r);
                        }} else {{
                            detectedBookings.push(currentBooking);
                            currentBooking = {{
                                van: vanName,
                                startDate: r.date,
                                endDate: r.date,
                                days: 1,
                                revenue: r.price,
                                details: [r]
                            }};
                        }}
                    }}
                }});
                
                if (currentBooking) {{
                    detectedBookings.push(currentBooking);
                }}
            }});
        }}

        function applyGlobalYearFilter() {{
            const selectedYear = document.getElementById("select-year-filter").value;
            
            let filteredRecords = records;
            if (selectedYear !== "all") {{
                const yearInt = parseInt(selectedYear);
                filteredRecords = records.filter(r => r.year === yearInt);
            }}
            
            const totalDays = filteredRecords.length;
            const reservedRecords = filteredRecords.filter(r => r.status === "Réservé");
            const totalBookedDays = reservedRecords.length;
            
            const totalRevenue = reservedRecords.reduce((sum, r) => sum + r.price, 0);
            const occupancyRate = totalDays > 0 ? (totalBookedDays / totalDays * 100) : 0;
            const adr = totalBookedDays > 0 ? (totalRevenue / totalBookedDays) : 0;
            
            document.getElementById("kpi-revenue").textContent = `${{totalRevenue.toLocaleString('fr-FR')}} €`;
            document.getElementById("kpi-occupancy").textContent = `${{occupancyRate.toFixed(1)}} %`;
            document.getElementById("kpi-booked-days").textContent = `${{totalBookedDays}} j`;
            document.getElementById("kpi-adr").textContent = `${{adr.toFixed(1)}} €`;
            
            renderVanPerformanceCards(filteredRecords);
            renderCharts(selectedYear);
        }}

        function renderVanPerformanceCards(filteredRecords) {{
            const container = document.getElementById("van-comparison-container");
            container.innerHTML = "";
            
            const vanClasses = {{
                "T7 California Beach Nomade": "van-1",
                "T6.1 California Beach Camper": "van-2",
                "T7 California Beach Routard": "van-3"
            }};
            
            orderedVans.forEach(van => {{
                const vanRecords = filteredRecords.filter(r => r.van === van);
                const total = vanRecords.length;
                const reserved = vanRecords.filter(r => r.status === "Réservé");
                const bookedCount = reserved.length;
                
                const revenue = reserved.reduce((sum, r) => sum + r.price, 0);
                const occupancy = total > 0 ? (bookedCount / total * 100) : 0;
                
                const initials = vanInitials[van] || "Van";
                const dotClass = van === "T7 California Beach Nomade" ? "van1" : (van === "T6.1 California Beach Camper" ? "van2" : "van3");
                
                container.innerHTML += `
                    <div class="van-comp-item ${{van === "T7 California Beach Nomade" ? 'van1' : (van === "T6.1 California Beach Camper" ? 'van2' : 'van3')}}">
                        <div class="van-comp-header">
                            <span class="van-comp-name">
                                <span class="van-comp-dot ${{dotClass}}"></span>
                                ${{van}}
                            </span>
                            <span class="van-comp-revenue">${{revenue.toLocaleString('fr-FR')}} €</span>
                        </div>
                        <div class="van-comp-metrics">
                            <span>Occ. : <strong>${{occupancy.toFixed(1)}}%</strong></span>
                            <span>Jours : <strong>${{bookedCount}} j</strong></span>
                        </div>
                        <div class="van-comp-progress">
                            <div class="van-comp-fill" style="width: ${{occupancy}}%"></div>
                        </div>
                    </div>
                `;
            }});
        }}

        function renderCharts(selectedYear) {{
            const monthsNames = ["Jan", "Fév", "Mar", "Avr", "Mai", "Jui", "Jul", "Aoû", "Sep", "Oct", "Nov", "Déc"];
            
            const vanRevenueData = {{}};
            const vanOccupancyData = {{}};
            
            orderedVans.forEach(van => {{
                vanRevenueData[van] = Array(12).fill(0);
                vanOccupancyData[van] = Array(12).fill(0);
                
                const totalDaysPerMonth = Array(12).fill(0);
                const bookedDaysPerMonth = Array(12).fill(0);
                
                let recordsToChart = records.filter(r => r.van === van);
                if (selectedYear !== "all") {{
                    const y = parseInt(selectedYear);
                    recordsToChart = recordsToChart.filter(r => r.year === y);
                }}
                
                recordsToChart.forEach(r => {{
                    const mIdx = r.month - 1;
                    totalDaysPerMonth[mIdx] += 1;
                    if (r.status === "Réservé") {{
                        vanRevenueData[van][mIdx] += r.price;
                        bookedDaysPerMonth[mIdx] += 1;
                    }}
                }});
                
                for (let i = 0; i < 12; i++) {{
                    vanOccupancyData[van][i] = totalDaysPerMonth[i] > 0 ? (bookedDaysPerMonth[i] / totalDaysPerMonth[i] * 100) : 0;
                }}
            }});
            
            if (revenueChart) revenueChart.destroy();
            if (occupancyChart) occupancyChart.destroy();
            
            const ctxRevenue = document.getElementById("monthly-revenue-chart").getContext("2d");
            revenueChart = new Chart(ctxRevenue, {{
                type: 'bar',
                data: {{
                    labels: monthsNames,
                    datasets: [
                        {{
                            label: 'Camper T6.1',
                            data: vanRevenueData["T6.1 California Beach Camper"],
                            backgroundColor: 'rgba(255, 159, 10, 0.75)',
                            borderColor: '#ff9f0a',
                            borderWidth: 1.5,
                            borderRadius: 6
                        }},
                        {{
                            label: 'Nomade T7',
                            data: vanRevenueData["T7 California Beach Nomade"],
                            backgroundColor: 'rgba(10, 132, 255, 0.75)',
                            borderColor: '#0a84ff',
                            borderWidth: 1.5,
                            borderRadius: 6
                        }},
                        {{
                            label: 'Routard T7',
                            data: vanRevenueData["T7 California Beach Routard"],
                            backgroundColor: 'rgba(191, 90, 242, 0.75)',
                            borderColor: '#bf5af2',
                            borderWidth: 1.5,
                            borderRadius: 6
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            labels: {{ color: '#8e8e93', font: {{ family: 'Inter', weight: '600' }} }}
                        }}
                    }},
                    scales: {{
                        x: {{ grid: {{ display: false }}, ticks: {{ color: '#8e8e93' }} }},
                        y: {{ grid: {{ color: 'rgba(255,255,255,0.04)' }}, ticks: {{ color: '#8e8e93' }} }}
                    }}
                }}
            }});
            
            const ctxOccupancy = document.getElementById("monthly-occupancy-chart").getContext("2d");
            occupancyChart = new Chart(ctxOccupancy, {{
                type: 'line',
                data: {{
                    labels: monthsNames,
                    datasets: [
                        {{
                            label: 'Camper T6.1',
                            data: vanOccupancyData["T6.1 California Beach Camper"],
                            borderColor: '#ff9f0a',
                            backgroundColor: 'transparent',
                            borderWidth: 3,
                            tension: 0.3,
                            pointBackgroundColor: '#ff9f0a'
                        }},
                        {{
                            label: 'Nomade T7',
                            data: vanOccupancyData["T7 California Beach Nomade"],
                            borderColor: '#0a84ff',
                            backgroundColor: 'transparent',
                            borderWidth: 3,
                            tension: 0.3,
                            pointBackgroundColor: '#0a84ff'
                        }},
                        {{
                            label: 'Routard T7',
                            data: vanOccupancyData["T7 California Beach Routard"],
                            borderColor: '#bf5af2',
                            backgroundColor: 'transparent',
                            borderWidth: 3,
                            tension: 0.3,
                            pointBackgroundColor: '#bf5af2'
                        }}
                    ]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{
                        legend: {{
                            labels: {{ color: '#8e8e93', font: {{ family: 'Inter', weight: '600' }} }}
                        }}
                    }},
                    scales: {{
                        x: {{ grid: {{ display: false }}, ticks: {{ color: '#8e8e93' }} }},
                        y: {{ 
                            min: 0,
                            max: 100,
                            grid: {{ color: 'rgba(255,255,255,0.04)' }}, 
                            ticks: {{ 
                                color: '#8e8e93',
                                callback: function(value) {{ return value + "%" }}
                            }} 
                        }}
                    }}
                }}
            }});
        }}

        // Render Calendar
        function renderCalendar() {{
            const month = parseInt(document.getElementById("select-month").value);
            const year = parseInt(document.getElementById("select-year").value);
            const container = document.getElementById("calendar-days-container");
            container.innerHTML = "";
            
            const firstDay = new Date(year, month - 1, 1);
            let startDayOfWeek = firstDay.getDay();
            startDayOfWeek = startDayOfWeek === 0 ? 6 : startDayOfWeek - 1;
            
            const totalDays = new Date(year, month, 0).getDate();
            
            for (let i = 0; i < startDayOfWeek; i++) {{
                const emptyCell = document.createElement("div");
                emptyCell.className = "calendar-day empty";
                container.appendChild(emptyCell);
            }}
            
            for (let day = 1; day <= totalDays; day++) {{
                const dateStr = `${{year}}-${{String(month).padStart(2, '0')}}-${{String(day).padStart(2, '0')}}`;
                
                const dayCell = document.createElement("div");
                dayCell.className = "calendar-day";
                
                const dayNumSpan = document.createElement("span");
                dayNumSpan.className = "day-num";
                dayNumSpan.textContent = day;
                dayCell.appendChild(dayNumSpan);
                
                const vansStatusDiv = document.createElement("div");
                vansStatusDiv.className = "day-vans-status";
                
                const dayRecords = records.filter(r => r.date === dateStr);
                
                orderedVans.forEach(vanName => {{
                    const r = dayRecords.find(x => x.van === vanName);
                    if (r) {{
                        const bar = document.createElement("div");
                        let statusCls = "unavail";
                        let statusText = "Indisp.";
                        
                        if (r.status === "Disponible") {{
                            statusCls = "avail";
                            statusText = `${{r.price}}€`;
                        }} else if (r.status === "Réservé") {{
                            statusCls = "res";
                            statusText = "Réservé";
                        }}
                        
                        bar.className = `van-mini-bar ${{statusCls}}`;
                        bar.innerHTML = `
                            <span class="van-lbl-long">${{vanInitials[vanName] || 'Van'}}</span>
                            <span class="van-lbl-short">${{vanShortNames[vanName] || 'V'}}</span>
                            <span class="van-price-lbl">${{statusText}}</span>
                        `;
                        bar.title = `${{vanName}} - ${{r.status}} (${{r.price}}€)`;
                        vansStatusDiv.appendChild(bar);
                    }}
                }});
                
                dayCell.appendChild(vansStatusDiv);
                container.appendChild(dayCell);
            }}
        }}

        function populateBookingsTable() {{
            const tbody = document.getElementById("bookings-table-body");
            
            tbody.innerHTML = detectedBookings.map(b => {{
                const start = new Date(b.startDate);
                const end = new Date(b.endDate);
                
                let tripStatus = "À venir";
                let tripClass = "future";
                
                if (end < SYSTEM_DATE) {{
                    tripStatus = "Passée";
                    tripClass = "past";
                }} else if (start <= SYSTEM_DATE && end >= SYSTEM_DATE) {{
                    tripStatus = "En cours";
                    tripClass = "active";
                }}
                
                const vanClass = b.van === "T7 California Beach Nomade" ? "van1" : (b.van === "T6.1 California Beach Camper" ? "van2" : "van3");
                
                return `
                    <tr data-van="${{b.van}}" data-status="${{tripStatus}}">
                        <td class="van-column ${{vanClass}}">${{b.van}}</td>
                        <td>${{b.startDate}}</td>
                        <td>${{b.endDate}}</td>
                        <td>${{b.days}} jours</td>
                        <td class="price-column" style="color: var(--color-avail)">${{b.revenue.toLocaleString('fr-FR')}} €</td>
                        <td>
                            <span class="badge-trip ${{tripClass}}">
                                ${{tripStatus}}
                            </span>
                        </td>
                    </tr>
                `;
            }}).join('');
        }}

        function filterBookingsTable() {{
            const search = document.getElementById("booking-search-input").value.toLowerCase();
            const status = document.getElementById("filter-booking-status").value;
            const rows = document.querySelectorAll("#bookings-table-body tr");
            
            rows.forEach(row => {{
                const van = row.getAttribute("data-van").toLowerCase();
                const rowStatus = row.getAttribute("data-status");
                
                const matchesSearch = van.includes(search);
                const matchesStatus = status === "" || rowStatus === status;
                
                if (matchesSearch && matchesStatus) {{
                    row.style.display = "";
                }} else {{
                    row.style.display = "none";
                }}
            }});
        }}

        function populateRawTable() {{
            const tbody = document.getElementById("raw-table-body");
            tbody.innerHTML = records.map(r => {{
                let statusCls = "unavail";
                if (r.status === "Disponible") statusCls = "avail";
                else if (r.status === "Réservé") statusCls = "res";
                
                return `
                    <tr data-van="${{r.van}}" data-status="${{r.status}}" data-date="${{r.date}}">
                        <td class="van-column">${{r.van}}</td>
                        <td>${{r.date}}</td>
                        <td class="price-column">${{r.price}} €</td>
                        <td>
                            <span class="badge-status ${{statusCls}}">
                                <span class="dot-blink"></span>
                                ${{r.status}}
                            </span>
                        </td>
                    </tr>
                `;
            }}).join('');
        }}

        function filterRawTable() {{
            const searchQuery = document.getElementById("raw-search-input").value.toLowerCase();
            const statusFilter = document.getElementById("filter-raw-status").value;
            const rows = document.querySelectorAll("#raw-table-body tr");
            
            rows.forEach(row => {{
                const van = row.getAttribute("data-van").toLowerCase();
                const date = row.getAttribute("data-date").toLowerCase();
                const status = row.getAttribute("data-status");
                
                const matchesSearch = van.includes(searchQuery) || date.includes(searchQuery);
                const matchesStatus = statusFilter === "" || status === statusFilter;
                
                if (matchesSearch && matchesStatus) {{
                    row.style.display = "";
                }} else {{
                    row.style.display = "none";
                }}
            }});
        }}
    </script>
</body>
</html>
"""

with open(html_output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated complete business analytics dashboard HTML at: {os.path.abspath(html_output_path)}")
