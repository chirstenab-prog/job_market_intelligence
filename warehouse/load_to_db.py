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

def get_or_create(cursor, table, id_col, where_cols, insert_cols, values):
    where = " AND ".join([f"{c}=?" for c in where_cols])
    cursor.execute(f"SELECT {id_col} FROM {table} WHERE {where}", values[:len(where_cols)])
    row = cursor.fetchone()
    if row:
        return row[0]
    placeholders = ", ".join(["?" for _ in insert_cols])
    cols = ", ".join(insert_cols)
    cursor.execute(f"INSERT INTO {table} ({cols}) OUTPUT INSERTED.{id_col} VALUES ({placeholders})", values)
    return cursor.fetchone()[0]

def load_data(csv_path):
    df = pd.read_csv(csv_path).fillna("")
    print(f"Loading {len(df)} jobs...")
    conn = get_connection()
    cursor = conn.cursor()

    for _, row in df.iterrows():
        try:
            location_id = get_or_create(cursor, "dim_location", "location_id",
                ["area","city","country"], ["area","city","country"],
                [clean(row.get("area")), clean(row.get("city")), clean(row.get("country"))])

            job_id = get_or_create(cursor, "dim_job", "job_id",
                ["title"], ["title","job_type"],
                [clean(row.get("title")), clean(row.get("job_type"))])

            company = clean(row.get("company")) or "Unknown"
            company_id = get_or_create(cursor, "dim_company", "company_id",
                ["company_name"], ["company_name"], [company])

            scrape_date = clean(row.get("scrape_date")) or "2026-01-01"
            cursor.execute("""
                IF NOT EXISTS (SELECT 1 FROM dim_date WHERE scrape_date=?)
                INSERT INTO dim_date (scrape_date, day, month, year)
                VALUES (?, DAY(?), MONTH(?), YEAR(?))
            """, scrape_date, scrape_date, scrape_date, scrape_date, scrape_date)
            cursor.execute("SELECT date_id FROM dim_date WHERE scrape_date=?", scrape_date)
            date_id = cursor.fetchone()[0]

            cursor.execute("""
                INSERT INTO fact_jobs (job_id, location_id, company_id, date_id, skills)
                VALUES (?, ?, ?, ?, ?)
            """, job_id, location_id, company_id, date_id, clean(row.get("skills")))

        except Exception as e:
            print(f"Error on row {_}: {e}")
            continue

    conn.commit()
    conn.close()
    print("تم تحميل البيانات بنجاح!")

if __name__ == "__main__":
    load_data("../transformation/jobs_clean.csv")