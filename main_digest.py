from agents.ipo_agent import fetch_ipo_data
from agents.reminder_agent import fetch_today_reminders
from mailer.html_builder import build_html_table
from mailer.email_sender import send_email


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

TAB = "open"


# GMP FILTER
# -----------------------------------
# -1 → Test mode (includes ₹0 GMP)
#  0 → Production mode (only positive GMP)

GMP_FILTER = 0


# =========================================================
# MAIN DIGEST EXECUTION
# =========================================================

def main():

    print("\n====================================")
    print("📊 Daily Digest Agent Running")
    print("====================================\n")

    print(f"TAB MODE: {TAB}")
    print(f"GMP FILTER: > {GMP_FILTER}\n")

    sections = []

    # ================================
    # IPO AGENT
    # ================================
    ipo_df = fetch_ipo_data(
        tab=TAB,
        gmp_filter=GMP_FILTER
    )

    if not ipo_df.empty:
        sections.append(
            build_html_table(
                ipo_df,
                "📊 IPO Alerts"
            )
        )

    # ================================
    # REMINDER AGENT
    # ================================
    reminder_df = fetch_today_reminders()

    if not reminder_df.empty:
        sections.append(
            build_html_table(
                reminder_df,
                "📌 Reminders Today"
            )
        )

    # ================================
    # EXIT IF NOTHING
    # ================================
    if not sections:
        print("No alerts today.")
        return

    final_html = "".join(sections)

    send_email(
        final_html,
        "📊 Daily IPO & Reminder Digest"
    )


# =========================================================
# ENTRY POINT
# =========================================================

if __name__ == "__main__":
    main()
