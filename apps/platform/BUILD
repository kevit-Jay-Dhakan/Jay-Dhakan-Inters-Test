python_requirement(
    name = 'platform_requirements',
    requirements = [
        'pydantic',
        'pydantic[email]'
    ]
)

python_sources(
    name = 'platform_app',
    sources = [
        'modules/**'
    ],
    dependencies = [
        ':platform_requirements',
        'libs/utils/jwt:jwt_util',
        'libs/utils/logger:logger_util',
        'libs/utils/limiter:limiter_util',
        'libs/utils/common:common_utils',
        'libs/domains/posts:posts_domain',
        'libs/domains/auth:users_domain'
    ]
)
