import requests
import pandas as pd
from datetime import datetime
import re
from html import unescape
import os
import smtplib
from email.mime.text import MIMEText

# =========================================================
# CONFIG SECTION
# Change values here only
# =========================================================

# TAB OPTIONS (InvestorGain API Tabs)
# -----------------------------------
# "open"            → All active IPOs
# "closing-today"   → IPOs closing today
# "current"         → Upcoming IPOs
# "ipo"             → Mainboard IPOs only
# "close"           → Closed IPOs

TAB = "open"   # Change to "closing-today" in production later


# GMP FILTER
# -----------------------------------
# -1 → Test mode (includes ₹0 GMP)
#  0 → Production mode (only positive GMP)

GMP_FILTER = 0


# =========================================================
# EMAIL CONFIG (Loaded from GitHub Secrets)
# =========================================================

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO = os.getenv("EMAIL_TO")

# =========================================================
# BUILD DYNAMIC API URL
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
print("📡 IPO Notifier Agent Running")
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

    gmp_value = int(gmp_match.group(1)) if gmp_match else 0

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
print("📊 RAW IPO DATA")
print("====================================\n")

if df.empty:
    print("No IPOs found.\n")

# =========================================================
# FILTER LOGIC
# =========================================================

filtered_df = df[df["GMP"] > GMP_FILTER]

print("====================================")
print("🧪 FILTERED IPO DATA")
print("====================================\n")

if filtered_df.empty:
    print("No IPO matches GMP filter. No email sent.\n")
    exit()

print(filtered_df.to_string(index=False))

# =========================================================
# EMAIL BODY
# =========================================================

body = "📊 IPO Alert — GMP > 0\n\n"
body += filtered_df.to_string(index=False)

msg = MIMEText(body)
msg["Subject"] = "IPO Alert — GMP > 0"
msg["From"] = EMAIL_USER
msg["To"] = EMAIL_TO

# =========================================================
# SEND EMAIL
# =========================================================

print("\nSending email alert...\n")

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(EMAIL_USER, EMAIL_PASS)
server.send_message(msg)
server.quit()

print("Email sent successfully ✅\n")

print("====================================\n")
