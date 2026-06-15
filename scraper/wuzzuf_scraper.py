from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape_wuzzuf(pages=3):
    jobs = []
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    for page in range(pages):
        url = f"https://wuzzuf.net/search/jobs/?q=&l=Egypt&start={page}"
        print(f"Scraping page {page + 1}...")
        driver.get(url)
        time.sleep(5)

        h2s = driver.find_elements(By.TAG_NAME, "h2")
        print(f"Found {len(h2s)} elements")

        for h2 in h2s:
            try:
                title = h2.text.strip()
                if not title or title.startswith("Browse"):
                    continue

                card = h2.find_element(By.XPATH, "./ancestor::div[3]")
                
                # Company
                try:
                    company = card.find_element(By.XPATH, ".//a[2]").text.strip()
                except:
                    company = ""

                # Location
                try:
                    location = card.find_elements(By.TAG_NAME, "span")[0].text.strip()
                except:
                    location = ""

                # Job Type (Full Time / Part Time)
                try:
                    badges = card.find_elements(By.XPATH, ".//span[contains(@class,'css-')]")
                    job_type = badges[0].text.strip() if badges else ""
                except:
                    job_type = ""

                # Skills
                try:
                    skills_elements = card.find_elements(By.XPATH, ".//div[last()]//span")
                    skills = ", ".join([s.text.strip() for s in skills_elements if s.text.strip()])
                except:
                    skills = ""

                # Date Posted
                try:
                    date_posted = card.find_element(By.XPATH, ".//div[contains(@class,'css-')]//span[last()]").text.strip()
                except:
                    date_posted = ""

                if title:
                    jobs.append({
                        "title": title,
                        "company": company,
                        "location": location,
                        "job_type": job_type,
                        "skills": skills,
                        "date_posted": date_posted
                    })

            except Exception as e:
                continue

    driver.quit()
    return pd.DataFrame(jobs)

if __name__ == "__main__":
    df = scrape_wuzzuf(pages=5)
    print(f"\nتم جمع {len(df)} وظيفة")
    print(df.head(10))
    df.to_csv("jobs_raw.csv", index=False, encoding="utf-8-sig")
    print("\nتم الحفظ في jobs_raw.csv")