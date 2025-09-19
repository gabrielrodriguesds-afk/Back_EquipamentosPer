from src.database import db

class Contador(db.Model):
    __tablename__ = 'contadores'
    
    tipo = db.Column(db.String(20), primary_key=True)  # 'computador' ou 'nobreak'
    ultimo_numero = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Contador {self.tipo}: {self.ultimo_numero}>'

    def to_dict(self):
        return {
            'tipo': self.tipo,
            'ultimo_numero': self.ultimo_numero
        }
    
    @staticmethod
    def get_proximo_numero(tipo):
        """Obtém o próximo número para o tipo especificado"""
        contador = Contador.query.filter_by(tipo=tipo).first()
        if not contador:
            # Criar contador se não existir
            contador = Contador(tipo=tipo, ultimo_numero=0)
            db.session.add(contador)
        
        contador.ultimo_numero += 1
        db.session.commit()
        return contador.ultimo_numero
    
    @staticmethod
    def gerar_codigo_computador():
        """Gera o próximo código para computador (P0001, P0002, etc.)"""
        numero = Contador.get_proximo_numero('computador')
        return f"P{numero:04d}"
    
    @staticmethod
    def gerar_codigo_nobreak():
        """Gera o próximo código para nobreak (N0001, N0002, etc.)"""
        numero = Contador.get_proximo_numero('nobreak')
        return f"N{numero:04d}"

