# 🧾 Spreetail MerchTech Product Performance Dashboard

A lightweight **Django-based analytics dashboard** that helps track and visualize **product performance** using sales, reviews, and return data.
It provides **key performance indicators (KPIs)**, visual insights, and intelligent suggestions to help identify which products are excelling and which need attention.

---

## ⚙️ Initial Setup Guide

Follow these steps to set up and run the project locally.

---

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/ThoratAkshu/Spreetail-Assignment.git
cd Spreetail-Assignment
```

---

### 2️⃣ Create and Activate a Virtual Environment

```bash
python -m venv venv_backend
```

#### ▶️ Activate the environment:

**On Windows:**

```bash
venv_backend\Scripts\activate
```

**On macOS/Linux:**

```bash
source venv_backend/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Run Database Migrations

```bash
cd backend
python manage.py makemigrations products
python manage.py migrate
```

---

### 5️⃣ Load the Dataset

```bash
python manage.py load_kpis
```

This command will:

* Clear any old data
* Load the dataset from `sde2_merchtech_dataset.txt`
* Aggregate sales, returns, and reviews
* Automatically generate product insights and suggested actions

---

### 6️⃣ Start the Development Server

```bash
python manage.py runserver
```

Then open your browser and go to:
👉 **[http://127.0.0.1:8000/dashboard/](http://127.0.0.1:8000/dashboard/)**

---

## 📊 Dashboard Overview

The dashboard provides a clean, interactive view of product performance metrics.
It helps business and tech teams make **data-driven decisions** faster.

📸 *Live Dashboard Snapshot:*
![Dashboard Overview]>![dashboard1](https://github.com/user-attachments/assets/0087cb62-e674-441e-aeb0-9e032efe6e9a)

)

💡 Note: The graphical view has the feature to unselect specific product lines or metrics on the chart, allowing analysts to focus on selected datasets for better visualization and presentation.

<img width="952" height="383" alt="Screenshot 2025-10-26 232834" src="https://github.com/user-attachments/assets/b6d80244-5802-455a-b788-1f4d5a0c2950" />

---

### 🧮 1. KPI Summary

At the top of the dashboard, you’ll see the main performance metrics:

| Metric                   | Description                             |
| :----------------------- | :-------------------------------------- |
| 💰 **Total GMV**         | Overall sales revenue                   |
| ⭐ **Average Rating**     | Average product rating from all reviews |
| ⚠️ **Total Returns (%)** | Percentage of items returned            |
| 🛍️ **Units Sold**       | Total quantity of products sold         |

Each card includes **trend indicators (↑ / ↓)** comparing performance with the previous week.

---

### 📈 2. GMV Trend by Product

Displays a **line chart** showing weekly GMV (Gross Merchandise Value).
This helps analyze how sales evolve week over week with unselecting graphical view for better presantations 


**💡 Note:** While unselecting any chart metric, the analytics recalculates the results dynamically to focus on the selected dataset only — helping analysts to perform deeper performance segmentation.

---

### 🔁 3. Return Reason Breakdown

A **doughnut chart** highlights the most common return reasons such as:

* Damaged Item
* Late Delivery
* Wrong Item Sent
* Size Mismatch


---

### 🧾 4. Product Insights Table

Each product entry includes:

* ASIN & Product Name
* GMV, Rating & Returns
* Return issue breakdown
* Suggested corrective actions

| Product        | GMV    | Rating | Returns | Common Issues     | Suggested Action                        |
| :------------- | :----- | :----- | :------ | :---------------- | :-------------------------------------- |
| Vacuum Cleaner | $4,095 | 2.8    | 6.5%    | Late Delivery — 6 | Optimize delivery partners and tracking |
| Office Chair   | $3,978 | 3.0    | 8.0%    | Damaged Item — 4  | Improve packaging and QA                |


---

### 🧠 5. Automated Suggestions

The system reads **reviews and return reasons** to generate meaningful insights.

| Condition                   | Suggested Action                                    |
| :-------------------------- | :-------------------------------------------------- |
| Low Rating (<3)             | Investigate product quality or recurring complaints |
| “Late Delivery” in reviews  | Optimize logistics & courier partners               |
| “Defective Item” in returns | Strengthen pre-shipment testing & QC                |

---

### 📤 6. Export Reports

Easily export reports for analysis or sharing:

* 📊 **CSV Export** → Tabular KPIs and issue breakdown
* 🧾 **PDF Export** → Styled report with formatted tables and text wrapping

---

## 💻 Tech Stack

| Category                   | Technology            |
| :------------------------- | :-------------------- |
| **Backend Framework**      | Django (Python)       |
| **Frontend**               | HTML, CSS, Bootstrap  |
| **Charts & Visualization** | Chart.js              |
| **Data Handling**          | Pandas                |
| **Exports**                | CSV & ReportLab (PDF) |
| **Database**               | SQLite (default)      |
| **Version Control**        | Git + GitHub          |

---

## 📂 Project Structure

```bash
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
```

---

## 🚀 Key Highlights

✅ Clean & responsive **Bootstrap UI**
✅ Real-time **KPI visualization**
✅ Interactive charts for **trends and returns**
✅ Intelligent **action recommendations**
✅ One-click **CSV & PDF exports**
✅ Lightweight & quick to **set up locally**

---

## 🧑‍💻 Author & Credits

**Developed by:** [Akshay Thorat](https://github.com/ThoratAkshu)
**Project:** Spreetail MerchTech — Software Engineer II Assignment
**Year:** 2025

---

⭐ *If you find this project helpful, don’t forget to give it a star on GitHub!* 🌟
