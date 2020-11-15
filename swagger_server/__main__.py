import connexion
import encoder
from flask_cors import CORS
from app import MyWebApplication
from flask_cors import CORS

worker = MyWebApplication().start()


def main():
    app = connexion.App('Object detection', specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Object detection'})
    CORS(app.app)
    app.run(port=3333)


if __name__ == '__main__':
    if worker:
        main()
