import pandas as pd
import pyodbc

def get_connection():
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=DESKTOP-JD0PB6T;"
        "DATABASE=job_market_db;"
        "Trusted_Connection=yes;"
    )
    return conn

def clean(val):
    if pd.isna(val):
        return ""
    return str(val).strip()

def load_data(csv_path):
    df = pd.read_csv(csv_path)
    df = df.fillna("")
    print(f"Loading {len(df)} jobs...")
    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute("""
            IF NOT EXISTS (SELECT 1 FROM dim_location WHERE area=? AND city=? AND country=?)
            INSERT INTO dim_location (area, city, country) VALUES (?, ?, ?)
        """, clean(row.get("area")), clean(row.get("city")), clean(row.get("country")),
            clean(row.get("area")), clean(row.get("city")), clean(row.get("country")))

        cursor.execute("SELECT location_id FROM dim_location WHERE area=? AND city=? AND country=?",
            clean(row.get("area")), clean(row.get("city")), clean(row.get("country")))
        location_id = cursor.fetchone()[0]

        cursor.execute("""
            IF NOT EXISTS (SELECT 1 FROM dim_job WHERE title=?)
            INSERT INTO dim_job (title, job_type) VALUES (?, ?)
        """, clean(row.get("title")), clean(row.get("title")), clean(row.get("job_type")))

        cursor.execute("SELECT job_id FROM dim_job WHERE title=?", clean(row.get("title")))
        job_id = cursor.fetchone()[0]

        company = clean(row.get("company")) or "Unknown"
        cursor.execute("""
            IF NOT EXISTS (SELECT 1 FROM dim_company WHERE company_name=?)
            INSERT INTO dim_company (company_name) VALUES (?)
        """, company, company)

        cursor.execute("SELECT company_id FROM dim_company WHERE company_name=?", company)
        company_id = cursor.fetchone()[0]

        scrape_date = clean(row.get("scrape_date")) or "2026-01-01"
        cursor.execute("""
            IF NOT EXISTS (SELECT 1 FROM dim_date WHERE scrape_date=?)
            INSERT INTO dim_date (scrape_date, day, month, year) VALUES (?, DAY(?), MONTH(?), YEAR(?))
        """, scrape_date, scrape_date, scrape_date, scrape_date, scrape_date)

        cursor.execute("SELECT date_id FROM dim_date WHERE scrape_date=?", scrape_date)
        date_id = cursor.fetchone()[0]

        cursor.execute("""
            INSERT INTO fact_jobs (job_id, location_id, company_id, date_id, skills)
            VALUES (?, ?, ?, ?, ?)
        """, job_id, location_id, company_id, date_id, clean(row.get("skills")))

    conn.commit()
    conn.close()
    print("تم تحميل البيانات بنجاح!")

if __name__ == "__main__":
    load_data("../transformation/jobs_clean.csv")