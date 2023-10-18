from flask import Flask, render_template, request, redirect, url_for
from flask_bcrypt import Bcrypt
from models import User, db

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db.init_app(app)
bcrypt = Bcrypt(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == "POST":
        hashed_senha = bcrypt.generate_password_hash(request.form['senha']).decode('utf-8')
        user = User(nome=request.form['nome'], sobrenome=request.form['sobrenome'], email=request.form['email'], 
                    hash_senha=hashed_senha, data_nascimento=request.form['data_nascimento'], 
                    sexo=request.form['sexo'])
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))  # Redirecione para a página inicial após o cadastro
    return render_template('cadastro.html')

@app.route('/senha', methods=['GET', 'POST'])
def senha():
    return render_template('senha.html')

@app.route('/create-db')
def create_db():
    db.create_all()
    return "DB criado!"

if __name__ == '__main__':
    app.run()

