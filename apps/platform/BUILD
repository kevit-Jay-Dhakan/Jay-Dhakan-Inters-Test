python_requirement(
    name = "platform_requirements",
    requirements = [
        "PyJwt",
        "marshmallow",
        "passlib",
        "datetime",
        "requests"
    ]
)

python_sources(
    name = "platform_app",
    sources = [
        "modules/**",
        "app.py",
        "config.py"
    ],
    dependencies = [
        ":platform_requirements",
        "libs/utils/jwt:jwt_config",
        "libs/domains/posts:posts_domains",
        "libs/domains/auth:auth_domains",
    ]
)

pex_binary(
    name = "main",
    dependencies = [
        ":platform_app",
    ],
    entry_point = "app.py",
    output_path = "platform/main.pex"
)
