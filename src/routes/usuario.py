from flask import Blueprint, request, jsonify
from src.models.usuario import Usuario, db

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/usuarios', methods=['GET'])
def listar_usuarios():
    """Lista todos os usuários"""
    try:
        usuarios = Usuario.query.all()
        return jsonify({
            'success': True,
            'data': [usuario.to_dict() for usuario in usuarios]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@usuario_bp.route('/usuarios/<string:usuario_id>', methods=['GET'])
def obter_usuario(usuario_id):
    """Obtém um usuário específico"""
    try:
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return jsonify({
                'success': False,
                'error': 'Usuário não encontrado'
            }), 404
        
        return jsonify({
            'success': True,
            'data': usuario.to_dict()
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@usuario_bp.route('/usuarios', methods=['POST'])
def criar_usuario():
    """Cria um novo usuário"""
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        if not data or not data.get('nome'):
            return jsonify({
                'success': False,
                'error': 'Nome é obrigatório'
            }), 400
        
        # Criar usuário
        usuario = Usuario.from_dict(data)
        db.session.add(usuario)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': usuario.to_dict(),
            'message': 'Usuário criado com sucesso'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@usuario_bp.route('/usuarios/<string:usuario_id>', methods=['PUT'])
def atualizar_usuario(usuario_id):
    """Atualiza um usuário existente"""
    try:
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return jsonify({
                'success': False,
                'error': 'Usuário não encontrado'
            }), 404
        
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'error': 'Dados não fornecidos'
            }), 400
        
        # Atualizar usuário
        usuario.update_from_dict(data)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': usuario.to_dict(),
            'message': 'Usuário atualizado com sucesso'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@usuario_bp.route('/usuarios/<string:usuario_id>', methods=['DELETE'])
def deletar_usuario(usuario_id):
    """Deleta um usuário"""
    try:
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return jsonify({
                'success': False,
                'error': 'Usuário não encontrado'
            }), 404
        
        db.session.delete(usuario)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Usuário deletado com sucesso'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@usuario_bp.route('/usuarios/buscar', methods=['GET'])
def buscar_usuarios():
    """Busca usuários por nome"""
    try:
        termo = request.args.get('q', '').strip()
        if not termo:
            return jsonify({
                'success': False,
                'error': 'Termo de busca é obrigatório'
            }), 400
        
        usuarios = Usuario.query.filter(
            Usuario.nome.ilike(f'%{termo}%')
        ).all()
        
        return jsonify({
            'success': True,
            'data': [usuario.to_dict() for usuario in usuarios]
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

