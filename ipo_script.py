import requests
import pandas as pd
from datetime import datetime
import re
from html import unescape

# =========================================================
# CONFIG SECTION (CHANGE ONLY HERE)
# =========================================================

TAB = "open"
# Options:
# "open"            → All active IPOs
# "closing-today"   → IPOs closing today
# "current"         → Upcoming IPOs
# "ipo"             → Mainboard IPOs
# "close"           → Closed IPOs

GMP_FILTER = 10
# Use:
# -1 → Test mode (include ₹0)
#  0 → Production mode (only positive GMP)

# =========================================================
# BUILD DYNAMIC URL
# =========================================================

today = datetime.now()

month = today.month
year = today.year

# Financial Year Logic
if month >= 4:
    fy = f"{year}-{str(year+1)[-2:]}"
else:
    fy = f"{year-1}-{str(year)[-2:]}"

URL = (
    f"https://webnodejs.investorgain.com/cloud/new/report/"
    f"data-read/331/1/{month}/{year}/{fy}/0/{TAB}"
)

HEADERS = {"User-Agent": "Mozilla/5.0"}

print("\n====================================")
print("📡 IPO DATA FETCHER")
print("====================================\n")

print(f"TAB MODE: {TAB}")
print(f"GMP FILTER: > {GMP_FILTER}")
print("URL:", URL, "\n")

# =========================================================
# FETCH API DATA
# =========================================================

response = requests.get(URL, headers=HEADERS)
response.raise_for_status()

data = response.json()
ipo_rows = data.get("reportTableData", [])

print(f"Total IPOs fetched: {len(ipo_rows)}\n")

# =========================================================
# PARSE DATA
# =========================================================

parsed_data = []

for ipo in ipo_rows:

    name = ipo.get("~ipo_name", "N/A")
    gmp_html = ipo.get("GMP", "")

    # Decode HTML entities
    gmp_text = unescape(gmp_html)

    # Remove HTML tags
    gmp_text = re.sub(r'<.*?>', '', gmp_text)

    # Extract numeric GMP
    gmp_match = re.search(r'(-?\d+)', gmp_text)

    if gmp_match:
        gmp_value = int(gmp_match.group(1))
    else:
        gmp_value = 0

    subscription = ipo.get("Sub", "N/A")
    close_date = ipo.get("~Srt_Close", "N/A")

    parsed_data.append([
        name,
        gmp_value,
        subscription,
        close_date
    ])

# =========================================================
# DATAFRAME
# =========================================================

df = pd.DataFrame(
    parsed_data,
    columns=[
        "IPO Name",
        "GMP",
        "Subscription",
        "Close Date"
    ]
)

print("====================================")
print("📊 RAW DATA")
print("====================================\n")

if df.empty:
    print("No IPOs found.\n")
else:
    print(df.to_string(index=False))

# =========================================================
# FILTER LOGIC
# =========================================================

filtered_df = df[df["GMP"] > GMP_FILTER]

print("\n====================================")
print("🧪 FILTERED DATA")
print("====================================\n")

if filtered_df.empty:
    print("No IPOs match GMP filter.\n")
else:
    print(filtered_df.to_string(index=False))
    print("\nTotal Matching IPOs:", len(filtered_df))

print("\n====================================\n")
