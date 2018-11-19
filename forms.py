from flask_wtf import Form
from wtforms import TextField, SubmitField, SelectField


class CompanyForm(Form):
   cmp = SelectField('Company', choices = [('1', 'JQ Warehouse'), ('3','D&V Wholesale INC')])
   from_date = TextField("From")
   to_date = TextField("TO")
   submit = SubmitField("Search")
