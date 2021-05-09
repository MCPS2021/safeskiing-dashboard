from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

from database import Stations, session
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
                       "safeskiing-db:3306" + "/" +
                       "safeskiing" + "?charset=utf8mb4")


    app.register_blueprint(view)

    # try db connection
    test_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    try:
        test_session.query(Stations).all()
    except Exception as e:
        app.logger.error("Can not connect to database! Exiting now")
        app.logger.error(e)
        exit(1)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        session.remove()

    return app

if __name__ == '__main__':

    app = create_app()
    app.run("0.0.0.0", 3000)
