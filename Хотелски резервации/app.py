from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'tajna_lozinka'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rezervacii.db'
db = SQLAlchemy(app)

# Модел
class Rezervacija(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tip_nastan = db.Column(db.String(50), nullable=False)
    ime = db.Column(db.String(50), nullable=False)
    prezime = db.Column(db.String(50), nullable=False)
    telefon = db.Column(db.String(20), nullable=False)
    broj_gosti = db.Column(db.Integer, nullable=False)
    datum = db.Column(db.Date, nullable=False)
    tip_sala = db.Column(db.String(50), nullable=False)

# Админ податоци
load_dotenv()

ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')
ADMIN_HASH = generate_password_hash(ADMIN_PASSWORD)

# Сали
SALI = ['Тераса', 'Розе сала', 'Надворешен амбиент', 'Банкет сала', 'Базен']

# Почетна страна
@app.route('/', methods=['GET', 'POST'])
def rezervacija():
    slobodni_sali = SALI.copy()

    if request.method == 'POST':
        try:
            tip_nastan = request.form['tip_nastan']
            ime = request.form['ime']
            prezime = request.form['prezime']
            telefon = request.form['telefon']
            broj_gosti = int(request.form['broj_gosti'])
            datum = datetime.strptime(request.form['datum'], '%Y-%m-%d').date()
            tip_sala = request.form.get('tip_sala')

            # Проверки за условите на бројот на гости
            if tip_sala.lower() == 'тераса' and broj_gosti < 80:
                flash('НАПОМЕНА: За да ја резервирате Тераса мора да има најмалку 80 гости!', 'warning')
                return render_template('rezervacija.html', slobodni_sali=slobodni_sali)
            if tip_sala.lower() == 'тераса' and broj_gosti > 480:
                flash('НАПОМЕНА: Максималниот капацитет на летната Тераса е максимум 480 гости')
                return render_template('rezervacija.html', slobodni_sali=slobodni_sali)
            if tip_sala.lower() == 'базен' and broj_gosti < 15:
                flash('НАПОМЕНА: За да резервирате Базен бројот на гости треба да биде најмалку 15 гости')
                return render_template('rezervacija.html', slobodni_sali=slobodni_sali)
            if tip_sala.lower() == 'базен' and broj_gosti > 80:
                flash('НАПОМЕНА: Капацитетот на гости кај Базен е максимум 80 гости!', 'warning')
                return render_template('rezervacija.html', slobodni_sali=slobodni_sali)
            if tip_sala.lower() == 'розе сала' and broj_gosti < 80:
                flash('НАПОМЕНА: За да резервирате Розе сала бројот на гости треба да биде најмалку 80 гости')
                return render_template('rezervacija.html', slobodni_sali=slobodni_sali)
            if tip_sala.lower() == 'розе сала' and broj_gosti > 250:
                flash('НАПОМЕНА: Максималниот капацитет на Розе сала е максимум 250 гости')
                return render_template('rezervacija.html', slobodni_sali=slobodni_sali)
            if tip_sala.lower() == 'надворешен амбиент' and broj_gosti > 550:
                flash('НАПОМЕНА: Максималниот капацитет во Надворешниот простор-Кепенци изнесува до 550 гости')
                return render_template('rezervacija.html', slobodni_sali=slobodni_sali)
            if tip_sala.lower() == 'банкет сала' and broj_gosti > 120:
                flash('НАПОМЕНА: Максималниот капацитет во Банкет сала изнесува до 120 гости')
                return render_template('rezervacija.html', slobodni_sali=slobodni_sali)
            if tip_sala.lower() == 'банкет сала' and broj_gosti < 15:
                flash('НАПОМЕНА: За да резервирате Банкет сала бројот на гости треба да биде најмалку 15', 'warning')
                return render_template('rezervacija.html', slobodni_sali=slobodni_sali)

            # Проверка дали е зафатена салата на тој датум
            postoi = Rezervacija.query.filter_by(datum=datum, tip_sala=tip_sala).first()
            if postoi:
                najblisku = najdi_sloboden_datum(datum, tip_sala)
                flash(f'Салата "{tip_sala}" е веќе резервирана за {datum.strftime("%d.%m.%Y")}. Најблискиот слободен датум е {najblisku.strftime("%d.%m.%Y")}.', 'danger')
                zatvoreni = [r.tip_sala for r in Rezervacija.query.filter_by(datum=datum).all()]
                slobodni_sali = [s for s in SALI if s not in zatvoreni]
                return render_template('rezervacija.html', slobodni_sali=slobodni_sali)

            # Се е во ред, зачувај резервација
            nova = Rezervacija(
                tip_nastan=tip_nastan,
                ime=ime,
                prezime=prezime,
                telefon=telefon,
                broj_gosti=broj_gosti,
                datum=datum,
                tip_sala=tip_sala
            )
            db.session.add(nova)
            db.session.commit()
            flash('Резервацијата е успешно зачувана, ќе ве контактираме на вашиот телефонски број!', 'success')
            return redirect(url_for('rezervacija'))

        except Exception as e:
            flash(f'Грешка: {str(e)}', 'danger')

    # Секогаш ажурирај го списокот на слободни сали
    if request.method == 'GET':
        today = datetime.now().date()
        zatvoreni = [r.tip_sala for r in Rezervacija.query.filter_by(datum=today).all()]
        slobodni_sali = [s for s in SALI if s not in zatvoreni]

    return render_template('rezervacija.html', slobodni_sali=slobodni_sali)

# Логирање
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        korisnik = request.form['korisnik']
        lozinka = request.form['lozinka']
        if korisnik == ADMIN_USERNAME and check_password_hash(ADMIN_HASH, lozinka):
            session['admin'] = True
            return redirect(url_for('admin_panel'))
        else:
            flash('Неточни податоци за најава.', 'danger')
    return render_template('login.html')

# Одлогирање
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('login'))

# Админ панел
@app.route('/admin')
def admin_panel():
    if not session.get('admin'):
        return redirect(url_for('login'))
    rezervacii = Rezervacija.query.order_by(Rezervacija.datum.asc()).all()
    return render_template('admin.html', rezervacii=rezervacii)

# Бришење резервација
@app.route('/delete/<int:id>', methods=['POST'])
def delete_rezervacija(id):
    if not session.get('admin'):
        return redirect(url_for('login'))
    rezervacija = Rezervacija.query.get_or_404(id)
    db.session.delete(rezervacija)
    db.session.commit()
    flash('Резервацијата е избришана.', 'success')
    return redirect(url_for('admin_panel'))

# Пронаоѓање слободен датум
def najdi_sloboden_datum(datum, tip_sala):
    delta = timedelta(days=1)
    nova_data = datum + delta
    while True:
        if not Rezervacija.query.filter_by(datum=nova_data, tip_sala=tip_sala).first():
            return nova_data
        nova_data += delta

# Креирање на базата
with app.app_context():
    db.create_all()

#Сервер
if __name__ == '__main__':
    app.run(host='192.168.56.1', port=5000, debug=True)
