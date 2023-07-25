import psycopg2

class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(host='localhost', database='parsing_hh', user='postgres', password='Stepa123')
        self.cursor = self.conn.cursor()


    def get_companies_and_vacancies_count(self):
        query = '''SELECT company_name, COUNT(*) as vacancies_count FROM company
                   JOIN vacancy ON company.company_id = vacancy.company_id
                   GROUP BY company_name'''
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results

    def get_all_vacancies(self):
        query = '''SELECT company_name, vacancy_name, salary_from, salary_to FROM company
                   JOIN vacancy ON company.company_id = vacancy.company_id'''
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results

    def get_avg_salary(self):
        query = '''SELECT company_name, AVG(salary) FROM companies
        LEFT JOIN vacancies ON companies.company_id = vacancies.company_id
        GROUP BY company_name'''
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result[0]

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        query = '''SELECT company_name, vacancy_name, salary_from, salary_to FROM company
                   JOIN vacancy ON company.company_id = vacancy.company_id
                   WHERE salary_to > %s'''
        self.cursor.execute(query, (avg_salary,))
        results = self.cursor.fetchall()
        return results

    def get_vacancies_with_keyword(self, keyword):
        query = '''SELECT company_name, vacancy_name, salary_from, salary_to FROM company
                   JOIN vacancy ON company.company_id = vacancy.company_id
                   WHERE vacancy_name LIKE '%s%' '''
        self.cursor.execute(query, ('%' + keyword + '%'))
        results = self.cursor.fetchall()
        return results

    def close_connection(self):
        self.conn.close()