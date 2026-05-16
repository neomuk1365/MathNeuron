from flask import Flask
from config import Config
from app.extensions import db, migrate

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.routes.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.routes.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    import re
    @app.template_filter('parse_markdown')
    def parse_markdown_filter(text):
        if not text:
            return text
        # Convert bold
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        # Convert italic
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        return text

    return app
