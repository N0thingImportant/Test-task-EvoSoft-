import requests
from bs4 import BeautifulSoup
import re

# Прокси-сервер и порт
proxy_server = "178.218.44.79"
proxy_port = "3128"

# Формирование URL для прокси
proxy_url = f"http://{proxy_server}:{proxy_port}"

# Настройка прокси в параметрах запроса
proxies = {
    "http": proxy_url,
    "https": proxy_url,
}

# 1. Получение своего IP-адреса с https://2ip.ru/
response_2ip = requests.get("https://2ip.ru/", proxies=proxies)
soup_2ip = BeautifulSoup(response_2ip.text, 'html.parser')
ip_address = soup_2ip.find('div', {'class': 'ip'}).text.strip()
print(ip_address)

# Шаг 2: Получение токена для получения тайм зоны
url = "https://www.maxmind.com/en/geoip2/demo/token"

headers = {
    "Host": "www.maxmind.com",
    "Cookie": "_ga=GA1.1.1597175671.1702370756; hubspotutk=a19db23b9cca668b15aec293f33920dd; __mmapiwsid=018c5d34-6c6c-7b49-ba62-ba073bdb4bb8:d846da2398453e66603ba56d26275514b8898ff1; messagesUtk=99014e34c16541bdbc0deac7ce71f413; mm_session=d3fcd950e64ee0549f5349ec0eeb3041d412cca3--d640c239a3bc84cd50355f7116696c109dc7e95ea4e87320ab376d43b13c0d8b; __hstc=227173954.a19db23b9cca668b15aec293f33920dd.1702370755916.1702379291756.1702379738802.6; __hssrc=1; __hssc=227173954.1.1702379738802; _ga_GXJVPD8HB5=GS1.1.1702379287.4.1.1702379755.0.0.0",
    "Content-Length": "0",
    "Accept": "*/*",
    "X-Csrf-Token": "7ad7ff8710252965098eeb1ca66d61d1c8f5a439",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.199 Safari/537.36",
    "Origin": "https://www.maxmind.com",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://www.maxmind.com/en/geoip2-precision-demo",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "Priority": "u=1, i"
}


response = requests.post(url, headers=headers)
token = ""
if response.status_code == 201:
    json_data = response.json()
    get_token = json_data.get("token")
    if get_token:
        print(f"Token: {get_token}")
        token = get_token
    else:
        print("Token not found in the response.")
else:
    print(f"Request failed with status code {response.status_code}.")
    print(response.text)

# Шаг 3: Запрос с токеном для получения timezone

url = "https://geoip.maxmind.com/geoip/v2.1/city/" + ip_address
params = {"demo": "1"}

headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5",
    "Authorization": "Bearer " + token,
    "Connection": "keep-alive",
    "DNT": "1",
    "Host": "geoip.maxmind.com",
    "Origin": "https://www.maxmind.com",
    "Referer": "https://www.maxmind.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Sec-GPC": "1",
    "TE": "trailers",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0"
}

response = requests.get(url, params=params, headers=headers)

timezone = ""
if response.status_code == 200:
    print(response.json())  # Assuming the response is JSON
    geoip2 = response.json()
    get_timezone = geoip2.get('location', {}).get('time_zone')
    timezone = get_timezone

    # Вывод результата
    print("Таймзона:", timezone)
else:
    print(f"Request failed with status code {response.status_code}.")
    print(response.text)

url = "https://gist.github.com/salkar/19df1918ee2aed6669e2"

response = requests.get(url)

if response.status_code == 200:
    target_timezone = timezone

    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим все элементы <td> с классом "blob-code-inner"
    td_elements = soup.find_all('td', class_='blob-code-inner')

    # Извлекаем названия регионов и соответствующие им таймзоны с использованием регулярного выражения
    region_timezone_pattern = re.compile(r'\["(.*?)", "(.*?)"]')
    region_timezone_list = [region_timezone_pattern.search(td.text).groups() if region_timezone_pattern.search(td.text) else (None, None) for td in td_elements]

    # Открываем файл для записи
    output_filename = f"regions_in_{target_timezone.replace('/', '_')}.txt"
    with open(output_filename, 'w') as file:
        for region, timezone in region_timezone_list:
            if region and timezone and target_timezone == timezone:
                file.write(f"Регион: {region}, Таймзона: {timezone}\n")

        print(f"Регионы входящие в таймзону {target_timezone} сохранены в файл {output_filename}")
else:
    print(f"Ошибка запроса. Код статуса: {response.status_code}")

