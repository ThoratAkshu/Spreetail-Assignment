# 🧾 MerchTech Product Performance Dashboard

This project is a lightweight **Django-based dashboard** that helps analyze product performance using sales, return, and review data.  
It provides clear KPIs, visual charts, and smart insights to understand which products are performing well and which need improvement.

---

## ⚙️ Project Setup

Follow these simple steps to run the project locally:

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/merchtech-dashboard.git
cd merchtech-dashboard
2️⃣ Create a Virtual Environment
bash
Copy code
python -m venv venv_backend
venv_backend\Scripts\activate       # On Windows
# OR
source venv_backend/bin/activate    # On macOS/Linux
3️⃣ Install Required Packages
bash
Copy code
pip install -r requirements.txt
4️⃣ Apply Database Migrations
bash
Copy code
cd backend
python manage.py makemigrations
python manage.py migrate
5️⃣ Load Dataset
bash
Copy code
python manage.py load_kpis
This command:

Clears any old data

Loads the dataset from sde2_merchtech_dataset.txt

Aggregates sales, reviews, and returns

Automatically generates product insights and improvement suggestions

6️⃣ Run the Server
bash
Copy code
python manage.py runserver
Now open your browser and visit:
👉 http://127.0.0.1:8000/dashboard/

📊 About the Dashboard
The dashboard gives a simple and interactive view of how products are performing.
It combines sales, reviews, and returns into one place so teams can take faster decisions.

🧮 1. KPI Summary
At the top of the dashboard, you’ll see quick statistics like:

Metric	Description
💰 Total GMV	The total sales amount for all products
⭐ Average Rating	Average customer rating from all reviews
⚠️ Total Returns (%)	Percentage of items returned out of total sold
🛍️ Units Sold	Total number of items sold

Each card also shows a small arrow indicator (↑/↓) comparing it to the previous week.

📸 Example:

📈 2. GMV Trend by Week
A line chart shows weekly GMV (Gross Merchandise Value) for each product.
It helps you track how performance is changing over time.

📸 Example:

🔁 3. Return Reason Breakdown
A doughnut chart highlights the most common return reasons (like Late Delivery, Damaged Item, Size Mismatch).
This makes it easy to see where problems occur most often.

📸 Example:

🧾 4. Product Insights Table
Each product is listed with:

ASIN and Product Name

GMV, Rating, and Total Returns

All reported issues (with count per reason)

suggested actions to fix the problem

Example:

Product	GMV	Rating	Returns	Issues	Suggested Action
Vacuum Cleaner	$4,095	2.8	6.5%	Late delivery — 6	Optimize delivery partners and improve tracking.
Office Chair	$3,978	3.0	8.0%	Damaged item — 4	Reinforce packaging and review handling process.

📸 Example:

🧠 5. Suggested Actions
The system scans product reviews and return reasons to generate improvement ideas automatically.

Some examples:

If reviews mention “late delivery” → Optimize logistics and courier partners.

If customers say “defective product” → Improve quality checks and pre-shipment testing.

If ratings are below 3 → Investigate recurring complaints and fix root causes.

📸 Example:

📤 6. Export Reports
You can download full reports in two formats:

📊 CSV Export – Simple data sheet with all KPIs and issues.

🧾 PDF Export – Nicely formatted report with wrapped text and alternating colors.

📸 Example:

📂 Folder Structure
bash
Copy code
merchtech-dashboard/
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
│
└── README.md
🚀 Key Highlights
Clean and simple Bootstrap-based UI

Real-time KPI updates

Easy-to-read trend and reason charts

suggested actions

One-click CSV & PDF export

Lightweight and easy to run locally


🏁 Author & Credits
Developed by: Akshay Thorat
Project: Spreetail MerchTech — Software Engineer II Assignment
Year: 2025