from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from view import view


def create_app():
    global login_manager
    app = Flask(__name__)

    #app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/areaClienti.db"
    app.config["SECRET_KEY"] = "HjuflJb&()sjhYN!mSikdnJ??b7298nHYSos"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config['DEBUG'] = True
    app.config['TESTING'] = False

    engine = create_engine("mysql+pymysql://" +
                       "root" + ":" +
                       "root" + "@" +
                       "127.0.0.1:3308" + "/" +
                       "safeskiing" + "?charset=utf8mb4")


    app.register_blueprint(view)

    return app

if __name__ == '__main__':

    app = create_app()
    app.run("0.0.0.0", 3000)
