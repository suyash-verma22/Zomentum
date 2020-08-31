from app import db

#########################
#####-Customer Model-####
#########################

class Customer(db.Model):
    __table__name = "customer"

    cid = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.Text)
    phone = db.Column(db.Text)
    ticket_id = db.Column(db.Integer,db.ForeignKey('ticket.tid'))

    def __init__(self,name,phone,ticket_id):
        self.name = name
        self.phone = phone
        self.ticket_id = ticket_id

#########################
#####-Ticket Model-####
#########################

class Ticket(db.Model):
    __table__name = "ticket"

    tid = db.Column(db.Integer,primary_key = True)
    customer = db.relationship('Customer',backref='ticket',useList=False)
    slot = db.relationship('Slot',backref='ticket',useList=False)

    def __init__(self):
        pass

    def __repr__(self):
        if self.ticket:
            return f"Ticket ID: {1000 + self.tid} | Name: {self.customer.name} | Phone: {self.customer.phone} | {self.slot.time}"


#########################
#####-Slot Model-####
#########################

class Slot(db.Model):
    __table__name = "slot"

    sid = db.Column(db.Integer,primary_key=True)
    time = db.Column(db.Text)
    ticket_id = db.Column(db.Integer,db.ForeignKey('ticket.tid'))

    def __init__(self,time,ticket_id):
        self.time = time
        self.ticket_id = ticket_id


