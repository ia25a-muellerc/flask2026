from db import get_db


def create_customer_payment(name, email, street, city, postal_code, country, payment_method):
    db = get_db()
    cursor = db.cursor()

    try:
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
            "SELECT payment_method_id FROM payment_method WHERE method = %s",
            (payment_method,)
        )
        payment_method_row = cursor.fetchone()

        if payment_method_row:
            payment_method_id = payment_method_row[0]
        else:
            cursor.execute(
                """
                INSERT INTO payment_method (method)
                VALUES (%s)
                RETURNING payment_method_id
                """,
                (payment_method,)
            )
            payment_method_id = cursor.fetchone()[0]

        cursor.execute(
            """
            INSERT INTO customer_payment (name, email, address_id, payment_method_id)
            VALUES (%s, %s, %s, %s)
            RETURNING customer_payment_id
            """,
            (name, email, address_id, payment_method_id)
        )
        customer_payment_id = cursor.fetchone()[0]

        db.commit()
        return customer_payment_id
    except Exception:
        db.rollback()
        raise
