from db import get_db
from flask import current_app

def add_account(name, surname, email, password, address, zip_code, city, country):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO accounts (name, surname, email, password, address, zip_code, city, country) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (name, surname, email, password, address, zip_code, city, country)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        current_app.logger.error(e)
    finally:
        cur.close()

def get_all_products():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders")
    orders = cur.fetchall()
    cur.close()
    return orders

def get_by_id(id):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT * FROM accounts WHERE id='%s'", ([id])
        )
        orders = cur.fetchall()
    except Exception as e:
        conn.rollback()
        current_app.logger.error(e)
    finally:
        cur.close()
    return orders

def get_by_email(email):
    conn = get_db()
    cur = conn.cursor()
    account = None
    try:
        cur.execute(
            "SELECT * FROM accounts WHERE email=%s", ([email])
        )
        account = cur.fetchall()
    except Exception as e:
        conn.rollback()
        current_app.logger.error(e)
    finally:
        cur.close()
    return account

def delete_account(email):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute(
            "DELETE FROM accounts WHERE email=%s", ([email])
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        current_app.logger.error(e)
    finally:
        cur.close()

def change_account_info(name, surname, email, id):
    conn = get_db()
    cur = conn.cursor()
    succeeded = False
    try:
        cur.execute(
            "UPDATE accounts SET name = %s WHERE id = %s;", (name, id)
        )
        cur.execute(
            "UPDATE accounts SET surname = %s WHERE id = %s;", (surname, id)
        )
        cur.execute(
            "UPDATE accounts SET email = %s WHERE id = %s;", (email, id)
        )
        conn.commit()
        succeeded = True
    except Exception as e:
        conn.rollback()
        current_app.logger.error(e)
    finally:
        cur.close()
    return succeeded
