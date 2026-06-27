from flask import Flask, render_template
from app.config import Config
from app.extensions import db, login_manager

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    from app.models.user import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Pendaftaran Blueprints (Modular MVC)
    from app.auth.routes import auth_bp
    from app.recipes.routes import recipes_bp
    from app.bookmarks.routes import bookmarks_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(recipes_bp)
    app.register_blueprint(bookmarks_bp, url_prefix='/bookmarks')

    @app.errorhandler(404)
    def not_found(e): return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(e): 
        db.session.rollback()
        return render_template('errors/500.html'), 500

    with app.app_context():
        db.create_all()

    return app