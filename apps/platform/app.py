from flask import Flask
from libs.utils.jwt.config import JWT_SECRET_KEY
from libs.utils.jwt.jwt_config import JWT

from apps.platform.config import ENVIRONMENT, PORT
from apps.platform.modules.posts.blueprint import posts_blueprint
from apps.platform.modules.users.blueprint import users_blueprint

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
JWT.init_app(app)

app.register_blueprint(users_blueprint)
app.register_blueprint(posts_blueprint)

if __name__ == "__main__":
    app.run(debug=ENVIRONMENT, port=PORT)
