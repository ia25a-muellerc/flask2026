from db import get_db
from flask import current_app

def add_order(date, status, shipping_address, price):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO orders (date, status, shipping_address, price, canceled) VALUES (%s, %s, %s, %s, %s)", (date, status, shipping_address, price, False)
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
            "SELECT * FROM orders WHERE id='%s'", ([id])
        )
        orders = cur.fetchall()
    except Exception as e:
        conn.rollback()
        current_app.logger.error(e)
    finally:
        cur.close()
    return orders

def cancel_order(id):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute(
            "UPDATE orders SET canceled = 'TRUE' WHERE id = %s;", (id)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        current_app.logger.error(e)
    finally:
        cur.close()