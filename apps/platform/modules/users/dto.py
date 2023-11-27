from marshmallow import fields, Schema, validate


class UsersSchema(Schema):
    user_id = fields.Str(
        required=True, error_messages={"required": "Username is required"}
    )
    first_name = fields.Str(
        required=True, error_messages={"required": "first_name is required"}
    )
    last_name = fields.Str(
        required=True, error_messages={"required": "last_name is required"}
    )


class RegisterSchema(UsersSchema):
    email = fields.Str(
        required=True,
        error_messages={"required": "email is required"}
    )
    password = fields.Str(
        load_only=True,
        required=True,
        error_messages={"required": "password is required"},
    )
    privilege = fields.Str(
        required=True,
        validate=validate.OneOf(["CUSTOMER", "ADMIN", "SUPER_ADMIN"]),
        error_messages={"required": "Privilege is required"}
    )


class UpdateSchema(Schema):
    first_name = fields.Str(
        required=True,
        error_messages={"required": "first_name must be updated."}
    )
    last_name = fields.Str(
        required=True,
        error_messages={"required": "last_name must be updated."}
    )
