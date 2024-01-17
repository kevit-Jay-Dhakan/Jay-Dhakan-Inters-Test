import uvicorn
from fastapi import FastAPI

from apps.app_config import ENVIRONMENT, HOST, PORT
from apps.auth.src import auth_route
from apps.platform.src.modules.posts import posts_route
from apps.platform.src.modules.users import users_route
from libs.util.common.src.modules.environments import is_internal_environment

is_internal_env = is_internal_environment(ENVIRONMENT)

app = FastAPI(
    title='Application: AUTH',
    version='0.0.1',
    docs_url='/docs' if is_internal_env else None,
    redoc_url='/redoc' if is_internal_env else None,
)

app.include_router(auth_route)
app.include_router(users_route)
app.include_router(posts_route)

if __name__ == '__main__':
    uvicorn.run(
        'apps.app:app',
        host=HOST,
        port=PORT,
        reload=ENVIRONMENT
    )
