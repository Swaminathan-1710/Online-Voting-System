from flask import Blueprint
from controllers.admin_controller import (
    admin_login, approve_user, add_candidate, create_election, election_results,
    list_users, list_all_elections, update_election, delete_election, delete_user,
    reject_user
)

admin_bp = Blueprint("admin_bp", __name__)

# Admin routes
admin_bp.add_url_rule("/api/admin/login", view_func=admin_login, methods=["POST"])
admin_bp.add_url_rule("/api/admin/users", view_func=list_users, methods=["GET"])
admin_bp.add_url_rule("/api/admin/elections", view_func=list_all_elections, methods=["GET"])
admin_bp.add_url_rule("/api/admin/approve_user/<string:user_id>", view_func=approve_user, methods=["PUT"])
admin_bp.add_url_rule("/api/admin/add_candidate", view_func=add_candidate, methods=["POST"])
admin_bp.add_url_rule("/api/admin/create_election", view_func=create_election, methods=["POST"])
admin_bp.add_url_rule("/api/admin/update_election", view_func=update_election, methods=["PUT"])
admin_bp.add_url_rule("/api/admin/delete_election/<string:election_id>", view_func=delete_election, methods=["DELETE"])
admin_bp.add_url_rule("/api/admin/results/<string:election_id>", view_func=election_results, methods=["GET"])
admin_bp.add_url_rule("/api/admin/delete_user/<string:user_id>", view_func=delete_user, methods=["DELETE"])
admin_bp.add_url_rule("/api/admin/reject_user/<string:user_id>", view_func=reject_user, methods=["DELETE"])

