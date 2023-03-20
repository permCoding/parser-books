from bs4 import BeautifulSoup
from time import sleep
import json
from parsing import get_html


def get_books(html):
    """получить список с одной страницы"""
    soup = BeautifulSoup(html, 'html.parser')
    prods = soup.find_all('article')
    books = []  # этот список будем заполнять
    pref = "https://www.chitai-gorod.ru"
    for prod in prods:
        head = prod.find('div', class_="product-title__head").text.strip()
        author = prod.find('div', class_="product-title__author").text.strip()
        price = prod.find('div', class_="product-price__value").text.strip().replace('\xa0','')
        ref = pref + prod.find('a', class_="product-card__row")['href']
        books.append([head,author,price,ref])  # добавим данные о книге
    return books

   
def get_all_books(count=0):
    """получить данные со всех count страниц"""
    all_books = []  # тут будет итоговый список
    page = 0  # ведём учёт просмотренных страниц
    while True:  # цикл перебора всех страниц
        page += 1  # новый номер страницы
        if count != 0 and page > count:
            break  # если больше не надо страниц

        sleep(1)  # делаем паузу между страницами
        print(f"page={page}")  # для контроля выводим номер текущей страницы
        
        url = f"https://www.chitai-gorod.ru/catalog/books/nauchnaya-fantastika-9693?page={page}"
        try:
            html = get_html(url)  # получить очередную страницу
            lst = get_books(html)  # получить с неё книги
            all_books.extend(lst)  # добавить их в общий список
        except:
            print('Ошибки на странице')
    return all_books

    
def write_json(filename, lst):
    name_columns = ['id', 'head', 'author', 'price', 'ref']  # названия полей для записи
    lst_w = []  # тут будем формировать список объектов
    for i in range(len(lst)):
        values = [i+1] + lst[i]  # номер + поля объекта
        obj = dict(zip(name_columns, values))  # сформируем объект
        lst_w.append(obj)  # добавим в список
    # теперь уже будем выводить список в файл
    with open(filename, 'w', encoding='utf8') as f:
        json.dump(lst_w, f, indent=4, ensure_ascii=False)


count = 4  # сколько страниц просмотреть
all_books = get_all_books(count)  # получить список всех книг
write_json('all_books.json', all_books)  # записать его в формате json

"""
собственно программа - это строки 54, 55, 56
и к ним три функции сверху
"""