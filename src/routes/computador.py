from flask import Blueprint, request, jsonify
from src.models.computador import Computador, db
from src.models.cliente import Cliente

computador_bp = Blueprint('computador', __name__)

@computador_bp.route('/computadores', methods=['GET'])
def listar_computadores():
    """Lista todos os computadores"""
    try:
        computadores = Computador.query.join(Cliente).all()
        return jsonify({
            'success': True,
            'data': [computador.to_dict() for computador in computadores]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@computador_bp.route('/computadores/<string:computador_id>', methods=['GET'])
def obter_computador(computador_id):
    """Obtém um computador específico"""
    try:
        computador = Computador.query.get(computador_id)
        if not computador:
            return jsonify({
                'success': False,
                'error': 'Computador não encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'data': computador.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@computador_bp.route('/computadores', methods=['POST'])
def criar_computador():
    """Cria um novo computador"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        if not data:
            return jsonify({
                'success': False,
                'error': 'Dados não fornecidos'
            }), 400
        
        required_fields = ['cliente_id', 'marca', 'modelo', 'numero_serie']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'{field} é obrigatório'
                }), 400
        
        # Verificar se cliente existe
        cliente = Cliente.query.get(data['cliente_id'])
        if not cliente:
            return jsonify({
                'success': False,
                'error': 'Cliente não encontrado'
            }), 404
        
        # Criar computador
        computador = Computador.from_dict(data)
        db.session.add(computador)
        db.session.commit()
        
        # Recarregar para obter o código gerado pelo trigger
        db.session.refresh(computador)
        
        return jsonify({
            'success': True,
            'data': computador.to_dict(),
            'message': f'Computador criado com sucesso! Código: {computador.codigo}'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@computador_bp.route('/computadores/<string:computador_id>', methods=['PUT'])
def atualizar_computador(computador_id):
    """Atualiza um computador existente"""
    try:
        computador = Computador.query.get(computador_id)
        if not computador:
            return jsonify({
                'success': False,
                'error': 'Computador não encontrado'
            }), 404
        
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Dados não fornecidos'
            }), 400
        
        # Verificar se cliente existe (se fornecido)
        if 'cliente_id' in data:
            cliente = Cliente.query.get(data['cliente_id'])
            if not cliente:
                return jsonify({
                    'success': False,
                    'error': 'Cliente não encontrado'
                }), 404
        
        # Atualizar computador
        computador.update_from_dict(data)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': computador.to_dict(),
            'message': 'Computador atualizado com sucesso'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@computador_bp.route('/computadores/<string:computador_id>', methods=['DELETE'])
def deletar_computador(computador_id):
    """Deleta um computador"""
    try:
        computador = Computador.query.get(computador_id)
        if not computador:
            return jsonify({
                'success': False,
                'error': 'Computador não encontrado'
            }), 404
        
        codigo = computador.codigo
        db.session.delete(computador)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Computador {codigo} deletado com sucesso'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@computador_bp.route('/computadores/buscar', methods=['GET'])
def buscar_computadores():
    """Busca computadores por código, marca, modelo ou cliente"""
    try:
        termo = request.args.get('q', '').strip()
        if not termo:
            return jsonify({
                'success': False,
                'error': 'Termo de busca é obrigatório'
            }), 400
        
        computadores = Computador.query.join(Cliente).filter(
            db.or_(
                Computador.codigo.ilike(f'%{termo}%'),
                Computador.marca.ilike(f'%{termo}%'),
                Computador.modelo.ilike(f'%{termo}%'),
                Cliente.nome.ilike(f'%{termo}%')
            )
        ).all()
        
        return jsonify({
            'success': True,
            'data': [computador.to_dict() for computador in computadores]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@computador_bp.route('/computadores/cliente/<string:cliente_id>', methods=['GET'])
def listar_computadores_cliente(cliente_id):
    """Lista computadores de um cliente específico"""
    try:
        computadores = Computador.query.filter_by(cliente_id=cliente_id).all()
        return jsonify({
            'success': True,
            'data': [computador.to_dict() for computador in computadores]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

