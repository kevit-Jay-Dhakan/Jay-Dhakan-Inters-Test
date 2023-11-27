from bson.objectid import ObjectId
from libs.domains.auth.enums import Role
from libs.domains.auth.repository import auth_repository


def check_token_validation(jwt_header, jwt_payload):
    try:
        jti = jwt_payload["jti"]
        user_id = jwt_payload["sub"]

        token = auth_repository.find_one(
            {"_id": ObjectId(user_id), "tokens": {"$elemMatch": {"$eq": jti}}}
        )

        return token is None  # returns True if it's not present

    except Exception as e:
        print(f"Error in check_if_token_in_blocklist: {str(e)}")
        return True


def add_privilege_claims_to_jwt(identity):
    user = auth_repository.find_one({"_id": ObjectId(identity)})
    claims = {"is_admin": False, "is_super_admin": False}

    # Check if the user has privileges
    if user and "privilege" in user:
        privilege = user["privilege"]

        if privilege == Role.ADMIN.value:
            claims["is_admin"] = True
        elif privilege == Role.SUPER_ADMIN.value:
            claims["is_admin"] = True
            claims["is_super_admin"] = True

    return claims
