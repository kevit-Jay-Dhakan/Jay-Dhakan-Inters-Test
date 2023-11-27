from flask_jwt_extended import JWTManager

from libs.utils.jwt.jwt_errors_messages import (
    expired_token_callback,
    invalid_token_callback,
    missing_token_callback,
    revoked_token_callback,
)
from libs.utils.jwt.jwt_methods import (
    add_privilege_claims_to_jwt,
    check_token_validation,
)

JWT = JWTManager()

JWT.token_in_blocklist_loader(check_token_validation)

JWT.additional_claims_loader(add_privilege_claims_to_jwt)

JWT.expired_token_loader(expired_token_callback)

JWT.invalid_token_loader(invalid_token_callback)

JWT.unauthorized_loader(missing_token_callback)

JWT.revoked_token_loader(revoked_token_callback)
