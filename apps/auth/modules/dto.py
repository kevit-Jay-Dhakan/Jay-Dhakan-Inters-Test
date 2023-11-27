from marshmallow import Schema, fields


class AuthSchema(Schema):
    user_id = fields.Str(
        required=True, error_messages={"required": "user_id is required"}
    )
    password = fields.Str(
        load_only=True,
        required=True,
        error_messages={"required": "password is required"},
    )
