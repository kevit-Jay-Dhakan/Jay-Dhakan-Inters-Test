from marshmallow import Schema, fields


class PostSchema(Schema):
    post_id = fields.Str(
        required=True, error_messages={"required": "post_id is required"}
    )
    post_description = fields.Str(
        required=True,
        error_messages={"required": "post_description is required"},
    )
