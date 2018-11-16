import datetime
from flask import *
from config import *
from forms import CompanyForm

from db import DatabaseConnection

app = Flask(__name__)
app.config.from_object(DevelopmentConfig())

cnx = DatabaseConnection()
cursor = cnx.cursor


@app.route('/', methods = ['GET', 'POST'])
def dashboard():
    form = CompanyForm()
    # import pdb; pdb.set_trace()
    cnx.calculate_category_cy_ytd(1)
    xAxis1 = {"categories": [datetime.datetime.now().year], "crosshair": 'true'}
    series1 = [{"name": 'LY YTD', "data": [cnx.calculate_ly_ytd(1)]},
               {"name": 'CY YTD', "data": [cnx.calculate_cy_ytd(1)]}]
    top_companies = cnx.get_top_companies()
    if request.method == 'POST':
        if form.validate():
            pass
        else:
            return render_template('form.html', form = form, form_name = 'add', xAxis1=xAxis1, series1=series1)
    return render_template('form.html', form = form, list_companies = cnx.get_companies(), form_name = 'add',  xAxis1=xAxis1, series1=series1, top_companies=top_companies)


if __name__ == '__main__':
    # To run this app, hit following commands on terminal-
    # flask run
    app.run()



