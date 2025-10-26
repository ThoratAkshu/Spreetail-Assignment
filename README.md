# 🧾 Spreetail MerchTech Product Performance Dashboard

A lightweight **Django-based analytics dashboard** that helps track and visualize **product performance** using sales, reviews, and return data.  
It provides **key performance indicators (KPIs)**, visual insights, and intelligent suggestions to help identify which products are excelling and which need attention.

---

## ⚙️ Initial Setup Guide

Follow these steps to set up and run the project locally.

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/ThoratAkshu/Spreetail-Assignment.git
cd Spreetail-Assignment
2️⃣ Create and Activate a Virtual Environment
bash
Copy code
python -m venv venv_backend
venv_backend\Scripts\activate       # On Windows
# OR
source venv_backend/bin/activate    # On macOS/Linux
3️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Run Database Migrations
bash
Copy code
cd backend
python manage.py makemigrations
python manage.py migrate
5️⃣ Load the Dataset
bash
Copy code
python manage.py load_kpis
This command will:

Clear any old data

Load the dataset from sde2_merchtech_dataset.txt

Aggregate sales, returns, and reviews

Automatically generate product insights and suggested actions

6️⃣ Start the Development Server
bash
Copy code
python manage.py runserver
Then open your browser and go to:
👉 http://127.0.0.1:8000/dashboard/

📊 Dashboard Overview
The dashboard provides a clean, interactive view of product performance metrics.
It helps business and tech teams make data-driven decisions faster.

🧮 1. KPI Summary
At the top of the dashboard, you'll see the main performance metrics:

Metric	Description
💰 Total GMV	Overall sales revenue
⭐ Average Rating	Average product rating from all reviews
⚠️ Total Returns (%)	Percentage of items returned
🛍️ Units Sold	Total quantity of products sold

Each card includes trend indicators (↑ / ↓) comparing performance with the previous week.

📸 Example Snapshot:

📈 2. GMV Trend by Week
Displays a line chart showing weekly GMV (Gross Merchandise Value).
This helps you analyze how sales evolve week over week.

📸 Example:

🔁 3. Return Reason Breakdown
A doughnut chart highlights the most common return reasons such as:

Damaged Item

Late Delivery

Wrong Item Sent

Size Mismatch

📸 Example:

🧾 4. Product Insights Table
Each product includes:

ASIN & Product Name

GMV, Rating & Returns

Return issue breakdown

Suggested corrective actions

Product	GMV	Rating	Returns	Common Issues	Suggested Action
Vacuum Cleaner	$4,095	2.8	6.5%	Late Delivery — 6	Optimize delivery partners and tracking
Office Chair	$3,978	3.0	8.0%	Damaged Item — 4	Improve packaging and QA

📸 Example:

🧠 5. Automated Suggestions
The system reads reviews and return reasons to generate meaningful insights.

Condition	Suggested Action
Low Rating (<3)	Investigate product quality or recurring complaints
“Late Delivery” in reviews	Optimize logistics & courier partners
“Defective Item” in returns	Strengthen pre-shipment testing & QC

📸 Example:

📤 6. Export Reports
Easily export your reports for analysis or sharing:

📊 CSV Export → Tabular KPIs and issue breakdown

🧾 PDF Export → Styled report with formatted tables and text wrapping

📸 Example:

📂 Project Structure
bash
Copy code
Spreetail-Assignment/
│
├── backend/
│   ├── manage.py
│   ├── products/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── templates/dashboard.html
│   │   ├── management/commands/load_kpis.py
│   │   └── data/
│   │       ├── sde2_merchtech_dataset.txt
│   │       ├── sde2_sales.csv
│   │       ├── sde2_returns.csv
│   │       └── sde2_reviews.csv
│   └── static/dashboard.css
│
├── requirements.txt
└── README.md
🚀 Key Highlights
✅ Clean & responsive Bootstrap UI
✅ Real-time KPI visualization
✅ Interactive charts for trends and returns
✅ Intelligent action recommendations
✅ One-click CSV & PDF exports
✅ Lightweight & quick to set up locally

🧑‍💻 Author & Credits
Developed by: Akshay Thorat
Project: Spreetail MerchTech — Software Engineer II Assignment
Year: 2025

