from flask import Flask, render_template, request
import requests
import csv
import os

app = Flask(__name__)

API_KEY = "2a8f3bae"  # Substitua pela sua API key da OMDb
CSV_FILE = "histórico.csv"

def salvar_historico(dados):
    existe = os.path.exists(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not existe:
            writer.writerow(["Título", "Ano", "Diretor", "IMDb"])
        writer.writerow([dados.get("Title", ""), dados.get("Year", ""), dados.get("Director", ""), dados.get("imdbRating", "")])

@app.route("/", methods=["GET", "POST"])
def index():
    filme = None
    erro = None
    if request.method == "POST":
        titulo = request.form.get("titulo")
        url = f"https://www.omdbapi.com/?apikey={API_KEY}&t={titulo}"
        resposta = requests.get(url).json()

        if resposta["Response"] == "True":
            filme = resposta
            salvar_historico(filme)
        else:
            erro = resposta.get("Error", "Erro ao buscar filme.")

    return render_template("index.html", filme=filme, erro=erro)

if __name__ == "__main__":
    app.run(debug=True)
