# AMZ Wholesale Analytics

## Overview
AMZ Wholesale Analytics is a proof-of-concept full-stack tool for Amazon sellers that provides:

- A **historical sales dashboard** with adjustable time filters.
- A **wholesale profit margin scanner** for uploaded CSVs.
- **Automated backend updates** via GitHub Actions (every 15 minutes).

> **Note:** This project requires an active Amazon SP-API subscription. Since the owner is no longer selling on Amazon, SP-API access may stop, so functionality could be affected after a month.

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

## How It Works

- **Amazon Seller Data Integration:** Fetches and processes sales/order data using SP-API credentials.
- **Historical Sales Dashboard:** Visualizes sales trends with interactive charts and tables.
- **Profit Margin Scanner:** Upload a CSV, parse UPC/costs, calculate profit margins minus fees, and display results in ag-grid tables.
- **Theme Switching:** Supports light/dark mode across the dashboard.
- **Firebase Integration:** Reads/writes data to Firebase Realtime Database.
- **Automated Data Updates:** GitHub Actions triggers backend scripts every 15 minutes to update data.

---

## Demo Videos
### Dashboard – Historical Sales
![Dashboard Demo 1](src/assets/Dashboard_part1.gif)  
*Showcases the adjustable time filter and sales chart visualization (Part 1).*

![Dashboard Demo 2](src/assets/Dashboard_part2.gif)  
*Additional sales chart interactions (Part 2).*

---

### Scanner – Profit Margin Analysis
![Scanner Demo 1](src/assets/sample_batch_part1.gif)  
*CSV upload and initial processing (Part 1).*

![Scanner Demo 2](src/assets/sample_batch_part2.gif)  
*Profit margin calculation in progress (Part 2).*

![Scanner Demo 3](src/assets/sample_batch_part3.gif)  
*Batch process visualization (Part 3).*

![Scanner Demo 4](src/assets/sample_batch_part4.gif)  
*Quick insights generation (Part 4).*

![Scanner Demo 5](src/assets/sample_batch_part5.gif)  
*Final results and summary (Part 5).*


### GitHub Actions Automation
![GitHub Actions Demo](path_to_github_actions_demo.mp4)  
*Shows the automated 15-minute backend data update workflow.*

> **Note:** Add your `.mp4` files to the repo and update these links.

---

## Quick Start

1. **Clone the repo**
```bash
git clone https://github.com/jhalzel/amz-wholesale-analytics.git
cd amz-wholesale-analytics
