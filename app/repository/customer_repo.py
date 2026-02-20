from db import get_db


def create_customer(salutation, name, surname, email, password, street, city, postal_code, country):
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
        INSERT INTO customer (salutation, name, surname, email, password, address_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING customer_id
        """,
        (salutation, name, surname, email, password, address_id)
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
        SELECT c.customer_id, c.salutation, c.name, c.surname, c.email, c.password,
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
            "salutation": row[1],
            "name": row[2],
            "surname": row[3],
            "email": row[4],
            "password": row[5],
            "address": row[6],
            "city": row[7],
            "zip": row[8],
            "country": row[9]
        }
    return None


def email_exists(email):
    """Prüft ob eine E-Mail bereits existiert"""
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT 1 FROM customer WHERE email = %s", (email,))
    return cursor.fetchone() is not None


def delete_customer(email):
    """Löscht einen Kunden und seine Adresse anhand der E-Mail"""
    db = get_db()
    cursor = db.cursor()

    # Erst address_id holen
    cursor.execute(
        "SELECT address_id FROM customer WHERE email = %s",
        (email,)
    )
    result = cursor.fetchone()
    address_id = result[0] if result else None

    # Kunde löschen
    cursor.execute("DELETE FROM customer WHERE email = %s", (email,))

    # Adresse löschen (falls vorhanden)
    if address_id:
        cursor.execute("DELETE FROM customer_address WHERE address_id = %s", (address_id,))

    db.commit()
    return True


def update_customer(old_email, name, surname, new_email):
    """Aktualisiert die Kundendaten in der Datenbank"""
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        """
        UPDATE customer
        SET name = %s, surname = %s, email = %s
        WHERE email = %s
        """,
        (name, surname, new_email, old_email)
    )

    db.commit()
    return cursor.rowcount > 0
