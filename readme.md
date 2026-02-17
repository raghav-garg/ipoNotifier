# 📊 IPO Notifier Agent

Automated daily IPO tracker that fetches live IPO data from InvestorGain API and filters IPOs based on configurable conditions like GMP, closing date, and IPO category.

Designed to run via cron (GitHub Actions or local scheduler).

---

## 🚀 Features

* Fetch IPO data from InvestorGain backend API
* Supports multiple IPO tabs:

  * Open IPOs
  * Closing Today
  * Upcoming IPOs
  * Mainboard IPOs
  * Closed IPOs
* GMP parsing from HTML response
* Subscription tracking
* Dynamic financial year handling
* Configurable GMP filters
* Cron-ready architecture
* Email/notification ready (extensible)

---

## 🧠 Data Source

Data is fetched from:

InvestorGain IPO GMP Live API (reverse-engineered from network calls).

Example endpoint pattern:

```
https://webnodejs.investorgain.com/cloud/new/report/data-read/
331/1/{month}/{year}/{financialYear}/0/{tab}
```

---

## 📂 Project Structure

```
ipo-notifier/
│
├── ipo_script.py     # Main automation script
├── requirements.txt # Python dependencies
└── README.md        # Project documentation
```

---

## ⚙️ Configuration

Edit config at the top of `ipo_script.py`.

### TAB Modes

```python
TAB = "open"
```

Available options:

| Value         | Meaning            |
| ------------- | ------------------ |
| open          | All active IPOs    |
| closing-today | IPOs closing today |
| current       | Upcoming IPOs      |
| ipo           | Mainboard IPOs     |
| close         | Closed IPOs        |

---

### GMP Filter

```python
GMP_FILTER = -1
```

| Value | Behavior                            |
| ----- | ----------------------------------- |
| -1    | Test mode (includes ₹0 GMP)         |
| 0     | Production mode (only positive GMP) |

---

## ▶️ Run Locally

Install dependencies:

```
pip3 install -r requirements.txt
```

Run script:

```
python3 ipo_script.py
```

---

## 📊 Sample Output

```
IPO Name                     GMP   Subscription   Close Date
Fractal Industries BSE SME   0     2.09x          2026-02-18
```

---

## 🏗️ Architecture

```
Scheduler (Cron)
        ↓
InvestorGain API
        ↓
JSON Parser
        ↓
Filter Engine
        ↓
Notification Layer
```

---

## 🔮 Planned Enhancements

* Email alerts (SMTP)
* WhatsApp notifications
* Telegram bot integration
* GMP trend tracking
* Subscription category breakdown
* IPO allotment probability scoring

---

## ⚠️ Disclaimer

Grey Market Premium (GMP) is unofficial and speculative.
Data sourced from InvestorGain for informational purposes only.

---

## 👨‍💻 Author

Built as an automated IPO tracking agent for daily investment monitoring.
