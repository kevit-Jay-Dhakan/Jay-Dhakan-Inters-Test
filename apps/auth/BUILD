python_sources(
    name = "auth_app",
    sources = [
        "modules/**",
        "app.py",
        "config.py",
    ],
    dependencies = [
        "apps/platform:platform_requirements",
        "libs/domains/auth:auth_domains",
        "libs/utils/jwt:jwt_config",
    ]
)

pex_binary(
    name = "main",
    dependencies = [
        ":auth_app",
    ],
    entry_point = "app.py",
    output_path = "auth/main.pex"
)
