from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:toledo2022@localhost:3306/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = "usuario"
    id = db.Column('usu_id', db.Integer, primary_key=True)
    cpf = db.Column('usu_cpf', db.String(256))
    nome = db.Column('usu_nome', db.String(256))
    email = db.Column('usu_email', db.String(256))
    login = db.Column('usu_login', db.String(256))
    senha = db.Column('usu_senha', db.String(256))
    tipo = db.Column('usu_tipo', db.String(256))

    def __init__(self, nome, cpf, email, login, senha, tipo):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.login = login
        self.senha = senha
        self.tipo = tipo


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/cadastro/usuario")
def cadUsuario():
    return render_template('cadastro_usuario.html', usuarios=Usuario.query.all(), titulo="Usuario")


@app.route("/cadastro/novousuario", methods=['POST'])
def novousuario():
    usuario = Usuario(request.form.get('nome'),
                      request.form.get('cpf'),
                      request.form.get('email'),
                      request.form.get('login'),
                      request.form.get('senha'),
                      request.form.get('tipoUsuario'))
    db.session.add(usuario)
    db.session.commit()
    return redirect(url_for('cadUsuario'))

@app.route("/usuario/editar/<int:id>", methods=['GET','POST'])
def editarusuario(id):
    usuario = Usuario.query.get(id)
    if request.method == 'POST':
        usuario.nome = request.form.get('nome')
        usuario.cpf = request.form.get('cpf')
        usuario.email = request.form.get('email')
        usuario.login = request.form.get('login')
        usuario.senha = request.form.get('senha')
        usuario.tipo = request.form.get('tipoUsuario')
        db.session.add(usuario)
        db.session.commit()
        return redirect(url_for('cadUsuario'))
    return render_template('eusuario.html', usuario=usuario)

@app.route("/usuario/deletar/<int:id>")
def deletarusuario(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('cadUsuario'))

@app.route("/cadastro/categoria")
def cadCategoria():
    return render_template('cadastro_categoria.html')


@app.route("/cadastro/anuncio")
def cadAnuncio():
    return render_template('cadastro_anuncio.html')


@app.route("/anuncio")
def anuncio():
    return render_template('anuncio.html')


@app.route("/relatorio")
def relatorio():
    return render_template('relatorio.html')


if __name__ == 'app':
    db.create_all()
