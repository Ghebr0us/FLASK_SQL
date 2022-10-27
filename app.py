from flask import Flask, render_template, request,redirect,url_for
app = Flask(__name__)



# collegamento al database
import pandas as pd
import pymssql
conn = pymssql.connect(server ='213.140.22.237\SQLEXPRESS',user='ghebrous.davide',password='xxx123##',database='ghebrous.davide')

@app.route('/', methods = ['GET'])
def home():
    return render_template("home.html")


@app.route('/selection', methods = ['GET'])
def selection():
    scelta = request.args["radio"]
    if scelta == "1":
        return render_template("search.html")
    if scelta == "2":
        return redirect(url_for('prod_category'))

@app.route('/search', methods = ['GET'])
def search():
    return render_template("search.html")


@app.route('/prod_category', methods = ['GET'])
def prod_category():
    query = "select category_name,count(*) as numero_prodotti from production.products inner join production.categories on products.category_id = categories.category_id group by category_name"
    df_prodotti = pd.read_sql(query,conn)

    fig = plt.figure()
    ax = plt.axes()
    fig.autofmt_xdate(rotation='vertical')
    ax.bar(df.category_name,df.numero_prodotti)
    return render_template("prod_category.html", table = df_prodotti.to_html())



@app.route('/result', methods = ['GET'])
def result():

    #invio query al database e ricezione informazioni
    nome_prodotto = request.args['nome_prodotto']
    query = f" select * from production.products where product_name like '{nome_prodotto}%' "
    df_prodotti = pd.read_sql(query,conn)
    #visualizzare le informazioni
    return render_template('result.html', nomiColonne = df_prodotti.columns.values, dati = list(df_prodotti.values.tolist()))




if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)