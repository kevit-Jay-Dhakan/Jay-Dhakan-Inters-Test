python_requirement(
    name="jwt_config_requirements",
    requirements=[
        "flask"
    ]
)

python_sources(
    name="jwt_config",
    sources=[
        "**"
    ],
    dependencies=[
        ":jwt_config_requirements",
        "libs/domains/auth:auth_domains"
    ]
)
