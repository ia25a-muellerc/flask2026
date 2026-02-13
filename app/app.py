import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
from dotenv import load_dotenv # Lädt .env Datei
from services import math_service
from config import DevelopmentConfig, ProductionConfig
import db
from repository import orders_repo, accounts_repo
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from datetime import date

# Definieren einer Variable, die die aktuelle Datei zum Zentrum
# der Anwendung macht.
app = Flask(__name__)

"""
Festlegen einer Route für die Homepage. Der String in den Klammern
bildet das URL-Muster ab, unter dem der folgende Code ausgeführt
werden soll.                                                                                                                                                                                                                                                                        
z.B.
* @app.route('/')    -> http://127.0.0.1:5000/
* @app.route('/home') -> http://127.0.0.1:5000/home
"""

#-------------------------------
#Vorbereitungen
# 1. .env laden (macht lokal Variablen verfügbar, auf Render passiert nichts)
load_dotenv()


# 2. Config wählen
if os.environ.get('FLASK_ENV') == 'development':
    app.config.from_object(DevelopmentConfig)
else:
    app.config.from_object(ProductionConfig)
#-------------------------------

db.init_app(app)

# mock data
languages = [
    {"name": "Python", "creator": "Guido van Rossum", "year": 1991},
    {"name": "JavaScript", "creator": "Brendan Eich", "year": 1995},
    {"name": "Java", "creator": "James Gosling", "year": 1995},
    {"name": "C#", "creator": "Microsoft", "year": 2000},
    {"name": "Ruby", "creator": "Yukihiro Matsumoto", "year": 1995},
]


# In-memory User-Store (nur fuer aktuelle Laufzeit)


@app.route('/')
def home():
    print(math_service.add(1.0, 2.0))
    app.logger.info("Rendering home page")
    return render_template("home.html")

@app.route('/result/', defaults={'name': 'Guest'})
@app.route('/result/<name>')
def result(name) -> str:
    app.logger.info(f"Showing result for {name}")
    return render_template("result.html", name=name)

@app.route("/about")
def about() -> str:
    return render_template("about.html", languages=languages)

@app.route("/warenkorb")
def warenkorb() -> str:
    # Warenkorb aus Session holen oder initialisieren
    if 'cart_quantity' not in session:
        session['cart_quantity'] = 1
    quantity = session['cart_quantity']
    total = quantity * 30.00
    return render_template("warenkorb.html", quantity=quantity, total=f"{total:.2f}")

@app.route("/payment")
def payment() -> str:
    return render_template("payment.html")

@app.route("/data")
def data() -> str:
    return render_template("data.html", languages=languages)

@app.route("/profile", methods=["GET", "POST"])
def profile():
    # Prüfen ob Benutzer eingeloggt ist
    if not session.get("user_email"):
        # Nicht eingeloggt -> zum Login weiterleiten
        return redirect(url_for("signin"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        surname = request.form.get("surname", "").strip()
        email = request.form.get("email", "").strip()
        user = accounts_repo.get_by_email(session['user_email'])
        id = user[0][0]
        succeeded = accounts_repo.change_account_info(name, surname, email, id)
        if succeeded:
            session['user_name'] = name
            session['user_surname'] = surname
            session['user_email'] = email
        else:
            app.logger.error("Couldn't change account info. Try again.")

        app.logger.info(f"Profile updated: {session.get('user_name')} {session.get('user_surname')}")
        return redirect(url_for("home"))

    return render_template("data.html")

@app.route("/shipping")
def shipping() -> str:
    return render_template("shipping.html", languages=languages)

@app.route("/contact")
def contact() -> str:
    return render_template("contact.html", languages=languages)

@app.route("/signin", methods=["GET", "POST"])
def signin() -> str:
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not email or not password:
            return render_template("signin.html", languages=languages, error="Email und Passwort erforderlich")

        #user = user_store.get(email)
        user = accounts_repo.get_by_email(email)
        if user == []:
            return render_template("signin.html", languages=languages, error="Kein Konto gefunden. Bitte registrieren.")

        if user[0][4] != password:
            return render_template("signin.html", languages=languages, error="Falsches Passwort")

        # Session speichern (nur fuer Browser-Sitzung, nicht permanent)
        session["user_email"] = user[0][3]
        session["user_name"] = user[0][1]
        session["user_surname"] = user[0][2]
        session["user_address"] = user[0][5]
        session["user_zip"] = user[0][6]
        session["user_city"] = user[0][7]
        session["user_country"] = user[0][8]

        app.logger.info(f"User logged in: {email}")
        return redirect(url_for("home"))

    return render_template("signin.html", languages=languages)

@app.route("/logout")
def logout():
    session.clear()
    #app.logger.info("User logged out")
    return redirect(url_for("home"))

@app.route("/delete_profile")
def delete_profile():
    """Löscht das Profil des eingeloggten Benutzers"""
    if session.get("user_email"):
        email = session.get("user_email")
        accounts_repo.delete_account(email)
        session.clear()
    return redirect(url_for("home"))

@app.route("/api/user")
def get_user():
    """API Endpoint für aktuellen User"""
    if 'user_email' in session:
        return jsonify({
            'logged_in': True,
            'email': session.get('user_email'),
            'name': session.get('user_name'),
            'surname': session.get('user_surname', ''),
        })
    else:
        return jsonify({'logged_in': False})

@app.route("/popUpPayment")
def popUpPayment() -> str:
    return render_template("popUpPayment.html", languages=languages)

@app.route("/popUpSaved")
def popUpSaved() -> str:
    return render_template("popUpSaved.html", languages=languages)

@app.route("/add-order", methods=["POST"])
def add_order() -> str:
    order_date = date.today()
    app.logger.info(order_date)
    status = "Ordered"
    shipping_address = request.form["address"] + ", " + request.form["zip"] + ", " + request.form["city"] + ", " + request.form["country"]
    price = 30
    app.logger.info(price)
    account_id = accounts_repo.get_by_email(request.form['email'])[0][0]
    orders_repo.add_order(order_date, status, shipping_address, price, account_id)
    return redirect(url_for("popUpPayment"))

@app.route("/cancel-order", methods=["POST"])
def cancel_order() -> str:
    id = request.form['order_id']
    orders_repo.cancel_order(id)
    return redirect(url_for("orders"))

@app.route("/download-order", methods=["POST"])
def download_order() -> str:
    id = int(request.form['order_id'])
    orders = orders_repo.get_by_id(id)
    generate_pdf(orders)
    return send_file("static/Order_Confirmation.pdf", as_attachment=True)

@app.route("/orders")
def orders() -> str:
    orders = orders_repo.get_all_products()
    return render_template("orders.html", orders=orders)

@app.route("/submit", methods=["POST"])
def submit():
    app.logger.info("Form submitted")
    name = request.form.get("name")
    return redirect(url_for("result", name=name))

@app.route("/register", methods=["GET", "POST"])
def register() -> str:
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        surname = request.form.get("surname", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        password_confirm = request.form.get("password_confirm", "").strip()
        address = request.form.get("address", "").strip()
        zip_code = request.form.get("zip", "").strip()
        city = request.form.get("city", "").strip()
        country = request.form.get("country", "").strip()

        if not all([name, surname, email, password, password_confirm, address, zip_code, city, country]):
            return render_template("register.html", error="Bitte alle Felder ausfuellen")

        if password != password_confirm:
            return render_template("register.html", error="Passwoerter stimmen nicht ueberein")

        if accounts_repo.get_by_email(email) != []:
            return render_template("register.html", error="Account existiert bereits")

        #user_store[email] = {
        #    "name": name,
        #    "surname": surname,
        #    "email": email,
        #    "password": password,  # Demo-only
        #    "address": address,
        #    "zip": zip_code,
        #    "city": city,
        #    "country": country,
        #}

        accounts_repo.add_account(name, surname, email, password, address, zip_code, city, country)

        session["user_name"] = name
        session["user_surname"] = surname
        session["user_email"] = email
        session["user_address"] = address
        session["user_zip"] = zip_code
        session["user_city"] = city
        session["user_country"] = country

        app.logger.info(f"User registered: {email}")
        return redirect(url_for("home"))

    return render_template("register.html")


def generate_pdf(orders):
    id = orders[0][0]
    date = orders[0][1]
    shipping_address = orders[0][3]
    price = orders[0][4]
    amount = price / 30
    my_doc = SimpleDocTemplate("app/static/Order_Confirmation.pdf")
    sample_style_sheet = getSampleStyleSheet()
    paragraph_1 = Paragraph("Your Order confirmation", sample_style_sheet['Heading1'])
    paragraph_2 = Paragraph(
        "Your Order ID is: " + str(id) + 
        "<br/>Your Order was created on " + str(date) + 
        "<br/>Your shipping address is: " + shipping_address + 
        "<br/>You ordered Desk Dunk " + str(amount) + "x" +
        "<br/>The final cost of your Order is: " + str(price),
        sample_style_sheet['BodyText']
    )
    flowables = []
    flowables.append(paragraph_1)
    flowables.append(paragraph_2)
    my_doc.build(flowables)

if __name__ == '__main__':
    app.run(port=5000)
