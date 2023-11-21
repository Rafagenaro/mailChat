
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session
from flask_bcrypt import Bcrypt
from models import User, db
from flask_mail import Mail, Message
import smtplib
import os

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mvrg123@localhost/mailChat'
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'

db.init_app(app)
bcrypt = Bcrypt(app)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['usuario']
        senha = request.form['senha']
        
        user = User.query.filter_by(email=email).first()
        
        if user and bcrypt.check_password_hash(user.hash_senha, senha):
            session['user_id'] = user.id
            return redirect(url_for('logado'))
        else:
            error = "E-mail ou senha incorretos."
    
    return render_template('index.html', error=error)
    
@app.route('/logado')
def logado():
    user_id = session.get('user_id')  # Obtenha o ID do usuário da sessão
    if user_id is None:
        # Se não há usuário logado, redireciona para a página de login
        return redirect(url_for('login'))

    logged_in_user = User.query.get(user_id)  # Obtenha o usuário logado
        
    
    
    if logged_in_user:
        sobrenome_logado = logged_in_user.sobrenome
        nome_logado = logged_in_user.nome  # Aqui está o nome do usuário logado
        other_users = User.query.filter(User.id != user_id).all()

        

        return render_template('logado.html', sobrenome_logado=sobrenome_logado, nome_logado=nome_logado, other_users=other_users, logged_in_user=logged_in_user)
    else:
        # Se o usuário não for encontrado, pode ser necessário lidar com isso (ex: redirecionar para login)
        return redirect(url_for('login'))
    






@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == "POST":
        hashed_senha = bcrypt.generate_password_hash(request.form['senha']).decode('utf-8')
        data_nascimento = datetime.strptime(request.form['data_nascimento'], '%Y-%m-%d')
        user = User(nome=request.form['nome'], sobrenome=request.form['sobrenome'], email=request.form['email'], 
                    hash_senha=hashed_senha, data_nascimento=data_nascimento, 
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