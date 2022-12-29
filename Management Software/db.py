import pymysql

try:
    connection = pymysql.connect(host="localhost", user="root", passwd="MySql", database="employee_management")

except:
    print("SQL Not Started")
else:
    print("Database Connected")

cursor = connection.cursor()

def display_all(id_value):
    query = "SELECT * FROM employees WHERE company_id=%s"

    cursor.execute(query, id_value)

    result = cursor.fetchall()

    return result


def login(email, password):
    query = "SELECT * FROM users WHERE email=%s AND password=%s"

    cursor.execute(query, (email,password))

    result = cursor.fetchone()

    if result:
        return True
    else:
        return False

def google_login(email):
    query = "SELECT * FROM users WHERE email=%s"

    cursor.execute(query, email)

    result = cursor.fetchone()

    if result:
        return True
    else:
        return False
    
def register(email, password, security_question, security_answer):

    check_query = "SELECT * FROM users WHERE email=%s"
    check_result = cursor.execute(check_query, email)

    if check_result:
        return "Email already Registered!"
    else:
        query = "INSERT INTO users (email, password, security_question, security_answer, type) VALUES (%s,%s,%s,%s,%s)"

        values = (email, password, security_question, security_answer, "normal")

        result = cursor.execute(query, values)

        connection.commit()

        if result:
            return "success"
        else:
            return "Failed to Register"

def google_register(email):
    check_query = "SELECT * FROM users WHERE email=%s"
    email_check = cursor.execute(check_query, email)
    
    if email_check:
        return "Email Already Registered! Login to Continue..."
    else:
        query = "INSERT INTO users(email, type) VALUES (%s, %s)"

        values = (email, "google")

        result = cursor.execute(query, values)

        connection.commit()

        if result:
            return "success"
        else:
            return "failed"

def reset_password(email, security_question, security_answer, new_password):

    check_query = "SELECT * FROM users WHERE email=%s AND type=%s"

    check_result = cursor.execute(check_query, (email, "normal"))

    if check_result:
        query = "SELECT * FROM users WHERE security_question=%s AND security_answer=%s"

        cursor.execute(query, (security_question, security_answer))

        result = cursor.fetchall()

        if result:
            update_query = "UPDATE users SET password=%s WHERE email=%s"
            update_result = cursor.execute(update_query, (new_password, email))
            connection.commit()

            if update_result:
                return "updated"
            else:
                return "failed"
        else:
            return "Security answer is Wrong"
    else:
        return "User Not Found or Registered with Google!"


def search_employee(search_by, search_text):
    query = "SELECT * FROM employees WHERE " + search_by + " = %s"

    cursor.execute(query, search_text)

    result = cursor.fetchall()

    return result

def add_employee(name, age, dob, gender, email, mobile, salary, address, image, user_id):
    query = "INSERT INTO employees(name, age, dob, gender, email, mobile, salary, address, image, company_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    values = (name, age, dob, gender, email, mobile, salary, address, image, user_id)

    result = cursor.execute(query, values)

    connection.commit()

    if result:
        return True
    else:
        return False


def update_employee(name, age, dob, gender, email, mobile, salary, address, image, emp_id):
    query = "UPDATE employees SET name=%s, age=%s, dob=%s, gender=%s, email=%s, mobile=%s, salary=%s, address=%s, image=%s WHERE id=%s"

    result = cursor.execute(query, (name, age, dob, gender, email, mobile, salary, address, image, emp_id))

    connection.commit()

    if result:
        return True
    else:
        return False


def delete_employee(emp_id):
    query = "DELETE FROM employees WHERE id = %s"

    result = cursor.execute(query, emp_id)

    connection.commit()

    if result:
        return True
    else:
        return False


def get_id(email):
    query = "SELECT id FROM users WHERE email=%s"

    cursor.execute(query, email)

    result = cursor.fetchone()

    return result


def change_password(email, old_password, new_password):
    check_query = "SELECT * FROM users WHERE email=%s AND type=%s"

    check_result = cursor.execute(check_query, (email, "normal"))

    if check_result:
        old_password_check = "SELECT * FROM users WHERE email=%s AND password=%s"

        check = cursor.execute(old_password_check, (email, old_password))

        if check:
            query = "UPDATE users SET password=%s WHERE email=%s"

            result = cursor.execute(query, (new_password, email))

            if result:
                return "success"
            else:
                return "Failed to Update Password"
        else:
            return "Old Password was Incorrect!"
    else:
        return "Google User can't Change Password"
    
