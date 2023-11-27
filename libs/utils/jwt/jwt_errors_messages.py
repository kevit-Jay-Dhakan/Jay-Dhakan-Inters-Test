from flask import make_response


def expired_token_callback(jwr_header, jwt_payload):
    return make_response(
        {"message": "Token Expire", "solution": "Please login again"}, 404
    )


def invalid_token_callback(error):
    return make_response(
        {
            "message": "Invalid token",
            "solution": "Please check your access token or login again",
        },
        404,
    )


def missing_token_callback(error):
    return make_response(
        {
            "message": "Token missing in header",
            "solution": "Please login again and make sure to add your token "
            "in header as Bearer token",
        },
        404,
    )


def revoked_token_callback(jwt_header, jwt_payload):
    return make_response(
        {
            "message": "User is already logged out please login again to "
            "perform this operation."
        },
        200,
    )
