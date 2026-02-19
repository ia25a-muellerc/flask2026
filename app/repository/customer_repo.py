from db import get_db


def create_customer(name, surname, email, password, street, city, postal_code, country):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        INSERT INTO customer_address (street, city, postal_code, country)
        VALUES (%s, %s, %s, %s)
        RETURNING address_id
        """,
        (street, city, postal_code, country)
    )
    address_id = cursor.fetchone()[0]

    cursor.execute(
        """
        INSERT INTO customer (name, surname, email, password, address_id)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING customer_id
        """,
        (name, surname, email, password, address_id)
    )
    customer_id = cursor.fetchone()[0]

    db.commit()
    return customer_id


def get_customer_by_email(email):
    """Holt einen Kunden anhand der E-Mail"""
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        SELECT c.customer_id, c.name, c.surname, c.email, c.password,
               a.street, a.city, a.postal_code, a.country
        FROM customer c
        LEFT JOIN customer_address a ON c.address_id = a.address_id
        WHERE c.email = %s
        """,
        (email,)
    )

    row = cursor.fetchone()
    if row:
        return {
            "customer_id": row[0],
            "name": row[1],
            "surname": row[2],
            "email": row[3],
            "password": row[4],
            "address": row[5],
            "city": row[6],
            "zip": row[7],
            "country": row[8]
        }
    return None


def email_exists(email):
    """Prüft ob eine E-Mail bereits existiert"""
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT 1 FROM customer WHERE email = %s", (email,))
    return cursor.fetchone() is not None
