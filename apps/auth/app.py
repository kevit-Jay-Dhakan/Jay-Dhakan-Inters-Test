from flask import Flask
from libs.utils.jwt.config import JWT_SECRET_KEY
from libs.utils.jwt.jwt_config import JWT

from apps.auth.config import ENVIRONMENT, PORT
from apps.auth.modules.blueprint import auth_blueprint

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
JWT.init_app(app)

app.register_blueprint(auth_blueprint)

if __name__ == "__main__":
    app.run(debug=ENVIRONMENT, port=PORT)
