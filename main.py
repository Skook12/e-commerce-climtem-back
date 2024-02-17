from app import routes
from configs.config import Config

if __name__ == '__main__':
    app = routes.create_server(Config)
    app.run(debug=True, host="0.0.0.0", port=5000)