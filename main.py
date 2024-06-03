from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_hashing import Hashing
import psycopg2
import psycopg2.extras
import hashlib


app = Flask(__name__)
hashing = Hashing(app)
app.secret_key = 'super secret key'

db_host = "rc1d-cmaunk4nlmo3ymjk.mdb.yandexcloud.net"
db_name = "dbKostyrin"
db_user = "kostyrin"
db_pass = "tW1q$@r@2d"


conn = psycopg2.connect(dbname = db_name, port = 6432, user = db_user, password = db_pass, host = db_host)

@app.route('/')
def index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT t.id_place, t.palce_location, t.place_state, t.place_country FROM datalogical.place t order by t.place_country "
    cur.execute(s)
    list_places = cur.fetchall()
    return render_template('index.html', list_users = list_places)
    

@app.route('/add_place', methods=['POST'])
def add_place():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        location = request.form['location']
        state = request.form['state']
        country = request.form['country']
        id = hashlib.md5((location+state+country).encode())

        cur.execute("INSERT INTO datalogical.place (id_place, palce_location, place_state, place_country) VALUES (%s,%s,%s,%s)", (id.hexdigest(), location, state, country))
        conn.commit()
        flash('Place added successfully', category='success')
        print(id, location, state, country)
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)