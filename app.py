from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservierungen.db'
app.config['SECRET_KEY'] = 'geheim'
db = SQLAlchemy(app)

class Reservierung(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    telefon = db.Column(db.String(20))
    simulator_typ = db.Column(db.String(50))
    anzahl = db.Column(db.Integer)
    datum = db.Column(db.String(20))
    uhrzeit = db.Column(db.String(20))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reservieren', methods=['POST'])
def reservieren():
    name = request.form['name']
    telefon = request.form['telefon']
    simulator_typ = request.form['simulator_typ']
    anzahl = request.form['anzahl']
    datum = request.form['datum']
    uhrzeit = request.form['uhrzeit']

    neue_reservierung = Reservierung(
        name=name,
        telefon=telefon,
        simulator_typ=simulator_typ,
        anzahl=anzahl,
        datum=datum,
        uhrzeit=uhrzeit
    )
    db.session.add(neue_reservierung)
    db.session.commit()

    flash("Deine Reservierung wurde weitergeleitet, ein Mitarbeiter wird sich zur Bestätigung bei dir melden.")
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    reservierungen = Reservierung.query.all()
    return render_template('admin.html', reservierungen=reservierungen)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=10000)
