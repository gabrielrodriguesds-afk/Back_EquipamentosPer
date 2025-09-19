from src.database import db
from datetime import datetime, date
import uuid



class Nobreak(db.Model):
    __tablename__ = 'nobreaks'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    codigo = db.Column(db.String(10), unique=True, nullable=False)  # N0001, N0002, etc.
    cliente_id = db.Column(db.String(36), db.ForeignKey('clientes.id'), nullable=False)
    marca = db.Column(db.String(100), nullable=False)
    modelo = db.Column(db.String(100), nullable=False)
    numero_serie = db.Column(db.String(100), nullable=False)
    data_bateria = db.Column(db.Date, nullable=True)
    modelo_bateria = db.Column(db.String(100), nullable=True)
    quantidade_baterias = db.Column(db.Integer, default=1)
    setor = db.Column(db.String(100), nullable=True)
    observacao = db.Column(db.Text, nullable=True)
    foto_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Nobreak {self.codigo}>'

    def to_dict(self):
        return {
            'id': self.id,
            'codigo': self.codigo,
            'cliente_id': self.cliente_id,
            'cliente_nome': self.cliente.nome if self.cliente else None,
            'marca': self.marca,
            'modelo': self.modelo,
            'numero_serie': self.numero_serie,
            'data_bateria': self.data_bateria.isoformat() if self.data_bateria else None,
            'modelo_bateria': self.modelo_bateria,
            'quantidade_baterias': self.quantidade_baterias,
            'setor': self.setor,
            'observacao': self.observacao,
            'foto_url': self.foto_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def from_dict(data):
        """Cria uma instância de Nobreak a partir de um dicionário"""
        nobreak = Nobreak()
        nobreak.cliente_id = data.get('cliente_id')
        nobreak.marca = data.get('marca')
        nobreak.modelo = data.get('modelo')
        nobreak.numero_serie = data.get('numero_serie')
        
        # Converter string de data para objeto date
        if data.get('data_bateria'):
            if isinstance(data['data_bateria'], str):
                nobreak.data_bateria = datetime.strptime(data['data_bateria'], '%Y-%m-%d').date()
            else:
                nobreak.data_bateria = data['data_bateria']
        
        nobreak.modelo_bateria = data.get('modelo_bateria')
        nobreak.quantidade_baterias = data.get('quantidade_baterias', 1)
        nobreak.setor = data.get('setor')
        nobreak.observacao = data.get('observacao')
        nobreak.foto_url = data.get('foto_url')
        # O código será gerado automaticamente pelo trigger do MySQL
        return nobreak
    
    def update_from_dict(self, data):
        """Atualiza os campos do nobreak a partir de um dicionário"""
        if 'cliente_id' in data:
            self.cliente_id = data['cliente_id']
        if 'marca' in data:
            self.marca = data['marca']
        if 'modelo' in data:
            self.modelo = data['modelo']
        if 'numero_serie' in data:
            self.numero_serie = data['numero_serie']
        if 'data_bateria' in data:
            if isinstance(data['data_bateria'], str):
                self.data_bateria = datetime.strptime(data['data_bateria'], '%Y-%m-%d').date()
            else:
                self.data_bateria = data['data_bateria']
        if 'modelo_bateria' in data:
            self.modelo_bateria = data['modelo_bateria']
        if 'quantidade_baterias' in data:
            self.quantidade_baterias = data['quantidade_baterias']
        if 'setor' in data:
            self.setor = data['setor']
        if 'observacao' in data:
            self.observacao = data['observacao']
        if 'foto_url' in data:
            self.foto_url = data['foto_url']
        self.updated_at = datetime.utcnow()

