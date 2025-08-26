# AMZ Wholesale Analytics

## Overview
AMZ Wholesale Analytics is a proof-of-concept full-stack tool for Amazon sellers that provides:

- A **historical sales dashboard** with adjustable time filters.
- A **wholesale profit margin scanner** for uploaded CSVs.
- **Automated backend updates** via GitHub Actions (every 15 minutes).

> **Note:** This project requires an active Amazon SP-API subscription. Since the owner is no longer selling on Amazon, SP-API access may stop, so functionality may be deprecated.

---

## Technical Stack

**Backend:**
- Flask (`/src/server/trial.py`, `/src/server/script.py`)
- Flask-CORS
- Firebase Admin SDK (`firebase_admin`)
- Amazon SP-API integration
- Python 3.9
- dotenv for environment variables

**Frontend:**
- React (`/src/client/src/pages/Scanner.jsx`, `/src/client/src/pages/Home.jsx`)
- ag-grid-react for data tables
- PapaParse for CSV parsing
- Tailwind CSS + DaisyUI for styling
- Theme switching (`/src/client/src/components/ThemeController.jsx`, `/src/client/src/context/themeContext/index.jsx`)

**Automation/CI:**
- GitHub Actions (`.github/workflows/actions.yaml`) runs `script.py` every 15 minutes

---

## Deployment

- **Backend (Python / SP-API)**: Hosted on [Render](https://render.com/)  
- **Frontend (Next.js / React)**: Hosted on [Netlify](https://www.netlify.com/)  

---

## How It Works

- **Amazon Seller Data Integration:** Fetches and processes sales/order data using SP-API credentials.
- **Historical Sales Dashboard:** Displays Visualization of sales trends with interactive charts and tables.
- **Profit Margin Scanner:** Upload a CSV, parse UPC/costs, calculate profit margins minus fees, ROI, etc., and display results in ag-grid tables.
- **Theme Switching:** Supports light/dark mode across the dashboard.
- **Firebase Integration:** Reads/writes data to Firebase Realtime Database.
- **Automated Data Updates:** GitHub Actions triggers backend scripts every 15 minutes to update data.

---
## Demo Videos

### Dashboard – Historical Sales
<p align="center">
  <img src="src/assets/Dashboard_part1.gif" alt="Dashboard Demo 1" width="1080"/>
</p>
<p align="center"><em>Showcases the login, theme switching and sales chart visualization with time filter adjustment (Part 1).</em></p>

<p align="center">
  <img src="src/assets/Dashboard_part2.gif" alt="Dashboard Demo 2" width="1080"/>
</p>
<p align="center"><em>Additional sales charts including line chart, bar chart and area chart graphs (Part 2).</em></p>

---

### Scanner – Profit Margin Analysis
<p align="center">
  <img src="src/assets/sample_batch_part1.gif" alt="Scanner Demo 1" width="1080"/>
</p>
<p align="center"><em>CSV upload; backend logic hosted on Render (Part 1).</em></p>

<p align="center">
  <img src="src/assets/sample_batch_part2.gif" alt="Scanner Demo 2" width="1080"/>
</p>
<p align="center"><em>Selecting parameters necessary for scanning CSV sheet with batch processing (Part 2).</em></p>

<p align="center">
  <img src="src/assets/sample_batch_part3.gif" alt="Scanner Demo 3" width="1080"/>
</p>
<p align="center"><em>Chart results (Part 3).</em></p>

<p align="center">
  <img src="src/assets/sample_batch_part4.gif" alt="Scanner Demo 4" width="1080"/>
</p>
<p align="center"><em>More chart results featuring column metrics such as fees, and profit margin calculations (Part 4).</em></p>

<p align="center">
  <img src="src/assets/sample_batch_part5.gif" alt="Scanner Demo 5" width="1080"/>
</p>
<p align="center"><em>Filtering by profit margin and ROI for best products (Part 5).</em></p>

---

### GitHub Actions Automation
<p align="center">
  <img src="src/assets/actions_part1.gif" alt="GitHub Actions Demo" width="1080"/>
</p>
<p align="center"><em>Shows the automated 15-minute backend data update workflow (Part 1)</em></p>

<p align="center">
  <img src="src/assets/actions_part2.gif" alt="GitHub Actions Demo" width="1080"/>
</p>
<p align="center"><em>Shows the python script execution and results (Part 2)</em></p>


---

## Quick Start

1. **Clone the repo**
```bash
git clone https://github.com/jhalzel/amz-wholesale-analytics.git
cd amz-wholesale-analytics
