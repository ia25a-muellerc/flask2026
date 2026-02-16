from fpdf import FPDF
from datetime import datetime

def generate_bestellbestaetigung(order_number, user_name, user_surname, user_address, user_zip, user_city, price, quantity):

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)


    content = (
        f"Betreff: Ihre Bestellung bei DeskDunk - Bestätigung\n\n"
        f"Hallo {user_name} {user_surname},\n\n"
        f"vielen Dank für Ihre Bestellung bei DeskDunk!\n"
        f"Wir freuen uns, Ihnen bestätigen zu können, dass Ihre Bestellung erfolgreich eingegangen ist.\n\n"
        f"BESTELLDETAILS\n"
        f"---------------\n"
        f"Bestellnummer: {order_number}\n"
        f"Bestelldatum: {datetime.today().strftime('%d.%m.%Y')}\n"
        f"Artikel: Mini-Bürobasketballkorb\n"
        f"Menge: {quantity}\n"
        f"Preis pro Artikel: CHF {price:.2f}\n"
        f"Gesamtpreis: CHF {quantity * price:.2f}\n"
        f"Versandart: Expressversand\n\n"
        f"LIEFERADRESSE\n"
        f"---------------\n"
        f"{user_name} {user_surname}\n"
        f"{user_address}\n"
        f"{user_zip} {user_city}\n\n"
        f"Ihre Bestellung wird nun bearbeitet und voraussichtlich in 2 Tagen versendet.\n"
        f"Sobald Ihr Paket unterwegs ist, erhalten Sie eine Versandbestaetigung mit Tracking-Informationen.\n\n"
        f"Wir danken Ihnen für Ihr Vertrauen und wuenschen viel Spass!\n\n"
        f"Bei Fragen oder Problemen:\n"
        f"Email: deskdunker@gmail.com\n"
        f"Tel: 079 700 62 83\n\n"
        f"Ihr Team von DeskDunk"
    )

    pdf.multi_cell(190, 8, txt=content, align='L')

    pdf_bytes = pdf.output()
    if isinstance(pdf_bytes, bytearray):
        pdf_bytes = bytes(pdf_bytes)
    return pdf_bytes
