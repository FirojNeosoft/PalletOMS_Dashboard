import datetime

from flask import *
from config import *
from forms import CompanyForm

from db import DatabaseConnection

app = Flask(__name__)
app.config.from_object(DevelopmentConfig())

cnx = DatabaseConnection()
cursor = cnx.cursor


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return redirect('/dashboard')


@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'triveni@123' and request.form['username'] == 'srujal':
        session['logged_in'] = True
    else:
        return render_template('login.html', message="Incorrect username or password")
    return home()


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return home()


@app.route('/dashboard', methods = ['GET', 'POST'])
def dashboard():
    form = CompanyForm()
    if request.method == 'POST':
        if form.validate():
            cmp_id = int(form.cmp.data)
            xAxis1 = {"categories": [datetime.datetime.now().year], "crosshair": 'true'}
            series1 = [{"name": 'LY YTD', "data": [cnx.calculate_ly_ytd(cmp_id)]},
                       {"name": 'CY YTD', "data": [cnx.calculate_cy_ytd(cmp_id)]}]
            top_companies = cnx.get_top_customers(cmp_id)

            xAxis2 = {"categories": [], "crosshair": 'true'}
            series2 = [{"name": 'LY YTD', "data": [cnx.calculate_ly_quaterly_ytd(cmp_id, 1), cnx.calculate_ly_quaterly_ytd(cmp_id, 2), cnx.calculate_ly_quaterly_ytd(cmp_id, 3), cnx.calculate_ly_quaterly_ytd(cmp_id, 4)]},
                       {"name": 'CY YTD', "data": [cnx.calculate_cy_quaterly_ytd(cmp_id, 1), cnx.calculate_cy_quaterly_ytd(cmp_id, 2), cnx.calculate_cy_quaterly_ytd(cmp_id, 3), cnx.calculate_cy_quaterly_ytd(cmp_id, 4)]}]

            xAxis3 = {"categories": [datetime.datetime.now().year], "crosshair": 'true'}
            series3 = [{"name": 'LY YTD', "data": cnx.calculate_category_ly_ytd(cmp_id)},
                       {"name": 'CY YTD', "data": cnx.calculate_category_ly_ytd(cmp_id)}]
            top_categories = cnx.get_top_categories(cmp_id)
            pie_chart_data = cnx.calculate_category_cy_ytd_pie(cmp_id)
            return render_template('form.html', form=form, list_companies=cnx.get_companies(), form_name='edit',\
                                   xAxis1=xAxis1, series1=series1, xAxis2=xAxis2, series2=series2, xAxis3=xAxis3, series3=series3,\
                                   top_companies=top_companies, top_categories=top_categories, pie_chart_data=pie_chart_data)
        else:
            return render_template('form.html', form = form, form_name = 'add', list_companies=cnx.get_companies())
    return render_template('form.html', form = form,  form_name='add', list_companies=cnx.get_companies())


if __name__ == '__main__':
    # To run this app, hit following commands on terminal-
    # flask run
    app.run()



