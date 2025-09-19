from src.database import db
from datetime import datetime
import uuid


class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=True)
    telefone = db.Column(db.String(20), nullable=True)
    cargo = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Usuario {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'cargo': self.cargo,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def from_dict(data):
        """Cria uma instância de Usuario a partir de um dicionário"""
        usuario = Usuario()
        usuario.nome = data.get('nome')
        usuario.email = data.get('email')
        usuario.telefone = data.get('telefone')
        usuario.cargo = data.get('cargo')
        return usuario
    
    def update_from_dict(self, data):
        """Atualiza os campos do usuário a partir de um dicionário"""
        if 'nome' in data:
            self.nome = data['nome']
        if 'email' in data:
            self.email = data['email']
        if 'telefone' in data:
            self.telefone = data['telefone']
        if 'cargo' in data:
            self.cargo = data['cargo']
        self.updated_at = datetime.utcnow()

