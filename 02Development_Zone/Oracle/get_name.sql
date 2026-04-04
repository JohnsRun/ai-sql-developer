create or REPLACE PROCEDURE get_employee_details (
    p_employee_id IN NUMBER
)
AS
    p_first_name employees.first_name%TYPE;
    p_last_name employees.last_name%TYPE;
    p_email employees.email%TYPE;
    p_hire_date employees.hire_date%TYPE;
    p_job_id employees.job_id%TYPE;
    p_salary employees.salary%TYPE;
BEGIN

    SELECT first_name, last_name, email, hire_date, job_id, salary
    INTO p_first_name, p_last_name, p_email, p_hire_date, p_job_id, p_salary
    FROM employees
    WHERE employee_id = p_employee_id;

    dbms_output.put_line('Employee Name: ' || p_first_name || ' ' || p_last_name);
END;
/   
