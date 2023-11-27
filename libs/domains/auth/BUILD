python_requirement(
    name="auth_domain_requirements",
    requirements=[
        "flask-jwt-extended"
    ]
)

python_sources(
    name="auth_domains",
    sources=[
        "**"
    ],
    dependencies=[
        ":auth_domain_requirements",
        "libs/utils/db:connection"
    ]
)
