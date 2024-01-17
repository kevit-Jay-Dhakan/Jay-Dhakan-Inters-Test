python_requirement(
    name = 'auth_requirements',
    requirements = [
        'passlib',
        'pydantic[email]'
    ]
)

python_sources(
    name = 'auth_app',
    sources = [
        'src/**'
    ],
    dependencies = [
        'apps/auth:auth_requirements',
        'libs/domains/auth:auth_domain',
        'libs/utils/jwt:jwt_util',
    ]
)
