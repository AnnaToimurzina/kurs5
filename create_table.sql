-- SQL-команды для создания таблиц

import psycopg2

CREATE TABLE company(company_id varchar(50) PRIMARY KEY,
company_name varchar(100) NOT NULL);



CREATE TABLE vacancy(vacancy_name varchar(100),
company_id varchar(100) REFERENCES company(company_id) NOT NULL,
salary_from INT,
salary_to INT)
;

SELECT * FROM company;
SELECT * FROM vacancy;

DROP TABLE vacancy;
DROP TABLE company;