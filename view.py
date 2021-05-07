from datetime import datetime, date, timedelta

from flask import Blueprint, current_app, render_template, jsonify, request

from database import Stations, LastUpdate, StationsHistory, session, Skiipass

view = Blueprint("views", __name__)


@view.route("/", methods=["GET"])
def index():
    registered_stations = session.query(Stations).all()
    return render_template("index.html")


@view.route("/api/skipass", methods=['GET'])
def get_all_skipass():
    day = request.args.get("day")

    if day is None:
        day = date.today()
    else:
        try:
            day = datetime.strptime(day, "%Y-%m-%d")
        except:
            return "Unable to parse date, need format YYYY-mm-dd", 400

    return jsonify([skipass.serialize() for skipass in session.query(LastUpdate).filter(LastUpdate.last_update > day).filter(LastUpdate.last_update < day + timedelta(days=1)).all()])


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
        try:
            from_instant = int(from_instant)
        except:
            return "from instant is not a integer", 400

        if from_instant > int(datetime.now().timestamp()):
            return "from_instant in the future", 400
        query = query.filter(StationsHistory.instant > datetime.utcfromtimestamp(from_instant))

    if to_instant is not None:
        try:
            to_instant = int(to_instant)
        except:
            return "to instant is not a integer", 400

        if from_instant is not None and to_instant < from_instant:
            return "from_instant is greater than to_instant", 400

        query = query.filter(StationsHistory.instant < datetime.utcfromtimestamp(to_instant))

    current_app.logger.debug(query)

    return jsonify([record.serialize() for record in query.all()])

@view.route("/api/score/", methods=['GET'])
def get_score():
    '''
    LOWER SCORE WIN !!!
    :return:
    score
    '''
    uuid = request.args.get("uuid")
    day = request.args.get("day")

    current_app.logger.debug(uuid)

    query = session.query(Skiipass)
    if uuid is not None:
        query = query.filter_by(uuid = uuid)

    if day is None:
        day = date.today()
    else:
        try:
            day = datetime.strptime(day, "%Y-%m-%d")
        except:
            return "Unable to parse date, need format YYYY-mm-dd", 400

    skipass_records = query.filter(Skiipass.departure_time >= day).filter(Skiipass.departure_time < (day + timedelta(days=1))).all()

    result = {}
    for record in skipass_records:
        if record.uuid in result:
            result[record.uuid] += int((record.departure_time - record.arrival_time).total_seconds() * record.total_people)
        else:
            result[record.uuid] = int((record.departure_time - record.arrival_time).total_seconds() * record.total_people)

    current_app.logger.debug(result)

    return jsonify(result)
