import requests
import pandas as pd
from datetime import datetime
import re
from html import unescape


# =========================================================
# IPO DATA FETCH AGENT
# Returns filtered IPO dataframe
# =========================================================

def fetch_ipo_data(tab="closing-today", gmp_filter=0):

    today = datetime.now()
    month = today.month
    year = today.year

    # -----------------------------------
    # Financial Year Calculation
    # -----------------------------------
    if month >= 4:
        fy = f"{year}-{str(year+1)[-2:]}"
    else:
        fy = f"{year-1}-{str(year)[-2:]}"

    url = (
        f"https://webnodejs.investorgain.com/cloud/new/report/"
        f"data-read/331/1/{month}/{year}/{fy}/0/{tab}"
    )

    headers = {"User-Agent": "Mozilla/5.0"}

    print("\n📡 Fetching IPO Data...")
    print(f"TAB: {tab}")
    print(f"URL: {url}\n")

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    data = response.json()
    ipo_rows = data.get("reportTableData", [])

    print(f"Total IPOs fetched: {len(ipo_rows)}\n")

    parsed_data = []

    # -----------------------------------
    # Parse API Response
    # -----------------------------------
    for ipo in ipo_rows:

        name = ipo.get("~ipo_name", "N/A")
        gmp_html = ipo.get("GMP", "")

        # Clean GMP HTML
        gmp_text = unescape(gmp_html)
        gmp_text = re.sub(r'<.*?>', '', gmp_text)

        gmp_match = re.search(r'(-?\d+)', gmp_text)
        gmp_value = int(gmp_match.group(1)) if gmp_match else 0

        subscription = ipo.get("Sub", "N/A")
        close_date = ipo.get("~Srt_Close", "N/A")

        parsed_data.append([
            name,
            gmp_value,
            subscription,
            close_date
        ])

    df = pd.DataFrame(
        parsed_data,
        columns=[
            "IPO Name",
            "GMP",
            "Subscription",
            "Close Date"
        ]
    )

    # -----------------------------------
    # Apply GMP Filter
    # -----------------------------------
    filtered_df = df[df["GMP"] > gmp_filter]

    return filtered_df
