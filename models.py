from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    sobrenome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hash_senha = db.Column(db.String(60), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    sexo = db.Column(db.String(50), nullable=False)

    def __init__(self, nome, sobrenome, email, hash_senha, data_nascimento, sexo,  id=None):
        self.id = id
        self.nome = nome
        self.sobrenome = sobrenome
        self.email = email
        self.hash_senha = hash_senha
        self.data_nascimento = data_nascimento
        self.sexo = sexo
