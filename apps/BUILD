python_sources(
    name = "main_app",
    sources = [
        "app.py",
        "config.py"
    ],
    dependencies = [
        "apps/auth:auth_app",
        "apps/platform:platform_app"
    ]
)

file(name='env', source='.env')

pex_binary(
    name = "main",
    dependencies = [
        ":main_app",
        ":env"
    ],
    entry_point = "app.py",
    output_path = "apps/main.pex"
)
