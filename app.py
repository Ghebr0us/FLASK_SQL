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
def home():
    return render_template("home.html")


@app.route('/selection', methods = ['GET'])
def selection():
    global scelta,tabella
    scelta = request.args["radio"]
    if scelta == "2":
        query = "select category_name,count(*) as numero_prodotti from production.products inner join production.categories on products.category_id = categories.category_id group by category_name"
        tabella = pd.read_sql(query,conn)
        tabella.sort_values(by='numero_prodotti',ascending=False,inplace=True)
    elif scelta =="3":
        query = 'select store_name,count(*) as numero_ordini from sales.orders inner join sales.stores on stores.store_id = orders.store_id group by store_name'
        tabella = pd.read_sql(query,conn)
    elif scelta =="4":
        query = 'select brand_name,count(*) as numero_prodotti from production.products inner join production.brands on products.brand_id = brands.brand_id group by brand_name'
        tabella = pd.read_sql(query,conn)
    else:
        return render_template("search.html")
    return render_template("result.html", nomiColonne = tabella.columns.values, dati = tabella.values)


@app.route('/search', methods = ['GET'])
def search():
    return render_template("search.html")


@app.route('/result', methods = ['GET'])
def result():

    #invio query al database e ricezione informazioni
    nome_prodotto = request.args['nome_prodotto']
    query = f" select * from production.products where product_name like '{nome_prodotto}%' "
    df_prodotti = pd.read_sql(query,conn)
    #visualizzare le informazioni
    return render_template('result.html', nomiColonne = df_prodotti.columns.values, dati = list(df_prodotti.values.tolist()))


@app.route("/grafico.png", methods=["GET"])
def visualizza():
    if scelta == "2":
        fig = plt.figure()
        ax = plt.axes()
        fig.autofmt_xdate(rotation='vertical')
        ax.bar(tabella.category_name,tabella.numero_prodotti)
    if scelta == "3":
        fig = plt.figure()
        ax = plt.axes()
        fig.autofmt_xdate(rotation='vertical')
        ax.barh(tabella.store_name,tabella.numero_ordini)
    if scelta == "4":
        perc = tabella['numero_prodotti']

        plt.rcParams.update({'font.size':14})

        fig = plt.figure(figsize = [10,10])
        ax = plt.axes()

        ax.pie(perc, labels=tabella['brand_name'],autopct='%1.2f%%')
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)