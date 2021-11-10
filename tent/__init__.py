from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS


def create_app(config_filename=None):
    application = Flask(__name__, instance_relative_config=True)
    application.config.from_pyfile(config_filename)
    initialize_extensions(application)
    register_blueprints(application)
    return application


def initialize_extensions(application):
    # probablemente imports innecesarios
    from tent.models.producto import Producto, ProductSchema
    from tent.models.compra import Compra, CompraSchema
    db = SQLAlchemy(application)
    ma = Marshmallow(application)


def register_blueprints(application):
    from tent.controllers import productos_bp, compras_bp
    CORS(compras_bp)
    CORS(productos_bp)
    application.register_blueprint(productos_bp)
    application.register_blueprint(compras_bp)


_env = os.environ.get('FLASK_ENV')
if _env is None:
    print('*'*25, 'DEVELOPMENT', '*'*25)
    _env = 'development'
config_filename = os.path.abspath(os.path.dirname(
    __file__)) + f"/../instance/{_env}.cfg"
app = Flask(__name__)
app.config.from_pyfile(config_filename)
db = SQLAlchemy(app)
ma = Marshmallow(app)