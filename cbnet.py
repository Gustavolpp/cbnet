from flask import Flask, render_template

app = Flask(__name__)

app.route("/")
def index():
    return render_template('index.html')

app.route("/cadastro/usuario")
def index():
    return render_template('cadastro_usuario.html')

app.route("/cadastro/categoria")
def index():
    return render_template('cadastro_categoria.html')

app.route("/cadastro/anuncio")
def index():
    return render_template('cadastro_anuncio.html')

app.route("/")
def index():
    return render_template('anuncio.html')

app.route("/")
def index():
    return render_template('relatorio.html')