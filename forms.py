from flask_wtf import Form
from wtforms import TextField, SubmitField, SelectField


class CompanyForm(Form):
   cmp = SelectField('Company', choices = [('T', 'Triveni'), ('N','Neosoft')])
   from_date = TextField("From")
   to_date = TextField("TO")
   submit = SubmitField("Search")
