import connexion
import encoder
import sys
from flask_cors import CORS
from app import MyWebApplication
from flask_cors import CORS
from connexion.decorators.uri_parsing import AlwaysMultiURIParser

worker = MyWebApplication().start()


def main():
    try:
        args = sys.argv
    except AttributeError:
        sys.argv = pymol_argv
        args = sys.argv

    try:
        port = int(args[1]) if 0 <= int(args[1]) <= 65535 else 3333
    except:
        port = 3333

    options = {'uri_parsing_class': AlwaysMultiURIParser}
    app = connexion.App('Object detection', specification_dir='./swagger/', options=options)
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Object detection'})
    CORS(app.app)
    app.run(port=port)


if __name__ == '__main__':
    if worker:
        main()
