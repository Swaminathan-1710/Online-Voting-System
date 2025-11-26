from flask import Flask, jsonify, render_template
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRES, CORS_ORIGINS
from routes.user_routes import user_bp
from routes.admin_routes import admin_bp


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # JWT Configuration
    app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = JWT_ACCESS_TOKEN_EXPIRES
    JWTManager(app)

    # CORS
    CORS(app, resources={r"/api/*": {"origins": CORS_ORIGINS}})

    # Blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(admin_bp)

    # Template routes
    @app.route("/")
    def index():
        return render_template("user/login.html")
    
    @app.route("/register")
    def register_page():
        return render_template("user/register.html")
    
    @app.route("/login")
    def login_page():
        return render_template("user/login.html")
    
    @app.route("/vote")
    def vote_page():
        return render_template("user/vote.html")
    
    @app.route("/profile")
    def profile_page():
        return render_template("user/profile.html")
    
    @app.route("/admin")
    def admin_login_page():
        return render_template("admin/login.html")
    
    @app.route("/admin/dashboard")
    def admin_dashboard():
        return render_template("admin/dashboard.html")
    
    @app.route("/admin/add_candidate")
    def admin_add_candidate():
        return render_template("admin/add_candidate.html")
    
    @app.route("/admin/create_election")
    def admin_create_election():
        return render_template("admin/create_election.html")
    
    @app.route("/admin/manage_elections")
    def admin_manage_elections():
        return render_template("admin/manage_elections.html")
    
    @app.route("/admin/manage_users")
    def admin_manage_users():
        return render_template("admin/manage_users.html")

    # Health endpoint
    @app.get("/health")
    def health():
        return jsonify({"status": "ok"}), 200

    # JWT error handlers
    @app.errorhandler(422)
    def handle_422(e):
        return jsonify({"error": "Invalid or missing token. Please login again."}), 422
    
    @app.errorhandler(401)
    def handle_401(e):
        return jsonify({"error": "Unauthorized. Please login."}), 401
    
    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({"error": "Resource not found"}), 404
    
    # Global error handler
    @app.errorhandler(Exception)
    def handle_exception(e):
        # Avoid leaking internal errors; provide minimal info
        import traceback
        if app.debug:
            traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500

    return app


if __name__ == "__main__":
    # Auto-initialize database on startup
    print("=" * 50)
    print("BallotHub - Starting Application")
    print("=" * 50)
    try:
        from database.init_db import init_database
        print("\nInitializing database...")
        init_database()
        print("\n" + "=" * 50 + "\n")
    except Exception as e:
        print(f"\n⚠ Warning: Database initialization failed: {e}")
        print("Make sure MongoDB is running on mongodb://localhost:27017")
        print("=" * 50 + "\n")
    
    app = create_app()
    print("Server starting on http://127.0.0.1:5000")
    print("Press Ctrl+C to stop\n")
    app.run(host="0.0.0.0", port=5000, debug=True)

