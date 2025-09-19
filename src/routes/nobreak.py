from flask import Blueprint, request, jsonify
from src.models.nobreak import Nobreak, db
from src.models.cliente import Cliente

nobreak_bp = Blueprint('nobreak', __name__)

@nobreak_bp.route('/nobreaks', methods=['GET'])
def listar_nobreaks():
    """Lista todos os nobreaks"""
    try:
        nobreaks = Nobreak.query.join(Cliente).all()
        return jsonify({
            'success': True,
            'data': [nobreak.to_dict() for nobreak in nobreaks]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@nobreak_bp.route('/nobreaks/<string:nobreak_id>', methods=['GET'])
def obter_nobreak(nobreak_id):
    """Obtém um nobreak específico"""
    try:
        nobreak = Nobreak.query.get(nobreak_id)
        if not nobreak:
            return jsonify({
                'success': False,
                'error': 'Nobreak não encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'data': nobreak.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@nobreak_bp.route('/nobreaks', methods=['POST'])
def criar_nobreak():
    """Cria um novo nobreak"""
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
        
        # Criar nobreak
        nobreak = Nobreak.from_dict(data)
        db.session.add(nobreak)
        db.session.commit()
        
        # Recarregar para obter o código gerado pelo trigger
        db.session.refresh(nobreak)
        
        return jsonify({
            'success': True,
            'data': nobreak.to_dict(),
            'message': f'Nobreak criado com sucesso! Código: {nobreak.codigo}'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@nobreak_bp.route('/nobreaks/<string:nobreak_id>', methods=['PUT'])
def atualizar_nobreak(nobreak_id):
    """Atualiza um nobreak existente"""
    try:
        nobreak = Nobreak.query.get(nobreak_id)
        if not nobreak:
            return jsonify({
                'success': False,
                'error': 'Nobreak não encontrado'
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
        
        # Atualizar nobreak
        nobreak.update_from_dict(data)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': nobreak.to_dict(),
            'message': 'Nobreak atualizado com sucesso'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@nobreak_bp.route('/nobreaks/<string:nobreak_id>', methods=['DELETE'])
def deletar_nobreak(nobreak_id):
    """Deleta um nobreak"""
    try:
        nobreak = Nobreak.query.get(nobreak_id)
        if not nobreak:
            return jsonify({
                'success': False,
                'error': 'Nobreak não encontrado'
            }), 404
        
        codigo = nobreak.codigo
        db.session.delete(nobreak)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Nobreak {codigo} deletado com sucesso'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@nobreak_bp.route('/nobreaks/buscar', methods=['GET'])
def buscar_nobreaks():
    """Busca nobreaks por código, marca, modelo ou cliente"""
    try:
        termo = request.args.get('q', '').strip()
        if not termo:
            return jsonify({
                'success': False,
                'error': 'Termo de busca é obrigatório'
            }), 400
        
        nobreaks = Nobreak.query.join(Cliente).filter(
            db.or_(
                Nobreak.codigo.ilike(f'%{termo}%'),
                Nobreak.marca.ilike(f'%{termo}%'),
                Nobreak.modelo.ilike(f'%{termo}%'),
                Cliente.nome.ilike(f'%{termo}%')
            )
        ).all()
        
        return jsonify({
            'success': True,
            'data': [nobreak.to_dict() for nobreak in nobreaks]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@nobreak_bp.route('/nobreaks/cliente/<string:cliente_id>', methods=['GET'])
def listar_nobreaks_cliente(cliente_id):
    """Lista nobreaks de um cliente específico"""
    try:
        nobreaks = Nobreak.query.filter_by(cliente_id=cliente_id).all()
        return jsonify({
            'success': True,
            'data': [nobreak.to_dict() for nobreak in nobreaks]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

