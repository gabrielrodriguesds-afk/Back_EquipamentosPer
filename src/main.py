import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from src.database import db
from src.routes.user import user_bp
from src.routes.cliente import cliente_bp
from src.routes.usuario import usuario_bp
from src.routes.computador import computador_bp
from src.routes.nobreak import nobreak_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Configurar CORS para permitir requisições do Flutter
CORS(app, origins="*")

# Registrar blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(cliente_bp, url_prefix='/api')
app.register_blueprint(usuario_bp, url_prefix='/api')
app.register_blueprint(computador_bp, url_prefix='/api')
app.register_blueprint(nobreak_bp, url_prefix='/api')

# Configuração do banco MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://pr_user:pr_password123@localhost/pr_equipamentos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

db.init_app(app)

# Não criar tabelas automaticamente - usaremos as já criadas no MySQL
# with app.app_context():
#     db.create_all()

# Rota de status da API
@app.route('/api/status', methods=['GET'])
def api_status():
    """Verifica se a API está funcionando"""
    return jsonify({
        'success': True,
        'message': 'API P&R Equipamentos funcionando!',
        'version': '1.0.0'
    }), 200

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
