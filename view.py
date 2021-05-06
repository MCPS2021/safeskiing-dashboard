from datetime import datetime

from flask import Blueprint, current_app, render_template, jsonify, request

from database import Stations, LastUpdate, StationsHistory, session

view = Blueprint("views", __name__)


@view.route("/", methods=["GET"])
def index():
    registered_stations = session.query(Stations).all()
    return render_template("index.html")


@view.route("/api/skipass", methods=['GET'])
def get_all_skipass():
    return jsonify([skipass.serialize() for skipass in session.query(LastUpdate).all()])


@view.route("/api/stations", methods=['GET'])
def get_all_stations():
    return jsonify([skipass.serialize() for skipass in session.query(Stations).all()])


@view.route("/api/totalPeople/", methods=['GET'])
def get_total_people():
    station_id = request.args.get("station_id")
    from_instant = request.args.get("from")
    to_instant = request.args.get("to")

    print(station_id, from_instant, to_instant)

    query = session.query(StationsHistory)

    if station_id is not None:
        if session.query(Stations).get(station_id) is None:
            return "station does not exists", 404

        query = query.filter_by(station_id = station_id)

    if from_instant is not None:
        if from_instant > int(datetime.now().timestamp()):
            return "from_instant in the future", 400
        query = query.filter(StationsHistory.instant > datetime.utcfromtimestamp(from_instant))

    if to_instant is not None:
        if to_instant < from_instant:
            return "from_instant is greater than to_instant", 400
        query = query.filter(StationsHistory.instant < datetime.utcfromtimestamp(to_instant))

    current_app.logger.debug(query)
    print(query.all())

    return jsonify([record.serialize() for record in query.all()])