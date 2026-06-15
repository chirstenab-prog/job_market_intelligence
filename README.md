# Job Market Intelligence

## 📌 Overview
Job Market Intelligence is an automated ETL pipeline designed to collect, process, and store job market data from Wuzzuf.net. The project provides insights into job trends, required skills, and hiring companies.

## 🚀 Features
- Web scraping job postings from Wuzzuf.net
- Data cleaning and transformation
- Data storage in a warehouse
- Workflow orchestration using Apache Airflow
- Automated ETL pipeline

## 🛠 Technologies Used
- Python
- Pandas
- BeautifulSoup
- Requests
- Apache Airflow
- PostgreSQL
- Docker
- Git & GitHub

## 📂 Project Structure

```text
job_market_intelligence/
│
├── airflow/         # Airflow DAGs and workflow configuration
├── scraper/         # Web scraping scripts
├── transformation/  # Data cleaning and transformation
├── warehouse/       # Data storage and loading
├── README.md
└── .gitignore
```

## ⚙️ ETL Process

### 1. Extract
Collect job postings data from Wuzzuf.net.

### 2. Transform
Clean and process the collected data.

### 3. Load
Store the processed data into the data warehouse.

## 📊 Expected Insights
- Most demanded job titles
- Most required technical skills
- Top hiring companies
- Job market trends

## 👩‍💻 Author

**Christina Beshay Wadid**

Data Engineering Enthusiast