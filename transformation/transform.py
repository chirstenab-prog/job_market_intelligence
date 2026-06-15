import pandas as pd

def transform_jobs(input_path, output_path):
    df = pd.read_csv(input_path)
    print(f"البيانات الخام: {len(df)} وظيفة")
    print(df.head())

    # 1. إزالة الصفوف المكررة
    df = df.drop_duplicates(subset=["title", "location"])
    print(f"\nبعد إزالة المكرر: {len(df)} وظيفة")

    # 2. تنظيف الـ title
    df["title"] = df["title"].str.strip()

    # 3. تقسيم الـ location
    df["area"] = df["location"].str.split(",").str[0].str.strip()
    df["city"] = df["location"].str.split(",").str[1].str.strip()
    df["country"] = df["location"].str.split(",").str[2].str.strip()

    # 4. تنظيف الـ company (إزالة التكرار مع الـ title)
    df["company"] = df.apply(
        lambda row: "" if row["company"] == row["title"] else row["company"], axis=1
    )

    # 5. إضافة scrape_date
    df["scrape_date"] = pd.Timestamp.today().strftime("%Y-%m-%d")

    # 6. إزالة الأعمدة الفاضية
    df = df.dropna(subset=["title"])
    df = df[df["title"] != ""]

    print(f"\nالبيانات بعد التنظيف: {len(df)} وظيفة")
    print(df.head(10))

    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"\nتم الحفظ في {output_path}")

    return df

if __name__ == "__main__":
    transform_jobs(
        input_path="../scraper/jobs_raw.csv",
        output_path="jobs_clean.csv"
    )