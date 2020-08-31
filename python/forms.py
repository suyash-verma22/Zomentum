from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField


class AddForm(FlaskForm):
    name = StringField('Name: ')
    phone = StringField('Phone Number: ')
    slot = StringField('Choose Slot: ')
    submit = SubmitField('Book Ticket')

class DelForm(FlaskForm):
    id = IntegerField('Ticket ID: ')
    submit = SubmitField('Delete Reservation')
