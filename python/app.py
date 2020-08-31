import os
from forms import  AddForm , DelForm
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sqlite3
#from models import customer,ticket,slot



app = Flask(__name__)


db = 'users.db'
con = sqlite3.connect(db)
c = con.cursor()
#Key for Forms
app.config['SECRET_KEY'] = 'mysecretkey'

##########################################
########### SQL DATABASE ################# 
##########################################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

##########################################
########### Model classes ################# 
##########################################

class Customer(db.Model):
    __table__name = "customer"

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(20),nullable=False)
    phone = db.Column(db.String(10),nullable=False)
    ticket = db.relationship('Ticket',backref='customer',uselist=False)

    def __init__(self,name,phone):
        self.name = name
        self.phone = phone

    def __repr__(self):
            return f"Name: {self.name} | Phone: {self.phone} | Ticket ID: {self.ticket.id} | Time: {self.ticket.time}"
        


class Ticket(db.Model):
    __table__name = "ticket"

    id = db.Column(db.Integer,primary_key = True)
    slot = db.Column(db.String(10))
    cid = db.Column(db.Integer,db.ForeignKey('customer.id'),nullable=False)

    def __init__(self,cid,slot):
        self.cid =cid
        self.slot =slot

        


class Slot(db.Model):
    __table__name = "slot"

    sid = db.Column(db.Integer,primary_key=True)
    time = db.Column(db.Text)
    ticket_id = db.Column(db.Integer,db.ForeignKey('ticket.tid'))

    def __init__(self,time,ticket_id):
        self.time = time
        self.ticket_id = ticket_id


##########################################
########### VIEWS WITH FORMS #############
##########################################
ticket_count = 0

@app.route("/")
def index():
        return render_template('home.html')

@app.route("/book_ticket",methods=['GET', 'POST'])
def book_ticket():
        form = AddForm()
        global ticket_count
        ticket_count = ticket_count + 1
        if form.validate_on_submit() and ticket_count<=20:
                name = form.name.data
                phone = form.phone.data
                slot = form.slot.data
                customer = Customer(name,phone)
                db.session.add(customer)
                db.session.commit()
                ticket = Ticket(customer.id,slot)
                db.session.add(ticket)
                db.session.commit()
                return redirect(url_for('ticket_booked'))
        elif ticket_count>20:
                return redirect(url_for('all_seat_booked'))
        return render_template('bookTicket.html',form=form)

@app.route('/all_seat_booked')
def all_seat_booked():
        return render_template("seatFull.html")

@app.route("/view_tickets")
def view_tickets():
         c.execute("SELECT * FROM ticket")
         tickets = c.fetchall()
         return render_template('viewTickets.html',tickets = tickets)
        

@app.route("/del_ticket",methods=['GET', 'POST'])
def del_ticket():
        form = DelForm()
        if form.validate_on_submit():
                id = form.id.data        
                ticket = Ticket.query.get(id)
                db.session.delete(ticket)
                db.session.commit()
                return redirect(url_for('ticketDeleted'))
        return render_template('deleteTicket.html')
                

@app.route("/ticket_booked")
def ticket_booked():
        return render_template('ticketBooked.html')

@app.route("/ticket_deleted")
def ticket_deleted():
        return render_template('ticketDeleted.html')


if __name__ == '__main__':
    app.run(debug=True)