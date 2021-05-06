from flask import Blueprint, current_app, render_template

from database import Stations

view = Blueprint("views", __name__)


@view.route("/", methods=["GET"])
def index():
    session = current_app.config['db_session']
    registered_stations = session.query(Stations).all()
    return render_template("index.html")



