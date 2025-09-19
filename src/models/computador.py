from datetime import datetime
import uuid
from src.database import db

class Computador(db.Model):
    __tablename__ = 'computadores'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    codigo = db.Column(db.String(10), unique=True, nullable=False)  # P0001, P0002, etc.
    cliente_id = db.Column(db.String(36), db.ForeignKey('clientes.id'), nullable=False)
    marca = db.Column(db.String(100), nullable=False)
    modelo = db.Column(db.String(100), nullable=False)
    numero_serie = db.Column(db.String(100), nullable=False)
    setor = db.Column(db.String(100), nullable=True)
    operador = db.Column(db.String(100), nullable=True)
    observacao = db.Column(db.Text, nullable=True)
    foto_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Computador {self.codigo}>'

    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'cliente_id': self.cliente_id,
            'cliente_nome': self.cliente.nome if self.cliente else None,
            'marca': self.marca,
            'modelo': self.modelo,
            'numero_serie': self.numero_serie,
            'setor': self.setor,
            'operador': self.operador,
            'observacao': self.observacao,
            'foto_url': self.foto_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def from_dict(data):
        """Cria uma instância de Computador a partir de um dicionário"""
        computador = Computador()
        computador.cliente_id = data.get('cliente_id')
        computador.marca = data.get('marca')
        computador.modelo = data.get('modelo')
        computador.numero_serie = data.get('numero_serie')
        computador.setor = data.get('setor')
        computador.operador = data.get('operador')
        computador.observacao = data.get('observacao')
        computador.foto_url = data.get('foto_url')
        # O código será gerado automaticamente pelo trigger do MySQL
        return computador
    
    def update_from_dict(self, data):
        """Atualiza os campos do computador a partir de um dicionário"""
        if 'cliente_id' in data:
            self.cliente_id = data['cliente_id']
        if 'marca' in data:
            self.marca = data['marca']
        if 'modelo' in data:
            self.modelo = data['modelo']
        if 'numero_serie' in data:
            self.numero_serie = data['numero_serie']
        if 'setor' in data:
            self.setor = data['setor']
        if 'operador' in data:
            self.operador = data['operador']
        if 'observacao' in data:
            self.observacao = data['observacao']
        if 'foto_url' in data:
            self.foto_url = data['foto_url']
        self.updated_at = datetime.utcnow()

