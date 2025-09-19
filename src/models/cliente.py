from datetime import datetime
import uuid
from src.database import db  # <-- importa o db criado em database.py

class Cliente(db.Model):
    __tablename__ = 'clientes'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=True)
    telefone = db.Column(db.String(20), nullable=True)
    endereco = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    computadores = db.relationship('Computador', backref='cliente', lazy=True, cascade='all, delete-orphan')
    nobreaks = db.relationship('Nobreak', backref='cliente', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Cliente {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'endereco': self.endereco,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def from_dict(data):
        """Cria uma instância de Cliente a partir de um dicionário"""
        cliente = Cliente()
        cliente.nome = data.get('nome')
        cliente.email = data.get('email')
        cliente.telefone = data.get('telefone')
        cliente.endereco = data.get('endereco')
        return cliente
    
    def update_from_dict(self, data):
        """Atualiza os campos do cliente a partir de um dicionário"""
        if 'nome' in data:
            self.nome = data['nome']
        if 'email' in data:
            self.email = data['email']
        if 'telefone' in data:
            self.telefone = data['telefone']
        if 'endereco' in data:
            self.endereco = data['endereco']
        self.updated_at = datetime.utcnow()

