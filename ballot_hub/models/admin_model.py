from typing import Optional, Dict, Any
import bcrypt
from bson import ObjectId
from database.connection import get_collection


def admin_login(username: str, password: str) -> Optional[Dict[str, Any]]:
    admins = get_collection("admins")
    admin = admins.find_one({"username": username})
    if not admin:
        return None
    if not bcrypt.checkpw(password.encode("utf-8"), admin["password"].encode("utf-8")):
        return None
    admin["admin_id"] = str(admin["_id"])
    admin.pop("_id", None)
    admin.pop("password", None)
    return admin

