import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from datetime import datetime
import os
import json


# =========================================================
# LOAD GOOGLE SERVICE ACCOUNT CREDENTIALS
# =========================================================

def load_credentials():

    creds_json = os.getenv("GOOGLE_CREDS_JSON")

    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.readonly"
    ]

    # GitHub mode
    if creds_json:
        creds_dict = json.loads(creds_json)

        creds = Credentials.from_service_account_info(
            creds_dict,
            scopes=scope
        )

        return creds

    # Local mode fallback
    else:
        print("Using local credentials.json")

        creds = Credentials.from_service_account_file(
            "credentials.json",
            scopes=scope
        )

        return creds


# =========================================================
# FETCH TODAY REMINDERS
# Supports One-Time + Monthly
# =========================================================

def fetch_today_reminders():

    print("\n📌 Fetching Reminders...")

    creds = load_credentials()
    client = gspread.authorize(creds)

    # Change sheet name if different
    sheet = client.open("Reminder Agent").sheet1

    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    if df.empty:
        print("No reminders found in sheet.\n")
        return df

    # -----------------------------------
    # Today's Date Values
    # -----------------------------------
    today_date_str = datetime.now().strftime("%d-%b-%Y")
    today_day = datetime.now().day

    # -----------------------------------
    # One-Time Reminders
    # -----------------------------------
    one_time_df = df[
        (df["Type"] == "One-Time") &
        (df["Date"] == today_date_str)
    ]

    # -----------------------------------
    # Monthly Recurring Reminders
    # -----------------------------------
    monthly_df = df[
        (df["Type"] == "Monthly") &
        (df["Day"] == today_day)
    ]

    # -----------------------------------
    # Combine Both
    # -----------------------------------
    final_df = pd.concat(
        [one_time_df, monthly_df],
        ignore_index=True
    )

    if final_df.empty:
        print("No reminders today.\n")
        return final_df

    # Keep only useful columns
    final_df = final_df[
        ["Reminder", "Category", "Notes"]
    ]

    print(
        f"Reminders found today: {len(final_df)}\n"
    )

    return final_df
