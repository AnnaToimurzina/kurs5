from abc import ABC, abstractmethod

import psycopg2 as psycopg2
import requests
import sqlite3

class Abstract_Vacancy(ABC):
    """
    Абстрактный класс для работы с платформами по поиску вакансий по API.
    """
    @abstractmethod
    def get_hh_data(self):
        pass


employer_ids = [78817, 5374297, 139, 598471, 14809, 5756945, 5441909, 5819349, 1469550, 2324020]

class HH(Abstract_Vacancy):
    def __init__(self):
        pass

    def get_hh_data(self, url):
        response = requests.get(url)
        return response.json()

hh=HH()

conn = psycopg2.connect(host='localhost', database='parsing_hh', user='postgres', password='Stepa123')
cursor = conn.cursor()

# Заполнение таблицы данными
for employer_id in employer_ids:
    url = f'https://api.hh.ru/vacancies?employer_id={employer_id}&per_page=50'
    data = hh.get_hh_data(url)

    # Вставка данных о компании в таблицу company
    company_id = data['items'][0]['employer']['id']
    company_name = data['items'][0]['employer']['name']
    cursor.execute("INSERT INTO company (company_id, company_name) VALUES (%s, %s)", (company_id, company_name))

    conn.commit()


    # Вставка данных о вакансиях в таблицу vacancy
    for vacancy in data['items']:
        vacancy_name = vacancy['name']

        company_id = data['items'][0]['employer']['id']
        salary_from = 0 if vacancy['salary'] is None or vacancy['salary']['from'] is None  or vacancy['salary']['from'] == 'null' else vacancy['salary']['from']
        salary_to = 0 if vacancy['salary'] is None or vacancy['salary']['to'] is None or vacancy['salary']['to'] == 'null' else vacancy['salary']['to']
        cursor.execute("INSERT INTO vacancy (vacancy_name, company_id, salary_from, salary_to) VALUES (%s, %s, %s, %s)",
                       (vacancy_name, company_id, salary_from, salary_to))
        conn.commit()
print('Данные успешно загружены')

# Закрытие соединения с базой данных
conn.close()
