# 🧾 Vendor Performance Analysis – Retail Inventory & Sales

_Analyzing vendor efficiency and profitability to support strategic purchasing and inventory decisions using Python, SQLite, and Jupyter Notebooks._

---

> 📄 **Looking for the detailed analysis?** The complete executive findings, charts, and comprehensive metrics are available in the [vendor analysis Report.pdf] file included in this repository.

---

## 📌 Table of Contents
- <a href="#overview">Overview</a>
- <a href="#business-problem">Business Problem</a>
- <a href="#dataset--architecture">Dataset & Architecture</a>
- <a href="#tools--technologies">Tools & Technologies</a>
- <a href="#project-structure">Project Structure</a>
- <a href="#data-cleaning--pipeline-optimization">Data Cleaning & Pipeline Optimization</a>
- <a href="#exploratory-data-analysis-eda">Exploratory Data Analysis (EDA)</a>
- <a href="#research-questions--key-findings">Research Questions & Key Findings</a>
- <a href="#how-to-run-this-project">How to Run This Project</a>
- <a href="#final-recommendations">Final Recommendations</a>
- <a href="#author--contact">Author & Contact</a>

---
## 📌 Overview

This project evaluates vendor performance and retail inventory dynamics to drive strategic insights for purchasing, pricing, and inventory optimization. An end-to-end data engineering and statistical pipeline was built to analyze **10,692 unique records** across **119 active vendors**, transforming raw transactional records into clear, data-driven business solutions.

---
## 💼 Business Problem

Effective inventory and sales management play a crucial role in maximizing profitability within the retail and wholesale industry. Businesses must maintain an optimal balance between inventory availability and sales performance to avoid losses caused by inefficient pricing strategies, slow-moving stock, and excessive dependency on specific vendors. 

The primary objectives of this analysis are to answer the following research questions:
- To identify underperforming brands that may require promotional campaigns or pricing adjustments to improve sales.
- To determine the top-performing vendors contributing the most to overall sales and gross profit.
- To Find out which vendor contribute the most to total purchase dollars?
- To analyze how bulk purchasing impacts unit costs and whether it leads to cost savings.
- To assess inventory turnover in order to reduce holding costs and improve stock movement efficiency.
- To investigate profitability differences between high-performing and low-performing vendors.

---
## 📊 Dataset & Architecture

The analysis was performed using six CSV datasets containing inventory, purchase, sales, pricing, and vendor invoice information. These datasets collectively provide a complete view of product movement from procurement to final sales:
- `Begin Inventory` (206,529 rows) — *Excluded from final analytical workflow*
- `End Inventory` (224,489 rows) — *Excluded from final analytical workflow*
- `Purchases` (2,372,474 rows) — *Included*
- `Purchase Prices` (12,261 rows) — *Included*
- `Sales` (12,825,363 rows) — *Included*
- `Vendor Invoice` (5,543 rows) — *Included*

_Note: The Begin Inventory and End Inventory tables were excluded from the final analytical workflow because they were not directly required for vendor-sales profitability analysis._

---
## 🛠️ Tools & Technologies

- **Python**: Core programming engine used for pipeline scripting, data handling, and processing logic.
- **SQLite (`sqlite3`)**: Relational database environment used to manage and query large datasets via a centralized database file (`vendorinventory.db`).
- **Pandas & NumPy**: Structural data manipulation, missing value replacement, and cross-sectional data profiling.
- **SciPy & Statsmodels**: Statistical data verification, hypothesis testing, and 95% Confidence Interval calculations.
- **Matplotlib & Seaborn**: Data plotting for distribution histograms, correlation heatmaps, boxplots, and trend charts.

---
## 📂 Project Structure

```text
vendor-performance-analysis/
│
├── README.md                              # Complete pipeline documentation and system layout
├── Vendor Performance Report.pdf          # Full formal business report with detailed analysis
│
├── notebooks/                             # Interactive analytical execution environments
│   ├── Vendor_Exploratory Data Analysis.ipynb # Complete analysis answering business problems 
│   └── Vendor_performance_analysis.ipynb   # Data profiling, outlier isolation, and distributions
│
└── scripts/                               # Production pipeline automation scripts
    ├── vendor_injestion_db.py             # Automates loading of raw CSVs into SQLite database
    └── get_vendor_performance_summary.py  # Uses CTEs to aggregate and output final metrics summaries
```

---
## 🧹 Data Cleaning & Pipeline Optimization

### Pipeline Refinement
Due to the massive size of the raw data—particularly the Sales and Purchases tables—direct SQL query execution time became extremely slow and computationally expensive. To optimize performance, the pipeline was refined using SQL Common Table Expressions (CTEs) and pre-aggregation to generate three specialized summary tables before building the final analytical dataset (`vendor_sale_summary`):
- `FreightSummary`: Aggregated total freight cost by vendor.
- `PurchaseSummary`: Aggregated purchase quantity and purchase dollars by vendor and brand.
- `SaleSummary`: Aggregated total sales quantity, total sales revenue, and excise tax by vendor and brand.

### Data Preparation Steps
- Missing values across variables were replaced with zero.
- Categorical fields (vendor names, descriptions) were stripped of extra trailing or leading spaces.
- Calculated business features were engineered to support performance analysis:
  - **Gross Profit** = `Total Sale Dollar` − `Total Purchase Dollar`
  - **Profit Margin (%)** = (`Gross Profit` / `Total Sale Dollar`) × 100
  - **Stock Turnover** = `Total Sales Quantity` / `Total Purchase Quantity`
  - **Sales-to-Purchase Ratio** = `Total Sale Dollar` / `Total Purchase Dollar`

---
## 🔍 Exploratory Data Analysis (EDA)

Key statistical profiles and anomalies extracted from the data streams include:
- **Negative and Zero Values**: Minimum `GrossProfit` reached **-\$52,002.78**, showing that some items sold lower than purchase costs or with heavy discounts. `ProfitMargin` fields displayed infinite values (`-inf`), highlighting a column calculation error requiring cleanup. Minimum values of zero for sales metrics indicated completely stagnant dead stock.
- **Outliers & Skewness**: Core transactional metrics show a heavy positive (right) skew. While average prices sit near \$24 (purchase) and \$36 (actual), maximum prices peak at **\$5,682** and **\$7,500**, indicating a niche luxury catalog segment.
- **Logistical Variance**: Freight costs showed a massive variation (**\$0.09 to \$257,032.00**), reflecting bulk shipment spikes.
- **Correlation Heatmap Profiles**: 
  - A perfect correlation (**1.00**) exists between total purchases and total sales quantities, verifying high product throughput.
  - A strong correlation (**0.98**) exists between Gross Profit and Total Sales Dollars, proving profitability is volume-driven.
  - A slight negative correlation (**-0.11**) between Profit Margin and Total Sales suggests margin compression due to quick stock clearance discounting.

---
## 📈 Research Questions & Key Findings

### To identify underperforming brands that may require promotional campaigns or pricing adjustments to improve sales.
The analysis isolated **106 underperforming niche brands** acting as hidden profit goldmines. These target brands hold premium profit margins above **65%** (with micro-brands like *Mad Dogs & Englishmen Jumil* hitting **97.66%** and *Vigne A Porrona Rosso* hitting **96.82%**), but fail to cross \$600 in total sales revenue due to low consumer visibility.

### To determine the top-performing vendors contributing the most to overall sales and gross profit.
**Diageo North America Inc.** serves as the absolute revenue engine, generating **\$67.99 Million in sales**, outperforming the next closest supplier by nearly \$30 Million. Behind Diageo, sales are anchored by a secondary tier of high-volume suppliers: *Martignetti Companies* (\$39.33M), *Pernod Ricard USA* (\$32.06M), and *Jim Beam Brands Company* (\$31.42M). 

### To Find out which vendor contribute the most to total purchase dollars?
**Diageo North America Inc.** dominates procurement spending with a **\$50.10 Million investment (16.30% of our entire purchasing budget)**. Procurement cash is heavily concentrated at the top, with the top four suppliers absorbing nearly \$123 Million of capital. Out of 119 active vendors, **only 10 vendors account for 65.7% of all purchases**, creating a high single-source supplier risk.

### To analyze how bulk purchasing impacts unit costs and whether it leads to cost savings.
Buying in larger sizes directly lowers individual unit costs. Small order brackets average a high cost of **\$39.07 per unit**. Moving to Medium orders drops costs by 60% down to **\$15.49**, while Large bulk orders secure the lowest price tier at **\$10.78 per unit**, proving massive scale economies.

### To assess inventory turnover in order to reduce holding costs and improve stock movement efficiency.
The warehouse network holds a massive capital bottleneck of **\$9.55 Million in unsold, stagnant stock**, with **64.4% concentrated in the top 10 vendors**. **Diageo alone accounts for \$1.40 Million** of this trapped cash, highlighting a storage bottleneck caused by over-ordering items faster than stores can clear them.

