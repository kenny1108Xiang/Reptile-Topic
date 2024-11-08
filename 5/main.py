import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import os

URL = 'http://app2.atmovies.com.tw/boxoffice/'
CSV_FILENAME = 'Taipei_movies.csv'
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE_PATH = os.path.join(SCRIPT_DIR, CSV_FILENAME)

def fetch_and_print_box_office():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
    }
    response = requests.get(URL, headers=headers)
    response.encoding = 'utf-8'
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        content_div = soup.find('div', class_='content content-left')
        if content_div:
            h3_tags = content_div.find_all('h3')
            for h3 in h3_tags:
                if '台北週末票房排行榜' in h3.text:
                    table = h3.find_next('table')
                    if table:
                        rows = table.find_all('tr')
                        print("排名 | 片名 | 票房")
                        print("-" * 30)
                        for row in rows[1:]:
                            columns = row.find_all('td')
                            if len(columns) >= 3:
                                rank = columns[0].get_text(strip=True)
                                title = columns[1].get_text(strip=True)
                                box_office = columns[2].get_text(strip=True)
                                print(f"{rank} | {title} | {box_office}")
                    break

def scrape_box_office_and_write_csv():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(URL)
    wait = WebDriverWait(driver, 10)
    view_more_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.viewMore[href="/boxoffice/twweekend/"]')))
    view_more_link.click()
    content_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.content.content-left')))
    tables = content_div.find_elements(By.TAG_NAME, 'table')
    second_table = tables[1]
    rows = second_table.find_elements(By.TAG_NAME, 'tr')
    table_data = [
        [cell.text.strip() for cell in row.find_elements(By.TAG_NAME, 'th') or row.find_elements(By.TAG_NAME, 'td')]
        for row in rows
    ]
    processed_data = []
    for i in range(1, len(table_data), 2):
        if len(processed_data) >= 20:
            break
        rank_and_title = table_data[i]
        box_office = table_data[i + 1]
        rank = rank_and_title[0] if len(rank_and_title) > 0 else ''
        title = rank_and_title[1] if len(rank_and_title) > 1 else ''
        weekly_box_office = box_office[2] if len(box_office) > 2 else ''
        cumulative_box_office = box_office[3] if len(box_office) > 3 else ''
        processed_data.append({
            '排行': rank,
            '片名': title,
            '本週票房': weekly_box_office,
            '累計票房': cumulative_box_office
        })
    driver.quit()
    with open(CSV_FILE_PATH, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.DictWriter(file, fieldnames=['排行', '片名', '本週票房', '累計票房'])
        writer.writeheader()
        for entry in processed_data:
            writer.writerow(entry)
    print(f"成功將前 {len(processed_data)} 筆資料寫入 {CSV_FILE_PATH}")

def main():
    fetch_and_print_box_office()
    scrape_box_office_and_write_csv()

if __name__ == '__main__':
    main()
