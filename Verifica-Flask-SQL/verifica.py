from flask import Flask, render_template, request,redirect,url_for,Response
app = Flask(__name__)


import io
# collegamento al database
import pandas as pd
import pymssql

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

matplotlib.use('Agg')
conn = pymssql.connect(server ='213.140.22.237\SQLEXPRESS',user='ghebrous.davide',password='xxx123##',database='ghebrous.davide')

@app.route('/', methods = ['GET'])
def search():
    return render_template("ricerca.html")


@app.route('/result', methods = ['GET'])
def result():
    global nome_store
    nome_store = request.args['store_name']
    query = f"select Sales.staffs.first_name,Sales.staffs.last_name from sales.stores inner join sales.staffs on stores.store_id = staffs.store_id where stores.store_name = '{nome_store}'"
    df_sales = pd.read_sql(query,conn)
    print(df_sales)
    if  df_sales.index != '' :
        return render_template('result.html', nomiColonne = df_sales.columns.values, dati = list(df_sales.values.tolist()))
    else:
         return render_template('error.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)