import requests
from bs4 import BeautifulSoup

URL = 'http://www.atmovies.com.tw/movie/new/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Accept-Language': 'zh-TW,zh;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive'
}

response = requests.get(URL, headers=HEADERS)
response.encoding = 'utf-8'

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    content_container = soup.find('div', class_='l-content container')
    main_section = content_container.find('div', class_='l-main')
    section = main_section.find('div', class_='c-section')
    movie_sections = section.find_all('article', class_='filmList')

    for movie in movie_sections:
        title_tag = movie.find('div', class_='filmTitle')
        title = title_tag.text.strip() if title_tag else '無標題'
        href = title_tag.find('a')['href'] if title_tag and title_tag.find('a') else None
        full_url = f'http://www.atmovies.com.tw{href}' if href else '無網址'
        
        description_tag = movie.find('p')
        description = description_tag.text.strip() if description_tag else '無簡介'
        
        runtime_tag = movie.find('div', class_='runtime')
        runtime = runtime_tag.text.strip() if runtime_tag else '無片長'
        
        print(f'標題: {title}')
        print(f'網址: {full_url}')
        print(f'簡介: {description}')
        print(f'片長: {runtime}')
        print('-' * 40)
else:
    print(f'無法取得網頁內容，狀態碼: {response.status_code}')
