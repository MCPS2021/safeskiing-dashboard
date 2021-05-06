from flask import Blueprint, current_app, render_template, jsonify

from database import Stations, LastUpdate

view = Blueprint("views", __name__)


@view.route("/", methods=["GET"])
def index():
    session = current_app.config['db_session']
    registered_stations = session.query(Stations).all()
    return render_template("index.html")


@view.route("/api/skipass", methods=['GET'])
def get_all_skipass():
    session = current_app.config['db_session']
    all_skipass = session.query(LastUpdate).all()
    return jsonify([skipass.serialize() for skipass in all_skipass])