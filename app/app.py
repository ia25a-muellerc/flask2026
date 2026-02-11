import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from dotenv import load_dotenv # Lädt .env Datei
from services import math_service
from config import DevelopmentConfig, ProductionConfig

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
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))


# 2. Config wählen
if os.environ.get('FLASK_ENV') == 'development':
    app.config.from_object(DevelopmentConfig)
else:
    app.config.from_object(ProductionConfig)
#-------------------------------

# mock data
languages = [
    {"name": "Python", "creator": "Guido van Rossum", "year": 1991},
    {"name": "JavaScript", "creator": "Brendan Eich", "year": 1995},
    {"name": "Java", "creator": "James Gosling", "year": 1995},
    {"name": "C#", "creator": "Microsoft", "year": 2000},
    {"name": "Ruby", "creator": "Yukihiro Matsumoto", "year": 1995},
]


# In-memory User-Store (nur fuer aktuelle Laufzeit)
user_store = {}




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


@app.route("/api/cart/update", methods=["POST"])
def update_cart():
    """Aktualisiert die Warenkorb-Menge"""
    data = request.get_json()
    quantity = int(data.get('quantity', 1))
    
    if quantity > 0:
        session['cart_quantity'] = quantity
        session.modified = True
    
    total = quantity * 30.00
    return jsonify({
        'quantity': quantity,
        'total': f"{total:.2f}"
    })


@app.route("/api/cart", methods=["GET"])
def get_cart():
    """Gibt die aktuelle Warenkorb-Menge zurück"""
    quantity = int(session.get('cart_quantity', 1))
    total = quantity * 30.00
    return jsonify({
        'quantity': quantity,
        'total': f"{total:.2f}"
    })


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
        session['user_name'] = request.form.get("name", "").strip()
        session['user_surname'] = request.form.get("surname", "").strip()
        session['user_email'] = request.form.get("email", "").strip()

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

        user = user_store.get(email)
        if not user:
            return render_template("signin.html", languages=languages, error="Kein Konto gefunden. Bitte registrieren.")

        if user.get("password") != password:
            return render_template("signin.html", languages=languages, error="Falsches Passwort")

        # Session speichern (nur fuer Browser-Sitzung, nicht permanent)
        session["user_email"] = user.get("email", "")
        session["user_name"] = user.get("name", "")
        session["user_surname"] = user.get("surname", "")
        session["user_address"] = user.get("address", "")
        session["user_zip"] = user.get("zip", "")
        session["user_city"] = user.get("city", "")
        session["user_country"] = user.get("country", "")

        app.logger.info(f"User logged in: {email}")
        return redirect(url_for("home"))

    return render_template("signin.html", languages=languages)

@app.route("/logout")
def logout():
    session.clear()
    app.logger.info("User logged out")
    return redirect(url_for("home"))

@app.route("/delete_profile")
def delete_profile():
    """Löscht das Profil des eingeloggten Benutzers"""
    if session.get("user_email"):
        email = session.get("user_email")
        # Benutzer aus dem user_store löschen (falls vorhanden)
        if email in user_store:
            del user_store[email]
            app.logger.info(f"Profile deleted: {email}")
        # Session löschen und zur Startseite umleiten
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

@app.route("/orders")
def minigame() -> str:
    return render_template("orders.html", languages=languages)

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

        if email in user_store:
            return render_template("register.html", error="Account existiert bereits")

        user_store[email] = {
            "name": name,
            "surname": surname,
            "email": email,
            "password": password,  # Demo-only
            "address": address,
            "zip": zip_code,
            "city": city,
            "country": country,
        }

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


if __name__ == '__main__':
    app.run(port=5000)
