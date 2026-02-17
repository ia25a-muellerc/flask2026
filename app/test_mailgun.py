#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, 'C:\\ZKB\\flask2026\\app')

from dotenv import load_dotenv
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

from services.mailgun_service import send_order_email

# Test mit Daten
result = send_order_email(
    order_number=12345,
    customer_name="Test Kunde",
    customer_email="test@example.com",
    customer_address="Teststrasse 123",
    customer_zip="8000",
    customer_city="Zürich",
    quantity=1,
    price=30.00
)

print("=" * 60)
print("MAILGUN TEST RESULT:")
print("=" * 60)
print(f"Success: {result['success']}")
print(f"Message: {result['message']}")
print("=" * 60)
