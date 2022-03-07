import time

from bs4 import BeautifulSoup
import requests

start_time = time.time()


def main(url):
    proxy_list = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    rows = soup.find_all('tr')
    for row in rows:
        ip = row.contents[0].text
        port = row.contents[1].text
        anonym = row.contents[4].text
        seconn = row.contents[6].text

        if seconn == 'yes' and (anonym == 'anonymous' or anonym == 'elite proxy'):
            line = f'http://{ip}:{port}'
            proxies = {'http': line, 'https': line}

            try:
                test_ip = requests.get('https://httpbin.org/ip', proxies=proxies, timeout=3)
                res_ip = test_ip.json()['origin']
                origin = res_ip.split(',')

                if origin[0] == ip:
                    print('...Proxy ok! Appending proxy to proxy_list...')
                    proxy_list.append(line)
            except:
                print('...Bad proxy!...')

            save_proxies(proxy_list)


def save_proxies(proxy_list):
    with open('proxies.txt', 'w') as file:
        file.write('\n'.join(proxy_list))


if __name__ == '__main__':
    main('https://free-proxy-list.net/')
    finish_time = time.time() - start_time
    print(f"Затраченное на работу скрипта время: {finish_time}")
