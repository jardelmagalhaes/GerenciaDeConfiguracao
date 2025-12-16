import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    matricula = db.Column(db.String(20), nullable=False)

    def to_json(self):
        return {"id": self.id, "nome": self.nome, "matricula": self.matricula}

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/alunos', methods=['POST'])
def criar_aluno():
    dados = request.get_json()
    novo_aluno = Aluno(nome=dados['nome'], matricula=dados['matricula'])
    db.session.add(novo_aluno)
    db.session.commit()
    return jsonify(novo_aluno.to_json()), 201

@app.route('/alunos', methods=['GET'])
def listar_alunos():
    alunos = Aluno.query.all()
    return jsonify([a.to_json() for a in alunos]), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)