from flask import Blueprint, request, jsonify
from src.models.cliente import Cliente, db

cliente_bp = Blueprint('cliente', __name__)

@cliente_bp.route('/clientes', methods=['GET'])
def listar_clientes():
    """Lista todos os clientes"""
    try:
        clientes = Cliente.query.all()
        return jsonify({
            'success': True,
            'data': [cliente.to_dict() for cliente in clientes]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@cliente_bp.route('/clientes/<string:cliente_id>', methods=['GET'])
def obter_cliente(cliente_id):
    """Obtém um cliente específico"""
    try:
        cliente = Cliente.query.get(cliente_id)
        if not cliente:
            return jsonify({
                'success': False,
                'error': 'Cliente não encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'data': cliente.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@cliente_bp.route('/clientes', methods=['POST'])
def criar_cliente():
    """Cria um novo cliente"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        if not data or not data.get('nome'):
            return jsonify({
                'success': False,
                'error': 'Nome é obrigatório'
            }), 400
        
        # Criar cliente
        cliente = Cliente.from_dict(data)
        db.session.add(cliente)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': cliente.to_dict(),
            'message': 'Cliente criado com sucesso'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@cliente_bp.route('/clientes/<string:cliente_id>', methods=['PUT'])
def atualizar_cliente(cliente_id):
    """Atualiza um cliente existente"""
    try:
        cliente = Cliente.query.get(cliente_id)
        if not cliente:
            return jsonify({
                'success': False,
                'error': 'Cliente não encontrado'
            }), 404
        
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Dados não fornecidos'
            }), 400
        
        # Atualizar cliente
        cliente.update_from_dict(data)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': cliente.to_dict(),
            'message': 'Cliente atualizado com sucesso'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@cliente_bp.route('/clientes/<string:cliente_id>', methods=['DELETE'])
def deletar_cliente(cliente_id):
    """Deleta um cliente"""
    try:
        cliente = Cliente.query.get(cliente_id)
        if not cliente:
            return jsonify({
                'success': False,
                'error': 'Cliente não encontrado'
            }), 404
        
        # Verificar se há equipamentos vinculados
        if cliente.computadores or cliente.nobreaks:
            return jsonify({
                'success': False,
                'error': 'Não é possível deletar cliente com equipamentos vinculados'
            }), 400
        
        db.session.delete(cliente)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cliente deletado com sucesso'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@cliente_bp.route('/clientes/buscar', methods=['GET'])
def buscar_clientes():
    """Busca clientes por nome"""
    try:
        termo = request.args.get('q', '').strip()
        if not termo:
            return jsonify({
                'success': False,
                'error': 'Termo de busca é obrigatório'
            }), 400
        
        clientes = Cliente.query.filter(
            Cliente.nome.ilike(f'%{termo}%')
        ).all()
        
        return jsonify({
            'success': True,
            'data': [cliente.to_dict() for cliente in clientes]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

