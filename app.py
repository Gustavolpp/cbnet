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


class Categoria(db.Model):
    __tablename__ = "categoria"
    id = db.Column('cat_id', db.Integer, primary_key=True)
    nome = db.Column('cat_nome', db.String(256))
    desc = db.Column('cat_desc', db.String(256))

    def __init__(self, nome, desc):
        self.nome = nome
        self.desc = desc


class Anuncio(db.Model):
    __tablename__ = "anuncio"
    id = db.Column('anu_id', db.Integer, primary_key=True)
    titulo = db.Column('anu_titulo', db.String(256))
    desc = db.Column('anu_desc', db.String(256))
    ativo = db.Column('anu_ativo', db.Boolean)
    valor = db.Column('anu_valor', db.Float)
    cat_id = db.Column('cat_id', db.Integer, db.ForeignKey("categoria.cat_id"))

    def __init__(self, titulo, desc, ativo, valor, cat_id):
        self.titulo = titulo
        self.desc = desc
        self.ativo = ativo
        self.valor = valor
        self.cat_id = cat_id


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/cadastro/usuario")
def cadUsuario():
    return render_template('cadastro_usuario.html', usuarios=Usuario.query.all())


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
    return render_template('cadastro_categoria.html', categorias=Categoria.query.all())


@app.route("/cadastro/novacategoria", methods=['POST'])
def novacategoria():
    categoria = Categoria(request.form.get('nome'),
                          request.form.get('desc'))
    db.session.add(categoria)
    db.session.commit()
    return redirect(url_for('cadCategoria'))


@app.route("/categoria/editar/<int:id>", methods=['GET','POST'])
def editarcategoria(id):
    categoria = Categoria.query.get(id)
    if request.method == 'POST':
        categoria.nome = request.form.get('nome')
        categoria.desc = request.form.get('desc')

        db.session.add(categoria)
        db.session.commit()
        return redirect(url_for('cadCategoria'))
    return render_template('ecategoria.html', categoria=categoria)


@app.route("/categoria/deletar/<int:id>")
def deletarcategoria(id):
    categoria = Categoria.query.get(id)
    db.session.delete(categoria)
    db.session.commit()
    return redirect(url_for('cadCategoria'))

@app.errorhandler(404)
def paginanaoencontrada(error):
    return render_template('pagnaoencontrada.html')


@app.route("/cadastro/anuncio")
def cadAnuncio():
    return render_template('cadastro_anuncio.html', anuncios=Anuncio.query.all(), categorias=Categoria.query.all())


@app.route("/cadastro/novoanuncio", methods=['POST'])
def novoanuncio():
    anuncio = Anuncio(request.form.get('titulo'),
                      request.form.get('desc'),
                      request.form.get('ativo') == '1',
                      request.form.get('valor'),
                      request.form.get('categoria'))
    db.session.add(anuncio)
    db.session.commit()
    return redirect(url_for('cadAnuncio'))

@app.route("/anuncio/editar/<int:id>", methods=['GET','POST'])
def editaranuncio(id):
    anuncio = Anuncio.query.get(id)
    if request.method == 'POST':
        anuncio.titulo = request.form.get('titulo')
        anuncio.desc = request.form.get('desc')
        anuncio.ativo = request.form.get('ativo') == '1'
        anuncio.valor = request.form.get('valor')
        anuncio.cat_id = request.form.get('categoria')

        db.session.add(anuncio)
        db.session.commit()
        return redirect(url_for('cadAnuncio'))
    return render_template('eanuncio.html', anuncio=anuncio, categorias=Categoria.query.all())

@app.route("/anuncio/deletar/<int:id>")
def deletaranuncio(id):
    anuncio = Anuncio.query.get(id)
    db.session.delete(anuncio)
    db.session.commit()
    return redirect(url_for('cadAnuncio'))


@app.route("/anuncio")
def anuncio():
    return render_template('anuncio.html')


@app.route("/relatorio")
def relatorio():
    return render_template('relatorio.html')


if __name__ == 'app':
    db.create_all()