from db import get_db
from flask import current_app, session
import psycopg2.extras

def add_order(date, status, shipping_address, price, customer_id=None, customer_payment_id=None):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur.execute(
            """
            INSERT INTO orders (date, status, shipping_address, price, customer_id, customer_payment_id, canceled)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (date, status, shipping_address, price, customer_id, customer_payment_id, False)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        current_app.logger.error(e)
    finally:
        cur.close()

def get_all_orders():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM orders")
    orders = cur.fetchall()
    cur.close()
    return orders

def get_orders_by_customer_id(customer_id):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur.execute(
            "SELECT * FROM orders WHERE customer_id=%s", (customer_id,)
        )
        orders = cur.fetchall()
    except Exception as e:
        conn.rollback()
        current_app.logger.error(e)
    finally:
        cur.close()
    return orders

def get_by_id(id):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur.execute(
            "SELECT * FROM orders WHERE id=%s", (id,)
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
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        current_app.logger.info(f"Canceling order with id: {id}")
        cur.execute(
            "UPDATE orders SET canceled = TRUE WHERE id = %s;", (id,)
        )
        conn.commit()
        current_app.logger.info(f"Order {id} canceled successfully, rows affected: {cur.rowcount}")
    except Exception as e:
        conn.rollback()
        current_app.logger.error(f"Error canceling order: {e}")
    finally:
        cur.close()