import uvicorn
from fastapi import FastAPI

from libs.util.common.src.modules.environments import is_internal_environment

is_internal_env = is_internal_environment(ENVIRONMENT)

app = FastAPI(
    title='Application: AUTH',
    version='0.0.1',
    docs_url='/docs' if is_internal_env else None,
    redoc_url='/redoc' if is_internal_env else None,
)
# TODO: logging remaining
app.include_router(auth_route)


if __name__ == '__main__':
    uvicorn.run(
        'apps.collector.src.app:app',
        host=HOST,
        port=PORT,
        reload=ENVIRONMENT
    )
