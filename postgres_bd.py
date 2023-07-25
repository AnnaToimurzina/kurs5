import psycopg2
import csv



def main():
        """Скрипт для заполнения данными таблиц в БД Postgres."""

'''Подключение к базе данных'''
conn = psycopg2.connect(host='localhost', database='parsing_hh', user='postgres', password='Stepa123')

'''Создание курсора для выполнения SQL-запросов'''
cur = conn.cursor()

'''Открыть CSV-файл с данными'''
try:
    with open('north_data\customers_data.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        ''' Прочитать и вставить данные в таблицу'''
        for row in reader:
            cur.execute('INSERT INTO company ("company_id", "company_name") VALUES (%s, %s)', row)
        conn.commit()

    with open('north_data\employees_data.csv', 'r') as file:
        reader = csv.reader(file)
        next(reader)
        'Прочитать и вставить данные в таблицу'
        for row1 in reader:
            cur.execute('INSERT INTO vacancy ("vacancy_name", "company_id", salary_from, salary_to) VALUES (%s, %s, %s, %s)', row1)
        conn.commit()



finally:
    conn.close()


if __name__ == "__main__":
    main()

# Вставка данных о вакансиях в таблицу vacancy
    for vacancy in data['items']:
        vacancy_name = vacancy['name']
        salary_from = vacancy['salary'].get('from') or 0
        salary_to = vacancy['salary'].get('to') or 0
        cursor.execute("INSERT INTO vacancy (vacancy_name, company_id, salary_from, salary_to) VALUES (%s, %s, %s, %s)",
                       (vacancy_name, company_id, salary_from, salary_to))