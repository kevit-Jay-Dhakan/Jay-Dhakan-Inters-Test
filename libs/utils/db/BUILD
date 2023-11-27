python_requirement(
    name = "db_requirements",
    requirements = [
        "pymongo",
        "python-dotenv"
    ]
)

python_sources(
    name="connection",
    sources=[
         "**"
    ],
    dependencies=[
        ":db_requirements"
    ]
)
