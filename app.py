from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/', methods = ['GET'])
def home():
    return render_template("search.html")

@app.route('/result', methods = ['GET'])
def result():
    # collegamento al database
    import pandas as pd
    import pymssql
    conn = pymssql.connect(server ='213.140.22.237\SQLEXPRESS',user='ghebrous.davide',password='xxx123##',database='ghebrous.davide')

    #invio query al database e ricezione informazioni
    nome_prodotto = request.args['nome_prodotto']
    query = f" select * from production.products where product_name like '{nome_prodotto}%' "
    df_prodotti = pd.read_sql(query,conn)
    #visualizzare le informazioni
    return render_template('result.html', nomiColonne = df_prodotti.columns.values, dati = list(df_prodotti.values.tolist()))
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)