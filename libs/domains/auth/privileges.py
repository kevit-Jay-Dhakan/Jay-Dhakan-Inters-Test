from flask_jwt_extended import get_jwt

from libs.domains.auth.enums import Role


def check_admin_privileges():
    claims = get_jwt()

    is_admin = claims.get("is_admin")
    is_super_admin = claims.get("is_super_admin")

    if is_super_admin:
        return Role.SUPER_ADMIN.value

    elif is_admin:
        return Role.ADMIN.value

    else:
        return Role.CUSTOMER.value
