from src.api import init_api
from application import app


init_api()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
