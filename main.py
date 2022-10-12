import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import csv


def main():
    header = Headers(headers=True).generate()

    main_url = f'https://mediakit.iportal.ru/our-team#team#!/tab/219191124-1'
    res = requests.get(url=main_url, headers=header).text
    soup = BeautifulSoup(res, 'lxml')

    items2 = soup.find('div', {'id': 'allrecords'}).findAll('div', {'data-elem-type': 'text',
                                                                    'data-field-top-value': 1})  # парсим города
    items21 = soup.find('div', {'id': 'allrecords'}).findAll('div', {'data-elem-type': 'text',
                                                                     'data-field-top-value': 0})  # парсим города под другим айди
    items2 += items21

    items3 = soup.find('div', {'id': 'allrecords'}).findAll('div', {'data-elem-type': 'text',
                                                                    'data-field-top-value': 200})  # парсим имена
    items31 = soup.find('div', {'id': 'allrecords'}).findAll('div', {'data-elem-type': 'text',
                                                                     'data-field-top-value': 209})  # парсим имена под другим айди
    items3 += items31

    items4 = soup.find('div', {'id': 'allrecords'}).findAll('div', {'data-elem-type': 'text',
                                                                    'data-field-top-value': 237})  # парсим работу
    items41 = soup.find('div', {'id': 'allrecords'}).findAll('div', {'data-elem-type': 'text',
                                                                     'data-field-top-value': 245})  # парсим работу под другим айди
    items4 += items41

    city = []
    for item in items2:
        city.append(item.text.replace('\n', ''))  # записываем в список города и убираем лишнее

    name = []
    for item in items3:
        name.append(item.text.replace('\n', ''))  # записываем в список имена и убираем лишнее

    mail = []
    for item in items4:
        t = item.text.replace('\n', '').split('8 800 2000-383, доб.')
        try:
            mail.append(t[1][5:])  # записываем в список почты, обрезаем должности
        except:
            mail.append(t[0][16:])

    job = []
    for item in items4:
        t = ''.join(item.text.replace('\n', '').split('8 800 2000-383, доб.')[
                    :1])  # записываем в список должности и почти убираем почты
        job.append(t)

    with open('data.csv', 'w', newline='', encoding="utf8") as file:
        writer = csv.writer(file)
        for i in range(50):
            try:
                writer.writerow([city[i], name[i], mail[i], job[i]])  # записываем в таблицу все данные

            except Exception as err:
                print(err)


if __name__ == "__main__":
    main()
