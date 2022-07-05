USE employees;

#Contagem de funcionarios.
SELECT count(*) FROM employees;

#Estrutura de colunas e tipos de dados.
DESCRIBE employees;

#Listando apenas um registro da tabela.
SELECT * FROM employees LIMIT 1;

# Listando os funcionarios, seus salários e títulos.
SELECT    emp.emp_no
        , emp.first_name
        , emp.last_name
        , sal.salary
        , titles.title 
FROM employees emp 
INNER JOIN (SELECT emp_no, MAX(salary) as salary 
            FROM salaries GROUP BY emp_no) 
    sal ON sal.emp_no = emp.emp_no 
    INNER JOIN titles 
    ON titles.emp_no = emp.emp_no 
    LIMIT 10;
