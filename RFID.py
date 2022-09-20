from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

RFID_Web = Flask(__name__)
RFID_Web.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///RFID.db'
RFID_Web.config['SQLALCHEMY_BINDS'] = {'two' : 'sqlite:///RFLog.db'}
db = SQLAlchemy(RFID_Web)

class RFID(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

class RFLog(db.Model):
    __bind_key__ = 'two'
    id = db.Column(db.Integer, primary_key=True)
    name_new = db.Column(db.String(200), nullable=True)
    rfid_new = db.Column(db.String(200), nullable=True)
    result_new = db.Column(db.String(200), nullable=True)
    date_new = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name_new, rfid_new, result_new):
        self.name_new = name_new
        self.rfid_new = rfid_new
        self.result_new = result_new 

@RFID_Web.route('/')
def home():
    return render_template("home.html")

@RFID_Web.route('/users', methods=['POST','GET'])
def index():
    if request.method == 'POST':
        RFID_content = request.form['content']
        RFID_name = request.form['name']
        new_RFID = RFID(content=RFID_content, name=RFID_name)

        try:
            db.session.add(new_RFID)
            db.session.commit()
            return redirect('/users')
        except:
            return 'There was an issue adding your data'
    else:
        tasks = RFID.query.order_by(RFID.date_created).all()
        return render_template('index.html', tasks=tasks)


@RFID_Web.route('/log')
def logs():
    ldata = RFLog.query.order_by(RFLog.date_new).all()
    return render_template('logs.html',ldata=ldata)

@RFID_Web.route('/check', methods=['POST'])
def check_database():
    data = request.getjson()
    rfid = data['rfid'].strip()
    new_RLog = RFID.query.filter_by(content=rfid).first()
    if new_RLog is None:
        Ukrid = rfid
        Urid = RFLog('Unkown',Ukrid,'Accessed Denied')
        try:
            db.session.add(Urid)
            db.session.commit()
            return '''<h1> Accessed Denied </h1>'''
        except:
            return 'Does Not Work None'
    else:
        Crf = new_RLog.content
        Cname = new_RLog.name
        Cnew = RFLog(Cname,Crf,'Access Granted')

        try:
            db.session.add(Cnew)
            db.session.commit()
            return '''<h1> Access Granted</h1>'''
        except:
            return 'There was an issue in Check RFLog List'

@RFID_Web.route('/delete/<int:id>')
def delete(id):
    RFID_to_delete = RFID.query.get_or_404(id)

    try:
        db.session.delete(RFID_to_delete)
        db.session.commit()
        return redirect('/users')
    except:
        return 'There was a problem deleting that RFID'

@RFID_Web.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task = RFID.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        task.name = request.form['name']

        try:
            db.session.commit()
            return redirect('/users')
        except:
            return 'There was an issue updating your RFID'
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    RFID_Web.run(debug=True)